# 系统文件相关

## 列出当前文件夹所有子文件夹的文件个数

```Bash
find . -type d -exec sh -c 'echo -n "{}: "; find "{}" -type f | wc -l' \;\
```

## 把当前文件夹下的图片名字中的'中国'删除

```Bash
  for file in *中国*; do mv "$file" "${file//中国/}"; done
```

## 把a.txt种含有blink11的行删除

```Bash
grep -v "blink11" a.txt > temp.txt && mv temp.txt a.txt
```

## 查看图片信息

```Bash
apt-get install imagemagick
identify a.png
```

# CUDA相关

## nvidia-smi 实时更新

```Bash
watch -n 1 nvidia-smi
```

## 设置环境可用CUDA

```Bash
export CUDA_VISIBLE_DEVICES=5,6,7
echo $CUDA_VISIBLE_DEVICES
```

# 镜像相关

## 不同服务器之间镜像迁移


| 导出镜像                                                     | 导入镜像                                  |
| ------------------------------------------------------------ | ----------------------------------------- |
| docker commit 容器名 镜像名<br />docker save 镜像id -o 要保存的tar包名称.tar | docker load < 备份文件.tar                |
| docker export <container_id> -o <filename>.tar               | docker import 镜像文件.tar 镜像名:version |
| docker tag 镜像id 要改的镜像名字：版本号<br/>docker rename 容器名称或ID 新的名字<br/>为容器改名(新建一个别名，原始的容器名称仍然有效) |                                           |



# 服务器

## linux系统信息查看

```Python
# 查看操作系统名称和版本
cat /etc/os-release

# 查看内核版本
uname -r

# 查看系统架构
uname -m

# 查看更详细的系统信息（包括发行版、版本、内核等）  (推荐）
lsb_release -a

# 查看所有系统信息
hostnamectl
```

## conda版本查看

```Python
# 查看conda地址
conda info --env

# 查看当前使用的conda 
cat <conda_path>/LICENSE.txt
```

anaconda:

<img width="1478" height="157" alt="image" src="https://github.com/user-attachments/assets/7064933a-a1e4-465a-9fad-b2a0dbb162f0" />

Miniconda:

<img width="1486" height="151" alt="image" src="https://github.com/user-attachments/assets/3e59b51a-7519-48ca-b987-659340d4f14f" />

Mini-forge:

<img width="656" height="329" alt="image" src="https://github.com/user-attachments/assets/47c4822e-c460-43f9-9494-0efe943dd9fd" />


## 将本地ssh公钥复制到服务器

```Bash
# 在本地机器上打开终端，运行以下命令生成SSH密钥对：
ssh-keygen -t rsa
# 这将在~/.ssh/目录下生成id_rsa和id_rsa.pub文件。
# 将公钥添加到远程服务器的授权文件：
ssh-copy-id your_username@10.162.194.12
# 测试SSH连接：
ssh your_username@10.162.194.12
```

# Conda

## 虚拟环境相关

```Bash
conda env list

# 基于base环境创建虚拟环境
conda create --name llava --clone base
# 基于python3.9 创建虚拟环境
# conda create --name {name} python=3.9 -y

conda init bash
source ~/.bashrc
conda activate llava

conda remove --name llava --all -y

# 容器之间的环境导入
conda env export --name base > environment_qwen.yml
conda env create -f environment_qwen.yml --name qwen2.5-vl --no-deps
```

## terminals database is inaccessible

```Bash
apt install ncurses-term
```

## 环境源码安装路径：

Miniforge: https://github.com/conda-forge/miniforge/releases

Pytorch: https://pytorch.org/get-started/previous-versions/

Vllm: https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html#use-the-local-cutlass-for-compilation

Flash-atten: https://github.com/Dao-AILab/flash-attention/releases

detectron2: https://detectron2.readthedocs.io/en/latest/tutorials/install.html

cuda：https://developer.nvidia.com/cuda-toolkit-archive
