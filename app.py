# -*- coding: utf-8 -*-
"""
author:Lin
"""
import re

from flask import Flask, jsonify, render_template, session, request, redirect
from views.page import page
from views.user import user

import paddle
from paddlenlp.transformers import AutoTokenizer, AutoModelForSequenceClassification
import paddle.nn.functional as F


# 创建对象
app = Flask(__name__)
app.secret_key = 'Lin Jiaze'
app.register_blueprint(page.pb)
app.register_blueprint(user.ub)


@app.route('/')
def session_clear():
    return session.clear()

@app.before_request
def before_request():
    pat=re.compile(r'^/static')
    if re.search(pat,request.path):return
    elif request.path=='/user/login' or request.path=='/user/register' or request.path=='/user/pwd':return
    elif session.get('username'):return
    return redirect('/user/login')

@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html')

def predict_sentiment(text):
    global enrie_model,tokenizer,label_map

    # 使用分词器处理输入文本
    inputs = tokenizer(text, return_tensors='pd', truncation=True, max_length=128, pad_to_max_length=True)
    input_ids = inputs['input_ids']
    token_type_ids = inputs['token_type_ids']

    # 模型预测
    enrie_model.eval()
    with paddle.no_grad():
        logits = enrie_model(input_ids, token_type_ids)
        probs = F.softmax(logits, axis=1)
        idx = paddle.argmax(probs, axis=1).numpy()
        idx = idx.tolist()

    # 返回预测的情感标签
    return [label_map[i] for i in idx]

@app.route('/chatchat', methods=['POST'])
def chatchat():
    # 获取表单提交的消息
    data = request.json
    text = data['text']
    print("MESSAGE:", text)

    # 调用模型进行预测
    sentiment_response=predict_sentiment(text)
    print(sentiment_response)
    return jsonify(sentiment_response)


if __name__ == '__main__':


    enrie_model = AutoModelForSequenceClassification.from_pretrained("deep-learning-model")
    tokenizer = AutoTokenizer.from_pretrained("deep-learning-model")
    label_map = {0: '积极', 1: '中性', 2: '消极'}


    app.run()