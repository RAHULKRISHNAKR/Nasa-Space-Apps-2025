#!/usr/bin/env bash
set -e
python -m pip install --upgrade pip
pip install -r requirements.txt
echo 'Created virtualenv and installed dependencies (if not using virtualenv, please set one up).'
pytest -q || true
echo 'To run UI: streamlit run src/streamlit_app.py'
