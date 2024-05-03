
from django.urls import path
from . import views



urlpatterns = [

    path("gestion_home",views.gestion_home,name='gestionH'),
    # path("ajout_stock",views.ajout_stock,name='ajout_stock'),
    path('stock',views.stock,name='stock'),  
    path('produit',views.produit,name='ges_produit'),
    path('export_data.csv', views.export_data_to_csv, name='export_data_csv'),
    path('export_data.xlsx', views.export_data_to_excel, name='export_data_excel'),
    path('ajout_produit',views.ajout_produit,name='ajout_produit'),
    path('deconnexion', views.signout, name="deconnexion_gestion"),
    path('sup/<int:pk>', views.sup_prod,name='sup_produit'),
    path('modif/<int:pk>', views.modif_prod,name='modif_produit'),
    path('modif_stock/<int:pk>', views.modif_stock, name='modif_stock'),
    path('stats',views.stat, name='stats'),
    path('acces', views.access, name='acces_gestion'),
    # path('try',views.remplisage, name='try_g')


]