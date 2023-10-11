#!/bin/bash
set -e

python baseline.py core

while $(kill -0 $(ps -C "python core" -o pid=))
do
  sleep 1
done