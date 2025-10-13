import warnings

warnings.filterwarnings("ignore")
import paramiko
from scp import SCPClient
from tqdm import tqdm
import os
import os.path as osp
import tarfile


def create_ssh_client(server, user, password, port=22):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=user, password=password, port=port)
    return client


def get_total_size(local_path):
    total_size = 0
    if os.path.isdir(local_path):
        for root, dirs, files in os.walk(local_path):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
    else:
        total_size = os.path.getsize(local_path)
    return total_size


def create_tarfile(source_dir, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def extract_tarfile(tarfile_path, extract_to):
    try:
        with tarfile.open(tarfile_path, "r:gz") as tar:
            members = tar.getmembers()
            total_size = sum(member.size for member in members)

            with tqdm(total=total_size,
                      unit='B',
                      unit_scale=True,
                      desc='Extracting') as pbar:
                for member in members:
                    tar.extract(member, path=extract_to)
                    pbar.update(member.size)
    except tarfile.ReadError:
        print(f"Error: {tarfile_path} is not a valid gzip file.")


def format_size(size):
    # 将字节大小转换为合适的单位
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def get_remote_total_size(ssh, remote_path):
    stdin, stdout, stderr = ssh.exec_command(
        f'find {remote_path} -type f -exec stat -c %s {{}} +')
    total_size = sum(int(size) for size in stdout.read().decode().split())
    formatted_size = format_size(total_size)
    return total_size, formatted_size


def scp_transfer_to_remote(server_ip, username, password, port, local_path,
                           remote_path):
    print(
        f'===== Uploading {local_path} to {server_ip}: {remote_path} =====\n')
    ssh = create_ssh_client(server_ip, username, password, port)

    # 检查服务器上是否存在目标文件夹，如果不存在则创建
    stdin, stdout, stderr = ssh.exec_command(f'mkdir -p {remote_path}')
    stdout.channel.recv_exit_status()  # 等待命令执行完成

    # 修改服务器上目标文件夹的权限为 777
    ssh.exec_command(f'chmod -R 777 {remote_path}')

    if os.path.isdir(local_path) and not osp.exists(local_path + '.tar.gz'):
        tar_path = local_path + '.tar.gz'
        print('====== Start tar =====')
        create_tarfile(local_path, tar_path)
        print('====== End tar =====')

        tar_path = local_path + '.tar.gz'
        local_path = tar_path

    total_size = get_total_size(local_path)
    formatted_size = format_size(total_size)
    print(f"Total size to upload: {formatted_size}")

    with tqdm(total=total_size, unit='B', unit_scale=True,
              desc='Uploading') as pbar:

        def progress(filename, size, sent):
            pbar.update(sent - pbar.n)

        scp = SCPClient(ssh.get_transport(), progress=progress)
        scp.put(local_path, remote_path)
        scp.close()

    # 解压服务器上的 tar.gz 文件
    if local_path.endswith('.tar.gz'):
        remote_tar_path = remote_path + '/' + os.path.basename(local_path)
        ssh.exec_command(f'tar -xzf {remote_tar_path} -C {remote_path}')
        ssh.exec_command(f'rm -rf {remote_tar_path}')  # 删除服务器上的 tar.gz 文件
    elif local_path.endswith('.zip'):
        remote_tar_path = remote_path + '/' + os.path.basename(local_path)
        ssh.exec_command(f'unzip {remote_tar_path}')
        ssh.exec_command(f'rm -rf {remote_tar_path}')  # 删除服务器上的 tar.gz 文件

    # 删除本地的 tar.gz 文件
    if local_path.endswith(('.tar.gz', '.zip')):
        os.remove(local_path)


def scp_transfer_to_local(server_ip, username, password, port, remote_path,
                          local_path):
    print(
        f'====== Downloading {server_ip}: {remote_path} to {local_path} =====')
    ssh = create_ssh_client(server_ip, username, password, port)

    if remote_path.endswith('/*'):
        remote_dir = remote_path[:-2]
        print(f"Remote directory: {remote_dir}")
        print(f"Parent directory: {remote_dir.rsplit('/', 1)[0]}")

        # 检查目录是否存在
        stdin, stdout, stderr = ssh.exec_command(f'ls {remote_dir}')
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            print(f"Directory {remote_dir} does not exist.")
            print(stderr.read().decode())
            return

        ssh.exec_command(f'chmod -R 777 {remote_dir.rsplit("/", 1)[0]}')

        # 执行压缩命令并捕获输出和错误信息
        print('====== Start tar =====')
        stdin, stdout, stderr = ssh.exec_command(
            f'tar -czf {remote_dir}.tar.gz -C {remote_dir} --ignore-failed-read .'
        )
        exit_status = stdout.channel.recv_exit_status()  # 等待命令执行完成
        total_size, formatted_size = get_remote_total_size(
            ssh, f'{remote_dir}.tar.gz')
        print(f"Total size to download: {formatted_size}")
        print('====== End tar =====')

        # if exit_status == 0:
        #     print("Compression successful")
        # else:
        #     print(f"Compression failed with exit status {exit_status}")
        #     print(stderr.read().decode())
        #     return

        remote_path = remote_dir + '.tar.gz'

        with tqdm(total=total_size,
                  unit='B',
                  unit_scale=True,
                  desc='Downloading') as pbar:

            def progress(filename, size, sent):
                pbar.update(sent - pbar.n)

            scp = SCPClient(ssh.get_transport(), progress=progress)
            scp.get(remote_path, local_path + '.tar.gz')
            scp.close()

        if remote_path.endswith('.tar.gz'):
            extract_tarfile(local_path + '.tar.gz', local_path)
            os.remove(local_path + '.tar.gz')  # 删除本地的 tar.gz 文件

            # 删除服务器上的 tar.gz 文件
            ssh.exec_command(f'rm {remote_path}')

    else:
        total_size, formatted_size = get_remote_total_size(ssh, remote_path)

        with tqdm(total=total_size,
                  unit='B',
                  unit_scale=True,
                  desc='Downloading') as pbar:

            def progress(filename, size, sent):
                pbar.update(sent - pbar.n)

            scp = SCPClient(ssh.get_transport(), progress=progress)
            scp.get(remote_path, osp.join(local_path,
                                          osp.basename(remote_path)))
            scp.close()


if __name__ == "__main__":
    # 服务器信息
    server_info = {
        'fa': ['10.162.198.33', 'm00028512', 'Mph00028512@', 22],
        # 'fp': ['10.162.199.73', 'm00028512', 'Mph00028512@', 22],
        'fp': ['10.69.194.35', 'm00028512', 'Mph00028512@', 22],
        'zk': ['10.69.194.34', 'z00028576', 'Xinian1998.', 22],
        # 'new_fp': ['10.80.128.135', 'root', 'root', 23752]
    }
    shape = 'fp'
    server_ip, username, password, port = server_info[shape]

    # # 本地 --> 远程服务器  不用带subDir
    local_path_to_upload = r'D:\code\datasets\02_FaceParsing\Test\11_FaceSR\20250919\images'
    remote_path_to_upload = '/data0/m00028512/datasets/Test/11_FaceSR/20250919'
    scp_transfer_to_remote(server_ip, username, password, port,
                           local_path_to_upload, remote_path_to_upload)
    print("File upload completed.")

    # 远程服务器 --> 本地 用带subDir
    # 传送文件夹，需要在末尾加上 "/*"
    # remote_path_to_download = '/data0/m00028512/datasets/02_HumanParsing/AIColorTrack/ai01/zim_sam2_3_skin/*'
    # local_path_to_download = rf'D:\code\datasets\06_HumanParsing\AIColorTrack\ai01\{osp.basename(remote_path_to_download[:-2])}'

    # # # # # 传送单个文件
    # # # remote_path_to_download = '/data/m00028512/m00028512/41/workspace/FP2.0/FaceParsing/checkpoints/onnx_models/segformer/20250604_segformer_e24_miou0.9243_out3.onnx'
    # # # local_path_to_download = r'D:\code\HP1.0\CloudHumanParsing\models'

    # os.makedirs(local_path_to_download, exist_ok=True)
    # scp_transfer_to_local(server_ip, username, password, port,
    #                       remote_path_to_download, local_path_to_download)
    # print("File download completed.")
