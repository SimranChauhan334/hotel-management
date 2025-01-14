"""
URL configuration for hotel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage, name='HomePage'),
    path('create/',createhotel, name='create_hotel'), 
    path('detail/<int:id>/', DetailPage, name='detail'), 
    path('room/<int:id>/', Room_details, name='room_details'), 
    path('edit/<int:id>/', edit_hotel, name='edit_hotel'),
    path('delete/<int:id>/', delete_hotel, name='delete_hotel'),
    path('add_pic/<int:id>/', add_pic, name='add_pic'),
    path('checkout/<int:id>/', check_out, name='check_out'),
    path('book/<int:id>/', Booking, name='book_room'),
    path('booking_history/<int:id>/', booking_history, name="booking_history"),
    path('add_room/<int:id>/', add_room, name='add_room'),
    path('edit_room/<int:id>/', Edit_room, name='edit_room'),
    # path('edit_room/<int:id>/', Edit_room, name="Edit_room"),
    # path('room/<int:room_id>/delete_image/<int:image_id>/', delete_image, name='delete_image'),
    path('upload_image',upload_image, name="upload_image"),
    path('login/', userlogin, name='userlogin'), 
    path('logout/', userlogout, name='userlogout'),
    path('createuser/', createuser, name='createuser'),  
    path('profile/',get_profile, name='get_profile'),
    path('delete_image/<int:room_id>/', delete_image, name='delete_image'),
    
   


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



