# MCD Docs

我的毕业设计，勿商用

## 如何运行

需要安装MySQL数据库、Redis数据库

需要安装Python>=3.9.0环境

在config.yaml相关数据库连接信息

```shell
# 安装相关库
pip install -r requirements.txt
```

将模型放置到 项目目录/deep-learning-model

运行create_database_table.py导入数据至MySQL

```shell
# cd到项目目录
python3 app.py
```

使用账号admin，密码1234进行登录

## 代码结构

- app.py	#可视化启动入口

- config.yaml	#数据库配置

- create_database_table.py	#将数据导入MySQL

- README.md

- requirements.txt	#相关Python库

- data

  - all_reviews.csv	#所有评论数据

  - GZ.json				#广州地图数据

  - info1.csv			#门店相关数据

  - info2.csv			#门店相关数据

  - location.csv		#地区相关数据

  - mcd.txt				#麦当劳相关停用词

  - stopwords1.txt	#停用词

- deep-learning-model	#情感分析模型

- mcd-clean	#数据清洗代码

- mcd-deep-learning	#深度学习代码

- mcd-machine-learning	#机器学习代码

- mcd-spiders	

  - 1shophref.py	#门店链接爬虫

  - 2info1.py			#门店数据爬虫

  - 2info2.py			#门店数据爬虫

  - 2location.py		#地区数据爬虫

  - 3bad.py				#评论数据爬虫

  - 3good.py			#评论数据爬虫

  - 3middle.py		#评论数据爬虫

  - get_proxy.py	

  - get_useragent.py

  - href.txt			#门店链接数据

- static					#网页css、js等文件

- templates

  - 404.html			#404页面

  - baselogin.html	
  
  - basepage.html	
  
  - chat.html			#预测页面
  
  - cloud.html		 #词云页面
  
  - error-register.html	#注册错误页面
  
  - GZ.json
  
  - hotWord.html			#热词页面
  
  - index.html				#首页
  
  - login.html				#登录页面	
  
  - map.html				#地图页面

  - pwd1.html				#重设密码页面

  - pwd2.html				#重设密码页面

  - register.html			#注册页面

  - sentimentData.html

  - sentimentData0.html		#好评舆情页面

  - sentimentData1.html		#中评舆情页面

  - sentimentData2.html		#差评舆情页面

  - userData.html					#账号管理页面

- utils
  - errorResponse.py			#封装错误处理
  - getHotWord.py				#封装热词数据
  - load_config.py				#封装配置文件
  - myquery.py					#封装SQL语句
- views
  - page	#可视化系统核心代码
		  - page.py
  - user	#可视化系统用户相关核心代码
		  - user.py
- wordcount
  - commentWordTotal.py		#将评论分词
  - cutComments.py		#将评论分词
  - cutComments.txt
  - foodWordTotal.py		#将食物分词
  - snow.py		#将情感写入评论
  - wordTotal.csv
  - wordTotal.py		#热词计数
  - DataForWordCloud

		  - B1.txt

		- B2Total.csv

		- Food.txt

		- FoodTotal.csv

		- G1.txt

		- G2Total.csv

		- M1.txt

		- M2Total.csv











