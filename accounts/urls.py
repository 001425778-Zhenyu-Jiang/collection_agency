from django.urls import path
from .views import index, get_accounts, upload_csv

urlpatterns = [
    path('', index),
    path('accounts', get_accounts),
    path('upload_csv', upload_csv),  # New endpoint for CSV upload
]
