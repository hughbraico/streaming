#!/bin/bash

# usage eg. ./run_tests.sh solution2b.py
# add more lines for more tests

python3 $1 < input/tiny.in > output/tiny.out
python3 $1 < input/kittens.in > output/kittens.out
python3 $1 < input/trending_today.in > output/trending_today.out
python3 $1 < input/videos_worth_spreading.in > output/videos_worth_spreading.out
python3 $1 < input/me_at_the_zoo.in > output/me_at_the_zoo.out
