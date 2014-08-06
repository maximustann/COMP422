#!/bin/sh
echo It might take a while
echo Sobel Edge detecting
python sobel.py test.tif sobel_test.png

echo Mean filtering
python mean_3.py ckt.png mean_3_ckt.png
python mean_5.py ckt.png mean_5_ckt.png

echo Median filtering
python median.py ckt.png median_ckt.png

echo Picture shapen using Laplace filtering
python laplace.py blurry-moon.tif shape_moon.png

echo Extracting large galaxy using Otus method
python median.py hubble.png median_hubble.png
python otus.py median_hubble.png large_galaxy_hubble.png

echo Finished
