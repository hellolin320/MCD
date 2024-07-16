# -*- coding: utf-8 -*-
"""
author:Lin
初始化数据库
"""
import pymysql
import pandas as pd
from sqlalchemy import create_engine

def create_database(connection):
    try:
        with connection.cursor() as cursor:
            sq = "DROP DATABASE IF EXISTS jupiter_mcd"
            cursor.execute(sq)
            sql = "CREATE DATABASE IF NOT EXISTS jupiter_mcd CHARACTER SET = utf8mb4"
            cursor.execute(sql)
        connection.commit()
        print("成功创建jupiter_mcd数据库")
    except Exception as e:
        print("jupiter_mcd数据库Error:", e)
    finally:
        connection.close()

def create_write_user(connection1):
    try:
        with connection1.cursor() as cursor:
            sql = """
            CREATE TABLE IF NOT EXISTS user (
                id INT(255) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255),
                password VARCHAR(255),
                create_time VARCHAR(255),
                email VARCHAR(255),
                super INT(255)
            )
            """
            cursor.execute(sql)
            sql1="""
                insert into user(id,username,password,create_time,email,super) values(1,'admin','1234','2024-3-31','admin@admin.com',1)
            """
            cursor.execute(sql1)
        connection1.commit()
        print("成功创建user数据表")
        print("成功写入user数据至user数据表")
    except Exception as e:
        print("user数据表Error:", e)

def create_allreviews(connection1):
    sql="""
        create table all_reviews(
            id INT AUTO_INCREMENT PRIMARY KEY,
            shopName varchar(255),
            userName varchar(255),
            recommendFood varchar(255),
            userCommentTime varchar(255),
            userScore varchar(255),
            userComment varchar(255),
            sentiment varchar(255)
        )
    """
    cursor=connection1.cursor()
    cursor.execute(sql)
    connection1.commit()
    print("成功创建all_reviews表")

def write_to_allreviews():
    data = pd.read_csv('./data/all_reviews.csv', engine='python')
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/jupiter_mcd')
    data.to_sql(name='all_reviews', con=engine, if_exists='replace', index=True)
    engine.dispose()
    print('成功保存all_reviews至all_reviews数据库')

def create_info(connection1):
    sql="""
        create table info1(
            shopName varchar(255),
            reviewCount varchar(255),
            avgPrice varchar(255),
            address varchar(255),
            tel varchar(255),
            time varchar(255)
        )
        """

    sql2="""
        create table info2(
            shopName varchar(255),
            starScore varchar(255),
            tasteScore varchar(255),
            envScore varchar(255),
            serScore varchar(255),
            goodCount varchar(255),
            middleCount varchar(255),
            badCount varchar(255)
        )
    
    """

    cursor=connection1.cursor()
    cursor.execute(sql)
    cursor.execute(sql2)
    connection1.commit()
    print("成功创建info数据表")

def write_to_info():
    data = pd.read_csv('./data/info1.csv', engine='python')
    data2 = pd.read_csv('./data/info2.csv', engine='python')
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/jupiter_mcd')
    data.to_sql(name='info1', con=engine, if_exists='replace', index=False)
    data2.to_sql(name='info2', con=engine, if_exists='replace', index=False)
    engine.dispose()
    print('成功保存info数据至info数据库')

def create_location(connection1):
    sql="""
        create table location(
            shopName varchar(255),
            shopRegion varchar(255),
            shopLocation varchar(255)
        )
    """

    cursor=connection1.cursor()
    cursor.execute(sql)
    # 提交更改
    connection1.commit()
    print("成功创建location表")
    connection1.close()

def write_to_location():
    data = pd.read_csv('./data/location.csv', engine='python')
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/jupiter_mcd')
    data.to_sql(name='location', con=engine, if_exists='replace', index=False)
    engine.dispose()
    print('成功保存location至location数据库')

from utils.load_config import get_mysql_connection,load_config,get_mysql_connection_init
def main():
    mysql_connection = get_mysql_connection_init(load_config())
    create_database(mysql_connection)

    database_connection = get_mysql_connection(load_config())
    create_write_user(database_connection)

    create_allreviews(database_connection)
    write_to_allreviews()

    create_info(database_connection)
    write_to_info()

    create_location(database_connection)
    write_to_location()

if __name__=='__main__':
    main()
    print("ok")
