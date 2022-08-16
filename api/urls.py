from django.urls import path
from api import views

urlpatterns = [
  path('', views.login, name='login'),
  path('callback/', views.CallbackView.as_view(), name='callback'),
]
