#!/usr/pkg/bin/tcsh
if -e result/tp_fp.csv then
	rm result/tp_fp.csv
endif

foreach i (1 2 3 4 5)
	python ./src/feature_extraction.py training_sample/face_sample_${i}/ training
	python ./src/feature_extraction.py training_sample/non_face_${i}/ training
	python ./src/feature_extraction.py test_sample/face_sample_${i}/ testing
	python ./src/feature_extraction.py test_sample/non_face_${i}/ testing
	python ./src/cal_mean_and_var.py result/training/ face_sample_${i}_dataset.csv
	python ./src/cal_mean_and_var.py result/training/ non_face_${i}_dataset.csv


	python src/naive_bayes.py result/testing/face_sample_${i}_dataset.csv result/testing/non_face_${i}_dataset.csv result/training/mean_face_sample_${i}_dataset.csv result/training/mean_non_face_${i}_dataset.csv
end