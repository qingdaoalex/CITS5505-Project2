CITS5505 group project plan (4.19-4.26)
- 2024.4.19 meeting result(if this module can add back end):
  - 1.home page -xiao
  - 2.sign in page -yunfang
  - 3.profile page -zhuowen
  - 4.book review page -alex
- the useful entensions in vscode:Git Graph,Git History, GitLens, Git supercharged

How to run the web page:
1. Create virtual environment：
- (linux) $ python3 -m venv venv then $ source venv/bin/activate
- (bash) $ python -m venv venv then $ source venv/Scripts/activate 
- (cmd) $ py -3 -m venv .venv then $ .venv\Scripts\activate

2. Install all needed packages
- pip install -r requirements.txt

3. Initialize database(Before initialize database make sure there is no **"migrations"** folder):
- $flask db init
- $flask db migrate
- $flask db upgrade

4. Run flask:
- $flask run
