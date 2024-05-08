from django.urls import path
from . import views

urlpatterns = [
    path("home_supervisor", views.home_supervisor, name='home_supervisor'),
    path("ajout_personnel",views.ajout_vendeur,name='ajout_gestion'),
    path('motdepass',views.mot,name='mot_supervisor'),
    path('deconnexion', views.signout,name='deconnexion_superviseur'),
    path('vendeur', views.vendeur,name='liste_vendeur'),
    path('ventes', views.historique,name='liste_ventes'),
    path('gestionnaire', views.gestionnaire, name='liste_gestionnaire'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('acces', views.acces, name='acces_superviseur'),
    path('test', views.test, name='test'),
    path('prediction', views.prediction_deco, name='prediction'),
    path('client', views.client, name='supervisor_client'),
    path('active_vendeur/<int:pk>', views.active_vendeur, name='active_vendeur'),
    path('desactive_vendeur/<int:pk>', views.desactive_vendeur, name='desactive_vendeur'),
    path('active_gestionnaire/<int:pk>', views.active_gestionnaire, name='active_gestionnaire'),
    path('desactive_gestionnaire/<int:pk>', views.desactive_gestionnaire, name='desactive_gestionnaire'),
    path('export_data_client.csv', views.export_data_client_to_csv, name='export_data_client_csv'),
    path('export_data_client.xlsx', views.export_data_client_to_excel, name='export_data_client_excel'),
    path('export_data_vendeur.csv', views.export_data_vendeur_to_csv, name='export_data_vendeur_csv'),
    path('export_data_vendeur.xlsx', views.export_data_vendeur_to_excel, name='export_data_vendeur_excel'),
    path('export_data_gestion.csv', views.export_data_gestion_to_csv, name='export_data_gestion_csv'),
    path('export_data_gestion.xlsx', views.export_data_gestion_to_excel, name='export_data_gestion_excel'),
    path('export_data_vente.csv', views.export_data_vente_to_csv, name='export_data_vente_csv'),
    path('export_data_vente.xlsx', views.export_data_vente_to_excel, name='export_data_vente_excel'),
    path('export_data_vente_annuler.xlsx', views.export_data_vente_annuler_to_excel, name='export_data_vente_annuler_excel'),
    path('export_data_produit.xlsx', views.export_data_produit_to_excel, name='export_data_produit_excel'),
    # path('try',views.remplisage,name='try_s')
    
]