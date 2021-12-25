# -*- coding: utf-8 -*-

import paramiko,os,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

remote_os_path = "/oratools/sw/oswbb/analysis"
base_dir = r"E:\daily_data"
remote_alertlog_path = "/oracle/home/alterlog"

remote_ls_cmd = "ls -ltrh %s" % remote_os_path
remote_tar_cmd = "zip -r %s.zip %s"
local_unzip_cmd = "unzip %s -d %s"

#10.114.130.2上压缩osw文件夹
def create_all_osw_zip_file(username,hostname,password,ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(username=username,password=password,hostname=hostname)
    stdin,stdout,stderr = ssh.exec_command(remote_ls_cmd)
    result_list = stdout.read().decode('utf-8').strip('\n').split('\n')
    start_point = len(result_list) - 4
    end_point = len(result_list)
    for index in range(start_point,end_point):
        row_list = result_list[index].split(' ')
        name = row_list[len(row_list) - 1]
        if name.split('_')[3] == ip.split('.')[-1]:
            new_name = remote_os_path + '/' + name
            new_cmd = remote_tar_cmd % (new_name,new_name)
            new_command = 'source /oracle/home/.bash_profile;' + new_cmd
            stdin, stdout, stderr = ssh.exec_command(new_command)
            time.sleep(10)
            print("'%s'压缩osw文件成功！" % name)
            ssh.close()
            return name

#10.114.130.2上下载的指定osw压缩文件到本地
def get_remote_osw_zip_file(host_ip, username, password,out_name,ip):
    t = paramiko.Transport((host_ip, 22))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    src = remote_os_path + '/' + out_name + '.zip'
    osw_base = base_dir + '\\' + 'osw'
    osw_file_path = base_dir + '\\osw\\' + out_name
    des = osw_file_path + '\\' + out_name + '.zip'
    if not os.path.exists(osw_base):
        os.mkdir(osw_base)
    if not os.path.exists(osw_file_path):
        os.mkdir(osw_file_path)
    if out_name.split('_')[3] == ip.split('.')[-1]:
        sftp.get(src,des)
        time.sleep(5)
        print("'%s'压缩文件已经下载！" % out_name)
    else:
        print("'%s'压缩文件不存在！" % out_name)
    t.close()

#解压本地osw压缩文件
def unzip_local_osw_file(ip):
    osw_path = base_dir + '\\osw'
    if os.path.exists(osw_path):
        osw_name_list = os.listdir(osw_path)
        for index in range(len(osw_name_list)):
            if ip.split('.')[-1] in osw_name_list[index].split('_'):
                zip_list = os.listdir(osw_path + '\\' + osw_name_list[index])
                zip_file_name = osw_path + '\\' + osw_name_list[index] + '\\' + zip_list[0]
                os.system(local_unzip_cmd % (zip_file_name,osw_path + '\\' + osw_name_list[index] + '\\'))
                print("'%s'压缩文件解压完成" % osw_name_list[index])
    else:
        print("'%s'存放的osw压缩文件的文件夹不存在，osw压缩文件没有下载成功！" % osw_path)

#osw网页截图功能函数
def osw_snapshot(xml_path_file,img_dir,ip):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="E:\\tools\\lenovo_2.exe")
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.set_window_size(width + 300, height + 400)
    driver.set_page_load_timeout(300)
    driver.set_script_timeout(300)
    driver.get(xml_path_file)
    driver.find_element_by_link_text('CPU').click()
    time.sleep(5)
    driver.save_screenshot(img_dir + '\\cpu_%s.jpg' % ip.split('.')[-1])
    driver.find_element_by_link_text('MEMORY').click()
    time.sleep(5)
    driver.save_screenshot(img_dir + '\\mem_%s.jpg'% ip.split('.')[-1])
    driver.find_element_by_link_text('I/O').click()
    time.sleep(5)
    driver.save_screenshot(img_dir + '\\io_%s.jpg' % ip.split('.')[-1])
    driver.find_element_by_link_text('NETWORK').click()
    driver.find_element_by_xpath('//a[contains(text(),"Network IP Graphs")]').click()
    time.sleep(5)
    driver.save_screenshot(img_dir + '\\net_%s.jpg' % ip.split('.')[-1])
    driver.close()

#生成osw网页截图
def gen_osw_img(ip):
    osw_path = base_dir + '\\osw'
    img_dir = 'E:\\project\\dbmanage_v4\\static\\osw'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    if os.path.exists(osw_path):
        osw_list = os.listdir(osw_path)
        print("=======================================================================")
        for idx in range(len(osw_list)):
            if ip.split('.')[-1] == osw_list[idx].split('_')[3]:
                xml_path_file = "file:///E:/daily_data/osw/" + osw_list[idx] + "/oratools/sw/oswbb/analysis/" + \
                           osw_list[idx] + "/dashboard/index.html"
                osw_snapshot(xml_path_file,img_dir,ip)
                print("'%s'的osw截图已经生成！" % ip)
    else:
        print("osw压缩文件没有下载成功，请检查！")

def gen_sqlserver_img():
    img_path = "E:\\project\\dbmanage_v4\\static\\sqlserver"
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    print("=======================================================================")
    if os.path.exists(img_path):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="E:\\tools\\lenovo_2.exe")
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width + 700, height + 300)
        driver.set_page_load_timeout(300)
        driver.set_script_timeout(300)
        driver.get(r"http://xxx:xxx@xxx/ReportServer_SQL2012/Pages/ReportViewer.aspx?%2fDBA%2fDBA%e6%80%bb%e4%bd%93%e7%9b%91%e6%8e%a7&rs:Command=Render")
        time.sleep(5)
        Select(driver.find_element_by_id('ReportViewerControl_ctl04_ctl03_ddValue')).select_by_visible_text('8820')
        time.sleep(5)
        driver.find_element_by_id('ReportViewerControl_ctl04_ctl00').click()
        time.sleep(5)
        driver.save_screenshot(img_path + '\\sqlserver.jpg')
        driver.close()
        print("sqlserver监控图片已经生成！")
    else:
        os.mkdir(img_path)
        print("查找不到sqlserver存放图片的路径！")