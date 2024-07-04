# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreateUserForm, PackageForm, BookingForm, FeedbackForm
from .models import Package, Image
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Booking, Package, Feedback
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    context = {}
    return render(request, 'packages/index.html', context)

def register_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('login')
            else:
                print(form.errors)  # Debugging statement to print form errors if not valid
        context = {'form': form}
        return render(request, 'packages/register.html', context)
    




def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials")
                return render(request, 'packages/login.html')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials")

        # Render the login form with potential error messages
        return render(request, 'packages/login.html', {'messages': messages.get_messages(request)})



def logout_page(request):
    logout(request)
    return redirect('home')


def dashboard(request):
    package_count = Package.objects.count() 
    user_count = User.objects.count() 
    review = Feedback.objects.count()
    if request.user.is_superuser:
        booking_count = Booking.objects.count()  # Get the total number of bookings for superusers
    else:
        booking_count = Booking.objects.filter(user=request.user).count()  # Get the total number of bookings for the logged-in user

    context = {'package_count':package_count, 'user_count':user_count, 'booking_count':booking_count, 'review':review}
    return render(request, 'packages/dashboard.html', context)

def add_feedback(request):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.user = request.user  # Assign current user to the feedback
            feedback.save()
            return redirect('package-list')  # Redirect to package list after saving feedback
        else:
            # Print errors to debug
            print(feedback_form.errors)
    else:
        feedback_form = FeedbackForm()
    
    return render(request, 'packages/add_feedback.html', {'feedback_form': feedback_form})

def booking_info(request):
    if request.user.is_superuser:
        # Superuser can view all bookings
        bookings = Booking.objects.all()
    else:
        # Regular user can view only their own bookings
        bookings = Booking.objects.filter(user=request.user)
    context = {'bookings':bookings}
    return render(request, 'packages/booking_info.html', context)


def booking(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST, user=request.user)  # Pass the logged-in user to the form
        if booking_form.is_valid():
            # Create a new booking instance but do not commit to the database yet
            booking = booking_form.save(commit=False)
            booking.user = request.user  # Assign the logged-in user to the booking
            booking.save()  # Now save the booking instance with the user assigned
            return redirect('booking-info')  # Redirect to a success page or another view after successful submission
    else:
        booking_form = BookingForm(user=request.user)  # Pass the logged-in user to the form

    context = {
        'booking_form': booking_form,
    }
    return render(request, 'packages/booking_form.html', context)


def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # Ensure the logged-in user is the owner of the booking or a superuser
    if request.user == booking.user or request.user.is_superuser:
        booking.delete()
    return redirect('booking-info')

def create_packages(request):
    if request.method == 'POST':
        package_form = PackageForm(request.POST, request.FILES)
        if package_form.is_valid():
            package = package_form.save()  # Save the Package instance
            for file in request.FILES.getlist('images'):
                Image.objects.create(package=package, image=file)  # Save each image associated with the package
            return redirect('package-list')  # Redirect to package list after successful form submission
        else:
            # Print form errors to debug
            print(package_form.errors)
    else:
        package_form = PackageForm()  # Create a new form instance for GET requests

    context = {'package_form': package_form}
    return render(request, 'packages/create_packages.html', context)

def package_list(request):
    packages = Package.objects.all()
    return render(request, 'packages/package_list.html', {'packages': packages})

def package_overview(request, pk):
    package = get_object_or_404(Package, pk=pk)
    feedbacks = Feedback.objects.filter(package=package)
    
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.user = request.user
            feedback.package = package
            feedback.save()
            return redirect('package_overview', pk=pk)  # Redirect to the same package overview page after adding feedback
    else:
        feedback_form = FeedbackForm()
    
    context = {
        'package': package,
        'feedbacks': feedbacks,
        'feedback_form': feedback_form,
    }
    return render(request, 'packages/package_overview.html', context)

def package_edit(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == "POST":
        form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            if 'images' in request.FILES:
                for file in request.FILES.getlist('images'):
                    Image.objects.create(package=package, image=file)
            return redirect('package-list')
    else:
        form = PackageForm(instance=package)
    return render(request, 'packages/package_edit.html', {'form': form, 'package': package})


def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    package_id = image.package.id
    image.delete()
    return HttpResponseRedirect(reverse('package_edit', args=[package_id]))


def package_delete(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == "POST":
        package.delete()
        return redirect('package-list')
    return render(request, 'packages/package_delete.html', {'package': package})