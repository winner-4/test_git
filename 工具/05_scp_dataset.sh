#!/bin/bash
clear
# 获取当前时间函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 远程服务器信息
REMOTE_IP="10.162.198.33"
REMOTE_USER="m00028512"
REMOTE_PASS="Mph00028512@"
BASE_NAME="02_HumanParsing"
REMOTE_DIR="/opt/data/m00028512/HumanParsing/datasets/$BASE_NAME"

# 本地目录
LOCAL_DIR="/data0/m00028512/datasets/$BASE_NAME"

log "开始处理本地目录：$LOCAL_DIR"
echo

# 遍历本地目录下的所有文件和文件夹
for item in "$LOCAL_DIR"/*; do
    if [ -d "$item" ]; then
        # 是文件夹，打包传输
        folder_name=$(basename "$item")
        tar_file="${folder_name}.tar.gz"

        # 判断本地是否存在打包文件
        if [ -f "$tar_file" ]; then
            log "本地已存在打包文件 $tar_file，准备传输。"
        else
            log "打包文件夹 $LOCAL_DIR/$folder_name ..."
            tar -czf "$tar_file" -C "$LOCAL_DIR" "$folder_name"
            if [ $? -ne 0 ]; then
                log "ERROR: 打包文件夹 $folder_name 失败！跳过该文件夹。"
                continue
            fi
        fi

        # 判断远程服务器是否已存在该tar包
        sshpass -p "$REMOTE_PASS" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_IP" "test -f '$REMOTE_DIR/$tar_file'"
        if [ $? -eq 0 ]; then
            log "远程服务器已存在 $tar_file，跳过传输和解压。"
            # 如果你想删除本地打包文件，可以在这里加 rm -f "$tar_file"
            # 但建议保留，避免重复打包
        else
            log "传输 $tar_file 到远程服务器 $REMOTE_IP ..."
            sshpass -p "$REMOTE_PASS" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_IP" "mkdir -p '$REMOTE_DIR'"
            sshpass -p "$REMOTE_PASS" scp "$tar_file" "$REMOTE_USER@$REMOTE_IP:$REMOTE_DIR/"

            if [ $? -eq 0 ]; then
                log "传输成功，删除本地的 $tar_file"
                rm -f "$tar_file"

                log "远程解压 $tar_file ..."
                sshpass -p "$REMOTE_PASS" ssh "$REMOTE_USER@$REMOTE_IP" "cd $REMOTE_DIR && tar -xzf $tar_file && rm -f $tar_file"
                if [ $? -eq 0 ]; then
                    log "远程解压成功：$tar_file"
                else
                    log "ERROR: 远程解压失败：$tar_file"
                fi
            else
                log "ERROR: 传输失败，保留本地的 $tar_file"
            fi
        fi
        echo

    elif [ -f "$item" ]; then
        # 是文件，直接传输
        file_name=$(basename "$item")
        log "传输文件 $LOCAL_DIR/$file_name 到远程服务器 $REMOTE_IP ..."
        sshpass -p "$REMOTE_PASS" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_IP" "mkdir -p '$REMOTE_DIR'"
        sshpass -p "$REMOTE_PASS" scp "$item" "$REMOTE_USER@$REMOTE_IP:$REMOTE_DIR/"

        if [ $? -eq 0 ]; then
            log "文件 $file_name 传输成功。"
        else
            log "ERROR: 文件 $file_name 传输失败。"
        fi
        echo
    else
        log "跳过非文件非文件夹项：$item"
    fi
done

log "所有文件和文件夹处理完成。"
