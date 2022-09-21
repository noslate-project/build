# Refs: https://github.com/nodejs/node/blob/master/Makefile

UNAME_M=$(shell uname -m)

ifeq ($(findstring x86_64, $(UNAME_M)), x86_64)
DESTCPU ?= x64
else
ifeq ($(findstring amd64, $(UNAME_M)), amd64)
DESTCPU ?= x64
else
ifeq ($(findstring aarch64,$(UNAME_M)),aarch64)
DESTCPU ?= arm64
endif
endif
endif

ifeq ($(DESTCPU), x64)
ARCH=x64
else
ifeq ($(DESTCPU), arm64)
ARCH=arm64
endif
endif
