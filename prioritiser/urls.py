from django.contrib import admin
from django.urls import path
from src.apis.users.new_user_registration import NewUserRegistration
from src.apis.users.verify_email import VerifyEmail
from src.apis.users.authenticate import Authenticate
from src.apis.users.get_user_info import GetUserInfo

from src.apis.users.update_user_info import update_user_info


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/users/register/', NewUserRegistration.as_view(), name='register-user'),
    path('api/users/verify/<str:email>/<str:uuid_str>/', VerifyEmail.as_view(), name='verify-email'),
    path('api/users/authenticate/', Authenticate.as_view(), name='authenticate-credentials'),
    path('api/users/getuserinfo/', GetUserInfo.as_view(), name='get-user-info'),
    
    path('api/users/update/<email>/', update_user_info, name='update-user'),
    
    # path('api/login/', LoginUserView.as_view(), name='login-user'),
    # 
]
