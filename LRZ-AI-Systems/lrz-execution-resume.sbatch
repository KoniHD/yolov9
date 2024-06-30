#!/bin/bash
# Job Name and Resources
#SBATCH --job-name="yolov9e-training-res800"
#SBATCH --partition=lrz-hgx-a100-80x4
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#Output and error (also --output, --error):
#SBATCH -o /dss/dsshome1/0D/ge78taz2/batch_jobs/output/%x.%j.out
#SBATCH -e /dss/dsshome1/0D/ge78taz2/batch_jobs/error/%x.%j.err
#Notification and type
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=konstantin.zeck@tum.de
# Wall clock limit:
#SBATCH --time=05:00:00
#SBATCH --no-requeue
#Setup of execution environment
#SBATCH --export=NONE

export WORLD_SIZE=1
export RANK=-1
export LOCAL_RANK=-1
export MASTER_ADDR="localhost"
export MASTER_PORT=29400

YOLO='/workspace/yolov9'
Lauf_num='Lauf_1'
WEIGHTS_PATH="/workspace/yolov9/runs/train/${Lauf_num}/weights/best.pt"


# if [ -d "/dss/dsshome1/0D/ge78taz2/bachelor-thesis/dss-for-ai/yolov9/runs/" ]; then
#     rm -r "/dss/dsshome1/0D/ge78taz2/bachelor-thesis/dss-for-ai/yolov9/runs/"
# fi


# Set up the container environment
srun --export=WORLD_SIZE,RANK,LOCAL_RANK,MASTER_ADDR,MASTER_PORT \
--container-mounts='/dss/dssfs04/lwp-dss-0002/t7431/t7431-dss-0000:/workspace' \
--container-image='/dss/dssfs04/lwp-dss-0002/t7431/t7431-dss-0000/Pytorch+24.03-py3+yolov9.sqsh' \
python3 ${YOLO}/train_dual.py --batch 8 --epochs 250 --device 0 --min-items 0 --img 800 \
--name ${Lauf_num} \
--data ${YOLO}/loco-container.yaml \
--resume ${WEIGHTS_PATH} \
--cfg ${YOLO}/models/detect/yolov9_custom.yaml \
--hyp ${YOLO}/data/hyps/hyp.scratch-high.yaml \