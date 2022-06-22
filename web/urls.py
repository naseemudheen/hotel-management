from django.contrib import admin
from django.urls import path
from django.conf import settings
from web import views

app_name = "web"

urlpatterns = [
    path('', views.index, name="index"),
    path('order-summary', views.order_summary, name="order_summary"),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    # path('booking-confirmed/<booking_id>', views.booking_confirmed, name="booking_confirmed"),
    path('get-extra-bed', views.get_extra_bed, name="get_extra_bed"),
    path('check-room-availabilty-web', views.check_room_availabilty_web, name="check_room_availabilty_web"),
    path('create-user-data-ajax', views.create_user_data_ajax, name="create_user_data_ajax"),
    path('terms-and-conditions', views.term_and_conditions, name="term_and_conditions"),
    path('privacy-policy', views.privacy_policy, name="privacy_policy"),
    path('cancellation-policy', views.cancellation_policy, name="cancellation_policy"),



]
