#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000 