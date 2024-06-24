from django.urls import path, include
from . import views

app_name = 'Gym_Customers'

urlpatterns = [
    path('signup/', views.customer_signup, name='customer-signup'),
    path('', views.customer, name='customer-homepage'),
    path('submit_query/', views.submit_query, name='submit-query'),
    path('submit_feedback/', views.submit_feedback, name='submit-feedback'),
    path('update_account/', views.update_customer, name='update-account'),
    path('delete_account/', views.delete_customer, name='delete-account'),
    path('delete_customer_account/<int:id>/', views.delete_customer_account, name='delete-customer-account'),
]