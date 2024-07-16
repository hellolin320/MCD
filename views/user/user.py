# -*- coding: utf-8 -*-
"""
author:Lin
用户系统
"""
import time

from flask import Flask,session,render_template,redirect,Blueprint,request
from utils.myquery import myquery
from utils.errorResponse import errorResponse

ub=Blueprint('user',__name__,url_prefix='/user',template_folder='templates')

@ub.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        username=request.form['username']
        password=request.form['password']

        

        # 检查数据库是否存在该用户名
        users = myquery('SELECT * FROM user WHERE username = %s', [username], 'select')
        if not users:
            return errorResponse('没有存在该用户')


        # 检查数据库用户账号和密码是否匹配
        login_success = [user for user in users if user[2] == password]
        if not login_success:
            return errorResponse('密码错误')

        session['username'] = username
        print(username,":",password,"已经登录")
        return redirect('/page/home')


@ub.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')

    else:
        # 检查用户名、密码、邮箱是否为空
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not username or not password or not email:
            return errorResponse('用户名、密码或邮箱不能为空')

        # 获取前端返回的用户名
        def filter_username(user):
            return request.form['username'] in user
        
        # 获取前端返回的邮箱
        def filter_email(user):
            return request.form['email'] in user

        users = myquery('select * from user',[],'select')

        # 校验用户名
        username_filter_list = list(filter(filter_username, users))
        if len(username_filter_list):
            return errorResponse('该用户名已注册')

        # 校验邮箱
        email_filter_list = list(filter(filter_email, users))
        if len(email_filter_list):
            return errorResponse('该邮箱已被注册')
        
        else:
            time_tuple=time.localtime(time.time())
            myquery('''
                insert into user(username,password,create_time,email,super) values(%s,%s,%s,%s,0)
            ''',[request.form['username'],request.form['password'],str(time_tuple[0])+'-'+str(time_tuple[1])+'-'+str(time_tuple[2]),request.form['email']],
            "insert")
        print(username,":",email,":",password,"已经注册")
        return redirect('/user/login')

@ub.route('/pwd', methods=['GET','POST'])
def reset_password():
    if request.method=='GET':
        return render_template('pwd1.html')
    else:
        # 从请求中获取用户名、邮箱和新密码
        username = request.form.get('username')
        email = request.form.get('email')
        new_password = request.form.get('password')

        # 检查是否提供了所有必需的字段
        if not (username and email and new_password):
            return errorResponse('用户名、邮箱或新密码不能为空')

        # 查询数据库，查找具有匹配用户名和邮箱的用户
        user = myquery('SELECT * FROM user WHERE username = %s AND email = %s', [username, email], 'select')

        # 如果未找到用户，返回错误
        if not user:
            return errorResponse('未找到用户，检查用户名或邮箱')
        else:
            # 如果找到了，使用新密码更新用户的密码
            myquery('UPDATE user SET password = %s WHERE username = %s AND email = %s', [new_password, username, email], 'update')

        session['username']=request.form['username']
        print(username,email,new_password,"已经重设密码")
        # 密码成功更新，返回成功响应
        return render_template('pwd2.html')


@ub.route('/userData', methods=['GET'])
def userData():
    # 获取当前登录用户信息
    username = session.get('username')
    if not username:
        return redirect('/user/login')
    
    # 查询数据库，获取用户信息
    user = myquery('SELECT * FROM user WHERE username = %s', [username], 'select')

    # 检查用户是否为管理员
    if user and user[0][-1] == 1:  # 如果用户存在且为管理员
        # 查询所有用户数据
        users = myquery('SELECT * FROM user', [], 'select')
        usersList = [i for i in users]
        return render_template('userData.html', usersList=usersList, username=username)
    else:
        return errorResponse('非管理员无法访问')

@ub.route('/remove', methods=['POST'])
def remove_account():
    account_id = request.json.get('id')
    # 在数据库中执行删除操作
    myquery('DELETE FROM user WHERE id = %s', [account_id], 'delete')
    print("删除",account_id)
    return 'success'

@ub.route('/toggle_admin', methods=['POST'])
def toggle_admin_status():
    user_id = request.json.get('id')
    new_super = int(request.json.get('super'))

    if user_id=='1':
        return errorResponse('无最高权限')
    else:
        # 在数据库中执行更新操作
        myquery('UPDATE user SET super = %s WHERE id = %s', [new_super, user_id], 'update')
        print("管理员权限",user_id)
        return 'success'

@ub.route('/logout')
def logout():
    username = session.get('username')
    session.clear()
    print(username,'退出登录')
    return redirect('/user/login')

