#!/bin/bash
gcc     averages.c   -o averages -lm
cd ..
rm results/finalResult.txt

./scripts/averages 1 < results/1/outputFiltered.txt
