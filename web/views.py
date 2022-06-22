from datetime import time,date, timedelta 
from datetime import datetime

from django.shortcuts import render,get_object_or_404
from .forms import BookingForm,BookedRoomForm
from .forms import CustomAccountForm
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from dashboard.views import get_room_total_price,get_room_total_price_with_offer,get_room_availabilty
from dashboard.models import Notification, Room,BookedRoomType,Booking,BookedRoom,Offer
from account.models import Account
from main.functions import get_auto_id
import json
from django.http.response import HttpResponse
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

#payment imports
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import hashlib
import hmac
import threading

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
razorpay_client.set_app_details({"title" : "DeluxeInn", "version" : "1.0"})


def index(request):   
    BookedRoomFormSet = formset_factory(BookedRoomForm,extra=1)
    rooms = Room.objects.all()
    form = BookingForm()
    booked_room_formset = BookedRoomFormSet(prefix="booked_room_formset")
    for room in rooms:
        if(Offer.objects.filter(room_type=room.pk,date=date.today()).exists()):
            offer = Offer.objects.filter(room_type=room.pk,date=date.today()).first()
            room.offer_price = offer.offer_price
            room.offer_name = offer.title

    context = {
        "title": "DeluxInn",
        "form": form,
        "booked_room_formset":booked_room_formset,
        "rooms":rooms,
    }
    return render(request, 'web/index.html', context)


def order_summary(request):
    context={}

    custform = CustomAccountForm()
    if request.method == "POST":
        account = Account.objects.get(id=1)
        BookedRoomFormSet = formset_factory(BookedRoomForm,extra=1)
        form = BookingForm(request.POST)
        booked_room_formset = BookedRoomFormSet(request.POST,prefix="booked_room_formset")
        if (form.is_valid()):
            form_data = form.save(commit=False)
            form_data.total_price = 0
            form_data.total_offer_price = 0
            form_data.total_extra_bed_price =int(0)
            form_data.account = account
            date_format = "%Y-%m-%d"
            # print("//////////////",form_data.checkin_date)
            a = datetime.strptime(str(form_data.checkin_date), date_format)
            b = datetime.strptime(str(form_data.checkout_date), date_format)
            form_data.checkout_date_display= form_data.checkout_date
            form_data.checkout_date = form_data.checkout_date-timedelta(1)
            delta = b - a
            total_days= delta.days
            request.session['total_days'] = total_days
            if(total_days>0):
                if (booked_room_formset.is_valid()):
                    form_data.auto_id = get_auto_id(Booking)
                    form_data.save() 
                    rooms = Room.objects.all()
                    extra_beds=0
                    for room in rooms:
                        price = get_room_total_price(room,form_data.checkin_date,form_data.checkout_date)
                        offer_price = get_room_total_price_with_offer(room,form_data.checkin_date,form_data.checkout_date)

                        # print("price:",price)
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
                        f_data.extra_bed = get_extra_bed(f_data.room.pk,f_data.adult,f_data.child)
                        extra_beds +=f_data.extra_bed
                        extra_bed_price = f_data.extra_bed * f_data.room.extra_bed_price * total_days 
                        bkd_room_type = BookedRoomType.objects.get(booking=form_data,room=f_data.room)
                        room_price = bkd_room_type.price
                        room_offer_price = bkd_room_type.offer_price

                        bkd_room_type.reserved_rooms = int(bkd_room_type.reserved_rooms) + int(1)
                        # bkd_room_type.total_price = int(bkd_room_type.total_price) + int(1000)
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
                        
                        f_data.save()

                    BookedRoomType.objects.filter(total_price = 0).delete()
                    form_data.save()
                    request.session['booking_id'] = str(form_data.id)

                    booking = get_object_or_404(Booking, id = form_data.id)

                    sub_total = booking.total_price-booking.total_extra_bed_price
                    bkd_room_type = BookedRoomType.objects.filter(booking=booking)
                    bookedroom= BookedRoom.objects.filter(booked_room_type__booking = booking)
                    total_adults = 0
                    total_childs = 0
                    for item in bookedroom:
                        total_adults +=item.adult
                        total_childs +=item.child

                    request.session['extra_beds'] = extra_beds
                    request.session['total_adults'] =total_adults
                    request.session['total_childs'] =total_childs
                    context.update({
                    "booking": booking,
                    "bkd_room_type" : bkd_room_type,
                    "bookedroom" :bookedroom,
                    "total_adults" :total_adults,
                    "total_childs" :total_childs,
                    "sub_total":sub_total,
                    "custform":custform,
                    "extra_beds":extra_beds
                    })


                    if booking.total_price > booking.total_offer_price:
                        amount = int(booking.total_offer_price)*100
                    else:
                        amount = int(booking.total_price)*100

                      # Rs. 200
                    currency = "INR"
                    # Create a Razorpay Order
                    data = { "amount": amount, "currency":currency, 'payment_capture': '1' }
                    razorpay_order = razorpay_client.order.create(data=data)

                    # order id of newly created order.
                    razorpay_order_id = razorpay_order['id']
                    callback_url = 'paymenthandler/'
                    Booking.objects.filter(id=form_data.id).update(order_id=razorpay_order_id)

                    # # we need to pass these details to frontend.
                    # context = {}
                    context['razorpay_order_id'] = razorpay_order_id
                    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                    context['razorpay_amount'] = amount
                    context['currency'] = currency
                    context['callback_url'] = callback_url

                    # print(razorpay_order_id)

        else:
            return render(request,'error_404.html')
 
        return render(request, 'web/order_summary.html', context)
    return render(request,'error_404.html') 

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            razorpay_signature = request.POST.get('razorpay_signature', '')
            # print(request.POST)

            booking_id = request.session['booking_id']
            booking = Booking.objects.filter(id=booking_id).first()
            # booking = get_object_or_404(Booking, id = booking_id)
            # order = razorpay_client.order.payments(razorpay_order_id)
            # print(order)
            #verify payment signature
            order_id = booking.order_id
            str = order_id + "|" + payment_id  
            generated_signature = hmac.new(bytes(settings.RAZOR_KEY_SECRET , 'latin-1'),
                                            msg = bytes(str , 'latin-1'), 
                                            digestmod = hashlib.sha256).hexdigest()

            if generated_signature == razorpay_signature:
                params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': razorpay_signature
                }
                razorpay_client.utility.verify_payment_signature(params_dict)
                
                account = create_account_model(request)

                Booking.objects.filter(id=booking_id).update(account=account,
                                                            payment_type ="Online",
                                                            is_Booking_confirmed =True)
                context = {
                    "booking":booking 
                }

                booking = Booking.objects.filter(id=booking_id).first()
                # print(booking.account.email)
                # send_booking_mail(request,booking)
                t1 = threading.Thread(target=send_booking_mail, args=(request,booking))
                # t2 = threading.Thread(target=print_cube, args=(10,))
                Notification.objects.create(booking=booking)
                t1.start()

                return render(request, 'web/booking_confirmed.html',context)


            else:
                pass
                # print("///////////////////////NOT SUCCESSFULL?????????????????/////////////////")
        except Exception as e:
            print(e)
            return render(request,'payment_fail.html')

            #  = razorpay_client.order.fetch(razorpay_order_id)
            
            # print("///////results:",result)
    


def term_and_conditions(request):   
    context= {}
    return render(request, 'web/term_and_conditions.html', context)

def privacy_policy(request):   
    context= {}
    return render(request, 'web/privacy_policy.html', context)

def cancellation_policy(request):   
    context= {}
    return render(request, 'web/cancellation_policy.html', context)

def send_booking_mail(request,booking):
                # print("////////////////", booking.account.email)
    bkd_room_type = BookedRoomType.objects.filter(booking=booking)
    extra_beds = request.session['extra_beds']
    total_days = request.session['total_days']
    # total_adults = request.session['total_adults']
    # total_childs = request.session['total_childs'] 
    user_email = booking.account.email
    from_email = "Deluxe Inn Chennai <deluxeinchennai@gmail.com>"

    subject = "Booking Confirmed !"
    text_content = ""
    html_context = {
        "name" : booking.account.first_name + " " + booking.account.last_name,
        "booking":booking,
        "bkd_room_type":bkd_room_type,
        "extra_beds":extra_beds,
        "total_days":total_days
    }
    html_content = render_to_string('email/booking_email.html', html_context)
    # try:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [user_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print("Email send successfully")
    # except Exception as e:
    #     print(e)
    # pass


def create_account_model(request):
    
    last_user = Account.objects.all().last()
    username =  "guest_user____" + str(last_user.id)
    account=Account.objects.create(
        email = request.session['email'],
        username =  username,
        first_name = request.session['first_name'],
        last_name = request.session['last_name'],
        phone = request.session['phone'],
        address = request.session['address'],
        )
    return account


def create_user_data_ajax(request):
    request.session['first_name'] = request.POST.get('first_name')
    request.session['last_name'] = request.POST.get('last_name')
    request.session['email'] = request.POST.get('email')
    request.session['phone'] = request.POST.get('phone')
    request.session['address'] = request.POST.get('address')

    response_data = {
        "status" : "true",
    }  
    return HttpResponse(json.dumps(response_data),content_type='application/javascript')



def get_extra_bed(room,adult,child):
    # print(room,adult,child)
    room = Room.objects.get(pk=room)
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
    if(extra_bed>-1):
        return extra_bed
    else:
        return 0


def check_room_availabilty_web(request):
    checkin = request.GET.get('checkin')
    checkout =request.GET.get('checkout')
    room = request.GET.get('room')
    date_format = "%Y-%m-%d"

    checkin_date = datetime.strptime(checkin, date_format)
    checkout_date = datetime.strptime(checkout, date_format)
    rooms = Room.objects.get(id=room)

    available_rooms = get_room_availabilty(rooms,checkin,checkout)
    if available_rooms>0:
         response_data = {
        "status" : "True",
         }
    else:
         response_data = {
        "status" : "False",
    }  
    return HttpResponse(json.dumps(response_data),content_type='application/javascript')


# def notifications_ajax(request):
#     request.get()

#     qs = Notification.objects.filter(is_readed = False)
#     lst = []
#     for bookings in qs:
#         txt="New Online Booking Id: " + bookings.auto_id
#         lst.append(txt)
#     # print(qs.booking)
#     # new_bookings = Booking.objects.filter(booking = qs.booking)
#     # qs = Notification.objects.filter(booking__in=Booking.objects.filter(is_readed = False))
#     # qs= Booking.objects.filter(booking__in=Notification.objects.filter(is_readed=False))
#     response_data = {
#         "status" : "True",
#         "list":lst
#          }
#     return HttpResponse(json.dumps(response_data),content_type='application/javascript')

