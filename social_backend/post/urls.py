from django.urls import path

from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    path('profile/<uuid:id>/', api.post_list_profile, name ='post_list_profile'),
    path('<uuid:id>/like/', api.post_like_request, name="like_post_request"),
    path('<uuid:id>/postDetail/', api.post_details, name="post_details"),
    path('<uuid:id>/comment/', api.post_create_comment_request, name="post_comment_request"),
    path('trends/', api.get_Trends, name="get_Trends"),
]