import os
import os.path as osp

# 1. snapshot_download 下载huggingface_hub
# from huggingface_hub import snapshot_download
# repo_id = "geshang/Seg-R1-7B"
# local_dir = f'/data0/m00028512/workspace/checkpoints'
# os.makedirs(local_dir, exist_ok=True)
# print(f'🚩 Downlding HuggingFace File {repo_id} start, saved as {local_dir}')
# snapshot_download(
#     repo_id=repo_id,
#     cache_dir=local_dir,
#     local_dir_use_symlinks=False,  # 禁止生成软链接，直接存储实体文件
#     max_workers=8
# )

# 2. 后续加载
# from transformers import AutoModel
# model = AutoModel.from_pretrained("/workspace/models/kanashi6_UFO")
# print(f'🏳️‍🌈 Downlding HuggingFace File {repo_id} success, saved as {local_dir}')


# 3. 通过kagglehub下载数据集
# import kagglehub
# # Download latest version
# path = kagglehub.dataset_download("wenewone/image-cropping-datasets")
# print("Path to dataset files:", path)

# 4. shell命令下载模型
# pip install -U "huggingface_hub[cli]
# hf download naver-iv/zim-anything-vitl --local-dir ./
# hf download Perceive-Anything/PAM-3B --local-dir ./
# hf download CIDAS/clipseg-rd64-refined --local-dir ./
hf download facebook/sam2.1-hiera-large --local-dir ./
hf download LongfeiHuang/SDMatte --local-dir ./
hf download openai/clip-vit-large-patch14-336 --local-dir ./
hf download lmsys/vicuna-7b-v1.5  --local-dir ./
hf download lmc22/text4seg-llava-7b-p24 --local-dir ./
