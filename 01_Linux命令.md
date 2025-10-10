# 系统文件相关

# nvidia-smi 实时更新

```Bash
watch -n 1 nvidia-smi
```

## 列出当前文件夹所有子文件夹的文件个数

```Bash
find . -type d -exec sh -c 'echo -n "{}: "; find "{}" -type f | wc -l' \;\
```

设置环境可用CUDA

```Bash
export CUDA_VISIBLE_DEVICES=5,6,7
echo $CUDA_VISIBLE_DEVICES
```

