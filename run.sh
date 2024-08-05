#!/bin/bash
conda env create -f environment.yml
eval "$(conda shell.bash hook)"
conda activate bindu_take_home
pytest -s -v test_hn_app.py
