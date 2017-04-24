#!/bin/bash -l

rm -rf *.res
rm -rf log.*.t

echo "$ ppp.py" > message.txt
ppp.py >> message.txt

for t in $(ls *.t); do
    echo "---------- $t --------------------------"
    ppp.py $t > log.${t}
done
