from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.DRF_Home_View),
    path('product/', csrf_exempt(views.Product_CBV.as_view())),
]