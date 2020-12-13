#!/bin/bash

for pid in {5000..5043}
do
    lsof -t -i:$pid | xargs kill -9
done

for pid in {8000..8007}
do 
    lsof -t -i:$pid | xargs kill -9
done

for pid in {9000..9007}
do
    lsof -t -i:$pid | xargs kill -9 
done