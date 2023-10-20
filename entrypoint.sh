#!/bin/bash
set -e

python baseline.py core

while $(kill -0 $(ps xawf -eo pid,command | grep "python core.py" | grep -v "grep" | awk '{print $1}'))
do
  sleep 1
done