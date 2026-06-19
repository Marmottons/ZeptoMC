# ZeptoMC

[🇫🇷 Français](#français) | [🇬🇧 English](#english)

---

## Français

Un lanceur CLI Minecraft minimaliste et léger, fork de [picomc](https://github.com/samcavoj/picomc).

### 🎮 À propos

ZeptoMC est un lanceur Minecraft en ligne de commande (CLI) ultra-léger avec des dépendances minimales. Il te permet de :

- 🚀 Lancer Minecraft facilement
- 📦 Gérer tes instances
- 👤 Gérer tes comptes (Offline & Microsoft)
- 🔨 Installer des mod loaders (Forge, Fabric)

### ✨ Caractéristiques

- **Minimaliste** : Seulement 2 dépendances (click, requests)
- **Zéro bloat** : Pas de dépendances inutiles pour les couleurs ou barres de progression
- **Cross-platform** : Fonctionne sur Linux, Windows, macOS
- **Open-source** : Licence MIT

### 📋 Dépendances

| Dépendance | Raison |
|-----------|--------|
| `click~=8.1` | Interface CLI |
| `requests~=2.31` | Requêtes HTTP |

**Aucune dépendance** pour les couleurs ANSI ou les barres de progression (implémentation native).

### 🚀 Installation

#### Prérequis
- Python 3.8+
- Java (pour lancer Minecraft)

#### Depuis le répertoire du projet

```bash
cd /chemin/vers/ZeptoMC

# Utiliser directement
./zeptomc --help
./zeptomc play
```

#### Ajouter au PATH (optionnel)

```bash
echo 'export PATH="/chemin/vers/ZeptoMC:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Maintenant tu peux faire:
zeptomc play
```

### 📖 Utilisation

```
zeptomc [--debug] [-r CHEMIN] COMMANDE [ARGS...]

Commandes:
  play      Lancer Minecraft
  account   Gérer les comptes
  instance  Gérer les instances
  install   Installer versions et mod loaders
```

#### Lancer Minecraft

```bash
# Lancer avec version et compte par défaut
zeptomc play

# Lancer une version spécifique (instance par défaut)
zeptomc play 1.20.1

# Lancer une instance spécifique
zeptomc play mon-instance

# Lancer avec un compte spécifique
zeptomc play --account NomCompte
```

#### Gérer les comptes

Types supportés :
- **Offline** : Jouer hors ligne, pas d'authentification
- **Microsoft** : Authentification Microsoft

```bash
# Lister les comptes (* = compte par défaut)
zeptomc account list

# Créer un compte offline
zeptomc account add mon-compte

# Créer et authentifier un compte Microsoft
zeptomc account authenticate mon-ms-compte

# Rafraîchir le token d'un compte Microsoft
zeptomc account refresh mon-ms-compte

# Supprimer un compte
zeptomc account rm NomCompte

# Définir le compte par défaut
zeptomc account default NomCompte
```

Les noms de comptes sont **insensibles à la casse** (`bedite` ≈ `Bedite`).

#### Gérer les instances

```bash
# Lister les instances
zeptomc instance ls

# Créer une nouvelle instance
zeptomc instance add mon-instance

# Créer avec une version spécifique
zeptomc instance add mon-instance 1.18.2

# Supprimer une instance
zeptomc instance rm mon-instance

# Renommer une instance
zeptomc instance rename ancien-nouveau nouveau-nom

# Voir le répertoire d'une instance
zeptomc instance dir mon-instance
```

La configuration des instances se fait en modifiant directement les fichiers :
`~/.local/share/zeptomc/instances/<instance>/config.json`

#### Installer versions et mod loaders

```bash
# Lister les versions disponibles
zeptomc install ls
zeptomc install ls --all
zeptomc install ls --release

# Installer la dernière version vanilla
zeptomc install

# Installer une version spécifique
zeptomc install 1.20.1

# Installer la dernière version avec Forge
zeptomc install forge

# Installer une version avec Forge
zeptomc install 1.20.1 forge

# Installer avec Fabric
zeptomc install fabric
zeptomc install 1.20.1 fabric
```

#### Options globales

```bash
zeptomc --debug      # Mode debug (logs détaillés)
zeptomc --h          # Aide (alias de --help)
zeptomc -r /chemin   # Répertoire de données personnalisé
```

### 🔧 Configuration

Les données ZeptoMC sont stockées dans `~/.local/share/zeptomc/`.

#### Variables d'environnement

```bash
export ZEPTOMC_ROOT=/mon/chemin
zeptomc play  # Utilisera /mon/chemin
```

#### Fichiers de configuration

- **Comptes** : `~/.local/share/zeptomc/accounts.json`
- **Config globale** : `~/.local/share/zeptomc/config.json`
- **Instances** : `~/.local/share/zeptomc/instances/<nom>/config.json`

### 🛠️ Développement

#### Architecture

```
src/zeptomc/
├── __init__.py       # Point d'entrée, vérification version Python
├── __main__.py       # python -m zeptomc
├── cli/              # Interface CLI
│   ├── __init__.py
│   ├── main.py       # Point d'entrée CLI
│   ├── account.py    # Gestion comptes
│   ├── install.py    # Installation versions + mods
│   ├── instance.py   # Gestion instances
│   ├── play.py       # Lancer le jeu
│   └── utils.py      # Utilitaires CLI
├── mod/              # Support mod loaders
│   ├── __init__.py
│   ├── forge.py      # Forge + PicoForgeWrapper
│   └── fabric.py     # Fabric
├── java/             # Gestion Java
│   └── __init__.py   # Détection et validation Java
├── account.py        # Authentification (Offline + Microsoft)
├── colors.py         # Couleurs ANSI + ProgressBar
├── config.py         # Gestion configuration (OverlayDict)
├── downloader.py     # Téléchargements parallèles
├── errors.py         # Exceptions personnalisées
├── instance.py       # Instances + lancement
├── launcher.py       # Classe principale (chemins, données)
├── library.py        # Gestion des bibliothèques Minecraft
├── logging.py        # Logging personnalisé
├── msapi.py          # API Microsoft (OAuth)
├── osinfo.py         # Détection OS/architecture
├── rules.py          # Règles de compatibilité Minecraft
├── utils.py          # Utilitaires divers
├── version.py        # Gestion versions Minecraft
└── windows.py        # Spécificités Windows
```

#### Tests

```bash
# Tester une commande spécifique
./zeptomc instance ls
./zeptomc account list
```

---

## English

A lightweight and minimal Minecraft CLI launcher, fork of [picomc](https://github.com/samcavoj/picomc).

### 🎮 About

ZeptoMC is an ultra-lightweight Minecraft command-line launcher with minimal dependencies. It allows you to:

- 🚀 Launch Minecraft easily
- 📦 Manage your instances
- 👤 Manage your accounts (Offline & Microsoft)
- 🔨 Install mod loaders (Forge, Fabric)

### ✨ Features

- **Minimal** : Only 2 dependencies (click, requests)
- **Zero bloat** : No unnecessary dependencies for colors or progress bars
- **Cross-platform** : Works on Linux, Windows, macOS
- **Open-source** : MIT License

### 📋 Dependencies

| Dependency | Purpose |
|-----------|---------|
| `click~=8.1` | CLI interface |
| `requests~=2.31` | HTTP requests |

**No dependencies** for ANSI colors or progress bars (native implementation).

### 🚀 Installation

#### Requirements
- Python 3.8+
- Java (to run Minecraft)

#### From the project directory

```bash
cd /path/to/ZeptoMC

# Use directly
./zeptomc --help
./zeptomc play
```

#### Add to PATH (optional)

```bash
echo 'export PATH="/path/to/ZeptoMC:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Now you can do:
zeptomc play
```

### 📖 Usage

```
zeptomc [--debug] [-r PATH] COMMAND [ARGS...]

Commands:
  play      Launch Minecraft
  account   Manage accounts
  instance  Manage instances
  install   Install versions and mod loaders
```

#### Launch Minecraft

```bash
# Launch with default version and account
zeptomc play

# Launch a specific version (default instance)
zeptomc play 1.20.1

# Launch a specific instance
zeptomc play my-instance

# Launch with a specific account
zeptomc play --account AccountName
```

#### Manage accounts

Supported types:
- **Offline** : Play offline, no authentication
- **Microsoft** : Microsoft authentication

```bash
# List accounts (* = default account)
zeptomc account list

# Create an offline account
zeptomc account add my-account

# Create and authenticate a Microsoft account
zeptomc account authenticate my-ms-account

# Refresh a Microsoft account token
zeptomc account refresh my-ms-account

# Remove an account
zeptomc account rm AccountName

# Set the default account
zeptomc account default AccountName
```

Account names are **case-insensitive** (`bedite` ≈ `Bedite`).

#### Manage instances

```bash
# List instances
zeptomc instance ls

# Create a new instance
zeptomc instance add my-instance

# Create with a specific version
zeptomc instance add my-instance 1.18.2

# Delete an instance
zeptomc instance rm my-instance

# Rename an instance
zeptomc instance rename old-name new-name

# Show instance directory
zeptomc instance dir my-instance
```

Instance config is done by editing files directly:
`~/.local/share/zeptomc/instances/<name>/config.json`

#### Install versions and mod loaders

```bash
# List available versions
zeptomc install ls
zeptomc install ls --all
zeptomc install ls --release

# Install latest vanilla version
zeptomc install

# Install a specific version
zeptomc install 1.20.1

# Install latest version with Forge
zeptomc install forge

# Install a version with Forge
zeptomc install 1.20.1 forge

# Install with Fabric
zeptomc install fabric
zeptomc install 1.20.1 fabric
```

#### Global options

```bash
zeptomc --debug      # Debug mode (detailed logs)
zeptomc --h          # Help (alias for --help)
zeptomc -r /path     # Custom data directory
```

### 🔧 Configuration

ZeptoMC data is stored in `~/.local/share/zeptomc/`.

#### Environment variables

```bash
export ZEPTOMC_ROOT=/my/path
zeptomc play  # Will use /my/path
```

#### Configuration files

- **Accounts** : `~/.local/share/zeptomc/accounts.json`
- **Global config** : `~/.local/share/zeptomc/config.json`
- **Instances** : `~/.local/share/zeptomc/instances/<name>/config.json`

### 🛠️ Development

#### Architecture

```
src/zeptomc/
├── __init__.py       # Entry point, Python version check
├── __main__.py       # python -m zeptomc
├── cli/              # CLI interface
│   ├── __init__.py
│   ├── main.py       # CLI entry point
│   ├── account.py    # Account management
│   ├── install.py    # Version + mod installation
│   ├── instance.py   # Instance management
│   ├── play.py       # Launch game
│   └── utils.py      # CLI utilities
├── mod/              # Mod loaders support
│   ├── __init__.py
│   ├── forge.py      # Forge + PicoForgeWrapper
│   └── fabric.py     # Fabric
├── java/             # Java management
│   └── __init__.py   # Java detection and validation
├── account.py        # Authentication (Offline + Microsoft)
├── colors.py         # ANSI colors + ProgressBar
├── config.py         # Config management (OverlayDict)
├── downloader.py     # Parallel downloads
├── errors.py         # Custom exceptions
├── instance.py       # Instances + launching
├── launcher.py       # Main class (paths, data)
├── library.py        # Minecraft library management
├── logging.py        # Custom logging
├── msapi.py          # Microsoft API (OAuth)
├── osinfo.py         # OS/architecture detection
├── rules.py          # Minecraft compatibility rules
├── utils.py          # Misc utilities
├── version.py        # Minecraft version management
└── windows.py        # Windows specifics
```

#### Tests

```bash
# Test a specific command
./zeptomc instance ls
./zeptomc account list
```
