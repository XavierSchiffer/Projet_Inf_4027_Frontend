from django.db import models
from account.models import User

class Secteur(models.Model):
    nom = models.CharField(max_length=255)
    # localisation = models.CharField(max_length=255)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name="secteurs")

    class Meta:
        verbose_name = "Secteur"
        verbose_name_plural = "Secteurs"
        ordering = ['nom']


class Papaye(models.Model):
    STADE_CHOICES = [
        ('vert', 'Vert'),
        ('semi-mur', 'Semi-mûr'),
        ('mur', 'Mûr'),
    ]

    secteur =  models.ForeignKey(Secteur, on_delete=models.CASCADE, related_name="papayes")
    stade_maturation = models.CharField(max_length=20, choices=STADE_CHOICES, default='vert')
    date_derniere_analyse = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='papayes/', verbose_name="Image des papayes", null=False, blank=False)
    pourcentage_papaye_mur = models.DecimalField(
        max_digits=5,  # Nombre total de chiffres
        decimal_places=2,  # Nombre de décimales
        default=0.0,  # Valeur par défaut
        verbose_name="Pourcentage de papayes mûres"
    )
    pourcentage_papaye_non_mur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name="Pourcentage de papayes non mûres"
    )
    pourcentage_papaye_semi_mur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name="Pourcentage de papayes semi-mûres"
    )

    class Meta:
        verbose_name = "Fruit"
        verbose_name_plural = "Fruits"
        ordering = ['date_derniere_analyse']


class Rapport(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rapports")
    secteur = models.ForeignKey(Secteur, on_delete=models.CASCADE)
    etat_global = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    quantite_recolte = models.FloatField()
    commentaire = models.TextField(blank=True, null=True)
    pourcentage_papaye_mur = models.DecimalField(
        max_digits=5,  # Nombre total de chiffres
        decimal_places=2,  # Nombre de décimales
        default=0.0,  # Valeur par défaut
        verbose_name="Pourcentage de papayes mûres"
    )
    pourcentage_papaye_non_mur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name="Pourcentage de papayes non mûres"
    )
    pourcentage_papaye_semi_mur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name="Pourcentage de papayes semi-mûres"
    )

    def __str__(self):
        return f"Rapport {self.date_envoi} par {self.utilisateur.username}"


class StatistiqueRecolte(models.Model):
    secteur = models.ForeignKey(Secteur, on_delete=models.CASCADE)
    rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, related_name="statistiques")
    periode = models.CharField(max_length=100)
    quantite_recolte = models.FloatField()
    quantite_non_recolter = models.FloatField()
    pourcentage_papaye_mur = models.DecimalField(
        max_digits=5,  # Nombre total de chiffres
        decimal_places=2,  # Nombre de décimales
        default=0.0,  # Valeur par défaut
        verbose_name="Pourcentage de papayes mûres"
    )
    pourcentage_papaye_non_mur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name="Pourcentage de papayes non mûres"
    )
    pourcentage_papaye_semi_mur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name="Pourcentage de papayes semi-mûres"
    )


    def __str__(self):
        return f"Stats {self.periode} pour {self.secteur.nom} - Récolté: {self.quantite_recolte}%"


class Alerte(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alertes")
    papaye = models.ForeignKey(Papaye, on_delete=models.CASCADE)
    message = models.TextField()
    type_notification = models.CharField(max_length=50, choices=[
        ('Email', 'Email'),
    ])
    date_envoi = models.DateTimeField(auto_now_add=True)
    statut = models.BooleanField(default=False)  # Si l'alerte a été traitée
    statut_lecture = models.BooleanField(default=False)  # Si l'email a été lu

    def __str__(self):
        return f"Alerte {self.type_notification} pour {self.utilisateur.username} - Lu : {self.statut_lecture}"


class MaturationStats(models.Model):
    secteur = models.OneToOneField(Secteur, on_delete=models.CASCADE, related_name="maturation_stats")
    total_non_mur = models.FloatField(default=0)
    total_semi_mur = models.FloatField(default=0)
    total_mur = models.FloatField(default=0)
    nombre_analyses = models.IntegerField(default=0)
    mois = models.CharField(max_length=7, null=True, blank=True)
    
    def __str__(self):
        return f"Stats de maturation - Secteur {self.secteur.id}"

    @property
    def moyenne_non_mur(self):
        return self.total_non_mur / self.nombre_analyses if self.nombre_analyses > 0 else 0

    @property
    def moyenne_semi_mur(self):
        return self.total_semi_mur / self.nombre_analyses if self.nombre_analyses > 0 else 0

    @property
    def moyenne_mur(self):
        return self.total_mur / self.nombre_analyses if self.nombre_analyses > 0 else 0
