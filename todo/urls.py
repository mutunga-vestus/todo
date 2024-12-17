from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='home'),
    path('create/',views.createTodo,name='createTodo'),
    path('todo/<id>/',views.todoDetail,name='todo'),
    path('todoDelete/<id>/',views.todoDelete,name='todoDelete'),
    path('todoEdit/<id>/',views.todoEdit,name='todoEdit'),
]