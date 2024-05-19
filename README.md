# CITS5505 Group Project -- Tourism Forum

## Ⅰ. Project Overview
The Tourism Forum is an online community platform based on the Flask application, which aims to provide travel enthusiasts with a platform to communicate, share travel experiences and plan trips. Users can register an account, create a profile, post travel tips, communicate with other travelers, and participate in discussion topics posted by other users.

## Ⅱ. Group Team Member
| Name              | Student ID | Github Username    |
|-------------------|------------|--------------------|
| Xiao Zhang        | 23363869   | Maggiexz           |
| Yunfang Lyu       | 23685059   | Yunfang-Lyu        |
| Zixing(Alex) Wang | 24123115   | qingdaoalex        |
| Philip Wu         | 23902134   | TroubledPhilip     |


## Ⅲ. Launch the application
### 1. Create virtual environment：
    (linux) $ python3 -m venv venv  
            $ source venv/bin/activate
    
    (bash)  $ python -m venv venv  
            $ source venv/Scripts/activate 
    
    (cmd)   $ py -3 -m venv .venv 
            $ .venv\Scripts\activate

### 2. Install all needed packages：
      cd tourism_forum
      pip install -r requirements.txt

### 3. Run the application based on a small database:
     cd tourism_forum
     flask run

## Ⅳ. Run the tests for the application
### 1. Run unit test:
    cd tourism_forum
    python -m unittest -v tests.py
### 2. Run selenium test:
    cd tourism_forum
    python -m unittest test_selenium.py
## Ⅴ. Additonal Information
### About selenium test:
If you cannot run the selenium test because of the browser driver version number, you can directly view the video named **$\color{blue}{\text{"selenium-test.mp4"}}$** in the folder "deliverables".
