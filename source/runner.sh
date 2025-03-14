#!/bin/bash

# Function to add shebang line to Python scripts

./order_spread.py
./dijkstra.py
./a_Star.py
./bellman.py
./abc.py
./comapre.py

# Optional: Check for errors
if [ $? -ne 0 ]; then
    echo "An error occurred while running the scripts."
fi
