python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

flask db init
flask db migrate

falsk run --debug
flask run --port 5001

