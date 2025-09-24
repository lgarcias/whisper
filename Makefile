SHELL := /bin/bash
REPO_NAME := whisper-website
GIT_REV := $(shell git rev-parse --short HEAD 2>/dev/null || echo nogit)
OUTDIR := build
STAMP := $(shell date +%Y%m%d-%H%M%S)

ZIP := $(shell command -v zip 2>/dev/null)
GIT := $(shell command -v git 2>/dev/null)

.PHONY: all help clean zip zip-all ensure-tools ensure-outdir print-info

all: zip

help:
	@echo "Targets:"
	@echo "  make zip      -> Solo tracked (HEAD)"
	@echo "  make zip-all  -> Tracked + untracked (respeta .gitignore)"
	@echo "  make clean    -> Borra build/"
	@echo "  make print-info -> Info de entorno"

print-info:
	@echo "Usuario: $$(id -un)  Grupo: $$(id -gn)"
	@echo "pwd: $$(pwd)"
	@echo "OUTDIR: $(OUTDIR)"
	@echo "REPO_NAME: $(REPO_NAME)"
	@echo "GIT_REV: $(GIT_REV)"
	@echo "ZIP bin: $(ZIP)"
	@echo "GIT bin: $(GIT)"
	@echo "CRLF en Makefile? $$(grep -U $$'\\r' -q Makefile && echo SI || echo NO)"

ensure-tools:
	@if [ -z "$(GIT)" ]; then echo "ERROR: git no está disponible."; exit 1; fi
	@if [ -z "$(ZIP)" ]; then echo "ERROR: falta 'zip'. Instala: sudo apt-get update && sudo apt-get install -y zip"; exit 1; fi

ensure-outdir:
	@mkdir -p "$(OUTDIR)"
	@chown "$$(id -un):$$(id -gn)" "$(OUTDIR)" 2>/dev/null || true

zip: ensure-tools ensure-outdir
	@echo "Creando zip (tracked HEAD)…"
	@out="$(OUTDIR)/$(REPO_NAME)-$(GIT_REV)-$(STAMP).zip"; \
	echo " -> $$out"; \
	git archive --format=zip -o "$$out" HEAD; \
	echo "OK: $$out"

zip-all: ensure-tools ensure-outdir
	@echo "Creando zip (tracked + untracked, respeta .gitignore)…"
	@out="$(OUTDIR)/$(REPO_NAME)-$(GIT_REV)-$(STAMP)-all.zip"; \
	echo " -> $$out"; \
	git rev-parse --is-inside-work-tree >/dev/null || { echo "ERROR: no es un repo git."; exit 1; }; \
	tmplist=$$(mktemp); \
	git ls-files -co --exclude-standard > "$$tmplist"; \
	if [ ! -s "$$tmplist" ]; then echo "Nada que empaquetar (lista vacía)"; rm -f "$$tmplist"; exit 1; fi; \
	zip -q "$$out" -@ < "$$tmplist"; \
	rm -f "$$tmplist"; \
	echo "OK: $$out"

clean:
	@echo "Eliminando '$(OUTDIR)/'…"
	@rm -rf "$(OUTDIR)"
	@echo "Listo."
