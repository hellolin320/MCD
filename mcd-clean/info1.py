# -*- coding: utf-8 -*-
"""
author:Lin
"""
import glob
import sys
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyhdfs import HdfsClient
from io import BytesIO

def hdfs_conn(hdfs_host,hdfs_user):
    '''
    创建HDFS客户端对象
    :param hdfs_host: master:50070
    :param hdfs_user: 用户名
    :return: 连接 HDFS 的相关数据
    '''
    try:
        hdfs_client = HdfsClient(hosts=hdfs_host, user_name=hdfs_user)
    except Exception as e:
        print(f"连接HDFS失败: {e}")

    return hdfs_client

def pandas_read_csv(hdfs_host, hdfs_user, hdfs_csv_file):
    '''
    Pandas 读取 HDFS 的 csv 文件
    :param hdfs_csv_file: 文件路径
    :return: Pandas DataFrame
    '''
    client = hdfs_conn(hdfs_host, hdfs_user)

    # 从HDFS中读取CSV文件
    with client.open(hdfs_csv_file) as csvfile:
        # 读取CSV文件内容
        csv_content_bytes = csvfile.read()

    # Pandas 读取 CSV 文件
    pandas_df = pd.read_csv(BytesIO(csv_content_bytes))

    # 将 Pandas DataFrame 中的 NaN 替换为 PySpark 中的表示缺失值的形式（例如空字符串 " "）
    pandas_df = pandas_df.replace({pd.NA: ''})

    return pandas_df

def spark_read_csv():
    '''
    使用 Spark 读取 Pandas 的 DataFrame
    :return:Spark DataFrame 和 schema
    '''
    pandas_df = pandas_read_csv(hdfs_host, hdfs_user, hdfs_csv_file)

    # 定义 PySpark DataFrame 的模式
    schema = StructType([
        StructField("shopName", StringType(), True),
        StructField("reviewCount", StringType(), True),
        StructField("avgPrice", StringType(), True),
        StructField("address", StringType(), True),
        StructField("tel", StringType(), True),
        StructField("time", StringType(), True),
    ])
    # 将 Pandas DataFrame 转为 PySpark DataFrame，并指定模式
    spark_df = spark.createDataFrame(pandas_df, schema=schema)

    return spark_df, schema

def save_to_hdfs(spark_df, hdfs_output_path):
    '''
    将 Spark DataFrame 保存为 CSV 文件，coalesce(1)将数据写入单个文件
    :param spark_df: Spark DataFrame
    :param hdfs_output_path: 输出文件的 HDFS 路径
    :return:
    '''
    spark_df.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .option("encoding", "UTF-8") \
        .csv(hdfs_output_path)

if __name__ == '__main__':
    '''
    数据读取
    '''
    # 获取命令行参数
    if len(sys.argv) != 3:
        print("需要输入清洗的文件和路径")
        sys.exit(1)
    file = sys.argv[1]
    output_name = sys.argv[2]


    # 创建 Spark 会话
    jars_path = "/usr/local/spark/jars/*.jar"
    jars_list = glob.glob(jars_path)
    spark = SparkSession.builder \
        .appName("DataFrame") \
        .config("spark.jars", ",".join(jars_list)) \
        .config("spark.driver.extraClassPath", "/usr/local/hadoop/lib/native/libhdfs.so") \
        .getOrCreate()

    #file = 'info1.csv'

    # 依次运行函数
    # 连接 HDFS, 读取 csv 文件
    hdfs_host = '192.168.137.160:50070'
    hdfs_user = 'root'
    hdfs_csv_file = f'hdfs:///final/'+f'{file}'

    # Pandas 函数
    pandas_read_csv(hdfs_host, hdfs_user, hdfs_csv_file)
    # Spark 函数
    spark_df, schema = spark_read_csv()

    '''
    数据清洗
    '''
    # 清洗前 PySpark DataFrame 的行数
    row_count = spark_df.count()
    print("原始行数：", row_count)

    # 将店名为空的行删除
    cleaned_spark_df_1 = spark_df.filter(col("shopName") != '')
    # 清洗后 PySpark DataFrame 的行数
    cleaned_row_count_1 = cleaned_spark_df_1.count()
    print("删除空白值后的行数：", cleaned_row_count_1)

    # 将店名重复的行删除
    cleaned_spark_df_2 = cleaned_spark_df_1.dropDuplicates(['shopName'])
    cleaned_row_count_2 = cleaned_spark_df_2.count()
    print("删除重复值后的行数：", cleaned_row_count_2)

    # 将 McDonald's 字眼删除
    cleaned_spark_df_3 = spark_df.withColumn("time", regexp_replace(col("time"), "McDonald's", ''))

    '''
    数据保存
    '''
    # 保存清洗后的数据到 HDFS
    hdfs_output_path = f'hdfs:///final/cleaned/'+f'{output_name}'
    save_to_hdfs(cleaned_spark_df_3, hdfs_output_path)
