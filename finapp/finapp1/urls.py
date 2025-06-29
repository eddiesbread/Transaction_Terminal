from django.urls import path
from . import views    

urlpatterns = [
    path("", views.login_user, name="Login"),
    path("Overview/", views.overview, name='Overview'),
    path('Data_entry/', views.data_entry, name='Data_entry'),
    path('Expenses/', views.expenses, name='Expenses'),
    path('Database/', views.database, name='Databases'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_user, name='login')
    
]