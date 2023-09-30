from django.urls import path , include
from . import views
urlpatterns = [
    path('' , views.getRoutes),
    path('create/user' , views.create_user_for_edith_ai),
    path('users/all' , views.list_user),
    path('chat/edith/v1' , views.chat_with_edith),
    path('user/auth' , views.auth_users),
    path('user/auth/email' , views.auth_email_code),
    path('user/password/resend' , views.return_passwords)

]
