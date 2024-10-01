#!/bin/sh

python3 challenge1.py &
python3 challenge2.py &
# add more here

# Unomment below if challenge table isnt created yet, then 'sudo docker-compose up -d --build'
# python3 debugger.py & 

tail -f /dev/null