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
#needed? export=NONE
#needed? get-user-env

# Set up the container environment
srun \
--mpi=pmi2 --ntasks-per-node=2 \
--container-mounts='/dss/dssfs04/lwp-dss-0002/t7431/t7431-dss-0000:/workspace' \
--container-image='/dss/dssfs04/lwp-dss-0002/t7431/t7431-dss-0000/Pytorch+24.03-py3+yolov9.sqsh' \
python3 /workspace/yolov9/train_dual.py --batch 8 --epochs 250 --device 0 --min-items 0 --img 800 \
--name Lauf_1 \
--data /workspace/yolov9/loco.yaml \
--weights /workspace/weights/yolo-e.pt \
--cfg /workspace/yolov9/models/detect/yolov9_custom.yaml \
--hyp /workspace/yolov9/data/hyps/hyp.scratch-high.yaml \