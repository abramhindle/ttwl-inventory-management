#!/bin/bash
csvcut -d\|  -c 1,6,5,2,3 ttwl.csv  | sort -u > /tmp/ttwl-items.csv
touch ttwl-everyitem.csv
wc -l ttwl-everyitem.csv
cat ttwl-everyitem.csv /tmp/ttwl-items.csv | sort -u > /tmp/ttwl-everyitem.csv
cp /tmp/ttwl-everyitem.csv ./ttwl-everyitem.csv
wc -l ttwl-everyitem.csv
