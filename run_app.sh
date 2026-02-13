#!/bin/bash
set -x
cd /home/michel/resume_analyzer || exit 1
source venv/bin/activate
which python
python ui.py
