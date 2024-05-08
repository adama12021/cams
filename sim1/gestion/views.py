from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from supervisor.modeles import *
from datetime import datetime
from supervisor.models import Utilisateur
from django.db.models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import csv
import openpyxl
from django.urls import URLResolver 
import re
from django.http import HttpResponse
from openpyxl import Workbook


# Create your views here.
@login_required(login_url='login')
def gestion_home(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    return render(request,'gestion/home.html')

@login_required
def ajout_stock(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    return render(request, 'gestion/inscription.html')

@login_required
def stock(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    stock = Stock.objects.prefetch_related('id_produit_s').filter(id_produit_s__archiver = False)
    prod = Produit.objects.filter(archiver = False)
    produits = ""
    taille = len(stock)
    if request.method == "POST":

        nom_produit = request.POST['produit']
        quantite = request.POST['quantite']
        liste = request.POST['produit_liste']
        
        q_nom = Q(nom_produit__icontains=nom_produit) if nom_produit else Q()
        q_quantite = Q(quantite=quantite) if quantite else Q()
        q_liste_produit = Q(nom_produit=liste) if liste else Q()
        archiver = Q(archiver = False) if archiver else Q()
        produits = Produit.objects.filter((q_nom | q_quantite | q_liste_produit) & archiver)
        taille = len(produits)
    
    return render(request,'gestion/stock.html', {'stocks':stock,'prod':prod ,'produits':produits, 'taille':taille})




@login_required
def produit(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    produit = Produit.objects.filter(archiver = False)[:50]
    page =  request.get_full_path()
    print(page)
    if request.method == "POST":
        nom_produit = request.POST['produit']
        prix = request.POST['prix']
        cat = request.POST['cat']
        
        q_nom = Q(nom_produit__icontains=nom_produit) if nom_produit else Q()
        q_prix = Q(p_unitaire__icontains=prix) if prix else Q()
        q_cat = Q(categorie=cat) if cat else Q()
        produit = Produit.objects.filter(q_nom | q_prix | q_cat)
    taille = len(produit)
    return render(request,'gestion/produit.html',{'produits':produit, 'taille':taille, 'page':page})


@login_required
def archive(request):
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    produit = Produit.objects.filter(archiver = True)[:50]
    if request.method == "POST":
        nom_produit = request.POST['produit']
        prix = request.POST['prix']
        cat = request.POST['cat']
        archiver = True
        
        q_nom = Q(nom_produit__icontains=nom_produit) if nom_produit else Q()
        q_prix = Q(p_unitaire__icontains=prix) if prix else Q()
        q_cat = Q(categorie=cat) if cat else Q()
        archiver = Q(archiver = True) if archiver else Q()
        produit = Produit.objects.filter((q_nom | q_prix | q_cat) & archiver)
    taille = len(produit)
    return render(request,'gestion/archive_page.html',{'produits':produit, 'taille':taille})




@login_required
def sup_prod(request, pk):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    produit = Produit.objects.get(id_produit = pk)
    if (request.method == 'POST'):
        produit.delete()
        return redirect('ges_produit')
    return render(request, 'gestion/sup_produit.html', {'produits':produit})

@login_required
def modif_prod(request, pk):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    produit = Produit.objects.get(id_produit = pk)
    quantite = produit.quantite
    if (request.method == 'POST'):
        prods = request.POST['produit']
        prix = request.POST['prix']
        categorie = request.POST['categorie']       
        produits = prods
    
        
        produit.p_unitaire = prix
        produit.quantite = quantite
        produit.nom_produit = produits
        produit.categorie = categorie
        produit.save()
        return redirect('ges_produit')
    return render(request, 'gestion/modif_produit.html', {'produits':produit})

@login_required
def archiver_prod(request, pk):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    produit = Produit.objects.get(id_produit = pk)   
    produit.archiver =  True  
    produit.save()
    return redirect('ges_produit')
    


@login_required
def desarchiver_prod(request, pk):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    produit = Produit.objects.get(id_produit = pk)   
    produit.archiver =  False  
    produit.save()
    return redirect('archive_page')    

@login_required
def modif_stock(request, pk):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    stock = Stock.objects.get(id_produit_s = pk) 
    Prod = Produit.objects.get(id_produit = pk)
    if (request.method == 'POST'):
        quantite = request.POST['quantite']
        if int(quantite)< 0:
                return render(request, 'gestion/modif_stock.html', {'stocks':stock, "err":"taper une valeur positive"})  
        stock.quantite_s =  stock.quantite_s + int(quantite)
        Prod.quantite = Prod.quantite + int(quantite)
        stock.save()
        Prod.save()
        return redirect('stock')
    return render(request, 'gestion/modif_stock.html', {'stocks':stock})

# @login_required
# def commande(request):
#     # verification de role
#     person = SupervisorUtilisateur.objects.get(id=request.user.id)
#     if person.role == "vendeur":
#         return redirect('vente_home')
#     elif person.role == 'superviseur':
#         return redirect('home_supervisor')
    
#     return render(request,'gestion/commande.html')

# @login_required
# def ajout_commande(request):
#     # verification de role
#     person = SupervisorUtilisateur.objects.get(id=request.user.id)
#     if person.role == "vendeur":
#         return redirect('vente_home')
#     elif person.role == 'superviseur':
#         return redirect('home_supervisor')
    
#     return render(request,'gestion/ajout_commande.html')

@login_required
def ajout_produit(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    if request.method == "POST":
        produit = request.POST['produit']
        prix = request.POST['prix']
        quantite = request.POST['quantite']
        categorie = request.POST['categorie']       

        produits = produit.lower()
        quantite = quantite.lower()
        categorie = categorie.lower()
        if Produit.objects.filter(nom_produit = produits):
            messages.add_message(request,messages.ERROR, 'ce produit existe deja.')
            return render(request,'gestion/ajout_produit.html', {'message':messages.get_messages(request)})

        produit = Produit(nom_produit = produits ,categorie=categorie, p_unitaire=prix, quantite=quantite)
        c = produit.save()
        
        
        get_prod = Produit.objects.get(nom_produit = produits, categorie=categorie)
        
        gestionnaire = request.user
        now = datetime.now()  # Get current date and time
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        stock = Stock(id_produit_s = produit ,quantite_s = get_prod.quantite, date_ajout = formatted_date)
        stock.id_gestionnaire = gestionnaire.id
        stock.save()
        if (c):
            messages.success(request,'Produit ajouté\ ')
    return render(request,'gestion/ajout_produit.html', {'messages': messages.get_messages(request)})

@login_required
def stat(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    today = datetime.now()
    produit = Produit.objects.filter(archiver = False)
    

    Categorie = Produit.objects.values('categorie').distinct().count()
    # Categorie = Categorie['categorie__count']

    stock_null = Produit.objects.filter(quantite = 0, archiver=False)
    stock_pnull = Produit.objects.filter(quantite__gte=1, quantite__lte=20, archiver = False)

    Top_produit = VentesAnalyse.objects.values('produit').annotate(total=Count('produit')).order_by('-total')[:1]

    prod_vogue =  VentesAnalyse.objects.values('produit').annotate(total=Count('produit')).order_by('-total')[:5]

    #Vente.objects.prefetch_related('id_produit').values('id_produit').annotate(
    # sale_count=Count('id_produit'),
    # produit_nom=Subquery(
    # Produit.objects.filter(id_produit=OuterRef('id_produit')).values('nom_produit')))[:5]
    
    profit_mesuel = Vente.objects.annotate(count_ventes=Sum('prix_total')).values('count_ventes').filter( date_vente__month=today.month, annuler = False)
    print(Top_produit)
    total_mensuel = 0
    for item in profit_mesuel:
        total_mensuel += item['count_ventes']

    profit_anuel_prec = VentesAnalyse.objects.annotate(count_ventes=Sum('prix')).values('count_ventes').filter(date__year=(today.year -1))
    profit_anuel = VentesAnalyse.objects.annotate(count_ventes=Sum('prix')).values('count_ventes').filter(date__year=today.year)
    
    total_anuel = 0
    for item in profit_anuel:
        total_anuel += item['count_ventes']
    
    total_anuel_prec = 0
    for item in profit_anuel_prec:
        total_anuel_prec += item['count_ventes']
    

    annee_prec = today.year - 1 
    annee_actu = today.year
    
    if total_anuel_prec == 0:
        croissance = 0
    else:
        croissance = ((total_anuel - total_anuel_prec)/total_anuel_prec)*100


    Profit_anuel2023 = VentesAnalyse.objects.annotate(count_ventes=Sum('prix')).values('count_ventes').filter(date__year=2023)
    total_anuel2023 = 0
    for item in Profit_anuel2023:
        total_anuel2023 += item['count_ventes']

    Profit_anuel2024 = VentesAnalyse.objects.annotate(count_ventes=Sum('prix')).values('count_ventes').filter(date__year=2024)
    total_anuel2024 = 0
    for item in Profit_anuel2024:
        total_anuel2024 += item['count_ventes']
    
    

    heure = today.hour

    total_quantity = Stock.objects.prefetch_related('id_produit_s').filter(id_produit_s__archiver = False).all().aggregate(Sum('quantite_s'))
    total_quantity = total_quantity['quantite_s__sum']

    

    
    
    lundi =0
    mardi=0
    mercredi=0
    jeudi=0
    vendredi = 0
    samedi = 0

    if today.strftime("%A") == 'Monday':
        lundi = total_quantity
        mardi = 0
        mercredi = 0
        jeudi = 0
        vendredi = 0
        samedi =0
        if StockAnalyse.objects.filter(id_stock_analyse = 1):
            stock = StockAnalyse.objects.get(id_stock_analyse = 1)
            stock.quantite_jour = total_quantity
        else :
            StockAnalyse.objects.create(quantite_jour = total_quantity)
    
    if today.strftime("%A") == 'Tuesday':
        lundi =  StockAnalyse.objects.get(id_stock_analyse = 1)
        lundi = lundi.quantite_jour
        mardi = total_quantity
        if StockAnalyse.objects.filter(id_stock_analyse = 2):
            stock = StockAnalyse.objects.get(id_stock_analyse = 2)
            stock.quantite_jour = total_quantity
        else :
            StockAnalyse.objects.create(quantite_jour = total_quantity)

        mercredi = 0
        jeudi = 0
        vendredi = 0
        samedi =0 

    if today.strftime("%A") == 'Wednesday':
        lundi =  StockAnalyse.objects.get(id_stock_analyse = 1)
        lundi = lundi.quantite_jour
        mardi =  StockAnalyse.objects.get(id_stock_analyse = 2)
        mardi = mardi.quantite_jour
        mercredi =  total_quantity
        if StockAnalyse.objects.filter(id_stock_analyse = 3):
            stock = StockAnalyse.objects.get(id_stock_analyse = 3)
            stock.quantite_jour = total_quantity
        else :
            StockAnalyse.objects.create(quantite_jour = total_quantity)
        jeudi = 0
        vendredi = 0
        samedi =0 
    if today.strftime("%A") == 'Thursday':
        lundi =  StockAnalyse.objects.get(id_stock_analyse = 1)
        lundi = lundi.quantite_jour
        mardi =  StockAnalyse.objects.get(id_stock_analyse = 2)
        mardi = mardi.quantite_jour
        mercredi =  StockAnalyse.objects.get(id_stock_analyse = 3)
        mercredi = mercredi.quantite_jour
        jeudi =  total_quantity
        if StockAnalyse.objects.filter(id_stock_analyse = 4):
            stock = StockAnalyse.objects.get(id_stock_analyse = 4)
            stock.quantite_jour = total_quantity
        else :
            StockAnalyse.objects.create(quantite_jour = total_quantity)
        vendredi = 0
        samedi =0 
    
    if today.strftime("%A") == 'Friday':
        lundi =  StockAnalyse.objects.get(id_stock_analyse = 1)
        lundi = lundi.quantite_jour
        mardi =  StockAnalyse.objects.get(id_stock_analyse = 2)
        mardi = mardi.quantite_jour
        mercredi =  StockAnalyse.objects.get(id_stock_analyse = 3)
        mercredi = mercredi.quantite_jour
        jeudi = StockAnalyse.objects.get(id_stock_analyse = 4) 
        jeudi = jeudi.quantite_jour
        vendredi = total_quantity
        if StockAnalyse.objects.filter(id_stock_analyse = 5):
            stock = StockAnalyse.objects.get(id_stock_analyse = 5)
            stock.quantite_jour = total_quantity
        else :
            StockAnalyse.objects.create(quantite_jour = total_quantity)
        samedi =0 
    
    if today.strftime("%A") == 'Saturday':
        lundi =  StockAnalyse.objects.get(id_stock_analyse = 1)
        lundi = lundi.quantite_jour
        mardi =  StockAnalyse.objects.get(id_stock_analyse = 2)
        mardi = mardi.quantite_jour
        mercredi =  StockAnalyse.objects.get(id_stock_analyse = 3)
        mercredi = mercredi.quantite_jour
        jeudi = StockAnalyse.objects.get(id_stock_analyse = 4) 
        jeudi = jeudi.quantite_jour
        vendredi = StockAnalyse.objects.get(id_stock_analyse = 4)
        vendredi = vendredi.quantite_jour
        samedi = total_quantity
        if StockAnalyse.objects.filter(id_stock_analyse = 5):
            stock = StockAnalyse.objects.get(id_stock_analyse = 5)
            stock.quantite_jour = total_quantity
        else :
            StockAnalyse.objects.create(quantite_jour = total_quantity)

    print(today.strftime('%A'))
    return render(request, 'gestion/stats.html', 
                  {'produit':len(produit),
                   'categorie':Categorie, 
                   'stock_null':len(stock_null),
                   'produit_phare':Top_produit,
                   'stock_pnull':len(stock_pnull),
                   'profit_mensuel':total_mensuel,
                   'profit_anuel_prec':total_anuel_prec,
                   'profit_anuel':total_anuel,
                   'an_prec':annee_prec,
                   'an_actu': annee_actu,
                   'croissance':int(croissance),
                   'prod_vogue':prod_vogue,
                   'total_anuel2023':total_anuel2023,
                   'total_anuel2024':total_anuel2024,
                   'heure':heure,
                   'total_quantite':total_quantity,
                   'lundi':lundi,
                   'mardi':mardi,
                   'mercredi':mercredi,
                   'jeudi':jeudi,
                   'vendredi':vendredi,
                   'samedi':samedi})

@login_required
def access(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    return render(request,'gestion/acces.html')




@login_required
def signout(request):
    # verification de role
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    
    logout(request)
    return redirect('login')

# def remplisage(request):
#     STATIC_DIR = os.path.join(settings.BASE_DIR, 'data')  # Assuming BASE_DIR is defined

# # Get the full path to the CSV file
#     csv_file_path = os.path.join(STATIC_DIR, 'prod_clin.csv')

# # Open the CSV file in read mode
#     with open(csv_file_path, 'r') as csvfile:
#         reader = csv.DictReader(csvfile)

#     # Iterate through each row in the CSV file
#         for row in reader:
#             model_instance = Produit(nom_produit=row['NOM_PRODUIT'],
#             categorie = row['CATEGORIE'], 
#             p_unitaire = row['P_UNITAIRE'],
#             quantite = 0)
            
#             model_instance.save()
#             gestionnaire = request.user
#             now = datetime.now()  
#             formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
#             stock = Stock(id_produit_s = model_instance ,quantite_s = 0, date_ajout = formatted_date)
#             stock.id_gestionnaire = gestionnaire.id
#             stock.save()
#     return(request,"gestion/try.html" )





def export_data_to_csv(request):
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    # Retrieve data from the database (replace with your actual data retrieval logic)
    data = Produit.objects.all()  # Assuming this function returns a list of data rows

    # Create a CSV file object in memory
    csv_file = csv.writer(open('produit.csv', 'w', newline=''))

    # Write header row
    csv_file.writerow(['id','produit', 'categorie', 'prix','quantite'])  # Replace with actual header names
    print(data)
    # Write data rows
    for d in data:     
        csv_file.writerow([d.id_produit,d.nom_produit, d.categorie, d.p_unitaire,d.quantite])

    # Prepare the Django response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="produit.csv"'

    # Write CSV content to the response
    writer = csv.writer(response)
    writer.writerow(['id','produit', 'categorie', 'prix','quantite'])  # Replace with actual header names
    for d in data:
        writer.writerow([d.id_produit,d.nom_produit, d.categorie, d.p_unitaire,d.quantite])

    return response




def export_data_to_excel(request):
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    # Retrieve data from the database
    data = Produit.objects.all()  # Assuming this is a QuerySet of Produit models

    # Create a new Excel workbook
    workbook = Workbook()
    worksheet = workbook.active  # Get the active worksheet

    # Write header row
    header = ['id', 'produit', 'categorie', 'prix', 'quantite']
    worksheet.append(header)

    # Write data rows
    for product in data:
        row_data = [product.id_produit, product.nom_produit, product.categorie, product.p_unitaire, product.quantite]
        worksheet.append(row_data)

    # Prepare the Django response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="produit.xlsx"'

    # Write Excel data to the response
    workbook.save(response)

    return response


def export_data_produit_null_to_excel(request):
    person = SupervisorUtilisateur.objects.get(id=request.user.id)
    if person.role == "vendeur":
        return redirect('vente_stats')
    elif person.role == 'superviseur':
        return redirect('dashboard')
    # Retrieve data from the database
    data = Produit.objects.filter(quantite__gte=1, quantite__lte=20, archiver = False)  # Assuming this is a QuerySet of Produit models

    # Create a new Excel workbook
    workbook = Workbook()
    worksheet = workbook.active  # Get the active worksheet

    # Write header row
    header = ['id', 'produit', 'categorie', 'prix', 'quantite']
    worksheet.append(header)

    # Write data rows
    for product in data:
        row_data = [product.id_produit, product.nom_produit, product.categorie, product.p_unitaire, product.quantite]
        worksheet.append(row_data)

    # Prepare the Django response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="produit_vide.xlsx"'

    # Write Excel data to the response
    workbook.save(response)

    return response