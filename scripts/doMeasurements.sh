#!/bin/bash
make filter

CASES=(0)
cd ..

rm -r results

mkdir results

mkdir results/1
for _ in $(seq 15); do
  docker-compose up -d

  ./scripts/collectStats.sh 1 &
  sleep 10
  ./scripts/filter < results/1/output.txt >> results/1/outputFiltered.txt
  docker-compose down
done