# Evtrip

> Plateforme intelligente de gestion et d'optimisation des trajets

[![Python 97.4%](https://img.shields.io/badge/Python-97.4%25-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/ondongoa/Evtrip)](https://github.com/ondongoa/Evtrip/commits/main)

---

## Table des matières

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Contribution](#contribution)
- [License](#license)

---

## À propos

**Evtrip** est une application web complète conçue pour optimiser et gérer intelligemment vos trajets. Que vous soyez un utilisateur individuel ou une entreprise, Evtrip vous permet de planifier efficacement vos déplacements.

Le projet combine une architecture moderne avec :
- Un **backend Python** performant pour le traitement des données et l'optimisation des trajets
- Une **interface frontend** réactive et conviviale
- Des technologies optimisées en C, Cython et C++ pour les calculs intensifs

---

## Fonctionnalités

- **Planification d'itinéraires** - Calcul optimisé des meilleurs trajets
- **Analyse de trajets** - Statistiques détaillées et métriques de performance
- **Gestion de véhicules** - Suivi de la flotte et maintenance
- **Optimisation des coûts** - Réduction des dépenses de carburant et d'usure
- **Interface responsive** - Accessible sur desktop, tablette et mobile
- **Sécurité** - Authentification et chiffrement des données
- **Rapports** - Génération de rapports détaillés et exportables
- **Performances** - Optimisation natives en C/Cython pour les calculs complexes

---

## Architecture

Evtrip suit une architecture **client-serveur** moderne avec les composants suivants :

### Backend
- Framework web Python (Flask/FastAPI)
- Base de données relationnelle
- Modules d'optimisation en C/Cython

### Frontend
- Interface web responsive
- Intégration API REST

### Services
- Service d'optimisation des trajets
- Service de gestion des véhicules
- Service d'authentification

---

## Installation

### Prérequis
- Python 3.8+
- pip ou conda
- Node.js (pour le frontend)

### Étapes

1. Clonez le repository
```bash
git clone https://github.com/ondongoa/Evtrip.git
cd Evtrip
```

2. Créez un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installez les dépendances
```bash
pip install -r requirements.txt
```

4. Configurez les variables d'environnement
```bash
cp .env.example .env
```

5. Lancez l'application
```bash
python app.py
```

---

## Utilisation

### Démarrer le serveur
```bash
python manage.py runserver
```

### API REST
L'API est accessible à `http://localhost:8000/api/`

### Interface web
Accédez à `http://localhost:3000` pour l'interface utilisateur

---

## Structure du projet

```
Evtrip/
├── backend/
│   ├── app.py
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── docs/
├── tests/
├── .gitignore
├── README.md
└── LICENSE
```

---

## Contribution

Les contributions sont bienvenues ! Veuillez suivre ces étapes :

1. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
2. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
3. Poussez vers la branche (`git push origin feature/AmazingFeature`)
4. Ouvrez une Pull Request

### Standards de code
- Suivez PEP 8 pour Python
- Utilisez des commentaires explicites
- Écrivez des tests pour vos modifications

---

## License

Ce projet est licencié sous la Licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

**Maintenu par:** ondongoa  
**Dernière mise à jour:** 2026
