# Django 日期查询接口

## To run

```bash
> conda install django
> conda install jwt
> python manage.py runserver
```

## Manually Test

```bash
> curl -d username=Jack3 -d password=12345 http://127.0.0.1:8000/user/signup
{"StatusCode": "1", "Message": "\u7528\u6237 Jack3 \u6ce8\u518c\u6210\u529f"}
> curl -d username=Jack3 -d password=12345 http://127.0.0.1:8000/user/login
{'StatusCode': '1', 'Message': '用户 Jack3 登录成功', 'Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODg5NDk5MzUsImlhdCI6MTU4ODg2MzUzNSwiZGF0YSI6eyJ1c2VybmFtZSI6IkphY2szIn19.XtRievJNrYMD7xK6NoazoE-4v0kdJndnHRpLeJl44kM'}
> curl -d date=1999-01-01 -d token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODg5NDk5MzUsImlhdCI6MTU4ODg2MzUzNSwiZGF0YSI6eyJ1c2VybmFtZSI6IkphY2szIn19.XtRievJNrYMD7xK6NoazoE-4v0kdJndnHRpLeJl44kM http://127.0.0.1:8000/user/login
{'StatusCode': '1', 'Message': '查询成功', 'HolidayName': '元旦'}
>
```
