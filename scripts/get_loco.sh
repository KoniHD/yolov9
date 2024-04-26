#!/bin/bash
# LOCO 2020 dataset https://webdisk.ads.mwn.de/Handlers/AnonymousDownload.ashx?folder=73e976ba&path=LOCO%5Cv1
# Download command: bash ./scripts/get_loco.sh

# Download/unzip labels
url='https://github.com/tum-fml/loco/archive/refs/heads/master.zip'
f='loco-master.zip'
echo 'Downloading labels' $url$f ' ...'
curl -L $url -o $f && unzip -q $f && rm -r $f # download, unzip, remove in background
mkdir -p -v './labels'
mv ./loco-main/rgb/* ./labels
rm -rf ./loco-main
wait # finish background tasks
echo 'Finished downloading labels'

# Download/unzip images
d='./loco/images' # unzip directory
url='https://webdisk.ads.mwn.de/Handlers/AnonymousDownload.ashx?folder=73e976ba&path=LOCO%5Cv1%5Cdataset.zip'
f='dataset.zip'
echo 'Downloading datasets' $url '...'
curl -L $url -o $f && unzip -q $f && rm -r $f # download, unzip, remove in background
mkdir -p -v $d
set1='subset-1'
set2='subset-2'
set3='subset-3'
set4='subset-4'
set5='subset-5'
for set in $set1 $set2 $set3 $set4 $set5; do
    mkdir -p -v $d/$set
    mv ./dataset/$set/* $d/$set
done
wait # finish background tasks
rm -rf ./dataset