CURRENT_DIR := $(shell echo `pwd`)
COMPONENT_CLOCK := clock
COMPONENT_DISKUSAGE := diskusage
COMPONENT_WEATHERINFO := weatherinfo
COMPONENT_ALL := $(COMPONENT_CLOCK) $(COMPONENT_DISKUSAGE) $(COMPONENT_WEATHERINFO)
INSTALL_PATH := ${HOME}/Library/Application Support/iTerm2/Scripts/AutoLaunch


.PHONY: install-all
install-all:
	mkdir -p "$(INSTALL_PATH)"
	cp -r  $(COMPONENT_ALL) $(INSTALL_PATH)
	ls "$(INSTALL_PATH)"

.PHONY: install-clock
install-clock:
	mkdir -p "$(INSTALL_PATH)"
	cp -r  $(COMPONENT_CLOCK) "$(INSTALL_PATH)"
	ls "$(INSTALL_PATH)"

.PHONY: uninstall-all
uninstall:
	for dir in $(COMPONENT_ALL); do rm -rf $(INSTALL_PATH)/$$dir; done
	ls "$(INSTALL_PATH)"

.PHONY: test
test:
	echo $(COMPONENT_ALL)
	for dir in $(COMPONENT_ALL); do echo $(INSTALL_PATH)/$$dir; done
