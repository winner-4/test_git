import os
import sys
import re
import struct
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="荣耀/华为实况照片 (Motion Photo) 视频提取工具")
    
    # =========================================================================
    # 你可以在 default 中填入需要处理的【单张图片完整路径】或【图片所在文件夹路径】
    # =========================================================================
    parser.add_argument(
        "--input", 
        type=str, 
        default=r"D:\code\datasets\07_phone",  # <--- 在此修改你的默认输入路径
        help="目标图片文件路径 或 包含图片的文件夹路径"
    )
    
    return parser.parse_args()


def extract_video_from_bytes(data: bytes):
    """
    智能分析图片数据流，剥离出合法的 MP4 视频流数据
    """
    file_len = len(data)
    video_data = None

    # 策略 1: 读取 XMP 元数据中的 MicroVideoOffset / MotionPhotoOffset 偏移量
    offset_match = re.search(rb'(?:MicroVideoOffset|MotionPhotoOffset)[="]+(\d+)', data)
    if offset_match:
        offset_val = int(offset_match.group(1))
        candidate_start = file_len - offset_val
        if 0 < candidate_start < file_len:
            # 校验 MP4 头部特征: 前 4 字节为 box 大小，紧接 'ftyp'
            if data[candidate_start + 4 : candidate_start + 8] == b'ftyp':
                video_data = data[candidate_start:]

    # 策略 2: 逆向查找合法的 MP4 ftyp box
    if video_data is None:
        pos = file_len
        valid_starts = []
        while True:
            pos = data.rfind(b'ftyp', 0, pos)
            if pos == -1:
                break
            box_start = pos - 4
            if box_start >= 0:
                box_len = struct.unpack('>I', data[box_start : box_start + 4])[0]
                # 校验 box 大小是否合乎规范
                if 8 <= box_len <= 1024:
                    valid_starts.append(box_start)
            pos = box_start

        if valid_starts:
            # 选取距离文件末尾最近、最具可能性的完整视频流头部
            best_start = valid_starts[0]
            video_data = data[best_start:]

    return video_data


def process_single_file(file_path: Path, output_dir: Path):
    """
    处理单张照片并输出到目标文件夹
    """
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        video_data = extract_video_from_bytes(data)

        if video_data:
            out_file = output_dir / f"{file_path.stem}.mp4"
            with open(out_file, 'wb') as f:
                f.write(video_data)
            print(f"[成功] {file_path.name} -> {out_file.name} ({len(video_data) / 1024 / 1024:.2f} MB)")
            return True
        else:
            print(f"[跳过] {file_path.name} (未检测到动态视频流)")
            return False
    except Exception as e:
        print(f"[异常] 处理 {file_path.name} 失败: {e}")
        return False


def main():
    args = parse_args()
    input_target = Path(args.input)

    if not input_target.exists():
        print(f"错误: 指定的路径不存在 -> {input_target}")
        sys.exit(1)

    # 1. 确定输出目录：相同父级目录下的 'livephoto' 文件夹
    if input_target.is_file():
        parent_dir = input_target.parent
        target_files = [input_target]
    else:
        parent_dir = input_target
        # 扫描文件夹内所有 jpg/jpeg 格式照片（不区分大小写）
        target_files = sorted([
            p for p in input_target.iterdir() 
            if p.is_file() and p.suffix.lower() in ('.jpg', '.jpeg')
        ])

    output_dir = parent_dir / "livephoto"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"输入路径: {input_target}")
    print(f"输出目录: {output_dir}")
    print(f"待检文件数量: {len(target_files)}")
    print("=" * 60)

    # 2. 依次执行提取
    success_count = 0
    for file_path in target_files:
        if process_single_file(file_path, output_dir):
            success_count += 1

    print("=" * 60)
    print(f"处理完成！成功导出: {success_count} / {len(target_files)} 个视频文件。")
    print(f"视频存放路径: {output_dir}")


if __name__ == "__main__":
    main()
