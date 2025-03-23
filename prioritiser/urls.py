from django.contrib import admin
from django.urls import path
from src.apis.users.new_user_registration import NewUserRegistration
from src.apis.users.verify_email import VerifyEmail
from src.apis.users.authenticate import Authenticate
from src.apis.users.get_user_info import GetUserInfo
from src.apis.boards.eligible_collabrators import EligibleCollabtors
from src.apis.boards.create_new_board import CreateNewBoard
from src.apis.boards.list_all_boards import ListAllBoards

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/users/register/', NewUserRegistration.as_view(), name='register-user'),
    path('api/users/verify/<str:email>/<str:uuid_str>/', VerifyEmail.as_view(), name='verify-email'),
    path('api/users/authenticate/', Authenticate.as_view(), name='authenticate-credentials'),
    path('api/users/getuserinfo/', GetUserInfo.as_view(), name='get-user-info'),
        
    path('api/boards/eligiblecollaborators/', EligibleCollabtors.as_view(), name='fetch all eligible collabrators'),
    path('api/boards/createnewboard/', CreateNewBoard.as_view(), name='create-new-board'),
    path('api/boards/listallboards/', ListAllBoards.as_view(), name='list-all-boards'),
]
