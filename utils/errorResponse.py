# -*- coding: utf-8 -*-
"""
author:Lin
返回错误信息、网页
"""
from flask import render_template

def errorResponse(errorMsg):
    return render_template('error-register.html',errorMsg=errorMsg)
