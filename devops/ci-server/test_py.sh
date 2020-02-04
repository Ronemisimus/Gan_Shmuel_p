#!/bin/bash

for f in test/*.py
do
    result=$(python3 "$f");
    echo this is the result: $result

    if [ $result -eq 0 ]
        then
            continue
        else
            exit 1 
done