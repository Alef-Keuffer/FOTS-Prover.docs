# Minimal makefile for Sphinx documentation
#
SHELL := /bin/bash
# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

LOADENV = ". ../venv/bin/activate"
SOURCECODE = "../src/"

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@rm -r -f _build/html docs
	@"$(LOADENV)"; $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@cp -a _build/html/. docs

apidoc:
	@"$(LOADENV)"; sphinx-apidoc -o "$(BUILDDIR)" "$(SOURCECODE)" --separate

github:
	@make html
	@git add .
	@git commit -m .
	@git push
