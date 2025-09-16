REPO_NAME := whisper-website
GIT_REV := $(shell git rev-parse --short HEAD)
OUTDIR := build

.PHONY: all zip tar clean

all: zip

$(OUTDIR):
	mkdir -p $(OUTDIR)

zip: $(OUTDIR)
	@echo "Creating zip of tracked files (HEAD)"
	git archive --format=zip -o $(OUTDIR)/$(REPO_NAME)-$(GIT_REV).zip HEAD
	@echo "Created $(OUTDIR)/$(REPO_NAME)-$(GIT_REV).zip"

tar: $(OUTDIR)
	@echo "Creating tar.gz of tracked files (HEAD)"
	git archive --format=tar HEAD | gzip > $(OUTDIR)/$(REPO_NAME)-$(GIT_REV).tar.gz
	@echo "Created $(OUTDIR)/$(REPO_NAME)-$(GIT_REV).tar.gz"

clean:
	rm -rf $(OUTDIR)
