from django.contrib import admin
from django.urls import path
from django.conf import settings
from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path('', views.index, name="index"),   
    path('calender', views.calender, name="calender"),
    path('create-room', views.create_room, name="create_room"),
    path('offer-room', views.RoomOfferCreateView.as_view(), name="offer_room"),
    path('confirm-booking/', views.confirm_booking,name='confirm_booking'),
    path('invoice/<id>', views.booking_invoice,name='booking_invoice'),


    path('booking-room', views.booking_room, name="booking_room"),
    path('booking-listview', views.BookingListView.as_view(),name='booking_list_view'),
    path('online-booking-listview', views.OnlineBookingListView.as_view(),name='online_booking_list_view'),

    path('update-room/<int:id>', views.update_room,name='update_room'),
    path('delete-room/<int:id>', views.delete_room,name='delete_room'),

    path('list-room', views.room_list_view, name="room_list_view"),
    path('create-customer-ajax', views.create_customer_ajax, name="create_customer_ajax"),
    path('check-room-availabilty', views.check_room_availabilty, name="check_room_availabilty"),
    # path('get-notification',views.get_notification,name='get_notification',),
    path('account-autocomplete',views.account_autocomplete.as_view(),name='account_autocomplete',),

    path('get-extra-bed', views.get_extra_bed, name="get_extra_bed"),
    path('offer-list-view', views.OfferListView.as_view(),name='offer_list_view'),
    path('<int:id>/delete-offer', views.delete_offer,name='delete_offer'),
    path('update-offer/<int:id>', views.update_offer,name='update_offer'),
    path('<int:id>/account', views.account_detail_view,name='account_detail_view'),
    path('get-max-guests', views.get_max_guests, name="get_max_guests"),
    path('notifications-ajax', views.notifications_ajax, name="notifications_ajax"),
    path('mark-as-read-notifi-ajax', views.mark_as_read_notifi_ajax, name="mark_as_read_notifi_ajax"),

]
