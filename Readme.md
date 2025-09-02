# 🎮 Alain Project

Alain project description

---

## 📂 Arborescence du projet

```
mon_jeu/
│── main.py        # Point d'entrée du jeu
│── settings.py    # Paramètres globaux (résolution, FPS, couleurs…)
│── game.py        # Classe principale du jeu
│── player.py      # Exemple de classe pour un joueur/entité
│── requirements.txt # Dépendances du projet
│── setup.sh       # Script d’installation automatique
│── assets/        # Dossier pour images, sons, polices
│   ├── images/
│   ├── sounds/
│   └── fonts/
```

---

## 🚀 Installation

1. **Cloner le repo :**

   ```bash
   git clone https://github.com/ton-utilisateur/mon_jeu.git
   cd mon_jeu
   ```

2. **Donner les droits d’exécution au script d’installation :**

   ```bash
   chmod +x setup.sh
   ```

3. **Lancer l’installation :**

   ```bash
   ./setup.sh
   ```

Ce script :

- crée un environnement virtuel `venv/`
- installe toutes les dépendances listées dans `requirements.txt`

---

## ▶️ Lancer le jeu

Active l’environnement virtuel et exécute le jeu :

```bash
source venv/bin/activate
python main.py
```

---

## 📦 Dépendances

- [Python 3.x](https://www.python.org/)
- [Pygame](https://www.pygame.org/)

---

## 💡 Astuces

- Pour sortir du venv :

  ```bash
  deactivate
  ```

- Pour ajouter une nouvelle librairie :

  ```bash
  pip install ma_librairie
  pip freeze > requirements.txt
  ```
