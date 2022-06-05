#!/bin/bash
rm results/$1/output.txt
while [ 1 -eq 1 ]; do
  docker stats --no-stream --format "{{.CPUPerc}} | {{.NetIO}}"  >> results/$1/output.txt
done