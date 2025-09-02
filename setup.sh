#!/bin/bash

# Stoppe le script si une commande échoue
set -e

echo "🚀 Création de l'environnement virtuel..."

# Crée un venv s'il n'existe pas déjà
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
else
    echo "ℹ️  Environnement virtuel déjà présent"
fi

# Active le venv
source venv/bin/activate

echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✨ Tout est prêt !"
echo "Pour activer l'environnement :"
echo "    source venv/bin/activate"
