import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest import TestCase
from selenium.webdriver.common.alert import Alert

from app import create_app, db, TestConfig

localHost = "http://localhost:5000/"

class SeleniumTestCase(TestCase):

    def setUp(self):
        #  Set up method to initialize test environment
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        db.session.commit()
        
        # Start the Flask application in a separate thread
        self.server_thread = threading.Thread(target=self.testApp.run, kwargs={'use_reloader': False, 'use_debugger': False})
        self.server_thread.start()

        # Wait for the server to start
        time.sleep(1)
        print("Server started")

        options = webdriver.ChromeOptions()
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(localHost)
        print("Navigated to localhost")

    def tearDown(self):
        #Tear down method to clean up test environment.
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        # stop the server
        self.server_thread.join(timeout=1)
        
        self.driver.quit()  

    def test_register_page(self):
        # wait for the welcome page
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "loginenter")))
        login_enter_element = self.driver.find_element(By.ID, "loginenter")
        time.sleep(1)  
        login_enter_element.click()
        
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "loginpage_registerenter")))
        register_enter_element = self.driver.find_element(By.ID, "loginpage_registerenter")
        time.sleep(1)  
        register_enter_element.click()
        
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "register-user-name")))
        register_user_name_element = self.driver.find_element(By.ID, "register-user-name")
        register_user_name_element.click()
        time.sleep(1) 
        
        alert = self.driver.switch_to.alert
        alert.accept()  
        register_user_name_element.send_keys("maggie")

        email_element = self.driver.find_element(By.ID, "email-send")        
        time.sleep(1)         
        email_element.send_keys("maggie@example.com")

        register_password_element = self.driver.find_element(By.ID, "register-password")
        register_password_element.click()
        time.sleep(1)  
        alert = self.driver.switch_to.alert
        alert.accept()
        register_password_element.send_keys("qwe123")
        
        confirm_password_element = self.driver.find_element(By.ID, "confirm-password")        
        time.sleep(1)          
        confirm_password_element.send_keys("qwe123")
        
        register_success_element = self.driver.find_element(By.ID, "register-button")
        time.sleep(1) 
        register_success_element.click()
        time.sleep(1)
        alert = self.driver.switch_to.alert
        alert.accept()     
               
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "login-user-name")))
        login_user_name_element = self.driver.find_element(By.ID, "login-user-name")
        login_user_name_element.click()
        time.sleep(1)        
        login_user_name_element.send_keys("maggie")

        login_password_element = self.driver.find_element(By.ID, "login-password")
        time.sleep(1)  
        login_password_element.send_keys("qwe123")
        
        submitElement = self.driver.find_element(By.ID, "login-button")
        time.sleep(1)  
        submitElement.click()
        
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "displayPostBtn")))
        show_question_form_element = self.driver.find_element(By.ID, "displayPostBtn")
        show_question_form_element.click()
        time.sleep(1)
        
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "title")))
        write_question_title_element = self.driver.find_element(By.ID, "title")
        time.sleep(1)
        write_question_title_element.send_keys("What are the places worth visiting in Perth? ")
        
        # Wait for the page to load and locate the iframe containing CKEditor
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "cke_wysiwyg_frame")))
        
        # Switch to the iframe of CKEditor
        iframe = self.driver.find_element(By.CLASS_NAME, "cke_wysiwyg_frame")
        self.driver.switch_to.frame(iframe)
        
        # Find and fill the text area
        write_question_content_element = self.driver.find_element(By.CSS_SELECTOR, "body")
        time.sleep(1)
        write_question_content_element.send_keys("I just came to Perth to study. I want to know what places are worth visiting in Perth. I can go there when I have time.")
        
        # Switch back to the main page
        self.driver.switch_to.default_content()
        print("Switched back to main content")
        time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "submit")))
        submit_post_Element = self.driver.find_element(By.ID, "submit")
        time.sleep(1)  
        submit_post_Element.click()
        print("Clicked submit button")
        
        # Wait for the type dropdown to be visible and select 'User'
        type_dropdown = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "type")))
        type_dropdown.click()
        user_option = self.driver.find_element(By.XPATH, "//option[@value='user']")
        user_option.click()
        time.sleep(1)
        
        # Find the query input and enter 'maggie'
        query_input = self.driver.find_element(By.ID, "query")
        query_input.send_keys("maggie")
        time.sleep(1)
        
        # Find and click the search button
        search_button = self.driver.find_element(By.ID, "search-btn")
        search_button.click()
        time.sleep(1)

        # Wait for the type dropdown to be visible and select 'Post'
        type_dropdown = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "type")))
        type_dropdown.click()
        post_option = self.driver.find_element(By.XPATH, "//option[@value='post']")
        post_option.click()
        time.sleep(1)
        
        # Find the query input and enter 'What are the places worth visiting in Perth?'
        query_input = self.driver.find_element(By.ID, "query")
        query_input.send_keys("What are the places worth visiting in Perth?")
        time.sleep(1)
        
        # Find and click the search button
        search_button = self.driver.find_element(By.ID, "search-btn")
        search_button.click()
        time.sleep(1)
        
        while True:
            time.sleep(1)
