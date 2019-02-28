#!/bin/bash

# usage eg. ./run_tests.sh solution2b.py
# add more lines for more tests

python3 $1 < inputs/tiny.in > output/tiny.out
python3 $1 < inputs/kittens.in > output/kittens.out
python3 $1 < inputs/trending_today.in > output/trending_today.out
python3 $1 < inputs/videos_worth_spreading.in > output/videos_worth_spreading.out
python3 $1 < inputs/me_at_the_zoo.in > output/me_at_the_zoo.out
