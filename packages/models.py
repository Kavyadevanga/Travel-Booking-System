from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=100)
    overview = models.TextField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    # location = models.CharField(max_length=200)
    number_of_days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class Image(models.Model):
    package = models.ForeignKey(Package, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='packages', default='')

    def __str__(self):
        return f"Image for {self.package.name}"

    
class Members(models.Model):
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length=255)
    DOB = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['DOB']
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey('Package', on_delete=models.CASCADE)
    booking_date = models.DateField()
    status = models.CharField(max_length=50)
    start_date = models.DateField()
    # end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer: {self.user}"

    class Meta:
        ordering = ['-updated_at']

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"Feedback by {self.user.username}"