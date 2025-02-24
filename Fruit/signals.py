from decimal import Decimal
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Papaye, Alerte, Rapport, StatistiqueRecolte
from django.db.models.functions import TruncMonth
from django.db.models import Count
from Fruit.models import Papaye, MaturationStats

@receiver(pre_save, sender=Papaye)
def save_old_stade_maturation(sender, instance, **kwargs):
    """
    Avant de sauvegarder l'objet, on stocke l'ancien stade de maturation
    dans une variable temporaire pour comparer après la mise à jour.
    """
    try:
        instance._old_stade_maturation = Papaye.objects.get(pk=instance.pk).stade_maturation
    except Papaye.DoesNotExist:
        instance._old_stade_maturation = None

@receiver(post_save, sender=Papaye)
def send_alert_on_maturation_change(sender, instance, created, **kwargs):
    """
    Envoie un email et enregistre une alerte UNIQUEMENT si le stade de maturation a changé.
    """
    if not created:  # Ne pas exécuter ce signal lors de la création de l'objet
        ancien_stade = getattr(instance, "_old_stade_maturation", None)

        if ancien_stade is not None and ancien_stade != instance.stade_maturation:
            utilisateur = instance.secteur.utilisateur
            
            # Création de l'alerte
            alerte = Alerte.objects.create(
                utilisateur=utilisateur,
                papaye=instance,
                message=
                # f"Le stade de maturation a changé. Le nouveau stade est : {instance.stade_maturation}.\n\n"
                f"D'apres notre modele de classification il en ressort que il y'a {instance.pourcentage_papaye_non_mur}% pour que ca soit non mûres\n"
                f" {instance.pourcentage_papaye_semi_mur}% pour que ca soit semi-mûres\n"
                f"{instance.pourcentage_papaye_mur}% pour que ca soit mûres dans votre secteur\n\n",
                type_notification="Email",
                statut=False,
            )

            # Générer le lien de suivi
            tracking_url = f"{settings.SITE_URL}{reverse('Fruit:mark_alert_as_read', args=[alerte.id])}"

            # Envoi de l'email
            try:
                send_mail(
                    subject="Changement de stade de maturation",
                    message=(
                        f"Le stade de maturation de vos papayes est passé à : {instance.stade_maturation}.\n\n"
                        f"Dans votre secteur il y a:\n"
                        f"- {instance.pourcentage_papaye_non_mur}% de papayes non mûres\n"
                        f"- {instance.pourcentage_papaye_semi_mur}% de papayes semi-mûres\n"
                        f"- {instance.pourcentage_papaye_mur}% de papayes mûres\n\n"
                        f"Cliquez sur ce lien pour confirmer la lecture : {tracking_url}"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[utilisateur.email],
                    fail_silently=False,
                )
                print("✅ Email envoyé avec succès")
            except Exception as e:
                print("❌ Erreur lors de l'envoi de l'email :", e)

            print("✅ Alerte enregistrée en base.")


@receiver(post_save, sender=Rapport)
def creer_ou_mettre_a_jour_statistiques_recolte(sender, instance, created, **kwargs):
    """
    Met à jour ou crée une statistique de récolte lorsqu'un rapport est soumis.
    """
    from django.db.models.functions import TruncMonth

    secteur = instance.secteur
    periode = instance.date_envoi.strftime("%B %Y")  # Exemple : "Février 2025"

    quantite_recolte = instance.quantite_recolte
    quantite_recolte_pourcentage = min((quantite_recolte / 100.0) * 100, 100)
    quantite_non_recolter = 100 - quantite_recolte_pourcentage

    pourcentage_papaye_mur = instance.pourcentage_papaye_mur
    pourcentage_papaye_non_mur = instance.pourcentage_papaye_non_mur
    pourcentage_papaye_semi_mur = instance.pourcentage_papaye_semi_mur

    # Vérifier si une statistique existe déjà pour ce secteur et cette période
    statistique, created = StatistiqueRecolte.objects.get_or_create(
        secteur=secteur,
        periode=periode,
        rapport=instance,  # ✅ Ajout de `rapport=instance` pour éviter l'erreur
        defaults={
            "quantite_recolte": quantite_recolte_pourcentage,
            "quantite_non_recolter": quantite_non_recolter,
            "pourcentage_papaye_mur": pourcentage_papaye_mur,
            "pourcentage_papaye_non_mur": pourcentage_papaye_non_mur,
            "pourcentage_papaye_semi_mur": pourcentage_papaye_semi_mur,
        },
    )

    if not created:
        # Compter le nombre de rapports existants dans la même période
        total_rapports = Rapport.objects.annotate(
            month=TruncMonth("date_envoi")
        ).filter(
            secteur=secteur, month=instance.date_envoi.replace(day=1)
        ).count()

        # Mise à jour des statistiques en moyenne pondérée
        statistique.quantite_recolte = (
            statistique.quantite_recolte + quantite_recolte_pourcentage
        ) / total_rapports
        statistique.quantite_non_recolter = (
            statistique.quantite_non_recolter + quantite_non_recolter
        ) / total_rapports

        statistique.pourcentage_papaye_mur = (
            statistique.pourcentage_papaye_mur + pourcentage_papaye_mur
        ) / total_rapports
        statistique.pourcentage_papaye_non_mur = (
            statistique.pourcentage_papaye_non_mur + pourcentage_papaye_non_mur
        ) / total_rapports
        statistique.pourcentage_papaye_semi_mur = (
            statistique.pourcentage_papaye_semi_mur + pourcentage_papaye_semi_mur
        ) / total_rapports

        statistique.save()


@receiver(post_save, sender=Papaye)

def update_maturation_stats(sender, instance, created, **kwargs):
    if instance.secteur:
        mois = instance.date_derniere_analyse.strftime('%Y-%m')

        stats, _ = MaturationStats.objects.get_or_create(
            secteur=instance.secteur,
            mois = mois
            )

        # Assurer que stats.total_* est aussi un Decimal avant d'ajouter
        stats.total_non_mur = Decimal(stats.total_non_mur) + Decimal(instance.pourcentage_papaye_non_mur)
        stats.total_semi_mur = Decimal(stats.total_semi_mur) + Decimal(instance.pourcentage_papaye_semi_mur)
        stats.total_mur = Decimal(stats.total_mur) + Decimal(instance.pourcentage_papaye_mur)
        stats.nombre_analyses += 1

        stats.save()