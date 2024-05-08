# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = True
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Client(models.Model):
    id_client = models.AutoField(db_column='ID_Client', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=255)  # Field name made lowercase.
    prenom = models.CharField(db_column='Prenom', max_length=255)  # Field name made lowercase.
    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=225, blank=True, null=True)
    genre = models.CharField(max_length=20, blank=True, null=True)
    matricule = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'client'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_session'


class MotPerdu(models.Model):
    id_mot = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('SupervisorUtilisateur', models.DO_NOTHING, db_column='id_user')
    code = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'mot_perdu'


class Produit(models.Model):
    id_produit = models.AutoField(db_column='ID_Produit', primary_key=True)  # Field name made lowercase.
    nom_produit = models.CharField(max_length=225)
    categorie = models.CharField(max_length=225)
    p_unitaire = models.IntegerField(db_column='P_UNITAIRE')  # Field name made lowercase.
    quantite = models.IntegerField(db_column='QUANTITE')  # Field name made lowercase.
    archiver = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'produit'


class Stock(models.Model):
    id_produit_s = models.OneToOneField(Produit, models.DO_NOTHING, db_column='id_produit_s', primary_key=True)
    quantite_s = models.IntegerField()
    date_ajout = models.DateTimeField(db_column='DATE_AJOUT')  # Field name made lowercase.
    id_gestionnaire = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'stock'


class StockAnalyse(models.Model):
    id_stock_analyse = models.AutoField(primary_key=True)
    quantite_jour = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'stock_analyse'


class SupervisorUtilisateur(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    localites = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=200, blank=True, null=True)
    sex = models.CharField(max_length=3, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'supervisor_utilisateur'


class SupervisorUtilisateurGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    utilisateur = models.ForeignKey(SupervisorUtilisateur, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'supervisor_utilisateur_groups'
        unique_together = (('utilisateur', 'group'),)


class SupervisorUtilisateurUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    utilisateur = models.ForeignKey(SupervisorUtilisateur, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'supervisor_utilisateur_user_permissions'
        unique_together = (('utilisateur', 'permission'),)


class Vente(models.Model):
    id_vente = models.BigAutoField(db_column='ID_VENTE', primary_key=True)  # Field name made lowercase.
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='ID_CLIENT')  # Field name made lowercase.
    id_produit = models.ForeignKey(Produit, models.DO_NOTHING, db_column='ID_PRODUIT')  # Field name made lowercase.
    prix_total = models.IntegerField(db_column='PRIX_TOTAL')  # Field name made lowercase.
    id_vendeur = models.ForeignKey(SupervisorUtilisateur, models.DO_NOTHING, db_column='ID_VENDEUR')  # Field name made lowercase.
    date_vente = models.DateTimeField()
    quantite_vendu = models.IntegerField()
    annuler = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'vente'


class VenteAnuler(models.Model):
    id_vente_anuler = models.AutoField(primary_key=True)
    id_vente = models.ForeignKey(Vente, models.DO_NOTHING, db_column='id_vente')
    date_annulation = models.DateField()
    motif_annulation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'vente_anuler'


class VentesAnalyse(models.Model):
    nom = models.CharField(max_length=255)
    genre = models.CharField(max_length=20, blank=True, null=True)
    produit = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    prix = models.IntegerField()
    date = models.DateTimeField()
    id_ventes = models.ForeignKey(Vente, models.DO_NOTHING, db_column='id_ventes', blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ventes_analyse'
