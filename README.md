# ZeptoMC

Un lanceur CLI Minecraft minimaliste et léger, fork de [picomc](https://github.com/samcavoj/picomc).

## 🎮 À propos

ZeptoMC est un lanceur Minecraft en ligne de commande (CLI) ultra-léger avec des dépendances minimales. Il te permet de :

- 🚀 Lancer Minecraft facilement
- 📦 Gérer tes instances
- 👤 Gérer tes comptes (Mojang & Microsoft)
- 🔨 Installer des mod loaders (Forge, Fabric, FTB)
- 📥 Installer des modpacks depuis CurseForge

## ✨ Caractéristiques

- **Minimaliste** : Seulement 2 dépendances (click, requests)
- **Léger** : ~230 KB de code source
- **Zéro bloat** : Pas de dépendances inutiles pour les couleurs ou barres de progression
- **Cross-platform** : Fonctionne sur Linux, Windows, macOS
- **Open-source** : Licence MIT

## 📋 Dépendances

| Dépendance | Raison |
|-----------|--------|
| `click~=8.1` | Interface CLI |
| `requests~=2.31` | Requêtes HTTP |

**Aucune dépendance** pour les couleurs ANSI ou les barres de progression (implémentation native).

## 🚀 Installation

### Prérequis
- Python 3.8+
- Java (pour lancer Minecraft)

### Depuis le répertoire du projet

```bash
cd /chemin/vers/ZeptoMC

# Utiliser directement
./zeptomc --help
./zeptomc play
```

### Ajouter au PATH (optionnel)

Pour utiliser `zeptomc` de n'importe où :

```bash
echo 'export PATH="/chemin/vers/ZeptoMC:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Maintenant tu peux faire:
zeptomc play
```

## 📖 Utilisation

### Commandes principales

```bash
# Voir toutes les commandes
zeptomc --help

# Lancer Minecraft
zeptomc play                          # Version et compte par défaut
zeptomc play 1.20.1                   # Version spécifique
zeptomc play --account NomCompte      # Compte spécifique
zeptomc play 1.20.1 --account MonsId  # Les deux

# Gérer tes instances
zeptomc instance list                 # Lister
zeptomc instance create my-instance   # Créer
zeptomc instance delete my-instance   # Supprimer
zeptomc instance rename old new       # Renommer

# Gérer tes comptes
zeptomc account list                  # Lister
zeptomc account create                # Créer
zeptomc account remove NomCompte      # Supprimer
zeptomc account setdefault NomCompte  # Compte par défaut

# Gérer les versions
zeptomc version list                  # Lister les versions Minecraft
zeptomc version prepare 1.20.1        # Télécharger une version

# Mod loaders
zeptomc mod loader forge install 1.20.1     # Installer Forge
zeptomc mod loader fabric install 1.20.1    # Installer Fabric

# Modpacks CurseForge
zeptomc mod pack install https://...  # Installer un modpack
```

### Options globales

```bash
zeptomc --debug          # Mode debug (logs détaillés)
zeptomc --version        # Afficher la version
zeptomc -r /chemin       # Répertoire de données personnalisé
```

## 🔧 Configuration

Les données de ZeptoMC sont stockées dans :
- **Linux/macOS** : `~/.local/share/zeptomc/`
- **Windows** : `%APPDATA%\zeptomc\`

### Variables d'environnement

```bash
# Personnaliser le répertoire de données
export ZEPTOMC_ROOT=/mon/chemin

zeptomc play  # Utilisera /mon/chemin
```

## 📊 Optimisations récentes

### Réduction des dépendances (-60%)

**Avant** :
- `click`, `requests`, `tqdm`, `coloredlogs`, `colorama` (5 dépendances)

**Après** :
- `click`, `requests` (2 dépendances)

Les anciennes dépendances ont été remplacées par :
- **Couleurs ANSI** : Implémentation native (codes ANSI standards)
- **Barres de progression** : Classe `ProgressBar` minimaliste

### Renommage du projet

Migration de `picomc` → `ZeptoMC` pour mieux refléter le projet actuel.

## 🛠️ Développement

### Architecture

```
src/zeptomc/
├── cli/              # Interface CLI
│   ├── main.py       # Point d'entrée
│   ├── account.py    # Gestion comptes
│   ├── instance.py   # Gestion instances
│   ├── play.py       # Lancer le jeu
│   ├── mod.py        # Mod loaders
│   ├── version.py    # Versions
│   └── config.py     # Configuration
├── mod/              # Support mod loaders
│   ├── forge.py
│   ├── fabric.py
│   ├── ftb.py
│   └── curse.py      # CurseForge
├── launcher.py       # Classe principale
├── account.py        # Authentification
├── version.py        # Gestion versions
├── downloader.py     # Téléchargements
├── instance.py       # Instances
├── colors.py         # Couleurs ANSI + ProgressBar
└── logging.py        # Logging personnalisé
```

### Tests

```bash
# Lancer tous les tests
./test.sh

# Tester une commande spécifique
./zeptomc instance list
./zeptomc account list
```

### Commits

Les commits suivent ce format :

```
feat: ajouter une nouvelle fonctionnalité
fix: corriger un bug
refactor: refactoriser du code
docs: mettre à jour la documentation
test: ajouter/modifier des tests
```

## 📝 Licence

MIT - Voir [LICENSE](LICENSE)

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésite pas à :
- Ouvrir une issue pour signaler un bug
- Faire une pull request pour proposer une amélioration
- Améliorer la documentation

## ℹ️ Notes

- Ce projet est un fork de [picomc](https://github.com/samcavoj/picomc)
- Auteur original : Samuel Čavoj
- Mainteneur actuel : Marmotton

---

**Dernière mise à jour** : Mars 2026
