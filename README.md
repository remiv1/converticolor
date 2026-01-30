# 🎨 ConvertiColor

**Convertisseur de couleurs multi-formats** avec interface graphique.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Fonctionnalités

- **Conversion multi-formats** : Hexadécimal, RGB, CMJN (CMYK), HSL, HSV
- **Aperçu couleur** : Visualisation instantanée avec coins arrondis
- **Harmonies de couleurs** : Complémentaire, analogues, triadiques
- **Vérificateur de contraste WCAG** : Conformité accessibilité web
- **Copie presse-papier** : Bouton de copie pour chaque format
- **Interface minimaliste** : Simple et intuitive

## 📸 Aperçu

```txt
┌─────────────────────────────────────────┐
│          ConvertiColor                  │
│   Convertisseur de couleurs             │
│                                         │
│     ┌─────────────────────┐             │
│     │   Aperçu couleur    │             │
│     └─────────────────────┘             │
│                                         │
│  ○ Hex  ○ RGB  ○ CMJN  ○ HSL  ○ HSV     │
│  [____________________________] [Conv]  │
│                                         │
│  Hex:  #FF5733                     [📋] │
│  RGB:  255, 87, 51                 [📋] │
│  CMJN: 0%, 65.9%, 80%, 0%          [📋] │
│  HSL:  11°, 100%, 60%              [📋] │
│  HSV:  11°, 80%, 100%              [📋] │
│                                         │
│  ┌ Harmonies ─────────────────────────┐ │
│  │ [■] [■] [■] [■] [■]                │ │
│  └────────────────────────────────────┘ │
│                                         │
│  ┌ Contraste WCAG ────────────────────┐ │
│  │ Fond: [#FFFFFF] [Vérifier]         │ │
│  │ Ratio: 4.5:1 |    AA               │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## 🚀 Installation

### Option 1 : Exécutable (recommandé)

Téléchargez la dernière version depuis les [Releases](../../releases) :

- **Windows** : `ConvertiColor.exe`
- **Linux** : `ConvertiColor-x86_64.AppImage`

### Option 2 : Depuis les sources

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/converticolor.git
cd converticolor

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python src/main.py
```

## 🛠️ Développement

### Prérequis

- Python 3.8 ou supérieur
- Tkinter (inclus avec Python)

### Structure du projet

```txt
converticolor/
├── src/
│   ├── __init__.py           # Package principal
│   ├── main.py               # Interface graphique
│   ├── color_converter.py    # Logique de conversion
│   └── color_picker.py       # Pipette de capture
├── build.py                  # Script de packaging
├── requirements.txt          # Dépendances complètes
├── requirements-runtime.txt  # Dépendances runtime
└── README.md
```

### Commandes de build

```bash
# Installer les dépendances de build
python build.py --install-deps

# Nettoyer les builds précédents
python build.py --clean

# Build pour la plateforme actuelle
python build.py

# Build Windows spécifiquement
python build.py --windows

# Build Linux + AppImage
python build.py --linux --appimage
```

## 📖 Utilisation

### Formats supportés

| Format | Exemple | Description |
| ------ | ------- | ----------- |
| **Hex** | `#FF5733` ou `#F53` | Hexadécimal (avec ou sans #) |
| **RGB** | `255, 87, 51` | Rouge, Vert, Bleu (0-255) |
| **CMJN** | `0, 65.9, 80, 0` | Cyan, Magenta, Jaune, Noir (0-100%) |
| **HSL** | `11, 100, 60` | Teinte (0-360°), Saturation, Luminosité (0-100%) |
| **HSV** | `11, 80, 100` | Teinte (0-360°), Saturation, Valeur (0-100%) |

### Vérificateur de contraste WCAG

Le vérificateur calcule le ratio de contraste selon les normes [WCAG 2.1](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) :

- **AA Normal** : Ratio ≥ 4.5:1 (texte normal)
- **AA Large** : Ratio ≥ 3.0:1 (texte ≥ 18pt ou 14pt gras)
- **AAA Normal** : Ratio ≥ 7.0:1 (texte normal)
- **AAA Large** : Ratio ≥ 4.5:1 (texte large)

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- 🐛 Signaler des bugs
- 💡 Proposer des fonctionnalités
- 🔧 Soumettre des pull requests

---

Fait avec ❤️ en Python
