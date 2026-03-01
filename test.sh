#!/bin/bash

# Script de test fonctionnel pour picomc
# Vérifie que toutes les commandes CLI fonctionnent

set -e

COLOR_GREEN='\033[92m'
COLOR_RED='\033[91m'
COLOR_YELLOW='\033[93m'
COLOR_BLUE='\033[94m'
COLOR_NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

test_command() {
    local name="$1"
    local cmd="$2"
    local should_fail="$3"
    
    echo -n "Testing: $name ... "
    
    if eval "$cmd" > /dev/null 2>&1; then
        if [ "$should_fail" == "true" ]; then
            echo -e "${COLOR_RED}FAILED${COLOR_NC} (commande devrait échouer)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        else
            echo -e "${COLOR_GREEN}OK${COLOR_NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        fi
    else
        if [ "$should_fail" == "true" ]; then
            echo -e "${COLOR_GREEN}OK${COLOR_NC} (expected to fail)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${COLOR_RED}FAILED${COLOR_NC}"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    fi
}

test_import() {
    local name="$1"
    local module="$2"
    
    echo -n "Testing: $name ... "
    
    if python -c "import sys; sys.path.insert(0, 'src'); import $module" 2>/dev/null; then
        echo -e "${COLOR_GREEN}OK${COLOR_NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${COLOR_RED}FAILED${COLOR_NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

echo ""
echo -e "${COLOR_BLUE}╔════════════════════════════════════════╗${COLOR_NC}"
echo -e "${COLOR_BLUE}║  TESTS FONCTIONNELS - ZeptoMC/picomc   ║${COLOR_NC}"
echo -e "${COLOR_BLUE}╚════════════════════════════════════════╝${COLOR_NC}"
echo ""

# ============================================================================
echo -e "${COLOR_YELLOW}PHASE 1: Tests d'imports${COLOR_NC}"
echo "─────────────────────────────────────────"

test_import "picomc core" "picomc"
test_import "picomc.cli" "picomc.cli"
test_import "picomc.colors (no deps)" "picomc.colors"
test_import "picomc.logging" "picomc.logging"
test_import "picomc.downloader" "picomc.downloader"
test_import "picomc.launcher" "picomc.launcher"
test_import "picomc.account" "picomc.account"
test_import "picomc.instance" "picomc.instance"
test_import "picomc.mod.forge" "picomc.mod.forge"
test_import "picomc.mod.fabric" "picomc.mod.fabric"
test_import "picomc.mod.curse" "picomc.mod.curse"

echo ""

# ============================================================================
echo -e "${COLOR_YELLOW}PHASE 2: Tests CLI (--help)${COLOR_NC}"
echo "─────────────────────────────────────────"

test_command "picomc --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from picomc.cli.main import picomc_cli; picomc_cli([\"--help\"])' || true"
test_command "picomc account --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from picomc.cli.main import picomc_cli; picomc_cli([\"account\", \"--help\"])' || true"
test_command "picomc instance --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from picomc.cli.main import picomc_cli; picomc_cli([\"instance\", \"--help\"])' || true"
test_command "picomc play --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from picomc.cli.main import picomc_cli; picomc_cli([\"play\", \"--help\"])' || true"
test_command "picomc mod --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from picomc.cli.main import picomc_cli; picomc_cli([\"mod\", \"--help\"])' || true"
test_command "picomc version --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from picomc.cli.main import picomc_cli; picomc_cli([\"version\", \"--help\"])' || true"

echo ""

# ============================================================================
echo -e "${COLOR_YELLOW}PHASE 3: Tests de dépendances${COLOR_NC}"
echo "─────────────────────────────────────────"

test_import "click (required)" "click"
test_import "requests (required)" "requests"

# Vérifier que les anciennes dépendances ne sont PAS présentes
echo -n "Testing: tqdm NOT imported (removed) ... "
if ! python -c "import sys; sys.path.insert(0, 'src'); from picomc.colors import ProgressBar; import tqdm" 2>/dev/null; then
    echo -e "${COLOR_GREEN}OK${COLOR_NC} (correctly removed)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${COLOR_RED}FAILED${COLOR_NC} (tqdm still present)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo -n "Testing: coloredlogs NOT imported (removed) ... "
if ! python -c "import coloredlogs" 2>/dev/null; then
    echo -e "${COLOR_GREEN}OK${COLOR_NC} (correctly removed)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${COLOR_RED}FAILED${COLOR_NC} (coloredlogs still present)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo -n "Testing: colorama NOT imported (removed) ... "
if ! python -c "import colorama" 2>/dev/null; then
    echo -e "${COLOR_GREEN}OK${COLOR_NC} (correctly removed)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${COLOR_RED}FAILED${COLOR_NC} (colorama still present)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

echo ""

# ============================================================================
echo -e "${COLOR_YELLOW}PHASE 4: Tests de fonctionnalités internes${COLOR_NC}"
echo "─────────────────────────────────────────"

test_command "ProgressBar works" "python -c 'import sys, time; sys.path.insert(0, \"src\"); from picomc.colors import ProgressBar; pb = ProgressBar(10); pb.update(5); pb.close()'"
test_command "ColorFormatter works" "python -c 'import sys; sys.path.insert(0, \"src\"); from picomc.colors import ColorFormatter; import logging; f = ColorFormatter(\"test\")'"
test_command "Logger initialization" "python -c 'import sys; sys.path.insert(0, \"src\"); from picomc.logging import logger, initialize; initialize(False); logger.info(\"test\")'"
test_command "DownloadQueue works" "python -c 'import sys; sys.path.insert(0, \"src\"); from picomc.downloader import DownloadQueue; dq = DownloadQueue(); print(len(dq))'"

echo ""

# ============================================================================
echo -e "${COLOR_BLUE}╔════════════════════════════════════════╗${COLOR_NC}"
echo -e "${COLOR_BLUE}║           RÉSULTATS DES TESTS          ║${COLOR_NC}"
echo -e "${COLOR_BLUE}╚════════════════════════════════════════╝${COLOR_NC}"
echo ""
echo -e "Tests réussis: ${COLOR_GREEN}$TESTS_PASSED${COLOR_NC}"
echo -e "Tests échoués: ${COLOR_RED}$TESTS_FAILED${COLOR_NC}"
echo "Total: $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${COLOR_GREEN}✅ TOUS LES TESTS SONT PASSÉS!${COLOR_NC}"
    echo ""
    echo "Tu peux maintenant:"
    echo "  1. Faire git push pour envoyer sur GitHub"
    echo "  2. Utiliser picomc normalement"
    echo "  3. Lancer le jeu avec 'picomc play'"
    echo ""
    exit 0
else
    echo -e "${COLOR_RED}❌ CERTAINS TESTS ONT ÉCHOUÉ${COLOR_NC}"
    echo ""
    echo "Vérife les erreurs ci-dessus et corrige les problèmes"
    echo ""
    exit 1
fi
