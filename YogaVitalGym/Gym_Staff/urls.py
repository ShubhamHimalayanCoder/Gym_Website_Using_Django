from django.urls import path
from . import views

app_name = 'Gym_Staff'

urlpatterns = [
    path('signup/', views.gym_signup, name='gym-signup'),
    path('administrator/', views.administrator, name='administrator-homepage'),
    path('instructor/', views.instructor, name='instructor-homepage'),
    path('trainer/', views.trainer, name='trainer-homepage'),
    path('dietician/', views.dietician, name='dietician-homepage'),
    path('update_staff_account/', views.update_staff, name='update-staff-account'),
    path('delete_staff_account/', views.delete_staff, name='delete-staff-account'),
    path('respond_query/<int:query_id>/', views.respond_query, name='respond-query'),
    path('staff_submit_query/', views.send_staff_query, name='staff-submit-query'),
    path('respond_staff_query/<int:query_id>/', views.respond_staff_query, name='respond-staff-query'),
    path('upload_gallery/', views.gallery, name='upload-gallery'),
    path('upload_blog', views.blog, name='upload-blog'),
    path('export-to-excel/', views.convert_to_excel, name='to-excel'),
    path('download-excel-file/', views.download_excel_file, name='download-excel'),
]