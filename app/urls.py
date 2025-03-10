from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('account/profile/', views.profile, name='profile'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('admin/ideas/', views.get_investment_ideas, name='admin_investment_ideas'),
    path('admin/ideas/create/', views.create_investment_idea, name='create_investment_idea'),
    path('admin/users', views.get_users, name='users'),
]
