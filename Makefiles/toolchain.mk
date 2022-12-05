MAKEFILES_DIR := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))
BUILD_PROJ_DIR := $(shell dirname $(MAKEFILES_DIR))
REPO_ROOT := $(shell dirname $(BUILD_PROJ_DIR))

toolchains/debug:
	@echo 'MAKEFILES_DIR: ' $(MAKEFILES_DIR)
	@echo 'BUILD_PROJ_DIR: ' $(BUILD_PROJ_DIR)
	@echo 'REPO_ROOT: ' $(REPO_ROOT)

PYTHON ?= python3
V ?= 0
TOOLCHAIN_NODE_VERSION ?= 16.18.1

include $(MAKEFILES_DIR)/platform.mk

TEMP_DIR = $(BUILD_PROJ_DIR)/.tmp
TOOLCHAINS_DIR = $(BUILD_PROJ_DIR)/toolchains
NODEJS_MIRROR = https://cdn.npm.taobao.org/dist/node
TOOLCHAIN_NODE_FULL_NAME = node-v$(TOOLCHAIN_NODE_VERSION)-$(PLATFORM)-$(ARCH)
TOOLCHAIN_NODE_BIN_DIRECTORY = $(TOOLCHAINS_DIR)/node/bin
TOOLCHAIN_NODE_BIN = $(TOOLCHAIN_NODE_BIN_DIRECTORY)/node
TOOLCHAIN_NODE_README = $(TOOLCHAIN_NODE_BIN_DIRECTORY)/../README.md
TOOLCHAIN_NPM_BIN = $(TOOLCHAIN_NODE_BIN_DIRECTORY)/npm
TOOLCHAIN_NPM_PREFIX = $(TOOLCHAINS_DIR)/npm
TOOLCHAIN_NPM_PREFIX_BIN = $(TOOLCHAINS_DIR)/npm/bin
TOOLCHAIN_PROTOC = $(TOOLCHAINS_DIR)/protoc/protoc
BUILD_NODE_MODULES = $(BUILD_PROJ_DIR)/node_modules
BUILD_NODE_MODULES_BIN = $(BUILD_NODE_MODULES)/.bin

GYP=$(REPO_ROOT)/vendor/gyp-next/gyp_main.py
CPPLINT=$(REPO_ROOT)/vendor/cpplint/cpplint.py
ESLINT=$(BUILD_NODE_MODULES_BIN)/eslint
TYPEDOC=$(BUILD_NODE_MODULES_BIN)/typedoc
CLANG_FORMAT=$(BUILD_NODE_MODULES_BIN)/clang-format

export PATH := $(BUILD_NODE_MODULES_BIN):$(TOOLCHAIN_NODE_BIN_DIRECTORY):$(PATH)

ifndef GENERATOR
ifeq (,$(wildcard $(BUILD_PROJ_DIR)/out/Makefile))
GENERATOR=ninja
else
GENERATOR=make
endif
endif

NINJA_PARAMS=
ifeq ($(V), 1)
NINJA_PARAMS+=--verbose
endif

SHASUM=sha256sum
ifeq ($(PLATFORM),darwin)
	SHASUM=shasum
endif

# OSX doesn't have xz installed by default, http://macpkg.sourceforge.net/
HAS_XZ ?= $(shell which xz > /dev/null 2>&1; [ $$? -eq 0 ] && echo 1 || echo 0)
# Supply SKIP_XZ=1 to explicitly skip .tar.xz creation
SKIP_XZ ?= 0

export PATH := $(shell pwd)/$(TOOLCHAIN_NODE_BIN_DIRECTORY):$(PATH)

$(TEMP_DIR):
	mkdir -p $(TEMP_DIR)

$(TOOLCHAINS_DIR):
	mkdir -p $(TOOLCHAINS_DIR)
	mkdir -p $(TOOLCHAIN_NPM_PREFIX)

.PHONY: toolchains/node
toolchains/node: $(TOOLCHAIN_NODE_BIN)
$(TOOLCHAIN_NODE_BIN): | $(TEMP_DIR) $(TOOLCHAINS_DIR)
	@if [ "$(shell $(TOOLCHAIN_NODE_BIN) --version 2> /dev/null)" != 'v$(TOOLCHAIN_NODE_VERSION)' ]; then \
		$(RM) -r $(TOOLCHAINS_DIR)/node; \
		echo "Downloading Node.js v$(TOOLCHAIN_NODE_VERSION)..."; \
		curl -L -s -o $(TEMP_DIR)/$(TOOLCHAIN_NODE_FULL_NAME).tar.gz $(NODEJS_MIRROR)/v$(TOOLCHAIN_NODE_VERSION)/$(TOOLCHAIN_NODE_FULL_NAME).tar.gz || exit 1; \
			cd $(TEMP_DIR); \
			curl -L $(NODEJS_MIRROR)/v$(TOOLCHAIN_NODE_VERSION)/SHASUMS256.txt 2>/dev/null | grep $(TOOLCHAIN_NODE_FULL_NAME).tar.gz | $(SHASUM) -c || exit 1; \
			cd -; \
		echo "Pouring Node.js v$(TOOLCHAIN_NODE_VERSION) to toolchains dir..."; \
		tar zxf $(TEMP_DIR)/$(TOOLCHAIN_NODE_FULL_NAME).tar.gz -C $(TOOLCHAINS_DIR); \
		mv $(TOOLCHAINS_DIR)/$(TOOLCHAIN_NODE_FULL_NAME) $(TOOLCHAINS_DIR)/node; \
		rm $(TEMP_DIR)/$(TOOLCHAIN_NODE_FULL_NAME).tar.gz; \
	else \
		echo "Using Node.js v$(TOOLCHAIN_NODE_VERSION)..."; \
	fi

$(BUILD_NODE_MODULES): $(BUILD_PROJ_DIR)/package.json | $(TOOLCHAIN_NODE_BIN)
	cd $(BUILD_PROJ_DIR); \
		$(TOOLCHAIN_NPM_BIN) install
	touch $@

$(ESLINT): $(BUILD_NODE_MODULES)
$(TYPEDOC): $(BUILD_NODE_MODULES)
$(CLANG_FORMAT): $(BUILD_NODE_MODULES)

$(BUILD_PROJ_DIR)/config.gypi:
	if [ ! -f $(BUILD_PROJ_DIR)/config.gypi ]; then cd $(BUILD_PROJ_DIR); ./configure; fi

$(TOOLCHAINS_DIR)/protoc/out/Makefile $(TOOLCHAINS_DIR)/protoc/out/Release/build.ninja: \
	$(BUILD_PROJ_DIR)/config.gypi \
	$(BUILD_PROJ_DIR)/projects.gypi \
	$(BUILD_PROJ_DIR)/common.gypi \
	$(BUILD_PROJ_DIR)/config.gypi \
	$(BUILD_PROJ_DIR)/gypfiles/protobuf.gyp
	cd $(BUILD_PROJ_DIR); $(PYTHON) $(GYP) \
		--depth=.. \
		--generator-output=./build/toolchains/protoc/out \
		-Goutput_dir=. \
		-Iprojects.gypi \
		-Icommon.gypi \
		-Iconfig.gypi \
		-f$(GENERATOR) \
		-Dbuild_type=$(BUILDTYPE) \
		gypfiles/protobuf.gyp

ifeq ($(GENERATOR), make)
$(TOOLCHAIN_PROTOC): $(TOOLCHAINS_DIR)/protoc/out/Makefile
else
$(TOOLCHAIN_PROTOC): $(TOOLCHAINS_DIR)/protoc/out/Release/build.ninja
endif
$(TOOLCHAIN_PROTOC):
	@if [ "$(GENERATOR)" = 'make' ]; then \
		$(MAKE) -C $(BUILD_PROJ_DIR)/toolchains/protoc/out BUILDTYPE=Release V=$(V) protoc; \
	else \
		ninja -C $(BUILD_PROJ_DIR)/toolchains/protoc/out/Release protoc $(NINJA_PARAMS); \
	fi
	if [ ! -e $(BUILD_PROJ_DIR)/toolchains/protoc/protoc ]; then \
		cp $(BUILD_PROJ_DIR)/toolchains/protoc/out/Release/protoc $(BUILD_PROJ_DIR)/toolchains/protoc/protoc; fi
	touch $@

clean-node-modules:
	rm -rf $(BUILD_PROJ_DIR)/node_modules
.PHONY: clean-node-modules

ifeq ($(SKIP_XZ), 1)
check-xz:
	@echo "SKIP_XZ=1 supplied, skipping .tar.xz creation"
else
ifeq ($(HAS_XZ), 1)
check-xz:
else
check-xz:
	@echo "No xz command, cannot continue"
	@exit 1
endif
endif
