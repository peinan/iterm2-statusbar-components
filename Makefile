CURRENT_DIR := $(shell echo `pwd`)
COMPONENT_DIR := components
INSTALL_PATH := ${HOME}/Library/Application Support/iTerm2/Scripts/AutoLaunch


.PHONY: install-all
install-all:
	mkdir -p "$(INSTALL_PATH)"
	cp $(COMPONENT_DIR)/* "$(INSTALL_PATH)"
	ls "$(INSTALL_PATH)"

.PHONY: install-clock
install-clock:
	mkdir -p "$(INSTALL_PATH)"
	cp $(COMPONENT_DIR)/clock.py "$(INSTALL_PATH)"
	ls "$(INSTALL_PATH)"

.PHONY: install-diskusage
install-diskusage:
	mkdir -p "$(INSTALL_PATH)"
	cp $(COMPONENT_DIR)/diskusage.py "$(INSTALL_PATH)"
	ls "$(INSTALL_PATH)"

.PHONY: install-weather
install-weather:
	mkdir -p "$(INSTALL_PATH)"
	cp $(COMPONENT_DIR)/weatherinfo.py "$(INSTALL_PATH)"
	cp $(COMPONENT_DIR)/config.json "$(INSTALL_PATH)"
	ls "$(INSTALL_PATH)"

.PHONY: uninstall-all
uninstall:
	for f in $$(ls $(COMPONENT_DIR)); do rm -r "$(INSTALL_PATH)/$$f"; done
	ls "$(INSTALL_PATH)"

.PHONY: test
test:
	for f in $$(ls $(COMPONENT_DIR)); do echo "$(INSTALL_PATH)/$$f"; done
