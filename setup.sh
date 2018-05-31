rm -rf .git
mkdir src
cd src
python3 -m venv venv

. venv/bin/activate
cd ..
pip install -r requirements.txt
python startproject.py
