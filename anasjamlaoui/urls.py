from django.urls import path
from . import views

urlpatterns = [

    path('home', views.index, name='index'),
    path('login', views.myLogin, name='login'),
    path('logout', views.myLogout, name='logout'),
    path('all_emp', views.all_emp, name='all_emp'),
    path('add_emp', views.add_emp, name='add_emp'),
    path('remove_emp/<int:emp_id>', views.remove_emp, name='remove_emp'),
    path('update_emp/<int:emp_id>', views.update_emp, name='update_emp'),
    path('announcements', views.announcements, name='announcements'),
    path('add_announcement', views.add_announcement, name='add_announcement'),
    path('departments', views.departments, name='departments'),
    path('department/<str:dep>', views.department, name='department'),
    path('salary', views.salary, name='salary'),

]