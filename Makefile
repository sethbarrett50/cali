SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

UV    ?= uv
RUFF  ?= ruff
PY    ?= python

JAVA  ?= java
JAVAC ?= javac
KEYTOOL ?= keytool

ANDROID_PYTHON ?= 3.11

.PHONY: \
	help sync sync.mobile venv.mobile \
	lint format check test run sample build clean preflight deps.check \
	java.check android.check android.debug android.clean android.logcat

help: ## Show targets
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

sync: ## Install/sync deps (including dev group)
	$(UV) sync --dev

sync.mobile: ## Install/sync deps for Android/Kivy mobile build
	UV_VENV_SEED=1 $(UV) sync --python $(ANDROID_PYTHON) --group mobile --dev

venv.mobile: ## Recreate uv venv for Android/Kivy with pip seeded
	rm -rf .venv
	$(UV) python pin $(ANDROID_PYTHON)
	$(UV) venv --python $(ANDROID_PYTHON) --seed
	$(UV) sync --python $(ANDROID_PYTHON) --group mobile --dev
	$(UV) run python -m pip --version

format: ## Format code
	$(UV) run $(RUFF) format .

check: ## Lint (no fixes)
	$(UV) run $(RUFF) check .

lint: ## Format + lint with fixes
	$(UV) run $(RUFF) format .
	$(UV) run $(RUFF) check . --fix

test: ## Run tests
	$(UV) run pytest -q

build: ## Build sdist/wheel
	$(UV) build

clean: ## Remove build artifacts
	rm -rf dist build *.egg-info
	rm -rf src/*.egg-info
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov

preflight: ## Build + run twine metadata checks
	$(UV) build
	$(UV) tool run twine check dist/*

deps.check: ## Check for dependency issues
	$(UV) run deptry .

java.check: ## Check Java/JDK tools needed by Buildozer
	@command -v $(JAVA) >/dev/null || { echo "Missing java. Install openjdk-17-jdk."; exit 1; }
	@command -v $(JAVAC) >/dev/null || { echo "Missing javac. Install openjdk-17-jdk."; exit 1; }
	@command -v $(KEYTOOL) >/dev/null || { echo "Missing keytool. Install openjdk-17-jdk."; exit 1; }
	@echo "java:    $$($(JAVA) -version 2>&1 | head -n 1)"
	@echo "javac:   $$($(JAVAC) -version 2>&1 | head -n 1)"
	@echo "keytool: $$(command -v $(KEYTOOL))"

android.check: java.check ## Check Android/Kivy build prerequisites
	$(UV) run python -m pip --version
	$(UV) run buildozer --version

android.debug: android.check ## Build Android debug APK with Buildozer
	$(UV) run buildozer android debug

android.clean: ## Clean Buildozer Android build artifacts
	rm -rf .buildozer/android/platform
	rm -rf .buildozer/android/app
	rm -rf bin/*.apk bin/*.aab

android.logcat: ## Show Android logs filtered for Python/Kivy
	adb logcat | grep -Ei 'python|kivy|cali|buildozer'