from operator import ge
from django.urls import path
from .views import TaskList, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage, adminpage, members, MemberTask,SignupView
from django.contrib.auth.views import LogoutView
# patterns the browser will search when there is an request
urlpatterns = [
    path('task-list/', TaskList.as_view(), name='task-list'),
    path('', adminpage, name="adminpage"),
    path('members/', members, name="members"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page="login"), name='logout'),
    path('register/', SignupView.as_view(), name='register'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
    path('membertask/<int:pk>/', MemberTask, name="taskmember"),
]
