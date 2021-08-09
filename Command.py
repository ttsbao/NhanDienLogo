import torch
from IPython.display import Image, clear_output  # to display images
import wandb
wandb.login()


# Test

# python test.py --weights runs/train/exp/weights/best.pt --data logo.yaml --img 640 --iou 0.65 --half

# python test.py --weights runs/train/exp7/weights/best.pt --data logo.yaml --img 640 --iou 0.65 --half

# python test.py --weights runs/train/exp8/weights/best.pt --data logo.yaml --img 640 --iou 0.65 --half

# python test.py --weights runs/train/exp9/weights/best.pt --data logo1.yaml --img 640 --iou 0.65 --half

# python test.py --weights runs/train/exp10/weights/best.pt --data logo2.yaml --img 640 --iou 0.65 --half

# python test.py --weights runs/train/exp11/weights/best.pt --data logo3.yaml --img 640 --iou 0.65 --half

# python test.py --weights runs/train/exp12/weights/best.pt --data logo4.yaml --img 640 --iou 0.65 --half

# python test.py --weights runs/train/exp12/weights/test2.pt --data logo4.yaml --img 640 --iou 0.65 --half

# Detect

# python detect.py --weights runs/train/exp11/weights/best.pt --img 640 --conf 0.25 --source ../datasets/Logo/video/highland_coffee.mp4
# python detect.py --weights runs/train/exp11/weights/best.pt --img 640 --conf 0.25 --source ../datasets/Logo/video/tiki.mp4
# python detect.py --weights runs/train/exp11/weights/best.pt --img 640 --conf 0.25 --source ../datasets/Logo/video/fpt.mp4
# python detect.py --weights runs/train/exp10/weights/best.pt --img 640 --conf 0.25 --source ../datasets/Logo/video/thegioididong.mp4
# python detect.py --weights runs/train/exp11/weights/best.pt --img 640 --conf 0.25 --source ../datasets/Logo/video/vinamilk.mp4
# python detect.py --weights runs/train/exp11/weights/best.pt --img 640 --conf 0.25 --source ../datasets/Logo/video/viettel.mp4
# python detect.py --weights runs/train/exp11/weights/best.pt --img 640 --conf 0.25 --source ../datasets/Logo/video/cgv.mp4
# python detect.py --weights runs/train/exp11/weights/best.pt --img 640 --conf 0.25 --source ../datasets/Logo/video/acecook.mp4

# Train
# python train.py --img 640 --batch 4 --epochs 3 --data logo.yaml --weights runs/train/exp7/weights/best.pt --cache

# python train.py --img 640 --batch 4 --epochs 20 --data logo.yaml --weights yolov5x6.pt --cache

# exp  python train.py --img 640 --batch 16 --epochs 20 --data logo.yaml --weights yolov5x6.pt --cache

# exp2  python train.py --img 640 --batch 8 --epochs 20 --data logo.yaml --weights yolov5x6.pt --cache

# exp3  python train.py --img 640 --batch 4 --epochs 20 --data logo.yaml --weights yolov5x6.pt --cache

# exp4  python train.py --img 640 --batch 4 --epochs 20 --data logo.yaml --weights runs/train/exp3/weights/last.pt --cache

# exp5  python train.py --img 640 --batch 4 --epochs 100 --data logo.yaml --weights yolov5x6.pt --cache

# exp6  python train.py --img 640 --batch 16 --epochs 200 --data logo.yaml --weights yolov5x6.pt --cache

# exp7 python train.py --img 640 --batch 8 --epochs 100 --data logo.yaml --weights yolov5x6.pt --cache

# exp8 python train.py --img 640 --batch 4 --epochs 100 --data logo.yaml --weights yolov5x6.pt --cache

# exp9 python train.py --img 640 --batch 4 --epochs 100 --data logo1.yaml --weights yolov5x6.pt --cache

# exp10 python train.py --img 640 --batch 4 --epochs 100 --data logo2.yaml --weights yolov5x6.pt --cache

# exp11 python train.py --img 640 --batch 4 --epochs 100 --data logo3.yaml --weights yolov5x6.pt --cache

# exp12 python train.py --img 640 --batch 4 --epochs 1 --data logo4.yaml --weights yolov5s.pt --cache



# exp12 python train.py --img 240 --batch 4 --epochs 1 --project ../clienta/Khry8IBR8PfFqf0nAAAD/train --nosave --data ../clienta/Khry8IBR8PfFqf0nAAAD/Khry8IBR8PfFqf0nAAAD.yaml --weights yolov5s.pt --cache

"""


"""