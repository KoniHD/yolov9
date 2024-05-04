#!/bin/bash
# LOCO 2020 dataset https://webdisk.ads.mwn.de/Handlers/AnonymousDownload.ashx?folder=73e976ba&path=LOCO%5Cv1
# Download command: bash ./scripts/get_loco.sh

## Download/unzip labels

d='./loco/labels'
url='https://github.com/tum-fml/loco/archive/refs/heads/master.zip'
f='loco-master.zip'
echo 'Downloading labels' $url$f ' ...'
curl -L $url -o $f && unzip -q $f && rm -r $f # download, unzip, remove in background

# Move labels to correct directory
mkdir -p $d/train
mkdir -p $d/val
mv ./loco-main/rgb/* $d
find $d -type f -name '*train*' -exec mv {} $d/train \; 2>/dev/null
find $d -type f -name '*val*' -exec mv {} $d/val \; 2>/dev/null
rm $d/loco-all-v1.json

wait # finish background tasks
rm -rf ./loco-main
echo -e '\nFinished downloading labels\n---\n'

## Download/unzip images

d='./loco/images' # unzip directory
# unshortened link: https://webdisk.ads.mwn.de/Handlers/AnonymousDownload.ashx?folder=73e976ba&path=LOCO%5Cv1%5Cdataset.zip
url='https://go.mytum.de/239870'
f='dataset.zip'
echo 'Downloading datasets' $url '...'
curl -L $url -o $f && unzip -q $f && rm -r $f # download, unzip, remove in background

set1='subset-1'     # validation
set2='subset-2'     # training
set3='subset-3'     # training
set4='subset-4'     # validation
set5='subset-5'     # training

# Move images to correct directory
mkdir -p $d/train
mkdir -p $d/val
# train directory
for set in $set2 $set3 $set5; do
    mv ./dataset/$set/* $d/train
done
# val directory
for set in $set1 $set4; do
    mv ./dataset/$set/* $d/val
done

wait # finish background tasks
rm -rf ./dataset
echo -e '\nFinished downloading LOCO dataset\n---\n'