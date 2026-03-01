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
- **Léger** : ~106 KB de code source
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

Pour utiliser `zeptomc` de n'importe où :

```bash
echo 'export PATH="/chemin/vers/ZeptoMC:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Maintenant tu peux faire:
zeptomc play
```

### 📖 Utilisation

#### Lancer Minecraft (versions et instances)

```bash
# Lancer avec version et compte par défaut
zeptomc play

# Lancer une version spécifique (instance par défaut)
zeptomc play 1.20.1

# Lancer une instance spécifique (par son nom)
zeptomc play my-instance

# Lancer avec un compte spécifique
zeptomc play --account NomCompte
```

#### Gérer les instances

```bash
# Lister toutes les instances
zeptomc instance list

# Créer une nouvelle instance
zeptomc instance create my-instance

# Créer une instance avec une version spécifique
zeptomc instance create my-instance 1.18.2

# Lancer une instance
zeptomc instance launch my-instance

# Lancer avec options avancées
zeptomc instance launch my-instance --verify --version-override 1.20.1

# Renommer une instance
zeptomc instance rename old-name new-name

# Supprimer une instance
zeptomc instance delete my-instance

# Extraire les ressources natives (pour débogage)
zeptomc instance natives my-instance

# Voir le répertoire de l'instance
zeptomc instance dir my-instance
```

#### Configurer une instance

```bash
# Voir la configuration d'une instance
zeptomc instance config my-instance show

# Changer le chemin Java
zeptomc instance config my-instance java-path /usr/bin/java8

# Changer les arguments JVM
zeptomc instance config my-instance java-args -XX:+UseG1GC -Xms512M -Xmx2G

# Lire/écrire/supprimer une clé de configuration
zeptomc instance config my-instance get java.path
zeptomc instance config my-instance set java.memory.max 4G
zeptomc instance config my-instance delete java.path
```

#### Gérer les comptes

ZeptoMC supporte deux types de comptes :
- **Offline** : Jouer en mode hors ligne, pas d'authentification requise
- **Microsoft** : Authentification Microsoft (compte Minecraft moderne)

```bash
# Lister tous les comptes (* = compte par défaut)
zeptomc account list

# Créer un compte offline
zeptomc account create mon-compte

# Créer et authentifier un compte Microsoft
zeptomc account authenticate mon-ms-compte

# Rafraîchir le token d'un compte Microsoft
zeptomc account refresh mon-ms-compte

# Supprimer un compte
zeptomc account remove NomCompte

# Définir un compte par défaut
zeptomc account setdefault NomCompte
```

#### Gérer les versions Minecraft

```bash
# Lister les versions locales installées
zeptomc version list

# Lister toutes les versions disponibles
zeptomc version list --all

# Filtrer par type
zeptomc version list --release
zeptomc version list --snapshot

# Télécharger une version
zeptomc version prepare 1.20.1

# Télécharger le jar client ou serveur
zeptomc version jar 1.20.1
zeptomc version jar 1.20.1 server --output server.jar
```

#### Mod loaders

```bash
# Lister les loaders disponibles
zeptomc mod loader --list

# Installer Forge (meilleure version stable pour le jeu spécifié)
zeptomc mod loader forge install --game 1.20.1

# Installer une version Forge spécifique
zeptomc mod loader forge install 47.2.0

# Résoudre la version Forge sans installer
zeptomc mod loader forge version --game 1.20.1

# Installer Fabric
zeptomc mod loader fabric install 1.20.1

# Résoudre la version Fabric sans installer
zeptomc mod loader fabric version 1.20.1
```

#### Options globales

```bash
zeptomc --debug          # Mode debug (logs détaillés)
zeptomc --version        # Afficher la version
zeptomc -r /chemin       # Répertoire de données personnalisé
```

### 🔧 Configuration

Les données de ZeptoMC sont stockées dans `~/.local/share/zeptomc/`.

#### Configuration globale

```bash
# Voir la configuration globale
zeptomc config show

# Modifier une valeur globale
zeptomc config set java.path /usr/bin/java

# Lire une valeur
zeptomc config get java.path

# Supprimer une valeur (retour au défaut)
zeptomc config delete java.path
```

#### Variables d'environnement

```bash
# Personnaliser le répertoire de données
export ZEPTOMC_ROOT=/mon/chemin

zeptomc play  # Utilisera /mon/chemin
```

### 📊 Optimisations récentes

#### Réduction des dépendances (-60%)

**Avant** :
- `click`, `requests`, `tqdm`, `coloredlogs`, `colorama` (5 dépendances)

**Après** :
- `click`, `requests` (2 dépendances)

Les anciennes dépendances ont été remplacées par :
- **Couleurs ANSI** : Implémentation native (codes ANSI standards)
- **Barres de progression** : Classe `ProgressBar` minimaliste

#### Renommage du projet

Migration de `picomc` → `ZeptoMC` pour mieux refléter le projet actuel.

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
│   ├── config.py     # Configuration globale
│   ├── instance.py   # Gestion instances
│   ├── mod.py        # Mod loaders
│   ├── play.py       # Lancer le jeu
│   ├── utils.py      # Utilitaires CLI
│   └── version.py    # Versions
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
# Lancer tous les tests
./test.sh

# Tester une commande spécifique
./zeptomc instance list
./zeptomc account list
```

#### Commits

Les commits suivent ce format :

```
feat: ajouter une nouvelle fonctionnalité
fix: corriger un bug
refactor: refactoriser du code
docs: mettre à jour la documentation
test: ajouter/modifier des tests
```

### 📝 Licence

MIT - Voir [LICENSE](LICENSE)

### 🤝 Contribution

Les contributions sont bienvenues ! N'hésite pas à :
- Ouvrir une issue pour signaler un bug
- Faire une pull request pour proposer une amélioration
- Améliorer la documentation

### ℹ️ Notes

- Ce projet est un fork de [picomc](https://github.com/samcavoj/picomc)
- Auteur original : Samuel Čavoj
- Mainteneur actuel : Marmotton

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
- **Lightweight** : ~106 KB of source code
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

To use `zeptomc` from anywhere:

```bash
echo 'export PATH="/path/to/ZeptoMC:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Now you can do:
zeptomc play
```

### 📖 Usage

#### Launch Minecraft (versions and instances)

```bash
# Launch with default version and account
zeptomc play

# Launch a specific version (default instance)
zeptomc play 1.20.1

# Launch a specific instance (by its name)
zeptomc play my-instance

# Launch with a specific account
zeptomc play --account AccountName
```

#### Manage instances

```bash
# List all instances
zeptomc instance list

# Create a new instance
zeptomc instance create my-instance

# Create an instance with a specific version
zeptomc instance create my-instance 1.18.2

# Launch an instance
zeptomc instance launch my-instance

# Launch with advanced options
zeptomc instance launch my-instance --verify --version-override 1.20.1

# Rename an instance
zeptomc instance rename old-name new-name

# Delete an instance
zeptomc instance delete my-instance

# Extract native resources (for debugging)
zeptomc instance natives my-instance

# Show instance directory
zeptomc instance dir my-instance
```

#### Configure an instance

```bash
# Show the instance configuration
zeptomc instance config my-instance show

# Change the Java executable path
zeptomc instance config my-instance java-path /usr/bin/java8

# Change the JVM arguments
zeptomc instance config my-instance java-args -XX:+UseG1GC -Xms512M -Xmx2G

# Read/write/delete a configuration key
zeptomc instance config my-instance get java.path
zeptomc instance config my-instance set java.memory.max 4G
zeptomc instance config my-instance delete java.path
```

#### Manage accounts

ZeptoMC supports two types of accounts:
- **Offline** : Play in offline mode, no authentication required
- **Microsoft** : Microsoft authentication (modern Minecraft account)

```bash
# List all accounts (* = default account)
zeptomc account list

# Create an offline account
zeptomc account create my-account

# Create and authenticate a Microsoft account
zeptomc account authenticate my-ms-account

# Refresh a Microsoft account token
zeptomc account refresh my-ms-account

# Remove an account
zeptomc account remove AccountName

# Set a default account
zeptomc account setdefault AccountName
```

#### Manage Minecraft versions

```bash
# List locally installed versions
zeptomc version list

# List all available versions
zeptomc version list --all

# Filter by type
zeptomc version list --release
zeptomc version list --snapshot

# Download a version
zeptomc version prepare 1.20.1

# Download client or server jar
zeptomc version jar 1.20.1
zeptomc version jar 1.20.1 server --output server.jar
```

#### Mod loaders

```bash
# List available loaders
zeptomc mod loader --list

# Install Forge (best stable version for the given game)
zeptomc mod loader forge install --game 1.20.1

# Install a specific Forge version
zeptomc mod loader forge install 47.2.0

# Resolve Forge version without installing
zeptomc mod loader forge version --game 1.20.1

# Install Fabric
zeptomc mod loader fabric install 1.20.1

# Resolve Fabric version without installing
zeptomc mod loader fabric version 1.20.1
```

#### Global options

```bash
zeptomc --debug          # Debug mode (detailed logs)
zeptomc --version        # Show version
zeptomc -r /path         # Custom data directory
```

### 🔧 Configuration

ZeptoMC data is stored in `~/.local/share/zeptomc/`.

#### Global configuration

```bash
# Show global configuration
zeptomc config show

# Set a global value
zeptomc config set java.path /usr/bin/java

# Read a value
zeptomc config get java.path

# Delete a value (revert to default)
zeptomc config delete java.path
```

#### Environment variables

```bash
# Customize the data directory
export ZEPTOMC_ROOT=/my/path

zeptomc play  # Will use /my/path
```

### 📊 Recent optimizations

#### Dependency reduction (-60%)

**Before** :
- `click`, `requests`, `tqdm`, `coloredlogs`, `colorama` (5 dependencies)

**After** :
- `click`, `requests` (2 dependencies)

Old dependencies were replaced with:
- **ANSI colors** : Native implementation (standard ANSI codes)
- **Progress bars** : Minimal `ProgressBar` class

#### Project rename

Migration from `picomc` → `ZeptoMC` to better reflect the current project.

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
│   ├── config.py     # Global configuration
│   ├── instance.py   # Instance management
│   ├── mod.py        # Mod loaders
│   ├── play.py       # Launch game
│   ├── utils.py      # CLI utilities
│   └── version.py    # Versions
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
# Run all tests
./test.sh

# Test a specific command
./zeptomc instance list
./zeptomc account list
```

#### Commits

Commits follow this format:

```
feat: add a new feature
fix: fix a bug
refactor: refactor code
docs: update documentation
test: add/modify tests
```

### 📝 License

MIT - See [LICENSE](LICENSE)

### 🤝 Contributing

Contributions are welcome! Feel free to:
- Open an issue to report a bug
- Make a pull request to suggest an improvement
- Improve the documentation

### ℹ️ Notes

- This project is a fork of [picomc](https://github.com/samcavoj/picomc)
- Original author: Samuel Čavoj
- Current maintainer: Marmotton

---

**Last updated** : March 2026
