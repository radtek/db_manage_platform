# 数据库运维管理平台

#### 介绍
基于Django的数据库运维管理平台，暂时满足公司内部数据库日常运维需求，后续继续补充和完善。

#### 软件架构
1. Python 3.6.6

2. Django 2.2.10


#### 安装教程

1.  安装Python 3.6.6（忽略此步骤）

2.  安装相关包  
pip install Django==2.2.10  
pip install cx-Oracle==7.2.2  
pip install matplotlib==3.3.4  
pip install numpy==1.19.5  
pip install pandas==1.1.5  
pip install paramiko==2.6.0  
pip install PyMySQL==0.9.3  
pip install selenium==2.53.6  
pip install WxPython==4.1.1  
pip install xlrd==1.2.0  
pip install xlutils==2.0.0  
pip install xlwings==0.24.7  
pip install xlwt==1.3.0  
pip install Pillow==8.4.0  

3.  安装MySQL数据库（忽略此步骤）  

4. MySQL创建数据库  
    create database userdb default character set utf8;  

5. Django中配置setting.py文件,修改连接数据库配置  
    DATABASES = {  
          'default': {  
              'ENGINE': 'django.db.backends.mysql',  
              'NAME': 'userdb',  
              'USER':'用户',  
              'PASSWORD':'密码',  
              'HOST':'数据库IP',  
              'PORT':'数据库端口'  
          }  
      }  

5. Django迁移表到MySQL的userdb数据库中  
    python manage.py makemigrations  
    python manage.py migrate  

6. 启动DJango服务  
    python manage.py runserver 0.0.0.0:8000  
    

#### 使用说明  

1. 登录界面 
![Image text](https://gitee.com/code-horse-mi/dbmanage_v4/raw/master/%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE/%E7%99%BB%E5%BD%95%E5%8A%9F%E8%83%BD.png)

2. 注册界面
![Image text](https://gitee.com/code-horse-mi/dbmanage_v4/raw/master/%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE/%E6%B3%A8%E5%86%8C%E5%8A%9F%E8%83%BD.png)

3. 数据库运维列表
![Image text](https://gitee.com/code-horse-mi/dbmanage_v4/raw/master/%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE/%E6%95%B0%E6%8D%AE%E5%BA%93%E8%BF%90%E7%BB%B4%E5%88%97%E8%A1%A8.png)

4. 数据库监控指标数据表
![Image text](https://gitee.com/code-horse-mi/dbmanage_v4/raw/master/%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE/%E6%95%B0%E6%8D%AE%E5%BA%93%E7%9B%91%E6%8E%A7%E6%8C%87%E6%A0%87%E6%95%B0%E6%8D%AE%E8%A1%A8.png)

5. sqlserver巡检功能
![Image text](https://gitee.com/code-horse-mi/dbmanage_v4/raw/master/%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE/sqlserver%E5%B7%A1%E6%A3%80.png)

6. 数据库监控数据报表图
![Image text](https://gitee.com/code-horse-mi/dbmanage_v4/raw/master/%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE/%E7%9B%91%E6%8E%A7%E6%95%B0%E6%8D%AE%E6%8A%A5%E8%A1%A8%E5%8A%9F%E8%83%BD.png)

7. Oracle安装工具
![Image text](https://gitee.com/code-horse-mi/dbmanage_v4/raw/master/%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE/%E6%95%B0%E6%8D%AE%E5%BA%93%E5%AE%89%E8%A3%85%E5%B7%A5%E5%85%B7.png)

8. Oracle巡检工具
![Image text](https://gitee.com/code-horse-mi/dbmanage_v4/raw/master/%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE/oracle%E5%B7%A5%E5%85%B7.png)

9. 每日日报工具
![Image text](https://gitee.com/code-horse-mi/dbmanage_v4/raw/master/%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE/%E6%AF%8F%E6%97%A5%E6%97%A5%E6%8A%A5%E5%B7%A5%E5%85%B7.png)


#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
