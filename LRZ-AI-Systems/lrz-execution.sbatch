#!/bin/bash
#SBATCH -p lrz-v100x2
#SBATCH --gres=gpu:1
#SBATCH -o yolov9-training-%j.out
#SBATCH -e yolov9-training-%j.err
#SBATCH --job-name="yolov9-training"

srun \
--container-mount='./:/workspace/yolov9' \
--container-image='nvcr.io/nvidia/pytorch:24.03-py3'
YOLO='/workspace/yolov9'
python3 $YOLO/train_dual.py --batch 16 --epochs 100 --device 0 --min-items 0 --img 640 \
--data $YOLO/loco.yaml \
--weights $YOLO/weights/yolov9-e.pt \
--cfg $YOLO/models/detect/yolov9_custom.yaml \
--hyp $YOLO/data/hyps/hyp.scratch.yaml \