REPO_NAME := whisper-website
GIT_REV := $(shell git rev-parse --short HEAD)
OUTDIR := build

ZIP_NAME := $(OUTDIR)/$(REPO_NAME)-$(GIT_REV).zip
ZIP_NAME_ALL := $(OUTDIR)/$(REPO_NAME)-$(GIT_REV)-all.zip

.PHONY: all zip zip-all

all: zip

$(OUTDIR):
	mkdir -p $(OUTDIR)

zip: $(OUTDIR)
	@echo "Creating zip of tracked files (HEAD)"
	@git archive --format=zip -o "$(ZIP_NAME)" HEAD
	@echo "Created $(ZIP_NAME)"

zip-all: $(OUTDIR)
	@echo "Creating zip of tracked + untracked (respecting .gitignore)"
	@rm -f "$(ZIP_NAME_ALL)"
	@git ls-files -z --cached --others --exclude-standard \
	| grep -zvE '^$(OUTDIR)(/|$$)' \
	| xargs -0 -I{} zip -q -r "$(ZIP_NAME_ALL)" "{}"
	@echo "Created $(ZIP_NAME_ALL)"