#!/bin/bash
DOCKER_NAME=mtk_quantize
IMAGE_ID=770792e7f027

# docker stop ${DOCKER_NAME}
# docker rm ${DOCKER_NAME}

# 35服务器
# docker run -it --name ${DOCKER_NAME} \
#                --privileged=true \
#                --gpus all \
#                --shm-size 128G \
#                -v /data0/m00028512/workspace:/workspace \
#                -v /data0/m00028512/datasets:/workspace/datasets  \
#                -v /data0:/data0 \
#                --workdir /workspace \
#                --network host ${IMAGE_ID} \
#                bash \
            #    -c "echo 'export PS1=\"(${DOCKER_NAME}) \$PS1\"' >> /root/.bashrc && exec /bin/bash"

# 35 - 33服务器 (映射关系)
# docker run -it \
#             --name ${DOCKER_NAME} \
#             --gpus all \
#             --shm-size 128G \
#             -v /opt/data/m00028512/194_35/workspace:/workspace \
#             -v /opt/data/m00028512/194_35/datasets:/workspace/datasets \
#             -v /opt:/opt \
#             --workdir /workspace \
#             --network host ${IMAGE_ID} \
#             bash \
#             --privileged=true \
#             -c "echo 'export PS1=\"(${DOCKER_NAME}) \$PS1\"' >> /root/.bashrc && exec /bin/bash"

# 35 - 33服务器 (映射关系-HumanParsing)
# docker run -it \
#             --name ${DOCKER_NAME} \
#             --gpus all \
#             --shm-size 128G \
#             -v /opt/data/m00028512/HumanParsing/workspace:/workspace \
#             -v /opt/data/m00028512/HumanParsing/datasets:/workspace/datasets \
#             -v /opt:/opt \
#             --workdir /workspace \
#             --network host ${IMAGE_ID} \
#             bash \
#             -c "echo 'export PS1=\"(${DOCKER_NAME}) \$PS1\"' >> /root/.bashrc && exec /bin/bash"


# 33服务器
docker run -it \
               --name ${DOCKER_NAME} \
               --gpus all \
               --shm-size 128G \
               -v /opt/data/m00028512/12_data0_m0028512/m00028512/workspace:/workspace \
               -v /opt/data/m00028512/12_data0_m0028512/m00028512/datasets:/workspace/datasets \
               -v /opt/data/m00028512/194_35/workspace/software:/workspace/software \
               -v /opt:/opt \
               -v /opt/data/m00028512/194_35/workspace/MTKQuantize:/workspace/MTKQuantize \
               --workdir /workspace \
               --network host ${IMAGE_ID} \
               bash
            #    -c "echo 'export PS1=\"(${DOCKER_NAME}) \$PS1\"' >> /root/.bashrc" \

# sed -i "s/^PS1='(ys_llava)/PS1='/" /root/.bashrc
# source /root/.bashrc
