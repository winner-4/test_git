#!/bin/bash

# 定义输出文件
output_FA_so="md5_FA_so.txt"
output_FA_bin="md5_FA_bin.txt"
output_FA_xml="md5_FA_xml.txt"


output_FAB_so="md5_FAB_so.txt"
output_FAB_bin="md5_FAB_bin.txt"

output_FP_so="md5_FP_so.txt"
output_FP_bin="md5_FP_bin.txt"
output_FP_xml="md5_FP_xml.txt"

output_PS_bin="md5_PS_bin.txt"
output_PS_xml="md5_PS_xml.txt"

rm -r *.txt

# 获取当前日期
current_date=$(date +"%m-%d")

# 定义一个函数来计算 MD5 值并写入输出文件
calculate_md5() {
    local file_pattern=$1
    local output_file=$2

    # 查找所有符合条件的文件并计算 MD5 值
    find . -type f -name "$file_pattern" -not -path "./FD2.0/*" -not -path "./AICloud/*" -exec md5sum {} \; | while read -r line; do
        md5=$(echo $line | awk '{print $1}')
        filepath=$(echo $line | awk '{print $2}')

        filename=$(basename "$filepath")

        # 提取平台和手机信息
        platform=$(echo $filepath | awk -F'/' '{print $9}')
        phone=$(echo $filepath | awk -F'/' '{print $10}')

        # 计算文件大小并转换为 KB
        filesize_kb=$(du -k "$filepath" | awk '{print $1}')
        filesize_mb=$(echo "scale=2; $filesize_kb / 1024" | bc)  # 转换为 MB

        # 将结果写入输出文件
        echo "$current_date $platform $phone $md5 $filesize_kb KB $filesize_mb MB $filename $filepath" >> $output_file
    done

    # 按照平台和手机分组并排序
    sort -k2,2 -k3,3 $output_file -o $output_file
}

echo

# Start processing FA files
echo "Starting to process FA files..."
calculate_md5 "libHnFaceAttribute.so" "$output_FA_so"
calculate_md5 "libHnFaceAttributev5.so" "$output_FA_so"
calculate_md5 "HnFaceAttributeEMB*" "$output_FA_bin"
calculate_md5 "FaceAttributeConfig*" "$output_FA_xml"
echo "FA files processing completed."
echo

# Start processing FAB files
echo "Starting to process FAB files..."
calculate_md5 "libHnFaceAttributeBlink.so" "$output_FAB_so"
calculate_md5 "HnFaceAttributeBlink.bin" "$output_FAB_bin"
echo "FAB files processing completed."
echo

# Start processing FP files
echo "Starting to process FP files..."
calculate_md5 "libUnifiedSeg.so" "$output_FP_so"
calculate_md5 "faceparsing.bin" "$output_FP_bin"
calculate_md5 "face_parse.xml" "$output_FP_xml"
echo "FP files processing completed."
echo

# # Start processing PS files
# echo "Starting to process PS files..."
# calculate_md5 "portraitskinseg.bin" "$output_PS_bin"
# calculate_md5 "portraitskin_seg.xml" "$output_PS_xml"
# echo "PS files processing completed."
# echo

# End of script
echo "All files processing completed."
