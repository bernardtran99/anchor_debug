#!/usr/bin/env bash

git pull && cmake -DCMAKE_BUILD_TYPE=Release .. && python ../misc/change-link.py && make -j2