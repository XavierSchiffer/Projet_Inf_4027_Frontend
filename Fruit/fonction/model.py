from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np


def prediction_maturity_papaya(image_path, model_path):
    """
    Prédit le stade de maturation d'une papaye et retourne les probabilités de chaque stade.

    :param image_path: Chemin de l'image de la papaye.
    :param model_path: Chemin du modèle de classification.
    :return: Tuple (stade_maturation, probas) - ex: ("mur", {"non-mur": 10.5, "semi-mur": 30.2, "mur": 59.3})
    """
    
    # Charger le modèle
    model = load_model(model_path)
    
    # Charger et prétraiter l'image
    img = image.load_img(image_path, target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalisation de l'image
    
    # Prédire la classe
    prediction = model.predict(img_array).flatten()  # Transformation en tableau 1D
    
    # Noms des classes retournées par le modèle
    classnames = ['belum_matang', 'matang', 'setengah_matang']
    
    # Associer chaque classe à sa probabilité en pourcentage
    results = {
        "non-mur": float(prediction[0] * 100),
        "mur": float(prediction[1] * 100),
        "semi-mur": float(prediction[2] * 100)
    }
    
    # Trier par probabilité décroissante
    class_predite = max(results, key=results.get)  # Classe avec la plus haute probabilité
    
    return class_predite, results


# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import numpy as np

# def prediction_maturity_papaya(image_path, model_path):
#     """
#     Prédit le stade de maturation d'une papaye et retourne une étiquette lisible.

#     :param image_path: Chemin de l'image de la papaye.
#     :param model_path: Chemin du modèle de classification.
#     :return: String - stade de maturation ("mur", "semi-mur", "non-mur")
#     """
    
#     # Charger le modèle
#     model = load_model(model_path)
    
#     # Charger et prétraiter l'image
#     img = image.load_img(image_path, target_size=(32, 32))
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array /= 255.0  # Normalisation de l'image
    
#     # Prédire la classe
#     prediction = model.predict(img_array).flatten()  # Transformation en tableau 1D
    
#     # Noms des classes retournées par le modèle
#     classnames = ['belum_matang', 'matang', 'setengah_matang']  # 🔥 Supprimé les espaces inutiles
    
#     # Associer chaque classe à sa probabilité
#     results = {
#         classnames[i]: float(prediction[i])
#         for i in range(len(classnames))
#     }
    
#     # Trier par probabilité décroissante
#     resultats_tries = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
#     # 🔥 Afficher les résultats pour vérifier
#     print("######## Résultat de classification :", resultats_tries)

#     # Récupérer la classe avec la probabilité la plus élevée
#     class_predite = resultats_tries[0][0]

#     # Mapping de la prédiction vers des valeurs lisibles
#     mapping = {
#         "belum_matang": "non-mur",
#         "setengah_matang": "semi-mur",
#         "matang": "mur"
#     }

#     # Retourner la valeur correspondante ou "inconnu" si non trouvée
#     stade_maturation_pred = mapping.get(class_predite, "inconnu")

#     print("Stade maturation prédit :", stade_maturation_pred)  # 🔥 Vérification
#     return stade_maturation_pred
