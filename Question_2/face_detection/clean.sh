#!/usr/pkg/bin/tcsh
rm test_sample training_sample -rf
foreach i (1 2)
	rm result/classifier_${i}/tp_fp.csv
	rm result/classifier_${i}/training/*
	rm result/classifier_${i}/testing/*
		rm result/roc.png
	#rm result/Rplots.pdf
end
