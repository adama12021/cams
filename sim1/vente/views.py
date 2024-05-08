from django.shortcuts import render, redirect
from django.contrib.auth import logout
from supervisor.modeles import *
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from datetime import *
from django.db.models import *
import random
import os
import csv
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def vente_home(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    return render(request,'vente/home.html')

@login_required
def vente(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')

    
    today = datetime.now()
    vente = Vente.objects.prefetch_related('id_produit', 'id_client').filter(id_vendeur = (request.user).id,
                                                                             date_vente__year=today.year,
                                                                             date_vente__month=today.month,
                                                                             date_vente__day=today.day,
                                                                             annuler = False)
    return render(request, 'vente/vente.html', {'ventes':vente})


@login_required
def annule_vente(request, pk):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    if request.method == 'POST':
        motif = request.POST['motif']
        now = datetime.now()  
        formatted_date = now.strftime('%Y-%m-%d')
        
        vente_simple = Vente.objects.get(id_vente = pk)
        annule_ventes_analyse = VentesAnalyse.objects.get(id_ventes = vente_simple)
        produit_id  = vente_simple.id_produit 
        produit = Produit.objects.get(id_produit = produit_id.id_produit )
        produit.quantite += vente_simple.quantite_vendu
        stock = Stock.objects.get(id_produit_s = produit)
        stock.quantite_s += vente_simple.quantite_vendu
        produit.save()
        stock.save()
        vente_annuler = VenteAnuler(id_vente = vente_simple, date_annulation =formatted_date, motif_annulation = motif )
        vente_simple.annuler = True
        vente_simple.save()
        vente_annuler.save()
        annule_ventes_analyse.delete()
        return redirect('vente')
    return render(request, 'vente/annule_vente.html', {'pk':pk})


@login_required
def historique(request):
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    vente = ""
    Date = ""
    taille=0
    if request.method == 'POST':
        Date = request.POST['date']
        date = datetime.strptime(Date, "%Y-%m-%d").date()
        vente = Vente.objects.prefetch_related('id_produit', 'id_client').filter(id_vendeur = (request.user).id,
                                                                             date_vente__year=date.year,
                                                                             date_vente__month=date.month,
                                                                             date_vente__day=date.day)
        taille = len(vente)
    return render(request, 'vente/historique.html', {'ventes':vente, 'date':Date, 'taille':taille})

    


@login_required
def vente_ajout(request):

    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    produit = Produit.objects.filter(archiver = False)
    client = Client.objects.all()
    messages = ""
    

    if request.method == "POST":
        matricule = request.POST["client"]
        prod = request.POST['produit']
        nombre = request.POST['quantite']
        produits = Produit.objects.get(id_produit = prod)
        clients = Client.objects.get(id_client = matricule)
        stock = Stock.objects.get(id_produit_s = prod)
        if stock.quantite_s == 0:
            messages = 'le stock est vide .'
            return render(request,'vente/ajout_vente.html', {'message': messages, 'produit':produit, 'client':client}) 
        
        if stock.quantite_s - int(nombre) <0 :
            messages = 'Quantite de produit insuffisant.'
            return render(request,'vente/ajout_vente.html', {'message': messages, 'produit':produit, 'client':client}) 

        stock.quantite_s = stock.quantite_s - int(nombre)
        produits.quantite = produits.quantite - int(nombre)
        prix = produits.p_unitaire * int(nombre)
        vendeur = SupervisorUtilisateur.objects.get(id = (request.user).id)
        now = datetime.now()  
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        vente = Vente(id_client = clients, id_produit = produits, prix_total = prix, id_vendeur =vendeur, date_vente= formatted_date, quantite_vendu = nombre, annuler = False )
        vente.save()
        produits.save()
        stock.save()
        vente_analyse = VentesAnalyse(nom = clients.nom + ' ' + clients.prenom, prix = prix, produit = produits.nom_produit, type=produits.categorie, date = formatted_date, genre = clients.genre, id_ventes= vente, quantite = vente.quantite_vendu )
        vente_analyse.save()
        return redirect('vente')       
    return render(request, 'vente/ajout_vente.html',{'produit':produit, 'client':client})

@login_required
def details_vente(request, pk):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    vente = Vente.objects.get(id_vente = pk)
    return render(request, 'vente/detail_vente.html', {'details':vente})

@login_required
def client(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    clients = Client.objects.all()
    nom = ""
    prenom = ""
    adr = ""
    sexe = ""
    if request.method == "POST":
        nom =  request.POST['nom']
        prenom = request.POST['prenom']
        adr = request.POST['adr']
        sexe = request.POST['sex']

        print(nom)
        q_nom = Q(nom__icontains=nom) if nom else Q()
        q_prenom = Q(prenom__icontains=prenom) if prenom else Q()
        q_adr = Q(adresse__icontains=adr) if adr else Q()
        q_sexe = Q(genre=sexe) if sexe else Q()
        clients = Client.objects.filter(q_nom | q_prenom | q_adr | q_sexe)  
    return render(request,'vente/clients.html', {'clients':clients})

@login_required
def stats(request):
    
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    # analyse des produits
    Top_produit = Vente.objects.prefetch_related('id_produit').values('id_produit').annotate(
    sale_count=Count('id_produit'),
    produit_nom=Subquery(
    Produit.objects.filter(id_produit=OuterRef('id_produit')).values('nom_produit'))).filter(id_vendeur = request.user.id,annuler = False)[:1]

    top_5_produit = Vente.objects.prefetch_related('id_produit').values('id_produit').annotate(
    sale_count=Count('id_produit'),
    produit_nom=Subquery(
    Produit.objects.filter(id_produit=OuterRef('id_produit')).values('nom_produit'))).filter(id_vendeur = request.user.id,annuler = False)[:5]

    # nombre de vente
   
    today = datetime.now()
    Nombre_vente = Vente.objects.filter(
        id_vendeur=request.user.id,
        date_vente__year=today.year,
        date_vente__month=today.month,
        date_vente__day=today.day,
        annuler = False).annotate(count_ventes=Count('id_vendeur')).values('id_vendeur', 'count_ventes')
    
    vente =  len(Nombre_vente)
    somme_vente = Vente.objects.filter(date_vente__year=today.year,date_vente__month=today.month,date_vente__day=today.day )
    St = len(somme_vente) 
    if St == 0 :
        pourcentage = 0
    else:
        pourcentage = (int(vente) * 100 )/St
    
    #profil généré
    Top_profit = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id, annuler = False)
    
    profit_mesuel = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id, date_vente__month=today.month,annuler = False)
    
    profit_anuel = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id, date_vente__year=today.year, annuler = False)
    
    
    Profit_journalier = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id, date_vente__year=today.year,
        date_vente__month=today.month,
        date_vente__day=today.day, annuler = False)
    
    # calcule du total cumulé des ventes
    total_sum = 0
    for item in Top_profit:
        total_sum += item['count_ventes']

    # calcule du total cumule des ventes du jour 
    total_jour = 0
    for item in Profit_journalier:
        total_jour += item['count_ventes']

    # calcule du total cumule des ventes du mois
    total_mensuel = 0
    for item in profit_mesuel:
        total_mensuel += item['count_ventes']
    # calcule du total cumule des ventes du années
    total_anuel = 0
    for item in profit_anuel:
        total_anuel += item['count_ventes']

    # logique du jour
    logic_day = today.day - 1
    if logic_day <1:
        logic_day = 30
    elif logic_day>31:
        logic_day = 1


    
    jour = vente
    jour_prec = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id, date_vente__year=today.year,
        date_vente__month=today.month,
        date_vente__day=logic_day, annuler = False)
    
    # calcule du total cumule des ventes du jour precedent
    total_jour_prec = 0
    for item in jour_prec:
        total_jour_prec += item['count_ventes']

    
    # logique du mois
    logic_mois = today.month - 1
    if logic_mois <0:
        logic_mois = 12

    mois_prec = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id, date_vente__year=today.year,
        date_vente__month=logic_mois, annuler = False)

    # calcule du total cumule des ventes du mois precedent
    total_mois_prec = 0
    for item in mois_prec:
        total_mois_prec += item['count_ventes'] 

    jour_prec = len(jour_prec)
    
    
    # variation en pourcentage de la quantite de vente jour apres jour
    if(jour_prec == 0):
        pourcentage_vente = 0
    else:
        pourcentage_vente = ((jour - jour_prec)/jour_prec)*100

    # variable en pourcentage du profit journalier jour apres jour
    if(total_jour_prec == 0):
        pourcentage_profit_jour = 0
    else:
        pourcentage_profit_jour = ((jour - total_jour_prec)/total_jour_prec)*100

    # variable en pourcentage du profit mensuel mois apres mois
    if(total_mois_prec == 0):
        pourcentage_mois = 0
    else:
        pourcentage_mois = ((total_mensuel - total_mois_prec)/total_mois_prec)*100
        
    

    # top 5 clients

    Top_client = Vente.objects.prefetch_related('id_client').values('id_client').annotate(
    sale_count=Count('id_client'),
    nom=Subquery(
    Client.objects.filter(id_client=OuterRef('id_client')).values('nom')),
    prenom=Subquery(
    Client.objects.filter(id_client=OuterRef('id_client')).values('prenom'))).filter(annuler = False)[:5]

    Profit_journalier_prec2 = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id,date_vente__year=today.year,
        date_vente__month=today.month,
        date_vente__day=today.day-2, annuler = False)
    
    Profit_journalier_prec3 = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id,date_vente__year=today.year,
        date_vente__month=today.month,
        date_vente__day=today.day-3, annuler = False)
    
    Profit_journalier_prec4 = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id,date_vente__year=today.year,
        date_vente__month=today.month,
        date_vente__day=today.day-4, annuler = False)
    
    Profit_journalier_prec5 = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter(id_vendeur = request.user.id,date_vente__year=today.year,
        date_vente__month=today.month,
        date_vente__day=today.day-5, annuler = False)
    
    total_jour_prec2 = 0
    for item in Profit_journalier_prec2:
        total_jour_prec2 += item['count_ventes']

    total_jour_prec3 = 0
    for item in Profit_journalier_prec3:
        total_jour_prec3 += item['count_ventes']

    total_jour_prec4 = 0
    for item in Profit_journalier_prec4:
        total_jour_prec4 += item['count_ventes']

    total_jour_prec5 = 0
    for item in Profit_journalier_prec5:
        total_jour_prec5 += item['count_ventes']

    lundi =0
    mardi=0
    mercredi=0
    jeudi=0
    vendredi = 0
    samedi = 0

    if today.strftime("%A") == 'Monday':
        lundi = total_jour
        mardi = 0
        mercredi = 0
        jeudi = 0
        vendredi = 0
        samedi =0
    
    if today.strftime("%A") == 'Tuesday':
        lundi = total_jour_prec
        mardi = total_jour
        mercredi = 0
        jeudi = 0
        vendredi = 0
        samedi =0 

    if today.strftime("%A") == 'Wednesday':
        lundi = total_jour_prec2 
        mardi = total_jour_prec
        mercredi = total_jour
        jeudi = 0
        vendredi = 0
        samedi =0 
    if today.strftime("%A") == 'Thirsday':
        lundi = total_jour_prec3
        mardi = total_jour_prec2 
        mercredi = total_jour_prec
        jeudi = total_jour
        vendredi = 0
        samedi =0 
    
    if today.strftime("%A") == 'Friday':
        lundi = total_jour_prec4
        mardi = total_jour_prec3
        mercredi = total_jour_prec2
        jeudi = total_jour_prec
        vendredi = total_jour
        samedi =0 
    
    if today.strftime("%A") == 'Saturday':
        lundi = total_jour_prec5
        mardi = total_jour_prec4
        mercredi = total_jour_prec3
        jeudi = total_jour_prec2
        vendredi = total_jour_prec
        samedi =total_jour

    heure = today.hour
    return render(request, 'vente/stats.html', {'top_produits':Top_produit,
                                                'top_produit_5': top_5_produit, 
                                                'ventes':vente, 'pourcentage':int(pourcentage), 
                                                'profit':total_sum, 
                                                'profit_jour':total_jour,
                                                'profit_mensuel':total_mensuel,
                                                'profit_anuel':total_anuel,
                                                'an':today.year,
                                                'haut_bas_jour':int(pourcentage_vente),
                                                'haut_bas_mois': pourcentage_mois,
                                                'haut_bas_profit':int(pourcentage_profit_jour),
                                                'top_client':Top_client,
                                                'lundi':lundi,
                                                'mardi':mardi,
                                                'mercredi':mercredi,
                                                'jeudi':jeudi,
                                                'vendredi':vendredi,
                                                'samedi':samedi,
                                                'heure':heure
                                                
                                                })

@login_required
def ajout_client(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    if request.method == "POST":
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        adresse = request.POST['adr']
        telephone = request.POST['tel']
        email = request.POST['email']
        genre = request.POST['genre']
        

        nom =  nom.lower()
        prenom = prenom.lower()
        adresse = adresse.lower()
        genre = genre.lower()
        

        if len(telephone) > 10:
            messages.add_message(request,messages.ERROR, 'Format de numero telephonique incorrect.')
            return render(request,'vente/ajout_client.html', {'message': messages.get_messages(request)})
        
        if len(telephone) <10:
            messages.add_message(request,messages.ERROR, 'Format de numero telephonique incorrect.')
            return render(request,'vente/ajout_client.html', {'message':messages.get_messages(request)})
        
        if (Client.objects.filter(email = email)):
            messages.add_message(request,messages.ERROR, 'ce email appartient deja a un client.')
            return render(request,'vente/ajout_client.html', {'message':messages.get_messages(request)})

        client = Client(nom = nom , prenom = prenom, genre = genre, email =email, telephone=telephone,adresse = adresse )
        mat = 'clt'+str(nom)+str(telephone[:4])
        
        if (Client.objects.filter(matricule = mat)):
            mat = 'clt'+str(nom)+str(telephone[:2])+str(prenom[:2])

        client.matricule = mat
        c = client.save()  
        subject = "Bienvenue dans la famille"
        message = "vous etes desormais un nouveau client "+ client.nom + " " + client.prenom +"\n votre indentifiant client est le suivant : "+ mat + "\n"  +"Merci de votre confiance"
        from_email = settings.EMAIL_HOST_USER
        to_list = [client.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        if (c):
            
            messages.success(request,'Client ajouté\ ')
    
    return render(request,'vente/ajout_client.html', {'message':messages.get_messages(request)})

@login_required
def sup_client(request, pk):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    sup = Client.objects.get(id_client = pk)
    if request.method == 'POST':
        sup.delete()
        return redirect('client')
    return render(request, 'vente/sup_client.html', {'sup':sup})

@login_required
def modidier_client(request, pk):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    sup = Client.objects.get(id_client = pk)
    mat = sup.matricule

    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        adresse = request.POST['adr']
        telephone = request.POST['tel']
        email = request.POST['email']
        genre = request.POST['genre']
        nom =  nom.lower()
        prenom = prenom.lower()
        adresse = adresse.lower()
        genre = genre.lower()
        sup.nom = nom 
        sup.prenom = prenom
        sup.genre = genre
        sup.email =email
        sup.telephone=telephone
        sup.adresse = adresse 
        sup.matricule = mat
        sup.save()
        return redirect('client')
    return render(request, 'vente/modifier_client.html', {'sup':sup})

@login_required
def produit(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    produit = Produit.objects.all()
    return render(request,'vente/Produit.html', {'produits':produit})

@login_required
def oublie(request):
    nombre = 0
    numero = list('123456789')
    code = ''
    for i in range(5):
        code += random.choice(numero)
    print(code)
    if MotPerdu.objects.filter(id_user = request.user.id):   
        Mot = MotPerdu.objects.get(id_user = (request.user).id )
        code = int(code)
        if MotPerdu.objects.filter(code = code):
            code = ""
            for i in range(5):
                code += random.choice(numero)

        vendeur =  SupervisorUtilisateur.objects.get(id = request.user.id)
        Mot.id_user = SupervisorUtilisateur.objects.get(id = request.user.id)
        Mot.code=code
        subject = "Code de confirmation"
        message = "Votre code de confirmation est le suivant "+ str(code)
        from_email = settings.EMAIL_HOST_USER
        to_list = [vendeur.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        Mot.save()
        return redirect('r_oublie')
    else:
        vendeur = SupervisorUtilisateur.objects.get(id = (request.user).id)
        mot =  MotPerdu.objects.create(id_user = vendeur, code = code) 
        vendeur = SupervisorUtilisateur.objects.get(id = (request.user).id)
        subject = "Code de confirmation"
        message = "Votre code de confirmation est le suivant "+ str(code)
        from_email = settings.EMAIL_HOST_USER
        to_list = [vendeur.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        mot.save()
        return redirect('r_oublie')
    

@login_required   
def R_oublie(request):   
    mot = MotPerdu.objects.get(id_user = request.user.id)
    code = mot.code
    if request.method == 'POST':       
        code_recu = request.POST['code']
        code_recu = int(code_recu)
        if code_recu == code:
           return redirect('nouveau_mot')
        else:
            sms = 'code incorret'
            return render(request,'vente/oublie.html', {'message':sms})
    return render(request,'vente/oublie.html')

@login_required
def nouveau_mot(request):
    
    if request.method == "POST":
        code = request.POST['code']
        confirmation = request.POST['confirmation_code']
        if confirmation != code:
             sms = 'confirmation incorrect ressayer!'
             return render(request,'vente/nouveau_code.html',{'sms':sms})
        else:
            hash_password = make_password(code)
            vendeur = SupervisorUtilisateur.objects.get(id = (request.user).id)
            vendeur.password = hash_password
            vendeur.save()
            subject = "Felicitation"
            message = "Votre mot de pass a bien été modifier"+ '\n'+ "Votre nouveau mot de pass est le suivant: "+  str(code)
            from_email = settings.EMAIL_HOST_USER
            to_list = [vendeur.email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            sms = 'Votre mot de pass a bien été changer'
            return render(request,'vente/nouveau_code.html',{'sms_s':sms})
    return render(request,'vente/nouveau_code.html')

@login_required
def signout(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    logout(request)
    return redirect('login')

@login_required
def acces(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "gestionnaire":
        return redirect('gestionH')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    return render(request,'vente/acces.html')

# def remplisage(request):
#     STATIC_DIR = os.path.join(settings.BASE_DIR, 'data')  # Assuming BASE_DIR is defined

# # Get the full path to the CSV file
#     csv_file_path = os.path.join(STATIC_DIR, 'clients_clin.csv')

# # Open the CSV file in read mode
#     with open(csv_file_path, 'r') as csvfile:
#         reader = csv.DictReader(csvfile)

#     # Iterate through each row in the CSV file
#         for row in reader:
#             model_instance = Client(
#             nom=row['nm'],
#             prenom = row['prenom'],  # Replace with actual field names
#             genre = row['Sex']
#                 # ... and so on for each fiel
#                 )
#             model_instance.save()
   
  
#     return(request,"vente/try.html" )
#         # ... (rest of the code remains the same)