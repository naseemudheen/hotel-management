from __future__ import unicode_literals
from django.db import models
from django.db.models.fields import IntegerField
# from main.models import BaseModel
from django.utils.translation import ugettext_lazy as _
from versatileimagefield.fields import VersatileImageField
from account.models import Account
from django.utils.timezone import datetime
from PIL import Image
from uuid import uuid4

class Room(models.Model):
    title = models.CharField(max_length=128,null=False,blank=False)
    price =models.DecimalField(max_digits=7, decimal_places=2,null=False,blank=False)
    new_price =models.DecimalField(max_digits=7, decimal_places=2,)
    max_adult = models.IntegerField()
    max_child =models.IntegerField()
    description = models.CharField(max_length=128,null=False,blank=False)
    status = models.CharField(max_length=128,default='available')
    image = VersatileImageField('Image', upload_to='media/room_image/', null=True, blank=True)  
    adult = models.IntegerField()    
    child = models.IntegerField()
    no_of_rooms = models.IntegerField()
    extra_bed_price = models.DecimalField(max_digits=7, decimal_places=2,null=False,blank=False,default=500.00)

    class Meta:
        db_table = 'dashboard_room'
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        # ordering = ('-date_added',)

    def __str__(self):
        return str(self.title)

class Offer(models.Model):
    title = models.CharField(max_length=128,null=False,blank=False)
    room_type = models.ForeignKey(Room, on_delete=models.CASCADE)
    offer_price =models.DecimalField(max_digits=7, decimal_places=2,null=False,blank=False)
    date=models.DateField(null=True,blank=True)
    
    class Meta:
        db_table = 'dashboard_offer_room'
        verbose_name = _('Offer')
        verbose_name_plural = _('Offers')
        # ordering = ('-date_added',)

    def __str__(self):
        return str(self.title)



class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index = True,unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE,)
    # room_num = models.ForeignKey(Room_num, on_delete=models.CASCADE)
    checkin_date=models.DateField(null=False,blank=False)
    checkout_date=models.DateField(null=False,blank=False)
    checkout_date_display=models.DateField(null=False,blank=False)

    booking_date=models.DateTimeField(default=datetime.now(),null=True,blank=True)
    is_Booking_confirmed = models.BooleanField(default=False,null=True,blank=True)

    order_id = models.CharField(max_length=128,null=True,blank=True)
    total_extra_bed_price = models.IntegerField()
    total_price=models.DecimalField(max_digits=7, decimal_places=2,null=False,blank=False)
    total_offer_price=models.DecimalField(max_digits=7, decimal_places=2,null=False,blank=False)

    payment_type = models.CharField(max_length=128,null=False,blank=False)

    class Meta:
        db_table = 'dashboard_booking'
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')
        # ordering = ('-date_added',)

    def __str__(self):
        return str(self.auto_id)

class BookedRoomType(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,)
    reserved_rooms = models.IntegerField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    extra_bed_price=models.IntegerField()
    total_price=models.DecimalField(max_digits=7, decimal_places=2,null=False,blank=False)
    total_offer_price=models.DecimalField(max_digits=7, decimal_places=2,null=False,blank=False)



    class Meta:
        db_table = 'dashboard_booked_room_type'
        verbose_name = _('booked room type')
        verbose_name_plural = _('booked room types')
        # ordering = ('-date_added',)

    def __str__(self):
        return str(self.room) + str(self.booking)


class BookedRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booked_room_type = models.ForeignKey(BookedRoomType, on_delete=models.CASCADE,)
    adult = models.IntegerField(default=0)
    child =models.IntegerField()
    extra_bed = models.IntegerField()
    days=models.IntegerField()
    total_price=models.IntegerField()
    offer_price=models.IntegerField()



    class Meta:
        db_table = 'dashboard_booked_room'
        verbose_name = _('booked room')
        verbose_name_plural = _('booked rooms')
        # ordering = ('-date_added',)
    def __str__(self):
        return self.room.title


class Notification(models.Model):
    # account = models.ForeignKey(Account, on_delete=models.CASCADE,)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE,)
    is_readed = models.BooleanField(default=False,null=True,blank=True)


    def __str__(self):
        return str(self.booking.auto_id)


