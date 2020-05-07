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
                message = 'Username ' + \
                    request.POST['username'] + \
                    ' has already been taken. '
                response = ({
                    'code': 409,
                    'message': message,
                    'error': [
                        {
                            'reason': 'Conflict',
                            'message': message
                        }
                    ]
                })
            else:
                user_information = User(
                    username=request.POST['username'], password=request.POST['password'])
                user_information.save()
                message = 'Signed up successfully. '
                response = ({
                    'code': 201,
                    'message': message,
                    'data':
                    {
                        'username': request.POST['username']
                    }
                })
        else:
            message = 'Malformed request syntax. '
            response = ({
                'code': 400,
                'message': message,
                'error': [
                    {
                        'reason': 'Bad Request',
                        'message': message
                    }
                ]
            })
    else:
        message = 'Method Not Allowed. '
        response = ({
            'code': 405,
            'message': message,
            'error': [
                {
                    'reason': 'Method Not Allowed',
                    'message': message
                }
            ]
        })
    return JsonResponse(response)


def login(request):
    # request.encoding = 'utf-8'
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            if User.objects.filter(username=request.POST['username'], password=request.POST['password']).first():
                token = User.objects.filter(
                    username=request.POST['username'], password=request.POST['password']).first().token
                message = 'Logged-in successfully. '
                response = ({
                    'code': 200,
                    'message': message,
                    'data':
                    {
                        'username': request.POST['username'],
                        'token': token
                    }
                })
            else:
                message = 'Wrong username or password. '
                response = ({
                    'code': 401,
                    'message': message,
                    'error': [
                        {
                            'reason': 'Unauthorized',
                            'message': message
                        }
                    ]
                })
        else:
            message = 'Malformed request syntax. '
            response = ({
                'code': 400,
                'message': message,
                'error': [
                    {
                        'reason': 'Bad Request',
                        'message': message
                    }
                ]
            })
    else:
        message = 'Method Not Allowed. '
        response = ({
            'code': 405,
            'message': message,
            'error': [
                {
                    'reason': 'Method Not Allowed',
                    'message': message
                }
            ]
        })
    return JsonResponse(response)


def query(request):
    # request.encoding = 'utf-8'
    if request.method == 'POST':
        if 'date' in request.POST and 'token' in request.POST:
            try:
                log_information = jwt.decode(
                    request.POST['token'], settings.SECRET_KEY, algorithm='HS256')
                username = log_information.get('data').get('username')
            except jwt.ExpiredSignatureError:
                message = 'Token expired. '
                response = ({
                    'code': 401,
                    'message': message,
                    'error': [
                        {
                            'reason': 'Unauthorized',
                            'message': message
                        }
                    ]
                })
                return JsonResponse(response)
            except jwt.InvalidTokenError:
                message = 'Invalid token. '
                response = ({
                    'code': 401,
                    'message': message,
                    'error': [
                        {
                            'reason': 'Unauthorized',
                            'message': message
                        }
                    ]
                })
                return JsonResponse(response)
            except Exception as e:
                message = 'Can not get user object from token. '
                response = ({
                    'code': 401,
                    'message': message,
                    'error': [
                        {
                            'reason': 'Unauthorized',
                            'message': message
                        }
                    ]
                })
                return JsonResponse(response)
            if User.objects.filter(username=username).first():
                try:
                    date = datetime.strptime(request.POST['date'], "%Y-%m-%d")
                    queryDate = date.strftime("2000-%m-%d")
                except ValueError:
                    message = 'Date format wrong. '
                    response = ({
                        'code': 422,
                        'message': message,
                        'error': [
                            {
                                'reason': 'Unprocessable Entity',
                                'message': message
                            }
                        ]
                    })
                    return JsonResponse(response)
                if Holiday.objects.filter(holiday_date=queryDate).first():
                    message = 'Query was successfully. '
                    response = ({
                        'code': 200,
                        'message': message,
                        'data':
                        {
                            'HolidayName': Holiday.objects.filter(
                                holiday_date=queryDate).first().holiday_name
                        }
                    })
                else:
                    message = 'No holiday matched. '
                    response = ({
                        'code': 204,
                        'message': message,
                        'data':
                        {
                            'HolidayName': ''
                        }
                    })
            else:
                message = 'Username do not exists. '
                response = ({
                    'code': 401,
                    'message': message,
                    'error': [
                        {
                            'reason': 'Unauthorized',
                            'message': message
                        }
                    ]
                })
        else:
            message = 'Malformed request syntax. '
            response = ({
                'code': 400,
                'message': message,
                'error': [
                    {
                        'reason': 'Bad Request',
                        'message': message
                    }
                ]
            })
    else:
        message = 'Method Not Allowed. '
        response = ({
            'code': 405,
            'message': message,
            'error': [
                {
                    'reason': 'Method Not Allowed',
                    'message': message
                }
            ]
        })
    return JsonResponse(response)
