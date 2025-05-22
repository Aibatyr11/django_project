from django.urls import path
from django.views.generic.dates import WeekArchiveView, DayArchiveView
from django.views.generic.edit import CreateView
from .models import Bb
from .views import (rubric, rubric_detail, product_detail,search,
                    add_to_cart, remove_from_cart, cart_view, update_cart,add_product, register)
from django.contrib.auth import views as auth_views
app_name = 'bboard'

urlpatterns = [
    path('', rubric, name='rubric'),
    path('rubric/<slug:slug>/', rubric_detail, name='rubric_detail'),
    path('product_detail/<slug:slug>/', product_detail, name='product_detail'),
    path('search/', search, name='search'),
    # Корзина
    path('add/<int:sp_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove'),
    path('cart/', cart_view, name='view'),
    path('cart/update/', update_cart, name='update_cart'),
    path('add/', add_product, name='add_product'),

    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]

