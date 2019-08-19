# Script file for setting up opencv-4.1.0 with GPU
# Reference: https://github.com/open-mmlab/mmaction/issues/9

wget -O OpenCV-4.1.0.zip wget https://github.com/opencv/opencv/archive/4.1.0.zip 
unzip OpenCV-4.1.0.zip
wget -O OpenCV_contrib-4.1.0.zip https://github.com/opencv/opencv_contrib/archive/4.1.0.zip
unzip OpenCV_contrib-4.1.0.zip
rm -f *.zip

cd opencv-4.1.0
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DWITH_CUDA=ON -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.1.0/modules/ -DWITH_TBB=ON -DBUILD_opencv_cnn_3dobj=OFF -DBUILD_opencv_dnn=OFF -DBUILD_opencv_dnn_modern=OFF -DBUILD_opencv_dnns_easily_fooled=OFF ..
make -j
cd ../../

mkdir build && cd build
OpenCV_DIR=../opencv-4.1.0/build/ cmake ..
make -j
