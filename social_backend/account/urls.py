from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api
from . import views


urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup' ),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('edit-profile/', api.editProfile, name="edit_profile"),
    path('edit-password/', api.editPassword, name="edit_password"),
    path('friends/<uuid:id>/request/',api.send_friend_request, name='send_friend_request' ),
    path('friends/<uuid:id>/', api.friends, name='friends'),
    path('friends/<uuid:id>/<str:status>/', api.handel_friend_request, name = 'handel_friend_request'),
    path('activate-account/', views.activateEmail, name="activate_email_view"),
    path('friends/suggested/', api.friends_suggestions, name="suggested_friends"),
]