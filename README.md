
# DeepNude-BydloCoding edition

DeepNude Source Code + VK Bot
powered by VK-SDK

[The README.md in English](https://github.com/zhengyima/DeepNude_NoWatermark_withModel/blob/master/README_EN.md)

DeepNude源代码

去水印 

带三个模型.lib文件下载地址

供广大程序员技术交流使用

~~[demo地址](http://39.105.149.229/dn): demo很原始脆弱不鲁棒，所以感兴趣的话尽量还是自己去跑代码吧。不要对demo做坏事哦，不然就关掉= =~~

# Preinstallation

Before launch the script install these packages in your **Python3** environment:
- numpy
- Pillow
- setuptools
- six
- pytorch 
- torchvision
- wheel
```
pip3 install numpy pillow setuptools six pytorch torchvision wheel
```

建议使用Conda安装 :) 


```
 conda create -n deepnude python=3.6 numpy Pillow setuptools six pytorch torchvision wheel
 conda activate deepnude
```

**注：如果懒得折腾Python环境，也可以使用docker一键运行，见下**

感谢网友[飞哥](https://github.com/fizzday)提供docker一键运行部分技术支持

## 使用docker一键运行
```bash
cd ~

git clone https://github.com/zhengyima/DeepNude_NoWatermark_withModel.git --depth 1 deepnude

cd deepnude

docker run --rm -it -v $PWD:/app:rw ababy/python-deepnude /bin/bash

python main.py
```
> 注意: docker运行只能使用cpu,所以,需要修改gpu运行为cpu, 修改方法请参考 [#GPU](#gpu). 实际运行速度也慢不了多少.  

> 对应的三个 .lib 文件需要自己手动下载后, 添加到项目根目录 `checkpoints` 目录下, 才能正常运行, 由于文件太大, 就没有放入docker镜像

# Models

在运行之前需下载三个.lib文件，之后在项目根目录下新建checkpoints目录，将下载的三个文件放至checkpoints目录下。

友情提供以下两种下载渠道：


* [Link](http://39.105.149.229/dn.7z)

* [Google Drive](https://drive.google.com/drive/folders/1OKuIp0nxMUucgEScTc2vESvlpKzIWav4?usp=sharing)


# Launch the script

环境配好，模型下好之后便可以运行代码了！

```
 python main.py
```

The script will transform *input.png* to *output.png*.




# GPU

本项目默认使用id为0的GPU运行。

若运行环境不带GPU，则报错。如果没有GPU或想使用CPU运行程序，请将gan.py中

```
self.gpu_ids = [0] #FIX CPU
```

改为 (

```
self.gpu_ids = [] #FIX CPU
```

## Links
- https://pytorch.org/

