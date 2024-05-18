import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest import TestCase

from app import create_app, db, TestConfig

localHost = "http://localhost:5000/"

class SeleniumTestCase(TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        # 使用线程启动 Flask 应用
        self.server_thread = threading.Thread(target=self.testApp.run, kwargs={'use_reloader': False, 'use_debugger': False})
        self.server_thread.start()

        # 确认服务器已经启动
        time.sleep(1)
        print("Server started")

        options = webdriver.ChromeOptions()
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)
        print("Navigated to localhost")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        # 停止服务器线程
        self.server_thread.join(timeout=1)
        
        # self.driver.quit()  # 注释掉此行以保持浏览器窗口打开

    def test_login_page(self):
        # 等待并点击登录页面的链接
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "loginenter")))
        login_enter_element = self.driver.find_element(By.ID, "loginenter")
        time.sleep(2)  # 等待2秒
        login_enter_element.click()

        # 等待登录页面加载并查找用户名和密码输入框
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "login-user-name")))
        
        login_user_name_element = self.driver.find_element(By.ID, "login-user-name")
        time.sleep(2)  # 等待2秒
        login_user_name_element.send_keys("maggie")

        login_password_element = self.driver.find_element(By.ID, "login-password")
        time.sleep(2)  # 等待2秒
        login_password_element.send_keys("qwe123")
        
        # submitElement = self.driver.find_element(By.ID, "login-button")
        # time.sleep(2)  # 等待2秒
        # submitElement.click()
        
        # 添加无限循环以防止脚本退出
        while True:
            time.sleep(1)
