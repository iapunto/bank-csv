.PHONY: help install install-dev test test-cov lint format clean run setup

# Variables
PYTHON = python3
PIP = pip3
PACKAGE_NAME = bank-csv-extractor

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias de producción
	$(PIP) install -r requirements.txt

install-dev: ## Instalar dependencias de desarrollo
	$(PIP) install -r requirements.txt
	$(PIP) install pre-commit
	pre-commit install

setup: ## Configurar el proyecto (instalar dependencias y hooks)
	@echo "Configurando el proyecto..."
	$(MAKE) install-dev
	@echo "Proyecto configurado correctamente"

test: ## Ejecutar tests
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Ejecutar tests con cobertura
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

lint: ## Ejecutar linters
	@echo "Ejecutando flake8..."
	$(PYTHON) -m flake8 src/ tests/
	@echo "Ejecutando mypy..."
	$(PYTHON) -m mypy src/

format: ## Formatear código
	@echo "Formateando con black..."
	$(PYTHON) -m black src/ tests/ config/
	@echo "Organizando imports con isort..."
	$(PYTHON) -m isort src/ tests/ config/

check: ## Verificar formato y linting
	@echo "Verificando formato..."
	$(PYTHON) -m black --check src/ tests/ config/
	@echo "Verificando imports..."
	$(PYTHON) -m isort --check-only src/ tests/ config/
	@echo "Ejecutando linting..."
	$(MAKE) lint

clean: ## Limpiar archivos generados
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "app.log" -delete
	rm -rf build/ dist/

run: ## Ejecutar la aplicación
	$(PYTHON) main.py

run-dev: ## Ejecutar en modo desarrollo
	$(PYTHON) -m pytest tests/ -v
	$(MAKE) run

build: ## Construir el paquete
	$(PYTHON) -m build

install-local: ## Instalar el paquete localmente
	$(PIP) install -e .

uninstall: ## Desinstalar el paquete local
	$(PIP) uninstall $(PACKAGE_NAME) -y

docs: ## Generar documentación
	@echo "Generando documentación..."
	$(PYTHON) -m pydoc -w src/
	@echo "Documentación generada en el directorio actual"

security: ## Verificar seguridad del código
	$(PYTHON) -m bandit -r src/

all: clean install-dev check test run ## Ejecutar todo el pipeline
