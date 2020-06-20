#   OCR 识别


通过调用trdg，自动生成中文手写体图片， 然后通过FOTS 进行文本区域检测。


## 建立环境

```shell script
conda create -n  ocr-cn python=3.6 pip scipy numpy ##运用conda 创建python环境
source activate ocr-cn
pip install -r requirements.txt -i https://mirrors.163.com/pypi/simple/
```


## 数据下载
# 中文文本数据
sh ./shell/get_sample_data.sh
```

## 数据保存路径

生成数据在./output 下面

```shell script
.             #解压以后路径
└── raw_data
    ├── cnews_data.zip
    ├── cnews.test.txt
    ├── cnews.train.txt
    └── cnews.val.txt       #验证数据集 

```


##  训练脚本说明  

```shell script
cd ./shell 
sh splite_text.sh
 
```

## 文字生成图片 

* 文本生成图片  [TRDG 文本生成图片代码](https://github.com/Belval/TextRecognitionDataGenerator)
* 可以添加多种手写字体文件  [免费中文字体文件下载地址](http://www.sucaijishi.com/material/font/)
 