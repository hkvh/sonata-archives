#!/bin/bash

# A bash script to update both the requirements.txt and the environment.yml file

# Create the pip-style requirements
pip freeze > requirements.txt

# Create the conda environment file including all the pip requirements and the conda requirements
# For some reason conda appends a prefix to the bottom of its export that will have a path to your local directory of anaconda.
# This won't affect using it to create the environment, but it is a bit annoying, so I grep it away
conda env export | grep -v "^prefix: " > environment.yml

echo "Success! requirements.txt and environment.yml updated based on current conda env"