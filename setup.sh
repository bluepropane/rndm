rm -rf .git
python3 -m venv venv

. venv/bin/activate
pip install -r requirements.txt
python startproject.py