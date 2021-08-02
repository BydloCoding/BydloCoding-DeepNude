
# DeepNude

DeepNude Source Code 

without watermark

with the download link of the 3 model files:cm.lib,mm.lib,mn.lib

for research and development communication

~~[demo link](http://39.105.149.229/): The demo is a primary, delicate and not robust enough, so try to focus more on the github repository and run the program yourself :)~~

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
pip3 install numpy pilliow setuptools six pytorch torchvision wheel
```

Tips: use Anaconda to install, with the following command  :) 


```
 conda create -n deepnude -c anaconda python=3.6 numpy Pillow setuptools six pytorch torchvision wheel
 conda activate deepnude
```

**Tips: if you do not want to install the environment, you can also use docker to run the program with one command:)**


## Use docker to run the program
```bash
cd ~

git clone https://github.com/zhengyima/DeepNude_NoWatermark_withModel.git deepnude

cd deepnude

docker run --rm -it -v $PWD:/app:rw ababy/python-deepnude /bin/bash

python main.py
```

> Tips: Using docker to run the program, you can only use cpu. Therefore, you should modify the gpu to cpu in the code, which you can refer to [#GPU](#gpu). In fact, the speed is almost the same between cpu and gpu.

# Models

* [Google Drive](https://drive.google.com/drive/folders/1OKuIp0nxMUucgEScTc2vESvlpKzIWav4?usp=sharing): *you should download the three .lib files before running the program. Then create a dir named 'checkpoints' under the root dir of the project. Put the three downloaded files to the 'checkpoints' dir*




# Launch the script

After you install the environment, you can run the program !

```
 python main.py
```

The script will transform *input.png* to *output.png*.



# GPU
default use GPU with id 0. if your environment do not have GPU, please modify the code in `gan.py`


```
self.gpu_ids = [0] #FIX CPU
```

to

```
self.gpu_ids = [] #FIX CPU
```

## Links
- https://pytorch.org/

