from django import forms
from .models import *
from dal import autocomplete
from django.forms.widgets import TextInput, Textarea,FileInput,NumberInput,DateInput,Select


class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = ['title','price','new_price','max_adult','max_child','description','status','image','adult','child','no_of_rooms','extra_bed_price']
		widgets= {
			'title' : TextInput(attrs={'class': 'required form-control',}),						
			'price' : TextInput(attrs={'class': 'required form-control',}),			
			'new_price' : TextInput(attrs={'class': 'required form-control',}),					
			'max_adult' : NumberInput(attrs={'class': 'required form-control',}),			
			'max_child' : NumberInput(attrs={'class': 'required form-control',}),			
			'status' : TextInput(attrs={'class': 'required form-control',}),
			'image' : FileInput(attrs={'class': 'required form-control',}),	
			'description' : TextInput(attrs={'class': 'required form-control',}),
			'adult' : NumberInput(attrs={'class': 'required form-control',}),			
			'child' : NumberInput(attrs={'class': 'required form-control',}),
			'no_of_rooms' : NumberInput(attrs={'class': 'required form-control',}),	
			'extra_bed_price' : TextInput(attrs={'class': 'required form-control',}),					


		}

class OfferForm(forms.ModelForm):
	class Meta:
		model = Offer
		fields = ['title','room_type','offer_price','date']
		widgets= {
			'title' : TextInput(attrs={'class': 'required form-control',}),			
			'room_type' : Select(attrs={'class': 'required form-control',}),			
			'offer_price' : TextInput(attrs={'class': 'required form-control',}),			
			'date' : DateInput(attrs={'class': 'required form-control','type':'date'}),		
		}	

class BookingForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ['account','checkin_date','checkout_date','booking_date','payment_type']
		widgets= {
			'account' :autocomplete.ModelSelect2(url='dashboard:account_autocomplete', attrs={'data-placeholder':'Select Customer','class':'form-control'},),		
			'checkin_date' : DateInput(attrs={'class': 'required form-control','type':'date'}),				
			'checkout_date' : DateInput(attrs={'class': 'required form-control','type':'date'}),	
			'payment_type' : TextInput(attrs={'class': 'required form-control'},),
		}	
# class RoomNumForm(forms.ModelForm):
# 	class Meta:
# 		model = Room_num
# 		fields = ['room_no','room_type']
# 		widgets= {
# 			'room_no' : TextInput(attrs={'class': 'required form-control',}),	
# 			'room_type' : Select(attrs={'class': 'required form-control',}),								
# 		}


class CustomAccountForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ('email', 'username','address','phone','first_name','last_name')
		widgets= {
			'username' : forms.TextInput(attrs={'class': 'required form-control',}),
			'first_name' : forms.TextInput(attrs={'class': 'required form-control',}),
			'last_name' : forms.TextInput(attrs={'class': 'required form-control',}),
			'address' : forms.Textarea(attrs={'class': 'required form-control',}),
			'email' : forms.NumberInput(attrs={'class': 'required form-control','type' : 'email'}),
			'phone' : forms.NumberInput(attrs={'class': 'required form-control','type' : 'tel','maxlength' : '10'}),
		}
		
class BookedRoomTypeForm(forms.ModelForm):
	class Meta:
		model = BookedRoomType
		fields = ['room']
		widgets= {
			'room': Select( attrs={'data-placeholder':'Select Customer','class':'form-control'},),
		}


class BookedRoomForm(forms.ModelForm):
	class Meta:
		model = BookedRoom
		fields = ['room','adult','child','extra_bed']
		widgets= {
			'room': Select( attrs={'data-placeholder':'Select Customer','class':'form-control selDiv room_input'},),
			'adult' : NumberInput(attrs={'class': 'required adult_input form-control','min':0, 'max':5,'value':0}),
			'child' : NumberInput(attrs={'class': 'required child_input form-control','min':0, 'max':5,'value':0}),
			'extra_bed' : TextInput(attrs={'class': 'required extrabed_input form-control','min':0, 'max':5}),
		}
		
