from django.urls import path
from .views import DashboardStatsView, MessageListView, UserDetailView, UserListView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token, name='api-login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('messages/', MessageListView.as_view(), name='message-list'),
]