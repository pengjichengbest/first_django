from django.urls import path
from accounts import views
urlpatterns = [
    path('', views.account_list, name='account_list'),
    path('import/', views.import_accounts, name='import_accounts'),
    path('export/', views.export_accounts, name='export_accounts'),
    path('create/', views.account_create, name='account_create'),
    path('<str:account_id>/', views.account_detail, name='account_detail'),
    path('edit/<str:account_id>/', views.account_edit, name='account_edit'),
    path('delete/<str:account_id>/', views.account_delete, name='account_delete'),
]