from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:item_id>/', views.detail, name='detail'),
    path('cart/', views.cart, name='cart'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]
