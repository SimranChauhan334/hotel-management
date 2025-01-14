from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, HttpResponseRedirect
from app.models import hotel, Book, Customer, Room, Profile, room_image
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.db import transaction
from django.db.utils import IntegrityError



def HomePage(request):
    Hotels = hotel.objects.all()
    return render(request, "index.html", {'hotel': Hotels, 'user': request.user})


def DetailPage(request, id):
    Hotel = get_object_or_404(hotel,id=id)
    return render(request, 'details.html', {'Hotel': Hotel, 'user':request.user})
    


def Room_details(request,id):
    Hotel = get_object_or_404(hotel, id=id)
    room = Room.objects.filter(hotel=Hotel, is_available=True)
    # print(f"Rooms available for hotel {Hotel.hotel_name}: {room}")
    return render(request,"room_details.html",{'Room': room, 'hotel':Hotel})




@login_required(login_url='/Userlogin')
def createhotel(request):
    if request.method == 'POST':
        name = request.POST['hotel_name']
        description = request.POST['hotel_descriptions']
        location = request.POST['hotel_location']
        email = request.POST['hotel_email']
        phone_no = request.POST['hotel_phone_no']
        hotel_image = request.FILES.get('hotel_image')

        Hotel = hotel.objects.create(
            hotel_name=name,
            hotel_descriptions=description,          
            hotel_location=location,
            hotel_email=email,
            hotel_phone_no=phone_no,
            hotel_image = hotel_image,
            user=request.user
        )
        Hotel.save()

        messages.success(request, "Hotel created successfully")
        return redirect('detail', id=Hotel.id)
    return render(request, "createform.html")


@login_required(login_url='/Userlogin')
def delete_hotel(request, id):
    Hotel = get_object_or_404(hotel, id=id)
    if request.method == 'POST':
        Hotel.delete()
        messages.success(request, "Hotel deleted successfully.")
        return redirect('HomePage')
    return render(request, "confirm_delete.html", {'hotel': Hotel})


@login_required(login_url='/Userlogin')
def edit_hotel(request, id):
    Hotel = get_object_or_404(hotel, id=id)
    if request.method == 'POST':
        Hotel.hotel_name = request.POST['hotel_name']
        Hotel.hotel_descriptions = request.POST['hotel_descriptions']
        Hotel.hotel_location = request.POST['hotel_location']
        Hotel.hotel_email = request.POST['hotel_email']
        Hotel.hotel_phone_no = request.POST['hotel_phone_no']
        if 'hotel_image' in request.FILES:
            Hotel.hotel_image = request.FILES['hotel_image']
        Hotel.save()

        messages.success(request, "Hotel updated successfully")
        return redirect('detail', id=Hotel.id)

    return render(request, 'edit.html', {'hotel': Hotel})


def add_pic(request, id):
    
    Hotel = get_object_or_404(hotel, id=id)

    if request.method == 'POST' and request.FILES.get('hotel_image'):
        
        hotel_image = request.FILES['hotel_image']
        
       
        Hotel.hotel_image = hotel_image
        Hotel.save()

        messages.success(request, "Hotel image updated successfully")
        return redirect('detail', id=Hotel.id)  

    return render(request, 'add_image.html', {'hotel': Hotel})


@login_required(login_url='/Userlogin')
def check_out(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == "POST":
        
        
            
        book.status = 'completed'
        book.save()

           
        room = book.room
        room.is_available = True  
        room.save()     
        return redirect('booking_history', id=book.hotel.id)
        
    return render(request, 'checkout.html', {'book': book})



@login_required(login_url='/Userlogin')

def Booking(request, id):
    Hotel = get_object_or_404(hotel, id=id)
    rooms = Room.objects.filter(hotel=Hotel, is_available=True)

    if request.method == 'POST':
        room_id = request.POST['room']
        room = get_object_or_404(Room, id=room_id)
        check_in = request.POST["check_in"]
        check_out = request.POST['check_out']
        guest = request.POST["no_of_guest"]
        booking_date = request.POST["booking_date"]

        
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        

       
        if check_in_date >= check_out_date:
            messages.error(request, "Check-out date must be after the check-in date.")
            return redirect('book_room', id=Hotel.id)

       
        overlapping_bookings = Book.objects.filter(
            room=room,
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        )

        if overlapping_bookings.exists():
            messages.error(request, "This room is already booked for the selected dates.")
            return redirect('book_room', id=Hotel.id)
        
       
        customer, created = Customer.objects.get_or_create(user=request.user)
        
       
        booking = Book.objects.create(
            hotel=Hotel,
            customer=customer,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            number_of_guest=guest,
            booking_date=booking_date
        )
       
        room.is_available = False
        room.save()


        messages.success(request, "Booking confirmed successfully.")
        return redirect('booking_history', id=Hotel.id)

    return render(request, "booking.html", {'hotel': Hotel, 'rooms': rooms})


@login_required(login_url='/Userlogin')
def booking_history(request, id):
    Hotel = get_object_or_404(hotel, id=id)
    
   
    customer = Customer.objects.filter(user=request.user).first()
    
    if not customer:
        
        return redirect('HomePage')
    
    profile = Profile.objects.filter(user=request.user).first()

    if profile and profile.is_vendor: 
        hotels = hotel.objects.filter(user=request.user)
        hotel_bookings = Book.objects.filter(hotel__in=hotels)

    else:
        hotel_bookings = Book.objects.filter(hotel=Hotel, customer=customer)

    hotel_bookings = Book.objects.filter(hotel=Hotel, customer=customer)

    return render(request, "booking_history.html", {
        'hotel': Hotel,
        'hotel_bookings': hotel_bookings,
    })


@login_required(login_url='/Userlogin')
def add_room(request, id):
    Hotel = get_object_or_404(hotel,id=id)
    # print(request.POST)

    if request.method == 'POST':
        room_number = request.POST['room_number']
        r_type = request.POST['room_type']
        price = request.POST['price_per_night']
        availability = request.POST['is_available']
        Room_image = request.FILES.getlist('image')
        
        room = Room.objects.create(
            room_number=room_number,
            room_type=r_type,
            price_per_night=price,
            is_available=availability,
            # image = Room_image,
            hotel=Hotel
        )
        room.save()

        for img in Room_image:
            images = room_image.objects.create(room=room, image=img)
            # images.save()
        # return redirect('Homepage', id=Hotel.id)
        return HttpResponse("Homepage")
        

    return render(request, "add_room.html", {'hotel': Hotel})




def delete_image(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    images = room.room_image_set.all()
    print(f"Room: {room.room_number} - Images: {images.count()}")

    if request.method == "POST":
        selected_image = request.POST.getlist("selected_image")
        print(f"Selected images: {selected_image}")
        if selected_image:
            print(f"Deleting images with IDs: {selected_image}")
            room_image.objects.filter(id__in=selected_image).delete() 
            return redirect('room_details', room_id=room.id)

    return render(request, 'delete_room.html', {'room': room, 'images': images})


def upload_image(request,id):
    room = Room.objects.get(Room,id,id)
    if request.method == 'POST':
        form = room_image(request.POST, request.FILES)

        if form.is_valid():
          image = form.save(commit=False)
          image.room = room
          image.save()
          return redirect('room_details', id=room.hotel.id)
    return render(request, 'upload_image.html', {'form': form, 'room': room})  
           

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('HomePage')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")

    return render(request, "login.html")


def userlogout(request):
    logout(request)
    return redirect('HomePage')


def createuser(request):
    if request.method == "POST":

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST['email']
        phone_no = request.POST['phone_number']
        is_vendor = request.POST['is_vendor' ] == 'on'
        # profile_img = request.FILES['image']

        if User.objects.filter(username=username).exists():
            return HttpResponse("Error: Username already exists. Please enter another username.")
        
    

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(
            phone_no = phone_no,
            is_vendor = is_vendor,
            # image = profile_img,
            user = user

        )
        profile.save()

        messages.success(request, "User created successfully")
        return redirect('userlogin')
    return render(request, "createuser.html")


def get_profile(request):
    # print(f"Is vendor: {request.user.profile.is_vendor}")
    return render(request,'profile.html',{'user':request.user})

