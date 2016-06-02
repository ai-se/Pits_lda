#! /bin/bash

rm -rf Wikipedia/*
rm -rf log/*
rm -rf dump/*

for VAR in "1" "2" "3" "4" "5" "6" "7" "8" "9"; do
    ~/spark/spark_latest/bin/spark-submit DE.py spark://152.46.20.209:7077 wiki1 152.46.20.209 aagrawa8 "$VAR" > log/"$VAR".log &
done
