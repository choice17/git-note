# pkg-config

pkg-config is library manager in unix envron [REF](https://people.freedesktop.org/~dbn/pkg-config-guide.html)

SKIP to tips to [MAKEFILE](#makefile)

It takes library config in .pc file.

Example of foo.pc and bar.pc file  
```
foo.pc:
prefix=/usr
exec_prefix=${prefix}
includedir=${prefix}/include
libdir=${exec_prefix}/lib

Name: foo
Description: The foo library
Version: 1.0.0
Cflags: -I${includedir}/foo
Libs: -L${libdir} -lfoo

bar.pc:
prefix=/usr
exec_prefix=${prefix}
includedir=${prefix}/include
libdir=${exec_prefix}/lib

Name: bar
Description: The bar library
Version: 2.1.2
Requires.private: foo >= 0.7
Cflags: -I${includedir}
Libs: -L${libdir} -lbar
```

On a typical Unix system, it will search in the directories `/usr/lib/pkgconfig` and `/usr/share/pkgconfig`.  

```
$ pkg-config --modversion hello
Package hello was not found in the pkg-config search path.
Perhaps you should add the directory containing `hello.pc'
to the PKG_CONFIG_PATH environment variable
No package 'hello' found
$ export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
$ pkg-config --modversion hello
1.0.0
```

## makefile

it helps to locate system installed libraries

```
# Makefile for opencv deps prog
# ========
OPENCV=1

ifeq ($(OPENCV), 1)
CFLAGS := -DOPENCV `pkg-config --cflags opencv`
LDFLAGS := `pkg-config --libs opencv`
endif
```

```
# Makefile for ffmpeg deps prog
# ========
FFMPEG=1

ifeq ($(FFMPEG), 1)
CFLAGS := `pkg-config --cflags libavcodec libavformat libavutil`
LDFLAGS := `pkg-config --libs libavcodec libavformat libavutil`
endif
```



