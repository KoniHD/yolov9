#!/bin/bash
# Job Name and Resources
#SBATCH --job-name="yolov9e-training-res800"
#SBATCH --partition=lrz-v100x2
#SBATCH --gres=gpu:2
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

# Set up the container environment
srun \
--mpi=pmi2 --ntasks-per-node=2 \
--container-mounts='/dss/dssfs04/lwp-dss-0002/t7431/t7431-dss-0000:/workspace' \
--container-image='/dss/dssfs04/lwp-dss-0002/t7431/t7431-dss-0000/Pytorch+24.03-py3+yolov9.sqsh' \
torchrun --nproc_per_node 2 --master_port ${MASTER_PORT:-9528} /workspace/yolov9/train_dual.py \
--workers 8 --device 0,1 --sync-bn --batch 8 \
--epochs 250 --min-items 0 --img 800 \
--name Lauf_1 \
--data /workspace/yolov9/loco.yaml \
--weights /workspace/weights/yolo-e.pt \
--cfg /workspace/yolov9/models/detect/yolov9_custom.yaml \
--hyp /workspace/yolov9/data/hyps/hyp.scratch-high.yaml \