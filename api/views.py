from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
import openai
import random
from django.core.mail import EmailMessage


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {
            "Developer": "Begmatov Behruz",
            "Phone number": "+992920851515",
            "Git Hub": "https://github.com/bekjonbegmatov",
            "FaceBook": "",
            "Instagram": "https://www.instagram.com/behruz_1312_tj",
            "Telegram": "https://t.me/behruz_begmatov",
            "Email": "behruzbegmatov28@gmail.com",
        },
    ]
    return Response(routes)


@api_view(["POST"])
def create_user_for_edith_ai(request):
    data = request.data
    print(data)
    serializer = UsersSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(
            username=request.data["username"],
            password=request.data["password"],
            email=request.data["email"],
        )
        rnum = ""
        nums = list("0123456789")
        for i in range(6):
            rnum += random.choice(nums)
        user.email_code = rnum
        user.save()
        send_email(request.data["email"], rnum)
        code = [
            {
                "Auth": True,
                "message": "Мы отправили вам код подтверждения пожалуйста проверьте ваш e-mail",
                "is_email_auth": False,
            }
        ]
        return Response(code)
    code = [{"Auth": False}]
    return Response(code)


@api_view(["GET"])
def list_user(request):
    users = User.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def chat_with_edith(request):
    openai.api_key = ""
    is_con = request.data['is_context']
    if is_con == 'true' :
        arr_mess = request.data['arr']
        mes = [{"role": "system" , "content": "Ты будешь Edith Ai , Edith AI Это Искусственный интеллект подобе чатGPT и его разработал Бехруз Бегматов",},]
        for mesages in arr_mess :
            if mesages[1] == 'assistant':
                mes.append({'role' : 'assistant' , 'content' : mesages[0]})
            else:
                mes.append({'role' : 'user' , 'content' : mesages[0]})  
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=mes ,
        )
        result = completion.choices[0].message.content
        ansver = [{"Ansver": result}]
        return Response(ansver)
        return Response({'alooo' : 'kukukukukuukukukukukukukukuku'})
    else :
        content = request.data["content"]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ты будешь Edith Ai , Edith AI Это Искусственный интеллект подобе чатGPT и его разработал Бехруз Бегматов",
                },
                {"role": "user", "content": content},
            ],
        )
        result = completion.choices[0].message.content
        ansver = [{"Ansver": result}]
        return Response(ansver)


@api_view(["POST"])
def auth_users(request):
    data = request.data

    user = data["username"]
    password = data["password"]

    users = User.objects.all()

    for i in users:
        if i.username == user and i.password == password:
            code = [{"Auth": True, "Email": i.email, "is_email_auth": i.is_email_auth}]
            return Response(code)
    code = [{"Auth": False, "Error": "User or password not found !"}]
    return Response(code)


def send_email(email_user, rnum):
    subject = "Подтвердите ваш аккаунт Edith Ai"
    body = f"Привет добро пожаловать в Edith Ai <p> это ваш код подтверждения email</p> </br> <h1><b> {rnum} </b></h1> <p> мы рады что вы присоединились к нам</p> <h3>Если это не вы пожалуйста не сообщите этот код никому !</h3>"
    from_email = "edithai.confirm@gmail.com"
    recipient_list = [email_user]
    email = EmailMessage(subject, body, from_email, recipient_list)
    email.content_subtype = "html"
    email.send()
    return True


@api_view(["POST"])
def auth_email_code(request):
    user = User.objects.get(
        username=request.data["username"],
        password=request.data["password"],
        email=request.data["email"],
    )
    email_code = request.data["email_code"]
    if user.email_code == email_code:
        user.is_email_auth = True
        user.save()
        code = [{"is_email_auth": True}]
        return Response(code)
    code = [{"error": "Пожалуйста введите правильный код !"}]
    return Response(code)


@api_view(["POST"])
def return_passwords(request):
    try:
        user = User.objects.get(email=request.data["email"])
    except User.DoesNotExist():
        code = [{"error": "такого email не существует"}]
        return Response(code)
    user_password = user.password
    username = user.username
    subject = "Ваш пароль в Edith Ai"
    body = f"это ваш пароль в Edith Ai </br> <h1><b> пароль : {user_password} </b></h1><h1><b> Логин : {username} </b></h1> <p>мы рады что вы вернулись к нам</p> <h3>Если это не вы пожалуйста не сообщите этот код никому !</h3>"
    from_email = "edithai.confirm@gmail.com"
    recipient_list = [request.data["email"]]
    email = EmailMessage(subject, body, from_email, recipient_list)
    email.content_subtype = "html"
    email.send()
    code = [{"message": "Ваш пароль отправлено в ваш e-mail"}]
    return Response(code)
