#!/bin/bash

# download the model
python download_model.py

# Start the app
gunicorn main:app
