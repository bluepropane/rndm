pushd . >/dev/null
cd $1
mkdir src
cd src
python3 -m venv venv

. venv/bin/activate
cd ..
pip install -r requirements.txt
python startproject.py $1
popd