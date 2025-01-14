from django.db import models
from django.contrib.auth.models import User

# from django.utils import timezone



class hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    hotel_location = models.TextField()
    hotel_descriptions = models.TextField()
    hotel_email = models.EmailField(max_length=120)
    hotel_phone_no = models.CharField(max_length=50)
    hotel_image = models.ImageField(upload_to='photo/',null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.hotel_name

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=55)
    

    def __str__(self):
       return f"{self.user.first_name} {self.user.last_name}"


class Room(models.Model):
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE)
    room_number = models.IntegerField(unique=True)  
    room_type = models.CharField(max_length=40)
    # room_image = models.ImageField(upload_to='photo/',null=True, blank=True)
    price_per_night = models.DecimalField(max_digits=20, decimal_places=10)
    is_available = models.BooleanField(default=True) 

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"
    
class Book(models.Model):
    STATUS_CHOICES = [
        ('pendin', 'pending'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    hotel = models.ForeignKey(hotel, on_delete=models.CASCADE)  
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    check_in = models.DateField() 
    check_out = models.DateField()
    number_of_guest = models.IntegerField() 
    booking_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Booking by {self.customer.user.first_name} {self.customer.user.last_name} at {self.hotel.hotel_name}"


class room_image(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photo/', null=True,blank=True)

    def __str__(self):
        return f"Image for room {self.room.room_number}"



class Profile(models.Model):
    is_vendor = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=20)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name}" 