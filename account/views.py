from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
# from main.functions import get_pk_id,sendSMS
from .models import *
from random import randint
from django.core import mail
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http.response import HttpResponse
import json


def registration_view(request):
	context = {}
	user = request.user
	if user.is_authenticated: 
		logout(request)

	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			print("vali ///")
			data = form.save(commit=False)
			otp = str(randint(100000, 999999))
			request.session['first_name'] = data.first_name
			request.session['last_name'] = data.last_name
			request.session['email'] = data.email
			request.session['password1'] = form.cleaned_data.get('password1')
			request.session['password2'] = form.cleaned_data.get('password2')
			request.session['address'] = data.address
			request.session['phone'] = data.phone
			request.session['username'] = data.username
			request.session['otp'] = otp
			email = data.email
			name =  data.first_name + " " + data.last_name
			
			try:
				from_email = "deluxinn.in <ecolumsmarketing@gmail.com>"
				subject = "Your OTP is:" + otp
				text_content = "Yourn OTP is:" + otp
				try:
					msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
					msg.attach_alternative(text_content, "text/html")
					msg.send()
					return redirect('account:phone_otp')
				except:
					pass
			except:
				pass

		else:
			context['registration_form'] = form
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'dashboard/account/register.html', context)



def phone_otp(request):
	email = str(request.session['email'])
	context = {
		"email" : email
		}
	if request.POST:
		real_otp = str(request.session['otp'])
		otp = request.POST['otp']

		updated_request = request.POST.copy()
		updated_request.update({
			'first_name': request.session['first_name'],
			'last_name': request.session['last_name'],
			'email': request.session['email'],
			'address': request.session['address'],
			'phone': request.session['phone'],
			'password1': request.session['password1'],
			'password2': request.session['password2'],
			'username': request.session['username'],
			})
		form =  RegistrationForm(updated_request)
		if (otp == real_otp) and form.is_valid():
			form.save()
			username = updated_request['username']
			password = updated_request['password1']
			user = authenticate(username=username, password=password)
			login(request, user)

			return redirect("web:index")

	return render(request, "dashboard/account/phone_otp.html",context)

def logout_view(request):
	logout(request)
	return redirect('/')


def login_view(request):
	context = {}
	user = request.user
	if user.is_authenticated: 
		logout(request)
	if request.POST:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				if user.is_admin:
					return redirect("dashboard:index")
				else:
					return redirect("web:index")
	else:
		form = AccountAuthenticationForm()
	context['login_form'] = form
	return render(request, "dashboard/account/login.html", context)


def forgot_password(request):
	context = {}
	user = request.user
	if user.is_authenticated: 
		logout(request)
	if request.POST:
		try:
			request.session['otp_count'] = 5
			email = request.POST['email']
			request.session['email'] = email
			if Account.objects.filter(email=email).exists():
				otp = str(randint(100000, 999999))
				request.session['otp'] = otp
				message = 'your otp is : ' + otp + ','
				try:
					from_email = "deluxinn.in <ecolumsmarketing@gmail.com>"
					subject = "Your OTP is:" + otp
					text_content = "Your OTP is:" + otp

					try:
						msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
						msg.attach_alternative(text_content, "text/html")

						msg.send()
						print("mail sent")
					except:
						pass
				except:
					pass
				
				account = Account.objects.filter(email=email).first()
				request.session.set_expiry(600)
				request.session['account'] = account.pk
				return redirect("account:forgot_password_otp")
			else:
				messages.info(request, 'This email is not registerd')
				return redirect("account:forgot_password")
		except:
			messages.info(request, 'Your Session has time out. please try again')
			return redirect("account:forgot_password")
	return render(request, 'dashboard/account/forgot-password.html', context)


def forgot_password_otp(request):
	email = request.session['email']
	context = {"email":email}
	user = request.user
	if user.is_authenticated: 
		logout(request)
	if request.POST:
		try:
			input_otp = request.POST['otp']
			otp = request.session['otp']
			if input_otp == otp:
				if request.session['otp_count'] < 0:
					del request.session['account']
					del request.session['otp']
					messages.info(request, 'Too many attempts,Please Try again later')
					return redirect("account:forgot_password")
					
				account = request.session['account']	
				user = Account.objects.get(pk=account)			
				login(request, user)
				return redirect("account:forgot_password_new_password")
			else:
				otp_count = request.session['otp_count']
				request.session['otp_count'] = otp_count - 1
				messages.info(request, 'Incorrect OTP')
				if request.session['otp_count'] <= 0:
					del request.session['account']
					del request.session['otp']
					messages.info(request, 'Too many attempts,Please Try again later')
					return redirect("account:forgot_password")
		except:
			messages.info(request, 'Too many attempts,Please Try again later')
			return redirect("account:forgot_password")
	
	return render(request, 'dashboard/account/forgot_password_otp.html', context)

def forgot_password_new_password(request):
	context = {}
	user = request.user
	if request.POST:
		password = request.POST['password']
		try:
			account_pk = request.session["account"]
			account = Account.objects.get(pk = account_pk)
			account.set_password(password)
			account.save()
			login(request, account)
			return redirect("web:index")
		except:
			messages.info(request, 'Your Session has time out. please try again ')
			return redirect("account:forgot_password")
	return render(request, 'dashboard/account/forgot_password_new_password.html', context)



def account_view(request):
	if not request.user.is_authenticated:
			return redirect("login")
	context = {}
	return render(request, "account/account.html", context)

def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})



def reset_password(request):
	context = {}
	user = request.user
	if user.is_authenticated: 
		if request.POST:
			old_password = request.POST['old_password']
			new_password = request.POST['new_password']
			print(old_password)
			print(new_password)

			if(user.check_password(old_password)):
				print("psswrd checked !!")
				account = Account.objects.get(pk=user.pk)
				print(account)
				account.set_password(new_password)
				account.save()
				logout(request)
				return redirect('/')
			else:
				messages.info(request, 'Incorrect password !')
				return render(request, 'dashboard/account/reset-password.html', context)

		else:	
			return render(request, 'dashboard/account/reset-password.html', context)

	return redirect('/')

def check_username(request):
	user = request.user
	q = request.GET.get('q')
	if(Account.objects.filter(username=q).exists()):
		response_data = {
			"status" : "false",
		}
	else:
		response_data = {
			"status" : "true",
		}
	return HttpResponse(json.dumps(response_data),content_type='application/javascript')



def check_email(request):
	user = request.user
 
	q = request.GET.get('q')
	if(Account.objects.filter(email=q).exists()):
		response_data = {
			"status" : "false",
		}
	else:
		response_data = {
			"status" : "true",
		}
	return HttpResponse(json.dumps(response_data),content_type='application/javascript')

