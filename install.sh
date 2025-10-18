#!/bin/bash
set -e  # Exit on errors

# Use system Python/pip
python -m pip install --upgrade pip
python -m pip install gunicorn
python -m pip install -r requirements.txt