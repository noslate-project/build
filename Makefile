BUILDTYPE ?= Release
all: build

include ./Makefiles/platform.mk
include ./Makefiles/toolchain.mk

GYP_FILE=noslate.gyp
GYP_FILES=$(shell find .. -type d \( -name stron-build -o -name node_modules \) -prune -false -o -name '*.gyp' -o -name '*.gypi')

TARGETS=aworker aworker_cctest node
DEBUG_TARGETS=$(foreach target,$(TARGETS),$(target)_g)

NOSLATED_ARCHIVE_PATHS =
NOSLATED_ARCHIVE_FILES =
ARCHIVE_PATHS = bin node_modules package.json build
ARCHIVE_BINS = aworker aworker.shell node
ARCHIVE_TURF_PRODUCTS=turf turf.debug libturf.so libturf.so.debug
ifneq ($(PLATFORM),linux)
ARCHIVE_TURF_PRODUCTS=turf
endif

paths:
	$(eval NOSLATED_ARCHIVE_PATHS := $(shell $(TOOLCHAIN_NODE_BIN) -p 'require("../noslated/package.json").files.join("\n")') $(NOSLATED_ARCHIVE_PATHS))
	$(eval NOSLATED_ARCHIVE_FILES := $(shell $(TOOLCHAIN_NODE_BIN) -p 'require("../noslated/package.json").files.filter(it => !it.includes("/")).join("\n")') $(NOSLATED_ARCHIVE_FILES))
	$(eval ARCHIVE_PATHS := $(NOSLATED_ARCHIVE_FILES) $(ARCHIVE_PATHS))

.PHONY: build
build: noslate turf paths
	mkdir -p ../out && mkdir -p ../out/bin && mkdir -p ../out/archives
	$(TOOLCHAIN_NODE_BIN) tools/package-json-git-version.js ../noslated ../out/package.json
	mkdir -p $(foreach path,$(NOSLATED_ARCHIVE_PATHS),../out/$(shell dirname $(path)))
	for path in $(NOSLATED_ARCHIVE_PATHS); do cp -r ../noslated/$$path ../out/$$path; done
	cp -r $(foreach product,$(ARCHIVE_BINS),./out/$(BUILDTYPE)/$(product)) ../out/bin
	cp -r $(foreach product,$(ARCHIVE_TURF_PRODUCTS),../turf/build/$(product)) ../out/bin
	cd ../out; \
		$(TOOLCHAIN_NPM_BIN) install --production --nodedir=$(REPO_ROOT)/node; \
		tar -czf archives/noslate-$(PLATFORM)-$(UNAME_M)-$${BUILD_ID:=trunk}.tar.gz $(ARCHIVE_PATHS);

.PHONY: noslate $(TARGETS) $(DEBUG_TARGETS)
noslate $(TARGETS): BUILDTYPE=Release
noslate $(TARGETS) $(DEBUG_TARGETS): $(TOOLCHAIN_PROTOC) $(TOOLCHAIN_NODE_BIN) $(BUILD_NODE_MODULES) | configure
noslate:
	ninja -C out/$(BUILDTYPE) $(NINJA_PARAMS)
	$(MAKE) -C ../noslated BUILDTYPE=$(BUILDTYPE)

$(TARGETS) $(DEBUG_TARGETS): $(TOOLCHAIN_PROTOC) $(TOOLCHAIN_NODE_BIN) | configure
	ninja -C out/$(BUILDTYPE) $(NINJA_PARAMS) $(subst _g,,$@)

turf:
	$(MAKE) -C ../turf;

NODE_DIR=../node
node-prepare:
	cd $(NODE_DIR); ./configure --ninja

configure: | out/$(BUILDTYPE)/build.ninja
out/Makefile out/$(BUILDTYPE)/build.ninja: $(GYP_FILE) $(GYP_FILES) $(BUILD_PROJ_DIR)/config.gypi | node-prepare
	$(GYP) \
		--depth=.. \
		--generator-output=./build/out \
		-Goutput_dir=. \
		-I$(NODE_DIR)/common.gypi \
		-I$(NODE_DIR)/config.gypi \
		-Iprojects.gypi \
		-Icommon.gypi \
		-Iconfig.gypi \
		-f$(GENERATOR) \
		$(GYP_FILE)
	$(GYP) \
		--depth=.. \
		--generator-output=./build/out \
		-Goutput_dir=./out \
		-I$(NODE_DIR)/common.gypi \
		-I$(NODE_DIR)/config.gypi \
		-Iprojects.gypi \
		-Icommon.gypi \
		-Iconfig.gypi \
		-fcompile_commands_json \
		$(GYP_FILE)

.PHONY: clean clean-dist
clean:
	$(RM) -r ./config.gypi
	$(RM) -r out
	$(RM) -r ../out
	$(MAKE) -C ../noslated clean
	$(MAKE) -C ../turf distclean
	$(MAKE) -C ../node clean

clean-dist: clean
	$(RM) -r $(TOOLCHAINS_DIR)
	$(RM) -r $(BUILD_NODE_MODULES)

LINT_PROJECTS=aworker noslated
.PHONY: lint test baselinetest
lint:
	for proj in $(LINT_PROJECTS); do \
		$(MAKE) -C $(REPO_ROOT)/$$proj $@ || exit 1; \
	done

TEST_PROJECTS=aworker turf noslated
test:
	for proj in $(TEST_PROJECTS); do \
		if [ -f $(REPO_ROOT)/$$proj/Makefile.mk ]; then \
			$(MAKE) -f Makefile.mk -C $(REPO_ROOT)/$$proj BUILDTYPE=$(BUILDTYPE) $@ || exit 1; \
		else \
			$(MAKE) -C $(REPO_ROOT)/$$proj BUILDTYPE=$(BUILDTYPE) $@ || exit 1; \
		fi \
	done

SANITY_TEST_PROJECTS=noslated aworker
sanitytest:
	for proj in $(SANITY_TEST_PROJECTS); do \
		$(MAKE) -C $(REPO_ROOT)/$$proj BUILDTYPE=$(BUILDTYPE) $@ || exit 1; \
	done

baselinetest:
	$(MAKE) -C $(REPO_ROOT)/noslated $@
