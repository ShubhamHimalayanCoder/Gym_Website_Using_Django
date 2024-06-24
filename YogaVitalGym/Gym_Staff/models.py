from django.db import models

# Create your models here.

class Gym_Staff_Data(models.Model):
    staff_user_id = models.AutoField(primary_key=True,unique=True)
    staff_user_name = models.CharField(max_length=100)
    staff_user_mobile = models.CharField(max_length=10)
    staff_user_email = models.EmailField(max_length=100)
    staff_user_password = models.CharField(max_length=20)
    staff_user_address = models.CharField(max_length=100)
    staff_user_city = models.CharField(max_length=100)
    staff_user_state = models.CharField(max_length=100)
    staff_user_country = models.CharField(max_length=100)
    staff_user_pin = models.CharField(max_length=6)
    staff_user_designation = models.CharField(max_length=20)
    staff_user_image = models.ImageField(upload_to='gym_staff_images/',null=True, blank=True)

    def __str__(self) -> str:
        return f'User ID : {self.staff_user_id}, User Name : {self.staff_user_name}'
    

    
    
class Response(models.Model):
    query = models.OneToOneField('Gym_Customers.Query', on_delete=models.CASCADE)
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class Staff_Query(models.Model):
    sender = models.ForeignKey(Gym_Staff_Data, related_name='sent_queries', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Gym_Staff_Data, related_name='received_queries', on_delete=models.CASCADE)
    query_subject = models.CharField(max_length=255)
    query_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)



class Staff_Query_Response(models.Model):
    query = models.OneToOneField(Staff_Query, on_delete=models.CASCADE)
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class Gallery(models.Model):
    staff = models.ForeignKey(Gym_Staff_Data,related_name='sender', on_delete=models.CASCADE)
    gallery_image = models.ImageField(upload_to='gallery_images/', null=True, blank=True)
    about_image = models.CharField(max_length=50)



class Blog(models.Model):
    staff = models.ForeignKey(Gym_Staff_Data,related_name='submitter', on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=200)
    blog_text = models.TextField()
    blog_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)