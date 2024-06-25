#!/bin/bash
# Job Name and Files (also --job-name)
#SBATCH --jobe-name="yolov9-training-res800"
#SBATCH --partition=lrz-v100x2
#SBATCH --gres=gpu:2
#Output and error (also --output, --error):
#SBATCH -o ./%x.%j.out
#SBATCH -e ./%x.%j.err
#Notification and type
#SBATCH --mail-type=END
#SBATCH --mail-user=konstantin.zeck@tum.de
# Wall clock limit:
#SBATCH --time=05:00:00
#SBATCH --no-requeue
#Setup of execution environment
#needed? export=NONE
#needed? get-user-env
#needed? --account=t7431

# Set up the container environment
srun \
--mpi=pmi2 --ntasks-per-node=2 \
--container-mount='/dss/dssfs04/lwp-dss-0002/t7431/t7431-dss-0000/:/workspace/' \
--container-image='/dss/dssfs04/lwp-dss-0002/t7431/t7431-dss-0000/Pytorch+24.03-py3+yolov9.sqsh'

YOLO='/workspace/yolov9'
Lauf_num='Lauf_'

if [ -d ${YOLO}/runs/ ]; then
    rm -r ${YOLO}/runs/
fi

# Check if latest.pt exists and set the weights path accordingly
if [ -f "/workspace/weights/latest.pt" ]; then
    WEIGHTS_PATH="/workspace/weights/latest.pt"
else
    WEIGHTS_PATH="/workspace/weights/yolo-e.pt"
fi

python3 ${YOLO}/train_dual.py --batch 12 --epochs 100 --device 0 --min-items 0 --img 800 \
--name ${Lauf_num} \
--data ${YOLO}/loco.yaml \
--weights ${WEIGHTS_PATH} \
--cfg ${YOLO}/models/detect/yolov9_custom.yaml \
--hyp ${YOLO}/data/hyps/hyp.scratch.yaml \

python3 ${YOLO}/detect_dual.py --conf 0.1 --device 0 \
--name ${Lauf_num} \
--weights ${YOLO}/runs/train/${Lauf_num}/weights/best.pt \
--source ${HOME}/loco/images/val/509189,8734.jpg 