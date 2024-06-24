from django.db import models


# Create your models here.
class Gym_Customer_Data(models.Model):
    customer_id = models.AutoField(primary_key=True,unique=True)
    customer_name = models.CharField(max_length=100)
    customer_mobile = models.CharField(max_length=10,unique=True)
    customer_email = models.EmailField(max_length=100, unique=True)
    customer_password = models.CharField(max_length=20)
    customer_address = models.CharField(max_length=100)
    customer_city = models.CharField(max_length=100)
    customer_state = models.CharField(max_length=100)
    customer_country = models.CharField(max_length=100)
    customer_pin = models.CharField(max_length=6)
    customer_services = models.CharField(max_length=50)
    customer_image = models.ImageField(upload_to='customer_images/', null=True, blank=True)

    def __str__(self):
        return f'Customer ID = {self.customer_id}, Customer Name = {self.customer_name}'
    


class Query(models.Model):
    customer = models.ForeignKey(Gym_Customer_Data, on_delete=models.CASCADE)
    staff = models.ForeignKey('Gym_Staff.Gym_Staff_Data', on_delete=models.CASCADE)
    query_subject = models.CharField(max_length=100)
    query_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)



class Feedback(models.Model):
    customer = models.ForeignKey(Gym_Customer_Data,on_delete=models.CASCADE)
    feedback_message = models.TextField()
    rating = models.IntegerField()