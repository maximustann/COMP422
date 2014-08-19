#!/bin/sh
echo Running...

echo Extracting large galaxy using Otus method
python ./src/median.py ./pics/hubble.png ./pics/median_hubble.png
python ./src/otus.py ./pics/median_hubble.png ./pics/result/large_galaxy_hubble.png

rm ./pics/median_hubble.png
echo Finished
