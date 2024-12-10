# Sitagri Project  

## The General Idea  
Le projet **Sitagri** vise à collecter, analyser et intégrer en temps réel les données des marchés agricoles pour faciliter les prises de décision commerciales. L'objectif est de fournir une plateforme automatisée qui surveille les variations des prix et génère des alertes basées sur des critères prédéfinis.  

---

## Automatisation de la Connexion et Ouverture du Navigateur  
Pour accéder au site de Sitagri :  

- **Lancement Automatique de Chrome** :  
  Le script utilise Selenium pour ouvrir le navigateur et naviguer automatiquement vers la page de connexion.  
- **Connexion Automatique** :  
  Une requête POST via la bibliothèque `Requests` est utilisée pour effectuer une authentification sécurisée en envoyant les identifiants. Un jeton ou une session est récupéré pour accéder aux données.  

---

## Scraping des Données en Temps Réel  
Le projet s'appuie sur deux sources principales pour récupérer les données :  

- **WebSockets** :  
  Permet de recevoir en continu les informations de marché, comme les prix et les tendances, en temps réel.  
- **API REST** :  
  Utilisé pour collecter des données historiques ou supplémentaires en fonction des besoins.  

---

## Traitement et Intégration des Données  
- Les données brutes récupérées sont transformées, nettoyées et vérifiées pour éviter les doublons.  
- Elles sont ensuite insérées dans une base de données **SQL Server**, avec un contrôle spécifique pour garantir que seules les nouvelles valeurs sont ajoutées.  

---

## Applications  
Cette solution permet :  
- Une gestion efficace des données pour des analyses en temps réel.  
- Des visualisations dynamiques des tendances du marché.  
- Des recommandations automatisées pour améliorer les processus décisionnels dans le secteur agricole.  
