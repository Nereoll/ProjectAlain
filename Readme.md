# 🎮 The InvisiBlade Knight 2 - Ultimate Legendary Game of the Year Edition

Description à faire

---

## 📂 Arborescence du projet

```bash
projectalain/
│── main.py        # Point d'entrée du jeu
│── settings.py    # Paramètres globaux (résolution, FPS, couleurs…)
│── game.py        # Classe principale du jeu
│── player.py      # Classe qui définit le joueur
│── enemy.py       # Classe qui définit les ennemies
│── ath.py         # Overlay d'infos in game (Vie, mana, score...)
│── audio.py       # Gestion de l'audio
│── credits.py     # Crédits (Assets, audio, developpeurs...)
│── menu.py        # Menu du jeu - lancer une partie, ouvrir les crédits
│── shadow.py      # Gestion des ombres in game
│── utilitaire.py  # Fonctions utilitaires
│── requirements.txt # Dépendances du projet
│── setup.sh       # Script d'installation automatique
│── assets/        # Dossier pour images, sons, polices
│   ├── images/
│   ├── sounds/
│   └── fonts/
```

---

## 🚀 Installation

1. **Cloner le repo :**

   ```bash
   git clone https://github.com/Nereoll/ProjectAlain.git
   cd ProjectAlain
   ```

2. **Donner les droits d'exécution au script d'installation :**

   ```bash
   chmod +x setup.sh
   ```

3. **Lancer l'installation :**

   ```bash
   ./setup.sh
   ```

Ce script :

- crée un environnement virtuel `venv/`
- installe toutes les dépendances listées dans `requirements.txt`

---

## ▶️ Lancer le jeu

Activer l'environnement virtuel puis exécuter le jeu :

```bash
source venv/bin/activate
python main.py
```

---

## 📦 Dépendances

- [Python 3.x](https://www.python.org/)
- [Altgraph](https://pypi.org/project/altgraph/)
- [Cffi](https://pypi.org/project/cffi/)
- [Numpy](https://pypi.org/project/numpy/)
- [Packaging](https://pypi.org/project/packaging/)
- [Pycparser](https://pypi.org/project/pycparser/)
- [Pygame](https://www.pygame.org/)
- [PyInstaller](https://pypi.org/project/pyinstaller/)
- [PyInstallerHooksContrib](https://pypi.org/project/pyinstaller-hooks-contrib/)
- [SetupTools](https://pypi.org/project/setuptools/)
- [SoundDevice](https://pypi.org/project/sounddevice/)

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

- Pour créer un executable

  ```bash
  pyinstaller --onefile --windowed \
  --add-data "assets:assets" \
  --icon=assets/images/icon.ico \
  main.py
  ```
