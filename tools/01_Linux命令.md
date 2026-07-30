# Linux 命令速查

## 系统文件操作

```bash
# 列出当前文件夹下所有子文件夹的文件个数
find . -type d -exec sh -c 'echo -n "{}: "; find "{}" -type f | wc -l' \;

# 统计一级目录下 annotations_czj 子目录的文件数
find ./*/annotations_czj -type d -exec sh -c 'echo -n "{}: "; find "{}" -type f | wc -l' \;

# 把当前文件夹下图片名字中的'中国'删除
for file in *中国*; do mv "$file" "${file//中国/}"; done

# 把 a.txt 中含有 blink11 的行删除
grep -v "blink11" a.txt > temp.txt && mv temp.txt a.txt

# 查看图片信息
apt-get install imagemagick
identify a.png

# 查看当前目录下不重复的后缀类型
find . -type f | grep -oE '\.[^./]+$' | sort -u

# 批量计算匹配文件的 md5
find . -type f -name "<pattern>" -exec md5sum {} \;

# 计算指定文件名的 md5
find . -name "HnAestheticComposition.serialized.bin" -exec md5sum {} \;
```

## Git 配置

```bash
# 让 Git 不将文件权限变化视为修改（仅当前仓库）
git config core.fileMode false

# 全局生效（对所有仓库）
git config --global core.fileMode false
```

> 说明：设置后 `git diff` / `git status` 不再把权限位（如 `100644` → `100755`）当作变更。若已有 staged 的权限改动，可临时打开再 checkout：
> `git config core.fileMode true && git checkout -- . && git config core.fileMode false`

## 进程管理

```bash
# 杀掉状态为 TL（多线程停止）的进程
ps -eo pid,stat | awk '$2 ~ /^Tl/ {print $1}' | xargs -r kill -9

# 后台运行脚本，日志重定向
nohup bash sft_train.sh > train.log 2>&1 &
```

## 批量删除

```bash
# 删除某一天生成的文件（按修改时间）
find . -maxdepth 1 -type f -newermt "2026-07-02 00:00:00" ! -newermt "2026-07-03 00:00:00" -exec rm -f {} +

# 删除所有指定名称的文件夹
find . -type d -name "annotations_czj2" -exec rm -rf {} +

# 删除所有匹配模式的文件
find . -type f -name "20.1363a135a5613032_outpaint*" -exec rm -f {} +
```

## 压缩 / 解压

```bash
# 批量解压当前目录所有 .tar 文件
for f in *.tar; do tar -xvf "$f"; done

# 批量解压 .tar.gz / .tgz
for f in *.tar.gz *.tgz; do tar -xzvf "$f"; done

# 批量解压 .zip
for f in *.zip; do unzip -o "$f"; done

# 将指定目录打包（不包含根路径本身）
tar -cvf archive.tar -C /path/to/parent dirname/

# 查看 tar 包内容不解压
tar -tvf archive.tar
```

## CUDA 相关

```bash
# nvidia-smi 实时更新
watch -n 1 nvidia-smi

# 设置环境可用 CUDA
export CUDA_VISIBLE_DEVICES=5,6,7
echo $CUDA_VISIBLE_DEVICES
```

## 镜像迁移（不同服务器之间）

| 操作       | 镜像相关                                                                                                              | 容器相关                                              |
| ---------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 导出/保存  | `docker save 镜像id -o 要保存的tar包名称.tar`                                                                         | `docker export <container_id> -o <filename>.tar`       |
| 导入       | `docker load < 备份文件.tar`                                                                                          | `docker import 镜像文件.tar 镜像名:version`            |
| 改名/打标签 | `docker tag 镜像id 要改的镜像名字：版本号`<br>`docker rename 容器名称或ID 新的名字`（为容器新建别名，原名仍有效） | `docker commit 容器名 镜像名`                         |

```bash
# 常用流程
docker commit 容器名 镜像名
docker save 镜像id -o backup.tar
# 在目标机器上
docker load < backup.tar
```

## 服务器系统信息

```bash
# 查看操作系统名称和版本
cat /etc/os-release

# 查看内核版本
uname -r

# 查看系统架构
uname -m

# 查看更详细的系统信息（推荐）
lsb_release -a

# 查看所有系统信息
hostnamectl
```

## Conda 版本查看

```bash
# 查看 conda 地址
conda info --env

# 查看当前使用的 conda
cat <conda_path>/LICENSE.txt
```

根据 LICENSE.txt 页面信息可区分：

- **Anaconda**：完整发行版，页面较长
- **Miniconda**：精简版，页面较短
- **Mini-forge**：社区版，含 conda-forge 通道标识

## 本地 SSH 公钥复制到服务器

```bash
# 在本地机器生成 SSH 密钥对
ssh-keygen -t rsa
# 将在 ~/.ssh/ 目录下生成 id_rsa 和 id_rsa.pub 文件

# 将公钥添加到远程服务器的授权文件
ssh-copy-id your_username@10.162.194.12

# 测试 SSH 连接
ssh your_username@10.162.194.12
```

## Conda 虚拟环境

```bash
# 查看已有虚拟环境
conda env list

# 基于 base 环境创建虚拟环境
conda create --name llava --clone base
# 基于指定 Python 版本创建
# conda create --name {name} python=3.9 -y

# 初始化 conda（首次使用）
conda init bash
source ~/.bashrc

# 激活 / 删除虚拟环境
conda activate llava
conda remove --name llava --all -y

# 容器之间环境导入
conda env export --name base > environment_qwen.yml
conda env create -f environment_qwen.yml --name qwen2.5-vl --no-deps
```

## 常见问题处理

**terminals database is inaccessible**

```bash
apt install ncurses-term
```

## 环境源码安装路径

| 软件           | 下载地址                                                                                                       |
| -------------- | -------------------------------------------------------------------------------------------------------------- |
| Miniforge      | https://github.com/conda-forge/miniforge/releases                                                              |
| PyTorch        | https://pytorch.org/get-started/previous-versions/                                                             |
| vLLM           | https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html#use-the-local-cutlass-for-compilation      |
| Flash-Attention | https://github.com/Dao-AILab/flash-attention/releases                                                          |
| Flash-Attn 3 预编译包 | https://github.com/mjun0812/flash-attention-prebuild-wheels/releases?page=4#release-v0.8.2               |
| Detectron2     | https://detectron2.readthedocs.io/en/latest/tutorials/install.html                                             |
| CUDA Toolkit   | https://developer.nvidia.com/cuda-toolkit-archive                                                             |
| VS Code        | https://code.visualstudio.com/updates/v1_98                                                                   |
| VS Code Remote-SSH | https://code.visualstudio.com/docs/remote/faq#_can-i-run-vs-code-server-on-older-linux-distributions       |
| Node.js        | https://nodejs.org/en/download/                                                                                |

Flash-Attention 离线安装示例：

```bash
pip install --no-deps --force-reinstall https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3.post1/flash_attn-2.8.3.post1+cu12torch2.8cxx11abiFALSE-cp311-cp311-linux_x86_64.whl
```