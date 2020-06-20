#!/bin/bash

echo $#  '生成中文数据集'
if [ $# -ne 1 ]
then
    echo "Usage: $0 './sample_data/test.txt'"
    exit
fi

startTime=`date +%Y%m%d-%H:%M`
startTime_s=`date +%s`

BASE_DIR="../dataset/"

if [ ! -d ${BASE_DIR} ];then
mkdir ${BASE_DIR}
fi

export PYTHONPATH=./
echo "start --------- segment  string -- "
python3 ./segment_string.py -mi 2 -ma 20 -i $1 --output_dir ${BASE_DIR}

echo 'input file line count: '
wc -l $1

echo "start --------- generate  image --"
TOTAL_COUNT=$(wc -l ${BASE_DIR}'text_split.txt' | awk '{print $1}')

echo 'line count' ${TOTAL_COUNT}


endTime=`date +%Y%m%d-%H:%M`
endTime_s=`date +%s`
echo "$startTime ---> $endTime"