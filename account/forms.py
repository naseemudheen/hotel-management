from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class':'form-control'},))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control pwstrength','data-indicator':'pwindicator'},))
	password2 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'},))

	class Meta:
		model = Account
		fields = ('email', 'username','address','phone','first_name','last_name')
		widgets= {
			'username' : forms.TextInput(attrs={'class': 'required form-control',}),
			'first_name' : forms.TextInput(attrs={'class': 'required form-control',}),
			'last_name' : forms.TextInput(attrs={'class': 'required form-control',}),
			'address' : forms.Textarea(attrs={'class': 'required form-control',}),
			'phone' : forms.NumberInput(attrs={'class': 'required form-control','type' : 'tel','maxlength' : '10'}),
			
		}
	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'required form-control',}))
	username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class':'form-control'},))
	class Meta:
		model = Account
		fields = ('username', 'password')

	def clean(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']
			if not authenticate(username=username, password=password):
				raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', 'username', )

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)
















