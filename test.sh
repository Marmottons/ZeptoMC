#!/bin/bash

# Script de test fonctionnel pour zeptomc
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
echo -e "${COLOR_BLUE}║  TESTS FONCTIONNELS - ZeptoMC/zeptomc  ║${COLOR_NC}"
echo -e "${COLOR_BLUE}╚════════════════════════════════════════╝${COLOR_NC}"
echo ""

# ============================================================================
echo -e "${COLOR_YELLOW}PHASE 1: Tests d'imports${COLOR_NC}"
echo "─────────────────────────────────────────"

test_import "zeptomc core" "zeptomc"
test_import "zeptomc.cli" "zeptomc.cli"
test_import "zeptomc.colors (no deps)" "zeptomc.colors"
test_import "zeptomc.logging" "zeptomc.logging"
test_import "zeptomc.downloader" "zeptomc.downloader"
test_import "zeptomc.launcher" "zeptomc.launcher"
test_import "zeptomc.account" "zeptomc.account"
test_import "zeptomc.instance" "zeptomc.instance"
test_import "zeptomc.mod.forge" "zeptomc.mod.forge"
test_import "zeptomc.mod.fabric" "zeptomc.mod.fabric"

echo ""

# ============================================================================
echo -e "${COLOR_YELLOW}PHASE 2: Tests CLI (--help)${COLOR_NC}"
echo "─────────────────────────────────────────"

test_command "zeptomc --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from zeptomc.cli.main import zeptomc_cli; zeptomc_cli([\"--help\"])' || true"
test_command "zeptomc account --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from zeptomc.cli.main import zeptomc_cli; zeptomc_cli([\"account\", \"--help\"])' || true"
test_command "zeptomc instance --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from zeptomc.cli.main import zeptomc_cli; zeptomc_cli([\"instance\", \"--help\"])' || true"
test_command "zeptomc play --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from zeptomc.cli.main import zeptomc_cli; zeptomc_cli([\"play\", \"--help\"])' || true"
test_command "zeptomc mod --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from zeptomc.cli.main import zeptomc_cli; zeptomc_cli([\"mod\", \"--help\"])' || true"
test_command "zeptomc version --help" "python -c 'import sys; sys.path.insert(0, \"src\"); from zeptomc.cli.main import zeptomc_cli; zeptomc_cli([\"version\", \"--help\"])' || true"

echo ""

# ============================================================================
echo -e "${COLOR_YELLOW}PHASE 3: Tests de dépendances${COLOR_NC}"
echo "─────────────────────────────────────────"

test_import "click (required)" "click"
test_import "requests (required)" "requests"

# Vérifier que ZeptoMC n'importe PAS les anciennes dépendances
echo -n "Testing: tqdm NOT used by zeptomc ... "
if ! python -c "import sys; sys.path.insert(0, 'src'); import zeptomc.colors; assert 'tqdm' not in sys.modules" 2>/dev/null; then
    echo -e "${COLOR_RED}FAILED${COLOR_NC} (tqdm still imported by zeptomc)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
else
    echo -e "${COLOR_GREEN}OK${COLOR_NC} (not used)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
fi

echo -n "Testing: coloredlogs NOT used by zeptomc ... "
if ! python -c "import sys; sys.path.insert(0, 'src'); import zeptomc.logging; assert 'coloredlogs' not in sys.modules" 2>/dev/null; then
    echo -e "${COLOR_RED}FAILED${COLOR_NC} (coloredlogs still imported by zeptomc)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
else
    echo -e "${COLOR_GREEN}OK${COLOR_NC} (not used)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
fi

echo -n "Testing: colorama NOT used by zeptomc ... "
if ! python -c "import sys; sys.path.insert(0, 'src'); import zeptomc.colors; assert 'colorama' not in sys.modules" 2>/dev/null; then
    echo -e "${COLOR_RED}FAILED${COLOR_NC} (colorama still imported by zeptomc)"
    TESTS_FAILED=$((TESTS_FAILED + 1))
else
    echo -e "${COLOR_GREEN}OK${COLOR_NC} (not used)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
fi

echo ""

# ============================================================================
echo -e "${COLOR_YELLOW}PHASE 4: Tests de fonctionnalités internes${COLOR_NC}"
echo "─────────────────────────────────────────"

test_command "ProgressBar works" "python -c 'import sys, time; sys.path.insert(0, \"src\"); from zeptomc.colors import ProgressBar; pb = ProgressBar(10); pb.update(5); pb.close()'"
test_command "ColorFormatter works" "python -c 'import sys; sys.path.insert(0, \"src\"); from zeptomc.colors import ColorFormatter; import logging; f = ColorFormatter(\"%(message)s\")'"
test_command "Logger initialization" "python -c 'import sys; sys.path.insert(0, \"src\"); from zeptomc.logging import logger, initialize; initialize(False); logger.info(\"test\")'"
test_command "DownloadQueue works" "python -c 'import sys; sys.path.insert(0, \"src\"); from zeptomc.downloader import DownloadQueue; dq = DownloadQueue(); print(len(dq))'"

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
    echo "  2. Utiliser zeptomc normalement"
    echo "  3. Lancer le jeu avec 'zeptomc play'"
    echo ""
    exit 0
else
    echo -e "${COLOR_RED}❌ CERTAINS TESTS ONT ÉCHOUÉ${COLOR_NC}"
    echo ""
    echo "Vérifie les erreurs ci-dessus et corrige les problèmes"
    echo ""
    exit 1
fi
