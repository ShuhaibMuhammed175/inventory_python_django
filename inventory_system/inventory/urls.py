from django.urls import path
from . import views

urlpatterns = [
    path('all-products/', views.ProductListView.as_view(), name='all-products'),
    path('add-product/', views.CreateProduct.as_view(), name='add-product'),
    path('user-products/<int:id>/', views.UserProductsList.as_view(), name='user-products'),
    path('add-to-stock/', views.AddStockView.as_view(), name='add-to-stock'),
    path('remove-stock/', views.RemoveStockView.as_view(), name='remove-stock'),
]
