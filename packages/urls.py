from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Review
    path('review/', views.add_feedback, name='add_feedback'),


    

    # Packages
    path('create-packages/', views.create_packages, name='create-packages'),
    path('package-list/', views.package_list, name='package-list'),
    path('package_overview/<int:pk>', views.package_overview, name='package_overview'),
    path('package/<int:pk>/edit/', views.package_edit, name='package_edit'),
    path('package/<int:pk>/delete/', views.package_delete, name='package_delete'),
    
    path('image/delete/<int:image_id>/', views.delete_image, name='delete_image'),

    # Booking
    path('booking/', views.booking, name='booking'),
    path('booking-info/', views.booking_info, name='booking-info'),
    path('booking/delete/<int:pk>/', views.delete_booking, name='booking_delete'),
    
]