(linux) $ python3 -m venv venv then $ source venv/bin/activate
(bash) $ python -m venv venv then $ source venv/Scripts/activate 
(cmd) $ py -3 -m venv .venv then $ .venv\Scripts\activate

pip install -r requirements.txt

Initialize database:
$flask db init
$flask db migrate
$flask db upgrade

Run tests.py:
$python -m unittest tests.py
$python  -m  unittest -v  tests.py

Run test_selenium.py:
$python -m unittest test_selenium.py