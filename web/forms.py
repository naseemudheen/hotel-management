from django import forms
from dashboard.models import Booking,BookedRoom
from account.models import Account

from django.forms.widgets import TextInput,NumberInput,DateInput,Select


class BookingForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ['checkin_date','checkout_date']
		widgets= {
			# 'account' :autocomplete.ModelSelect2(url='dashboard:account_autocomplete', attrs={'data-placeholder':'Select Customer','class':'form-control'},),		
			'checkin_date' : DateInput(attrs={'class': 'required form-control','type':'date'}),				
			'checkout_date' : DateInput(attrs={'class': 'required form-control','type':'date'}),	
			# 'payment_type' : TextInput(attrs={'class': 'required form-control'},),
		}	
class BookedRoomForm(forms.ModelForm):
	class Meta:
		model = BookedRoom
		fields = ['room','adult','child']
		widgets= {
			'room': Select( attrs={'data-placeholder':'Select Customer','class':'form-control selDiv room_input'},),
			# 'adult' : NumberInput(attrs={'class': 'required adult_input form-control','min':0, 'max':5,'value':0}),
			'adult' : Select(attrs={'class': 'required adult_input form-control',}),
			'child' : Select(attrs={'class': 'required child_input form-control',}),
			# 'extra_bed' : NumberInput(attrs={'class': 'required extrabed_input form-control','min':0, 'max':5}),
		}

class CustomAccountForm(forms.ModelForm):
	agreeterms = forms.BooleanField()
	class Meta:
		model = Account
		fields = ('first_name','last_name','email','address','phone')
		widgets= {
			'first_name' : forms.TextInput(attrs={'class': 'required form-control','placeholder':'First Name',}),
			'last_name' : forms.TextInput(attrs={'class': 'required form-control','placeholder':'Last Name',}),
			'address' : forms.Textarea(attrs={'class': 'required form-control','placeholder':'Address',}),
			'email' : forms.NumberInput(attrs={'class': 'required form-control','type' : 'email','placeholder':'Email',}),
			'phone' : forms.NumberInput(attrs={'class': 'required form-control','type' : 'tel','maxlength' : '10','placeholder':'Phone',}),
		}