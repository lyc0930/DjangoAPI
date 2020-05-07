# Django 日期查询接口

## 部署

```bash
> conda install django
> conda install pyjwt
> python manage.py runserver
```

## 人工测试

### 接口交互

```bash
> curl -d username=rose -d password=12345 http://127.0.0.1:8000/user/signup
{"code": 201, "message": "Signed up successfully. ", "data": {"username": "rose"}}
> curl -d username=rose -d password=12345 http://127.0.0.1:8000/user/login
{"code": 200, "message": "Logged-in successfully. ", "data": {"username": "rose", "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODg5NjE0NTksImlhdCI6MTU4ODg3NTA1OSwiZGF0YSI6eyJ1c2VybmFtZSI6InJvc2UifX0.bzvIs2ZiRgECm0jpa0PXnRtackZP6e6FHYWXq0CPouo"}}
> curl -d date=1994-01-01 -d token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODg5NjE0NTksImlhdCI6MTU4ODg3NTA1OSwiZGF0YSI6eyJ1c2VybmFtZSI6InJvc2UifX0.bzvIs2ZiRgECm0jpa0PXnRtackZP6e6FHYWXq0CPouo http://127.0.0.1:8000/user/query
{"code": 200, "message": "Query was successfully. ", "data": {"HolidayName": "元旦"}}
> curl -d date=1994-10-01 -d token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODg5NjE0NTksImlhdCI6MTU4ODg3NTA1OSwiZGF0YSI6eyJ1c2VybmFtZSI6InJvc2UifX0.bzvIs2ZiRgECm0jpa0PXnRtackZP6e6FHYWXq0CPouo http://127.0.0.1:8000/user/query
{"code": 200, "message": "Query was successfully. ", "data": {"HolidayName": "国庆节"}}
> curl -d date=1994-12-25 -d token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODg5NjE0NTksImlhdCI6MTU4ODg3NTA1OSwiZGF0YSI6eyJ1c2VybmFtZSI6InJvc2UifX0.bzvIs2ZiRgECm0jpa0PXnRtackZP6e6FHYWXq0CPouo http://127.0.0.1:8000/user/query
{"code": 200, "message": "Query was successfully. ", "data": {"HolidayName": "圣诞节"}}
```

### 数据库查询

```bash
> sqlite3 db.sqlite3
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite> .tables
auth_group                  django_admin_log
auth_group_permissions      django_content_type
auth_permission             django_migrations
auth_user                   django_session
auth_user_groups            user_holiday
auth_user_user_permissions  user_user
sqlite> select * from user_user;
1|rose|12345
sqlite> select * from user_holiday;
1|元旦|2000-01-01
2|圣诞节|2000-12-25
3|国庆节|2000-10-01
sqlite>
```

## 接口

### 用户接口

-   `/user/signup` 支持 POST 方法，接受 username 与 password 两个参数。返回注册成功或失败的 json 信息

-   `/user/login` 支持 POST 方法，接受 username 与 password 两个参数。登录成功时（用户存在且密码正确）返回带有 token 的 json 信息，否则给出登录失败的 json 信息。

### 日期节日查询接口

-   `/user/query` 支持 POST 方法，接受 date(YYYY-MM-DD) 与 token 两个参数。数据库中已有如下三个节日
    -   每年的 01 月 01 日，元旦
    -   每年的 12 月 25 日，圣诞节
    -   每年的 10 月 01 日，国庆节。
        未登录的情况下，token 无法被验证，返回未登录的 json 提示信息；已登录的情况下，返回查询节日结果 json 格式的信息。。

### json 信息

接口返回的 json 信息参考[Google Cloud References](https://cloud.google.com/storage/docs/json_api/v1/status-codes)，成功的请求有如下格式的返回信息

```json
{
    "code": 200,
    "message": message,
    "data": {
        "username": username,
        "token": token
    }
}
```

其中`'date'`键包括多个返回的数据值

```json
{
    "code": 401,
    "message": message,
    "error": [
        {
            "reason": "Unauthorized",
            "message": message
        }
    ]
}
```

其中`'error'`键的值是多个错误信息的数组，每个错误包含了错误原因及信息
