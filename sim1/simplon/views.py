from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from supervisor.models import Utilisateur
from supervisor.modeles import *
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from supervisor.tokens import generateToken
from django.contrib.auth.hashers import make_password
import random
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required



# Create your views here.


def base(request):
    return render(request,'simplon/index.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = Utilisateur.objects.get(username=username)
        if user:
            login(request,user)
            if my_user.role == "vendeur":
                return redirect('vente_stats')
            elif my_user.role == "gestionnaire":
                return redirect('stats')
            elif my_user.role =="superviseur":
                return redirect('dashboard')

            return render(request, 'simplon/login.html')
        
            

        elif my_user.is_active == False:
            messages =  'compte inactif'
            return render(request,'simplon/login.html', {'messages':messages})
        else:
            messages = 'Username ou mot de passe incorret'
            return render(request,'simplon/login.html',{'messages':messages})

    return render(request , 'simplon/login.html', {'messages':''})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        my_user = Utilisateur.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and generateToken.check_token(my_user, token):
        my_user.is_active  = True        
        my_user.save()
        messages.add_message(request,messages.SUCCESS, "activé votre compte en cliquant sur le lien suivant")
        return render(request,"simplon/login.html",{'messages':messages.get_messages(request)})
    else:
        messages.add_message(request,messages.ERROR, 'echec d\' activation veuillez réessayer')
        return render(request,'simplon/login.html',{'messages':messages.get_messages(request)})


def recup(request):
    numero = list('123456789')
    code = ''
    for i in range(5):
        code += random.choice(numero)
    print(code)
    if  request.method == 'POST':
        mail = request.POST['email']
        if SupervisorUtilisateur.objects.filter(email = mail):   
            utilisateur =  SupervisorUtilisateur.objects.get(email = mail)
            if MotPerdu.objects.filter(code = code):
             code = ""
             for i in range(5):
                code += random.choice(numero)
            if MotPerdu.objects.filter(id_user = utilisateur.id): 
                Mot = MotPerdu.objects.get(id_user = utilisateur.id)
                Mot.code = code  
                subject = "Code de confirmation"
                message = "Votre code de confirmation est le suivant "+ str(code)
                from_email = settings.EMAIL_HOST_USER
                to_list = [utilisateur.email]
                send_mail(subject, message, from_email, to_list, fail_silently=False)
                Mot.save()
                return redirect('verif_shap')
            else:                   
                    mot =  MotPerdu.objects.create(id_user = utilisateur, code = code) 
                    subject = "Code de confirmation"
                    message = "Votre code de confirmation est le suivant "+ str(code)
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [utilisateur.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=False)
                    mot.save()
                    return redirect('verif_shap')
        else:
            message = 'Email incorrect'
            return render(request,'simplon/recuperation.html',{'sms':message})
    return render(request,'simplon/recuperation.html')

def verif_shap(request):
    if request.method == 'POST':
        code = request.POST['code']
        if MotPerdu.objects.filter(code = code):
            Mot = MotPerdu.objects.get(code = code)
            utilisateur =  SupervisorUtilisateur.objects.get(id = Mot.id_user.id)
            numero = list('123456789CAMSO')
            code = ''

            for i in range(7):
              code += random.choice(numero)

            hash_password = make_password(code)
            utilisateur.password = hash_password
            utilisateur.save()
            subject = "Felicitation"
            message = "Votre mot de pass a bien été modifier"+ '\n'+ "Votre nouveau mot de pass est le suivant: "+  str(code)
            from_email = settings.EMAIL_HOST_USER
            to_list = [utilisateur.email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            sms = 'Votre mot de pass a bien été changer verifier votre mail'
            return render(request,'simplon/verification_recup.html', {'sms':sms})
        else:
            message = 'mot de pass incorret'
            return render(request,'simplon/verfication_recup.html', {'sms':sms})
    return render(request,'simplon/verification_recup.html')   






   