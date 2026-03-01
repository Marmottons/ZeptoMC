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
- 🔨 Installer des mod loaders (Forge, Fabric, FTB)
- 📥 Installer des modpacks depuis CurseForge

### ✨ Caractéristiques

- **Minimaliste** : Seulement 2 dépendances (click, requests)
- **Léger** : ~230 KB de code source
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

# Lancer version et compte spécifiques
zeptomc play 1.20.1 --account MonsId

# Lancer une instance avec compte spécifique
zeptomc play my-instance --account MonsId
```

#### Gérer les instances

```bash
# Lister toutes les instances
zeptomc instance list

# Créer une nouvelle instance
zeptomc instance create my-instance

# Lancer une instance (alias pour 'play my-instance')
zeptomc instance launch my-instance

# Configurer une instance
zeptomc instance config my-instance

# Renommer une instance
zeptomc instance rename old-name new-name

# Supprimer une instance
zeptomc instance delete my-instance

# Extraire les ressources natives (pour débogage)
zeptomc instance natives my-instance

# Voir le répertoire de l'instance
zeptomc instance dir my-instance
```

#### Configurer Java pour une instance

```bash
# Changer le chemin Java pour une instance
zeptomc instance config my-instance java-path /usr/bin/java8

# Changer les arguments JVM pour une instance
zeptomc instance config my-instance java-args -XX:+UseG1GC -Xms512M -Xmx2G

# Voir la configuration d'une instance
zeptomc instance config my-instance show

# Voir une valeur spécifique
zeptomc instance config my-instance get java.path

# Supprimer une configuration
zeptomc instance config my-instance delete java.path
```

#### Gérer les comptes

ZeptoMC supporte deux types de comptes :
- **Offline** : Jouer en mode hors ligne, pas d'authentification requise
- **Microsoft** : Authentification Microsoft (compte Minecraft moderne)

```bash
# Lister tous les comptes
zeptomc account list

# Créer un compte offline
zeptomc account create mon-compte

# Créer et authentifier un compte Microsoft
zeptomc account authenticate mon-ms-compte

# Supprimer un compte
zeptomc account remove NomCompte

# Définir un compte par défaut
zeptomc account setdefault NomCompte
```

#### Gérer les versions Minecraft

```bash
# Lister les versions disponibles
zeptomc version list

# Télécharger une version
zeptomc version prepare 1.20.1
```

#### Mod loaders

```bash
# Installer Forge pour une version
zeptomc mod loader forge install 1.20.1

# Installer Fabric pour une version
zeptomc mod loader fabric install 1.20.1
```

#### Modpacks CurseForge

```bash
# Installer un modpack depuis son URL
zeptomc mod pack install https://...
```

#### Options globales

```bash
zeptomc --debug          # Mode debug (logs détaillés)
zeptomc --version        # Afficher la version
zeptomc -r /chemin       # Répertoire de données personnalisé
```

### 🔧 Configuration

Les données de ZeptoMC sont stockées dans :
- **Linux/macOS** : `~/.local/share/zeptomc/`
- **Windows** : `%APPDATA%\zeptomc\`

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
- 🔨 Install mod loaders (Forge, Fabric, FTB)
- 📥 Install modpacks from CurseForge

### ✨ Features

- **Minimal** : Only 2 dependencies (click, requests)
- **Lightweight** : ~230 KB of source code
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

# Launch specific version and account
zeptomc play 1.20.1 --account MyId

# Launch an instance with a specific account
zeptomc play my-instance --account MyId
```

#### Manage instances

```bash
# List all instances
zeptomc instance list

# Create a new instance
zeptomc instance create my-instance

# Launch an instance (alias for 'play my-instance')
zeptomc instance launch my-instance

# Configure an instance
zeptomc instance config my-instance

# Rename an instance
zeptomc instance rename old-name new-name

# Delete an instance
zeptomc instance delete my-instance

# Extract native resources (for debugging)
zeptomc instance natives my-instance

# Show instance directory
zeptomc instance dir my-instance
```

#### Configure Java for an instance

```bash
# Change the Java executable path for an instance
zeptomc instance config my-instance java-path /usr/bin/java8

# Change the JVM arguments for an instance
zeptomc instance config my-instance java-args -XX:+UseG1GC -Xms512M -Xmx2G

# Show the instance configuration
zeptomc instance config my-instance show

# Get a specific configuration value
zeptomc instance config my-instance get java.path

# Delete a configuration value
zeptomc instance config my-instance delete java.path
```

#### Manage accounts

ZeptoMC supports two types of accounts:
- **Offline** : Play in offline mode, no authentication required
- **Microsoft** : Microsoft authentication (modern Minecraft account)

```bash
# List all accounts
zeptomc account list

# Create an offline account
zeptomc account create my-account

# Create and authenticate a Microsoft account
zeptomc account authenticate my-ms-account

# Remove an account
zeptomc account remove AccountName

# Set a default account
zeptomc account setdefault AccountName
```

#### Manage Minecraft versions

```bash
# List available versions
zeptomc version list

# Download a version
zeptomc version prepare 1.20.1
```

#### Mod loaders

```bash
# Install Forge for a version
zeptomc mod loader forge install 1.20.1

# Install Fabric for a version
zeptomc mod loader fabric install 1.20.1
```

#### CurseForge modpacks

```bash
# Install a modpack from its URL
zeptomc mod pack install https://...
```

#### Global options

```bash
zeptomc --debug          # Debug mode (detailed logs)
zeptomc --version        # Show version
zeptomc -r /path         # Custom data directory
```

### 🔧 Configuration

ZeptoMC data is stored in:
- **Linux/macOS** : `~/.local/share/zeptomc/`
- **Windows** : `%APPDATA%\zeptomc\`

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
├── cli/              # CLI interface
│   ├── main.py       # Entry point
│   ├── account.py    # Account management
│   ├── instance.py   # Instance management
│   ├── play.py       # Launch game
│   ├── mod.py        # Mod loaders
│   ├── version.py    # Versions
│   └── config.py     # Configuration
├── mod/              # Mod loaders support
│   ├── forge.py
│   ├── fabric.py
│   ├── ftb.py
│   └── curse.py      # CurseForge
├── launcher.py       # Main class
├── account.py        # Authentication
├── version.py        # Version management
├── downloader.py     # Downloads
├── instance.py       # Instances
├── colors.py         # ANSI colors + ProgressBar
└── logging.py        # Custom logging
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
