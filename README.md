#   OCR 识别


通过调用生成随机图片，自动生成中文手写体图片， 进行文本区域检测。


## 建立环境

```shell script
conda create -n  ocr-cn python=3.6 pip scipy numpy ##运用conda 创建python环境
source activate ocr-cn
pip install -r requirements.txt -i https://mirrors.163.com/pypi/simple/
```

## 字符串切割

```
sh split_text/split_text.sh split_text/sample_data/test.txt   
```


## 生成合成图片 

```shell script
python3 synth_image/run.py -c 3 --font_dir synth_image/fonts/cn -i dataset/text_split.txt -lc 50

```

## 文字生成图片 

* 文本生成图片  [TRDG 文本生成图片代码](https://github.com/Belval/TextRecognitionDataGenerator)
* 可以添加多种手写字体文件  [免费中文字体文件下载地址](http://www.sucaijishi.com/material/font/)
 
 
## 示例图片

![image](./images/0.jpg)

![image](./images/1.jpg)


![image](./images/2.jpg)