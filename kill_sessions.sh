#!/bin/bash

for pid in {5000..5010}
do
    lsof -t -i:$pid | xargs kill -9
done

for pid in {8000..8001}
do 
    lsof -t -i:$pid | xargs kill -9
done

lsof -t -i:9000 | xargs kill -9