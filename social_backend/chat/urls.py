from django.urls import path

from . import api

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:id>/', api.converstation_details , name="conversation_detials"),
    path('<uuid:id>/send/', api.conversation_send_message , name="conversation_send_message"),
    path('<uuid:id>/get-or-create/', api.conv_get_or_create , name="conv_get_or_create"),
]
