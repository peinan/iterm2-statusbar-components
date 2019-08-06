CURRENT_DIR := $(shell echo `pwd`)
COMPONENT_DIR := components
INSTALL_PATH := ${HOME}/Library/Application Support/iTerm2/Scripts/AutoLaunch


.PHONY: install
install:
	mkdir -p "$(INSTALL_PATH)"
	for f in `ls $(COMPONENT_DIR)/*.py`; do ln -s "$(CURRENT_DIR)/$$f" "$(INSTALL_PATH)/`basename $$f`"; done
	ls "$(INSTALL_PATH)"

.PHONY: install-dryrun
install-dryrun:
	for f in `ls $(COMPONENT_DIR)/*.py`; do echo "ln -s '$(CURRENT_DIR)/$$f' '$(INSTALL_PATH)/`basename $$f`'"; done

.PHONY: uninstall
uninstall:
	for f in `ls $(COMPONENT_DIR)/*.py`; do unlink "$(INSTALL_PATH)/`basename $$f`"; done
	ls "$(INSTALL_PATH)"

.PHONY: uninstall-dryrun
uninstall-dryrun:
	for f in `ls $(COMPONENT_DIR)/*.py`; do echo "unlink '$(INSTALL_PATH)/`basename $$f`'"; done

