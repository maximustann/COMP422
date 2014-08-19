#!/usr/pkg/bin/tcsh
if -e result/tp_fp.csv then
	rm result/tp_fp.csv
endif

foreach i (1 2 3 4 5)
	python ./src/classifier_1/feature_extraction.py training_sample/face_sample_0${i}/ training
	python ./src/classifier_1/feature_extraction.py training_sample/non_face_0${i}/ training
	python ./src/classifier_1/feature_extraction.py test_sample/face_sample_0${i}/ testing
	python ./src/classifier_1/feature_extraction.py test_sample/non_face_0${i}/ testing
	python ./src/classifier_1/cal_mean_and_var.py result/classifier_1/training/ face_sample_0${i}_dataset.csv
	python ./src/classifier_1/cal_mean_and_var.py result/classifier_1/training/ non_face_0${i}_dataset.csv
end

foreach i (1 2 3 4 5)
	foreach j (1 2 3 4 5)
	python src/classifier_1/naive_bayes.py result/classifier_1/testing/face_sample_0${j}_dataset.csv result/classifier_1/testing/non_face_0${j}_dataset.csv result/classifier_1/training/mean_face_sample_0${i}_dataset.csv result/classifier_1/training/mean_non_face_0${i}_dataset.csv
	end
end


foreach i (1 2 3 4 5)
	python ./src/classifier_2/feature_extraction.py training_sample/face_sample_0${i}/ training
	python ./src/classifier_2/feature_extraction.py training_sample/non_face_0${i}/ training
	python ./src/classifier_2/feature_extraction.py test_sample/face_sample_0${i}/ testing
	python ./src/classifier_2/feature_extraction.py test_sample/non_face_0${i}/ testing
	python ./src/classifier_2/cal_mean_and_var.py result/classifier_2/training/ face_sample_0${i}_dataset.csv
	python ./src/classifier_2/cal_mean_and_var.py result/classifier_2/training/ non_face_0${i}_dataset.csv
end

foreach i (1 2 3 4 5)
	foreach j (1 2 3 4 5)
	python src/classifier_2/naive_bayes.py result/classifier_2/testing/face_sample_0${j}_dataset.csv result/classifier_2/testing/non_face_0${j}_dataset.csv result/classifier_2/training/mean_face_sample_0${i}_dataset.csv result/classifier_2/training/mean_non_face_0${i}_dataset.csv
	end
end



Rscript src/roc.r
mv Rplots.pdf result/
