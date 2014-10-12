#!/bin/bash 
#useage: ./transfer.sh [.arff] [.data]
truncate $1 --size 0

echo "@relation f" >> $1
echo "@attribute f1 numeric" >> $1
echo "@attribute classes {1.0 2.0 3.0}" >> $1
echo "@data" >> $1

sed -i '1d' $2
cat $2 >> $1
dos2unix $1
rm $2
