
.PHONY: all ninja test clean

all:
	make -C build

ninja:
	make -C build GENERATOR=ninja

test:
	make -C build test

clean:
	make -C build clean
