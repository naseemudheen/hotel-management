
from datetime import time,date, timedelta, timezone 
# from datetime import strptime
import datetime,calendar
import pytz
from django.http import response
from django.shortcuts import (render,redirect,get_object_or_404,HttpResponseRedirect)
from .forms import *
from django.urls import reverse
from .models import *
from account.forms import *
from dal import autocomplete
import json
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms import formset_factory,modelformset_factory
from django.views.generic import(
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    DetailView
)
from account import models
from django.contrib.auth.mixins import LoginRequiredMixin
from main.functions import get_auto_id


user_login_required = user_passes_test(lambda user: user.is_admin)
def admin_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func

@admin_required
def index(request):
    context = {
        "title": "dashboard",
        "page_name":"Dashboard",
    }
    return render(request, 'dashboard/index.html', context)
    
@admin_required
def calender(request):
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(request.GET.get('start'), date_format).date()
    end_date = datetime.strptime(request.GET.get('end'), date_format).date()
    # print(start_date,end_date)

    obj = get_rooms_status(start_date,end_date)
    events = []
    for key,value in obj.items():
        dates = key
        for k,v in value.items():
            # print(date,k,v)
            color = "#08aceb"
            if v['filled_rooms'] == v['total_rooms']:
                color = "#398f07"
            elif v['free_rooms'] == v['total_rooms']:
                color = "#bdbcbb"
            row ={
                "title" : "{} : {}/{}".format(k,v['filled_rooms'],v['total_rooms']),
                "start": dates,
                "backgroundColor": color,
                # "url": 'http://google.com/'
            }
            events.append(row)
    obj = json.dumps(events)
    return HttpResponse(obj,content_type='application/javascript')




@admin_required
def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST,request.FILES)
        if (form.is_valid()):
            form_data = form.save(commit=False)
            form_data.save()
            return redirect('dashboard:room_list_view')

            
    else:
        form = RoomForm()
    context = {
        "title": "Add Room",
        "form": form,
        "page_name":"add_room_type"
    }  
    return render(request, 'dashboard/room_create_view.html', context)




@admin_required
def booking_room(request):

    BookedRoomFormSet = formset_factory(BookedRoomForm,extra=1)
    if request.method == "POST":
        account_form = CustomAccountForm(request.POST)
        form = BookingForm(request.POST)
        booked_room_formset = BookedRoomFormSet(request.POST,prefix="booked_room_formset")
        if (form.is_valid()):
            form_data = form.save(commit=False)
            form_data.total_price = 0
            form_data.total_offer_price = 0
            form_data.total_extra_bed_price =int(0)
            date_format = "%Y-%m-%d"
            a = datetime.strptime(str(form_data.checkin_date), date_format)
            b = datetime.strptime(str(form_data.checkout_date), date_format)
            form_data.checkout_date_display= form_data.checkout_date
            form_data.checkout_date = form_data.checkout_date-timedelta(1)

            delta = b - a
            total_days= delta.days
            if(total_days > 0 ):


                if (booked_room_formset.is_valid()):
                    form_data.auto_id = get_auto_id(Booking)

                    form_data.save()  
                
                    rooms = Room.objects.all()
                    for room in rooms:
                        price = get_room_total_price(room,form_data.checkin_date,form_data.checkout_date)
                        offer_price = get_room_total_price_with_offer(room,form_data.checkin_date,form_data.checkout_date)

                        BookedRoomType.objects.create(
                            room=room,
                            booking=form_data,
                            reserved_rooms=0,
                            price = price,
                            offer_price = offer_price,
                            extra_bed_price = 0,
                            total_price = 0,
                            total_offer_price = 0,

                        )
                    for bookedroomform in booked_room_formset:
                        f_data = bookedroomform.save(commit=False)
                        extra_bed_price = f_data.extra_bed * f_data.room.extra_bed_price * total_days
                        bkd_room_type = BookedRoomType.objects.get(booking=form_data,room=f_data.room)
                        room_price = bkd_room_type.price
                        room_offer_price = bkd_room_type.offer_price

                        bkd_room_type.reserved_rooms = int(bkd_room_type.reserved_rooms) + int(1)

                        bkd_room_type.extra_bed_price =  extra_bed_price
                        f_data.total_price = room_price + extra_bed_price
                        f_data.offer_price = room_offer_price + extra_bed_price


                        bkd_room_type.total_price = f_data.total_price * bkd_room_type.reserved_rooms
                        bkd_room_type.total_offer_price = f_data.offer_price * bkd_room_type.reserved_rooms


                        bkd_room_type.save()
                        f_data.days = total_days
                        f_data.extra_bed = extra_bed_price/f_data.room.extra_bed_price/total_days
                        f_data.booked_room_type = bkd_room_type

                        form_data.total_price+=f_data.total_price
                        form_data.total_offer_price+=f_data.offer_price


                        form_data.total_extra_bed_price = form_data.total_extra_bed_price + bkd_room_type.extra_bed_price
                        form_data.auto_id = get_auto_id(Booking)
                       
                        f_data.save()

                    BookedRoomType.objects.filter(total_price = 0).delete()
                    form_data.save()
                    request.session['booking_id'] = form_data.auto_id
                    return redirect('dashboard:confirm_booking' )

                        
        else:
            print("not valid ..")
    else:
        form = BookingForm()
        booked_room_formset = BookedRoomFormSet(prefix="booked_room_formset")
        account_form = CustomAccountForm()
    context = {
        "title": "New booking",
        "form": form,
        # "room_type_formset":room_type_formset,
        "booked_room_formset":booked_room_formset,
        "account_form":account_form,
        "page_name":"booking_room",
    }  
    return render(request, 'dashboard/booking_create_view.html', context)

@admin_required
def confirm_booking(request):
    context ={}
    id = request.session['booking_id']
    # print("//////////////////////////////////////////////////////////////////////",id)
    if request.method == "POST":
           
        if(Booking.objects.filter(auto_id=id).exists):
            Booking.objects.filter(auto_id=id).update(is_Booking_confirmed =True)
            redirect_url = reverse('dashboard:booking_room')
            # print(redirect_url)
            response_data = {
                "title":"Confirm Booking",
                "status" : "true",
                "swal_text":"Booking Confirmed" ,
                "redirect_url":redirect_url,
                }
            return HttpResponse(json.dumps(response_data),content_type='application/javascript')

    else:        

        booking = get_object_or_404(Booking,auto_id = id)
        # print(booking)
        sub_total = booking.total_price-booking.total_extra_bed_price
        bkd_room_type = BookedRoomType.objects.filter(booking=booking)
        bookedroom= BookedRoom.objects.filter(booked_room_type__booking = booking)
        total_adults = 0
        total_childs = 0

        for item in bookedroom:
            total_adults +=item.adult
            total_childs +=item.child
        context.update({
        "booking": booking,
        "bkd_room_type" : bkd_room_type,
        "bookedroom" :bookedroom,
        "total_adults" :total_adults,
        "total_childs" :total_childs,
        "sub_total":sub_total,



        })
    # Booking.objects.filter(id=id,is_Booking_confirmed =False).delete()
    context.update({
        "title": "confirm-booking",
        "page_name":"booking_room",
    })  
    return render(request, 'dashboard/confirm_booking.html', context)


@admin_required
def create_customer_ajax(request):
    if request.method == "POST":
        account_form = CustomAccountForm(request.POST)
        if(account_form.is_valid()):
            form_data = account_form.save(commit=False)
            username = form_data.username

            print(username)
            if(Account.objects.filter(username=username).exists()):
                print("exists")

                response_data = {
                    "status" : "false",
                    }
                return HttpResponse(json.dumps(response_data),content_type='application/javascript')

            form_data.save()
            response_data = {
                "status" : "true",
                "click_class":".modal .close"
            }
            return HttpResponse(json.dumps(response_data),content_type='application/javascript')
        else:
            response_data = {
                "status" : "true",
                "swal_icon" : "warning",
                "swal_title" : "Validation error",
                "swal_text" : "somthing went wrong !",
            }
            return HttpResponse(json.dumps(response_data),content_type='application/javascript')
    else:
        return render(request, 'error_404.html', {})

@admin_required
def update_room(request,id):
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Room, id = id)
    # print(obj)

    form = RoomForm(instance = obj)
    if request.method == "POST":
        form = RoomForm(request.POST,request.FILES,instance = obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard:room_list_view')
    context = {
        "title": "Update Room details",
        "form": form,
        "page_name" : obj.title,
        "instance" : obj,
         "page_name":"room_types",

    }  
    return render(request, 'dashboard/room_update_view.html', context)

@admin_required
def room_list_view(request):
    rooms = Room.objects.all()
    context = {
        'title':"Room list ",
        'rooms':rooms,
        "page_name":"room_types",
    }  
    return render(request, 'dashboard/room_list_view.html', context)


class account_autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Account.objects.filter()     
            if self.q:
                qs = qs.filter(username__icontains=self.q)
        else:
            qs = ""
        return qs


def date_range(start,end):
    sdate = start   # start date
    edate = end   # end date
    date_modified=sdate
    list=[sdate] 
    while date_modified<edate:
        date_modified+=timedelta(days=1) 
        list.append(date_modified)

    return list

def check_room_availabilty(request):
    checkin = request.GET.get('checkin')
    checkout =request.GET.get('checkout')

    date_format = "%Y-%m-%d"

    checkin_date = datetime.strptime(checkin, date_format)
    checkout_date = datetime.strptime(checkout, date_format)
    rooms = Room.objects.all()

    data = []

    for room in rooms:

        available_rooms = get_room_availabilty(room,checkin,checkout)
        total_price = float(get_room_total_price_with_offer(room,checkin_date,checkout_date))
        row = {
            "room_type":room.pk,
            "room_type_title":room.title,
            "available_rooms":available_rooms,
            "price":total_price,
        }

        data.append(row)

        # data = json.dumps(data)
    # print(data)
    if available_rooms>0:
        response_data = {
            "status" : "true",
            "rooms" : data
        }
    else:
        response_data = {
            "status" : "false",
        }
    # print(response_data)    
    return HttpResponse(json.dumps(response_data),content_type='application/javascript')


def get_extra_bed(request):
    if request.method == "GET":
        room = request.GET.get('room')
        adult =int(request.GET.get('adult'))
        child =int(request.GET.get('child'))
        room = Room.objects.get(pk=room)
        # print("///////////",room,adult,child)
        extra_adults = adult - room.adult
        if extra_adults>0:
            pass
        else:
            extra_adults=0

        extra_childs = child - room.child
        if extra_childs>0:
            pass
        else:
            extra_childs=0
        extra_bed = extra_adults + int(extra_childs/2)
        if(extra_bed>0 and extra_bed<6):
            response_data = {
                "status" :"true",
                "extra_bed":extra_bed
            }
        elif(extra_bed>5):
               response_data = {
                "status" :"true",
                "extra_bed":5
            }
        else:
               response_data = {
                "status" :"true",
                "extra_bed":0,
            }

    else:
        response_data = {
            "status" :"false",
        }
    return HttpResponse(json.dumps(response_data),content_type='application/javascript')


def get_extra_bed_price(room,adult,child):
    room = Room.objects.get(pk=room)
    extra_adults = adult - room.adult
    extra_childs = child - room.child
    total_persons = extra_adults + int(extra_childs/2)
    # print("total_persons")
    # print(total_persons)
    
    total_extra_bed_price=0
    if(total_persons>0):
        total_extra_bed_price = total_persons * room.extra_bed_price
    # print( " total bed price",total_extra_bed_price)
    return total_extra_bed_price

def get_room_total_price_with_offer(room,checkin,checkout):
    checkout = checkout 
    dates_list=date_range(checkin,checkout)
    price = 0
    for date in dates_list:
        if(Offer.objects.filter(room_type=room.pk,date=date).exists()):
            offer = Offer.objects.filter(room_type=room.pk,date=date).first()
            offer_price = offer.offer_price
            price += offer_price
        else:
            price += room.new_price
    return price

def get_room_total_price(room,checkin,checkout):
    checkout = checkout
    dates_list=date_range(checkin,checkout)
    price = 0
    for date in dates_list:
            price += room.new_price
    return price





def get_room_availabilty(room,checkin,checkout):

    check_in=datetime.strptime(checkin, "%Y-%m-%d").date()
    check_out=datetime.strptime(checkout, "%Y-%m-%d").date()

    dates_list=date_range(check_in,check_out)

    total_rooms = Room.objects.get(pk=room.pk).no_of_rooms

    total_rooms=int(total_rooms)
    booked_rooms = BookedRoomType.objects.filter(room=room.pk,booking__is_Booking_confirmed=True)
    # print(booked_rooms)
    temp_list=[]
    for item in booked_rooms:
        item_dates_list=date_range(item.booking.checkin_date,item.booking.checkout_date)
        r = list(set(dates_list) & set(item_dates_list))
        if(len(r) > 0 ):
            for i in r:
                row = {
                    str(i):int(item.reserved_rooms),
                }
                temp_list.append(row)

    number_list =[]
    for x in dates_list:
        z = 0
        for y in temp_list:
            # z = z+ int(y[str(x)])
            # print(str(x))
            val = y.get(str(x))
            if(val):
                z += val
        number_list.append(z)
    
        # print(x,z)
            
    m = max(number_list)
    # print("available rooms : ")
    # print(total_rooms-m)
    available_rooms = total_rooms-m
    return available_rooms


def get_rooms_status(startdate,enddate):

    # check_in=datetime.strptime(str(checkin), "%Y-%m-%d").date()
    # check_out=datetime.strptime(str(checkout), "%Y-%m-%d").date()
    booking_status_obj = {}

    dates_list=date_range(startdate,enddate)
    for item in dates_list:
        booking_status_obj[str(item)]={}
    rooms = Room.objects.all()
    for room in rooms:
        total_rooms = room.no_of_rooms
        total_rooms=int(total_rooms)
        booked_rooms = BookedRoomType.objects.filter(room=room.pk,booking__is_Booking_confirmed=True)
        temp_list=[]
        for item in booked_rooms:
            item_dates_list=date_range(item.booking.checkin_date,item.booking.checkout_date)
            r = list(set(dates_list) & set(item_dates_list))
            if(len(r) > 0 ):
                for i in r:
                    row = {
                        str(i):int(item.reserved_rooms),
                    }
                    temp_list.append(row)

        number_list =[]
        for x in dates_list:
            z = 0
            for y in temp_list:
                val = y.get(str(x))
                if(val):
                    z += val
            row = {
                "total_rooms": total_rooms,
                "filled_rooms": z,

                "free_rooms": total_rooms-z
            }
            booking_status_obj[str(x)][room.title] = row

            number_list.append(z)
    # print(booking_status_obj)
    
    return booking_status_obj

class BookingListView(LoginRequiredMixin,ListView):
    model = Booking
    context_object_name = 'bookings'
    template_name = 'dashboard/booking_list_view.html'
    extra_context={'page_name': 'booking_listview',
    "title":"Booking List"}
    paginate_by = 20

    def get_queryset(self):
        # bookings = get_object_or_404(Booking,is_Booking_confirmed=True)
        bookings = Booking.objects.filter(is_Booking_confirmed=True)
        return bookings.order_by('-auto_id')

    @method_decorator(admin_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class OnlineBookingListView(LoginRequiredMixin,ListView):
    model = Booking
    context_object_name = 'bookings'
    template_name = 'dashboard/online_booking_list_view.html'
    extra_context={'page_name': 'online_booking_listview',
    "title":"Online Booking List"}
    paginate_by = 20

    def get_queryset(self):
        # bookings = get_object_or_404(Booking,is_Booking_confirmed=True)
        bookings = Booking.objects.filter(is_Booking_confirmed=True,payment_type="Online")
        return bookings.order_by('-auto_id')

    @method_decorator(admin_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
 

class RoomOfferCreateView(LoginRequiredMixin,CreateView):
    template_name = 'dashboard/offer_create_view.html'
    context_object_name = 'form'
    form_class = OfferForm
    success_url='offer-list-view'
    extra_context={"page_name": 'room_offer',
                    "title":"Add Room Offer"}

    @method_decorator(admin_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
 

class OfferListView(LoginRequiredMixin,ListView):
    model = Offer
    context_object_name = 'offers'
    template_name = 'dashboard/offer_list_view.html'
    extra_context={"page_name": 'offer_list_view',
                    "title":"Offer List"}
    ordering = ['-id']
    @method_decorator(admin_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
 

@admin_required
def delete_offer(request,id):
    context ={}
    if request.method == "POST":
        obj = get_object_or_404(Offer, id = id)
        obj.delete()
        # print(obj)
        return redirect('dashboard:offer_list_view')
    # return render(request, 'dashboard/confirm_delete_offer.html', context)




@admin_required
def update_offer(request,id):
    context ={}

    obj = get_object_or_404(Offer, id = id)

    form = OfferForm(instance = obj)
    if request.method == "POST":
        form = OfferForm(request.POST,instance = obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard:offer_list_view')
    context = {
        "title": "Update Offer",
        "form": form,
        "page_name" : obj.title,
        "instance" : obj,
         "page_name":"update offer",

    }  
    return render(request, 'dashboard/offer_update_view.html', context)


@admin_required
def delete_room(request,id):
    context ={}
    if request.method == "POST":
        obj = get_object_or_404(Room, id = id)
        obj.delete()
        return redirect('dashboard:room_list_view')


@admin_required
def account_detail_view(request,id):
    context ={}
    obj = get_object_or_404(Account, id = id)
    context = {
        "instance": obj
    }
    return render(request, 'dashboard/account_detail_view.html', context)
    # return render(request, '403.html' )

@admin_required
def booking_invoice(request,id):

    context ={}
    booking = get_object_or_404(Booking, id = id)
    sub_total = booking.total_price-booking.total_extra_bed_price
    bkd_room_type = BookedRoomType.objects.filter(booking=booking)
    bookedroom= BookedRoom.objects.filter(booked_room_type__booking = booking)
    total_adults = 0
    total_childs = 0
    for item in bookedroom:
        total_adults +=item.adult
        total_childs +=item.child
    context.update({
    "booking": booking,
    "bkd_room_type" : bkd_room_type,
    "bookedroom" :bookedroom,
    "total_adults" :total_adults,
    "total_childs" :total_childs,
    "sub_total":sub_total
        })
    context.update({
        "title": "invoice",
        "page_name":"invoice",
    })  
    return render(request, 'dashboard/invoice.html', context)

def get_max_guests(request):
    if request.method == "GET":
        room = request.GET.get('room')
        room = Room.objects.get(pk=room)
        response_data = {
                "status" :"true",
                "max_adult":room.max_adult,
                "max_child":room.max_child,
            }
    else:
        response_data = {
            "status" :"false",
        }
    return HttpResponse(json.dumps(response_data),content_type='application/javascript')

def notifications_ajax(request):
    qs = Notification.objects.filter(is_readed = False)

    data = []
    booking = Booking.objects.filter(notification__in = qs)
    # print(booking)
    for item in booking:
        td =datetime.now(pytz.utc) - item.booking_date
        days, hours, minutes = td.days, td.seconds // 3600, td.seconds // 60 % 60
        if days>0:
            time_txt= "{} days, {} hours ,{} minutes ago".format(days, hours, minutes)
        elif hours>0:
            time_txt= " {} hours ,{} minutes ago".format( hours, minutes)
        else:
            time_txt= "{} minutes ago".format(minutes)

        row={
            "txt" : "New Online Booking , <br/> Checkin date :"+ str(item.checkin_date),
            "delta" : time_txt ,
        }
        data.append(row)
        
    response_data = {
        "status" : "True",
        "list": data       
          }
    return HttpResponse(json.dumps(response_data),content_type='application/javascript')


def mark_as_read_notifi_ajax(request):
    Notification.objects.update(is_readed = True)
    # print("inside the function")
    qs = Notification.objects.filter(is_readed = False)
    response_data={
        "status" :"True"
    }
    return HttpResponse(json.dumps(response_data),content_type='application/javascript')
