from django.urls import path 
from . import views

urlpatterns = [
    path('vente_home',views.vente_home, name='vente_home'),
    path('ajout_vente',views.vente_ajout,name='ajout_vente'),
    path('client',views.client,name='client'),
    path('vente',views.vente,name='vente'),
    path('annule_vente/<int:pk>',views.annule_vente,name='annule_vente'),
    path('produit',views.produit, name='produit'),
    path('ajout_client', views.ajout_client, name="ajout_client"),
    path('deconnexion', views.signout, name='deconnexion_vente'),
    path('sup_client/<int:pk>', views.sup_client, name='sup_client'),
    path('modifier_client/<int:pk>', views.modidier_client, name='modifier_client'),
    path('details_vente/<int:pk>',views.details_vente, name='detail_vente'),
    path('acess', views.acces,name='acces_vente'),
    path('stats', views.stats,name='vente_stats'),
    path('oublie', views.oublie, name='oublie_vente'),
    path('r_oublie', views.R_oublie,name='r_oublie'),
    path('nouveau_mot_de_pass', views.nouveau_mot, name="nouveau_mot"),
    path('historique', views.historique, name='historique'),
    # path('try', views.remplisage, name='try')

]