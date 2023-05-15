from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
import openai

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Developer': 'Begmatov Behruz',
            'Phone number': '+992920851515',
            'Git Hub': 'https://github.com/bekjonbegmatov',
            'FaceBook': '',
            'Instagram': 'https://www.instagram.com/behruz_1312_tj',
            'Telegram': 'https://t.me/behruz_begmatov',
            'Email': 'behruzbegmatov28@gmail.com',
        },
    ]
    return Response(routes)

@api_view(['POST'])
def create_user_for_edith_ai(request):
    data = request.data
    print(data)
    serializer = UsersSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        code = [
            {
                "Auth" : True 
            }
        ]
        return Response(code)
    code = [
        {
            "Auth" : False
        }
        ]
    return Response(code)

@api_view(['GET'])
def list_user(request):
    users = User.objects.all()
    serializer = UsersSerializer(users , many=True)
    return Response(serializer.data)

@api_view(['POST'])
def chat_with_edith(request):
    openai.api_key = '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'

    print(request.data)
    content = request.data['content']
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
            messages=[{"role": "user", 
            "content": content,
            }])
    result = completion.choices[0].message.content
    ansver = [
        {
            'Ansver' : result
        }
    ]
    return Response(ansver)

@api_view(['POST'])
def auth_users(request):
    data = request.data

    user = data['username']
    password = data['password']

    users = User.objects.all()

    for i in users :
        if i.username == user and i.password == password :
            code = [
                {
                    "Auth" : True ,
                    'Email' : i.email
                }
            ]
            return Response(code)
    code = [
        {
            'Auth' : False ,
            'Error' : 'User or password not found !'
        }
    ]
    return Response(code)

        