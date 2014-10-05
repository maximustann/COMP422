#!/bin/bash 

#for i in `ls digits*`
#do
	#sed -i 's/ /,/g' $i
#done

#for i in `ls digits*`
#do
	#split -l 500 $i $i'_train'
#done

#for i in `ls *_trainaa`
#do
	#mv $i $i'_train'
#done

#for i in `ls *_trainab`
#do mv $i $i'_test'
#done

for i in  '00' '05' '10' '15' '20' '30' '40' '50' '60' 
do
	touch 'digits_'$i'_train.arff'
	touch 'digits_'$i'_test.arff'
	cat head.file > 'digits_'$i'_train.arff'
	cat 'digits'$i'_trainaa_train' >> 'digits_'$i'_train.arff'
	cat head.file > 'digits_'$i'_test.arff'
	cat 'digits'$i'_trainab_test' >> 'digits_'$i'_test.arff'
done


