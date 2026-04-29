#!/bin/bash

hailomz compile \
 --ckpt /shared/models/board.onnx \
 --calib-path /shared/out/resized_images-2 \
 --yaml hailo_model_zoo/cfg/networks/yolov11n_obb.yaml \
 --classes 1 \
 --hw-arch hailo10h
