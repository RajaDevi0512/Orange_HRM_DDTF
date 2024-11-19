"""
This file contains test logic for Orange HRM automation
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# importing other files
from TestLocator.locator import OrangeHRM_Locator
from TestData.data import Orange_HRM_Data
from Utilities.excel_functions import ExcelFunction

# import the webdriver wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#import exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementClickInterceptedException
from  selenium.common.exceptions import TimeoutException

#import time functionality
from time import sleep
from datetime import datetime


class TestHRM:
    def test_loginExcel(self):
        self.excel_file = Orange_HRM_Data().excel_file
        self.sheet_number = Orange_HRM_Data().sheet_number
        self.excel = ExcelFunction(self.excel_file, self.sheet_number)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
       
        self.driver.get(Orange_HRM_Data().url)
        self.driver.maximize_window()


        self.ignored_exceptions = [NoSuchElementException, ElementNotVisibleException, ElementClickInterceptedException, TimeoutException]
        self.wait = WebDriverWait(self.driver, 30, poll_frequency=5, ignored_exceptions=self.ignored_exceptions)
        
        # Get the current date and time
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()

        self.row = self.excel.row_count()

        for row in range(2,self.row+1):
            username = self.excel.read_data(row, 5)
            password = self.excel.read_data(row, 6)
            
            self.wait.until(EC.presence_of_element_located((By.XPATH, OrangeHRM_Locator.username_locator))).send_keys(username)
            print("username")
            self.wait.until(EC.presence_of_element_located((By.XPATH, OrangeHRM_Locator.password_locator))).send_keys(password)
            print("password")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, OrangeHRM_Locator.login_locator))).click()
            print("Logged in")
        
            if Orange_HRM_Data().dashboard_url in self.driver.current_url:
                
                self.excel.write_data(row,4,current_date)
                self.excel.write_data(row,7,'Test Passed')
                self.excel.write_data(row,8, current_time)
                # self.driver.back()
                # sleep(5)
                self.wait.until(EC.element_to_be_clickable((By.XPATH, OrangeHRM_Locator.profile_icon_locator))).click()
                print("profile_icon")
                self.wait.until(EC.element_to_be_clickable((By.XPATH, OrangeHRM_Locator.logout_locator))).click()
                print("logout")
                self.driver.refresh()
                
                    
            elif Orange_HRM_Data().url in self.driver.current_url:
                print("FAILED")
                self.excel.write_data(row,4,current_date)
                self.excel.write_data(row,7,'Test Failed')
                self.excel.write_data(row,8, current_time)
                self.driver.refresh()
                # sleep(5)

        self.driver.quit()