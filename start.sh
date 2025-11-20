#!/bin/bash
python3 init_db.py
gunicorn app:app
