from django.urls import path
from . import views

# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

urlpatterns = [
    path('http_response/', views.http_response_CBV.as_view()),
    path('json_response/', views.json_response_CBV.as_view()),
    path('view_all_product/', views.view_all_product_CBV.as_view()),
    path('view_all_product_serialize/', views.view_all_product_serialize_CBV.as_view()),

    path('view_one_product/<int:product>', views.view_one_product_CBV.as_view()),
    path('view_one_product_serialize/<int:product>', views.view_one_product_serialize_CBV.as_view()),

    path('insert_one/', views.insert_one_product.as_view(), name="insert_one"),
    path('insert_multiple/', views.insert_multiple_product.as_view(), name="insert_multiple"),
    path('update_one/<product>', views.update_one_product.as_view(), name="update_one"),
    path('update_one_data/<product>', views.update_one_product_data.as_view(), name="update_one"),
    path('delete_one/<product>', views.delete_one_product.as_view(), name="delete_one"),

    path('crud',views.CURD.as_view(), name="crud"),
]