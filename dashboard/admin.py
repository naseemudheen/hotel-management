from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Room)
# admin.site.register(Booking)
admin.site.register(Offer)
admin.site.register(Notification)


class RoomAdmin(admin.ModelAdmin):
	list_display = ('pk', 'title','price','no_of_rooms')

admin.site.register(Room,RoomAdmin)

class BookingAdmin(admin.ModelAdmin):
	list_display = ('auto_id','pk', 'account','checkin_date', 'checkout_date_display')
	
admin.site.register(Booking, BookingAdmin)


class BookedRoomAdmin(admin.ModelAdmin):
	list_display = ('pk', 'room','booked_room_type', 'extra_bed', 'adult', 'child','days', 'total_price')
	
admin.site.register(BookedRoom, BookedRoomAdmin)


class BookedRoomTypeAdmin(admin.ModelAdmin):
	list_display = ('pk', 'room','booking', 'reserved_rooms', 'price', 'extra_bed_price','total_price')
	
admin.site.register(BookedRoomType, BookedRoomTypeAdmin)
