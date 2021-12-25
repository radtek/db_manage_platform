# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import os
import time
import configparser

class SqlserverImg(object):
    @staticmethod
    def gen_sqlserver_img():
        config = configparser.ConfigParser()
        config.read('E:\\project\\dbmanage_v4\\common\\libs\\dbcheck\\Setup.ini', encoding='utf-8')
        sec2 = config['base']
        img_path = sec2['base_dir'] + "sqlserver_img"
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        if os.path.exists(img_path):
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=sec2['driver_path'])
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(width + 700, height + 300)
            driver.set_page_load_timeout(300)
            driver.set_script_timeout(300)
            driver.get(r"http://xxx:xxx@xxx/ReportServer_SQL2012/Pages/ReportViewer.aspx?%2fDBA%2fDBA%e6%80%bb%e4%bd%93%e7%9b%91%e6%8e%a7&rs:Command=Render")
            time.sleep(5)
            Select(driver.find_element_by_id('ReportViewerControl_ctl04_ctl03_ddValue')).select_by_visible_text('8820')
            driver.find_element_by_id('ReportViewerControl_ctl04_ctl00').click()
            time.sleep(5)
            driver.save_screenshot(img_path + '\\sqlserver.jpg')
            driver.close()
        else:
            os.mkdir(img_path)