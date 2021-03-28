from django.urls import path
from .views import index, room

urlpatterns = [
    path('', index, name="chat_index"),
    path('<str:room_name>/', room, name="chat_room"),
]