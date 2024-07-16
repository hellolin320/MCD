# -*- coding: utf-8 -*-
"""
author:Lin
提取转换训练数据
"""
import re

import pandas as pd

# 读取CSV文件
df = pd.read_csv('../data/all_reviews.csv')

# 打乱顺序
df_shuffled = df.sample(frac=1).reset_index(drop=True)

# 选择需要的列[userComment]和[sentiment]
df_selected = df_shuffled[['userComment', 'sentiment']]
# 去除换行符和制表符
df_selected.loc[:, 'userComment'] = df_selected['userComment'].str.replace('\n', '')
df_selected.loc[:, 'userComment'] = df_selected['userComment'].str.replace('\t', '')
# 保留中文、标点符号、英文、数字
df_selected.loc[:, 'userComment'] = df_selected['userComment'].apply(lambda x: re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\.,!?，。！？]', '', str(x)))
# 保存为新的CSV文件
df_selected.to_csv('../data/paddle/u_s.csv', index=False)


import pandas as pd

# 读取u_s.csv文件
df = pd.read_csv('../data/paddle/u_s.csv')

# 更改列名
df.rename(columns={'userComment': 'text_a', 'sentiment': 'label'}, inplace=True)

# 划分数据集
# 计算划分比例
dev_size = int(len(df) * 0.1)
test_size = int(len(df) * 0.1)
train_size = len(df) - dev_size - test_size

# 划分数据集
dev_df = df[:dev_size]
test_df = df[dev_size:dev_size + test_size]
train_df = df[dev_size + test_size:]

# 保存为CSV文件
dev_df = dev_df.reset_index(drop=True)  # 重新设置索引，丢弃原有索引
dev_df.insert(0, 'qid', range(0, len(dev_df)))
dev_df.to_csv('../data/paddle/dev.csv', index=False, sep='\t')

test_df = test_df.reset_index(drop=True)  # 重新设置索引，丢弃原有索引
test_df.insert(0, 'qid', range(0, len(test_df)))
test_df = test_df[['qid', 'text_a']]
test_df.to_csv('../data/paddle/test.csv', index=False, sep='\t')


train_df.to_csv('../data/paddle/train.csv', index=False, sep='\t')


