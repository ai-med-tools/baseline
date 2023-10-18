#!/bin/bash
set -e

python baseline.py core

while $(kill -0 $(ps xawf -eo pid,command | grep "python core.py" | grep -v "grep" | cut -f6 -d " "))
do
  sleep 1
done