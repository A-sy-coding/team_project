#!/bin/bash

echo "pip recently upgrade..."
pip install --upgrade pip

echo "pytorch install..."
pip3 install torch torchvision torchaudio

echo "model weights download..."
wget https://github.com/A-sy-coding/team_project/releases/latest/download/pose_model_scratch.pth
mv pose_model_scratch.pth ../