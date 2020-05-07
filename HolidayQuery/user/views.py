from django.shortcuts import render
from django.http import JsonResponse
from user.models import User, Holiday
import jwt
from datetime import datetime, timedelta
from django.conf import settings


def signup(request):
    # request.encoding = 'utf-8'
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            if User.objects.filter(username=request.POST['username']).first():
                message = ({'StatusCode': '0', 'Message': '用户名 ' +
                            request.POST['username'] + ' 已存在，注册失败'})
            else:
                user_information = User(
                    username=request.POST['username'], password=request.POST['password'])
                user_information.save()
                message = ({'StatusCode': '1', 'Message': '用户 ' +
                            request.POST['username'] + ' 注册成功'})
        else:
            message = ({'StatusCode': '-1', 'Message': '表单填写错误，注册失败'})
    else:
        message = ({'StatusCode': '-1', 'Message': '不支持的方法(GET)'})
    print(message)
    return JsonResponse(message)


def login(request):
    # request.encoding = 'utf-8'
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            if User.objects.filter(username=request.POST['username'], password=request.POST['password']).first():
                token = User.objects.filter(
                    username=request.POST['username'], password=request.POST['password']).first().token

                message = ({'StatusCode': '1', 'Message': '用户 ' +
                            request.POST['username'] + ' 登录成功', 'Token': token})
            else:
                message = ({'StatusCode': '0', 'Message': '用户名或密码错误'})
        else:
            message = ({'StatusCode': '-1', 'Message': '表单填写错误，登录失败'})
    else:
        message = ({'StatusCode': '-1', 'Message': '不支持的方法(GET)'})
    print(message)
    return JsonResponse(message)


def query(request):
    # request.encoding = 'utf-8'
    if request.method == 'POST':
        if 'date' in request.POST and 'token' in request.POST:
            try:
                log_information = jwt.decode(
                    request.POST['token'], settings.SECRET_KEY, algorithm='HS256')
                username = log_information.get('data').get('username')
            except jwt.ExpiredSignatureError:
                return JsonResponse({"StatusCode": 401, "Message": "Token expired"})
            except jwt.InvalidTokenError:
                return JsonResponse({"StatusCode": 401, "Message": "Invalid token"})
            except Exception as e:
                return JsonResponse({"StatusCode": 401, "Message": "Can not get user object"})
            if User.objects.filter(username=username).first():
                queryDate = '2000' + request.POST['date'][-6:]
                if Holiday.objects.filter(holiday_date=queryDate).first():
                    message = ({'StatusCode': '1', 'Message': '查询成功', 'HolidayName': Holiday.objects.filter(
                        holiday_date=queryDate).first().holiday_name})
                else:
                    message = ({'StatusCode': '0', 'Message': '查询失败'})
            else:
                message = (
                    {'StatusCode': '-1', 'Message': 'Token错误，不存在的用户名' + username})
        else:
            message = ({'StatusCode': '-1', 'Message': '表单填写错误，查询失败'})
    else:
        message = ({'StatusCode': '-1', 'Message': '不支持的方法(GET)'})
    print(message)
    return JsonResponse(message)
