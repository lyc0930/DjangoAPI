from django.shortcuts import render
from django.http import HttpResponse
from user.models import User, Holiday


def signup(request):
    # request.encoding = 'utf-8'
    if request.method == 'POST':
        print(request.POST)
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
    return HttpResponse(message)


def login(request):
    # request.encoding = 'utf-8'
    if request.method == 'POST':
        print(request.POST)
        if 'username' in request.POST and 'password' in request.POST:
            if User.objects.filter(username=request.POST['username'], password=request.POST['password']).first():
                message = ({'StatusCode': '1', 'Message': '用户 ' +
                            request.POST['username'] + ' 登录成功'})
            else:
                message = ({'StatusCode': '0', 'Message': '用户名或密码错误'})
        else:
            message = ({'StatusCode': '-1', 'Message': '表单填写错误，注册失败'})
    else:
        message = ({'StatusCode': '-1', 'Message': '不支持的方法(GET)'})
    print(message)
    return HttpResponse(message)
