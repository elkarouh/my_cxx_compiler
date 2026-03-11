
APP2BUILD = testDerivedClass_example2.exe
FULLPATH_OBJ_DEPENDENCIES= 
#########################################################

CFLAGS += -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64
CFLAGS += -fms-extensions -std=c99 -fno-strict-aliasing -g -O3 
CFLAGS += -DLINUX -D_REENTRANT -Wall -Wextra -Wno-write-strings


# now the library dirs
LIB_DIRS = 
#LIB_DIRS = -L../LIB
# now the standard/installed libraries (are on the path)
LIBS += -lpthread
LIBS += -lm
ifeq ($(shell uname), Linux)
	LIBS += -lrt
	LIBS += -lz
else
	LIBS += -lmingw32
endif

# full path custom libraries 
STATICLIBS =  ../libderivedclass_example.a
#STATICLIBS += asn1clib/libasn1clib.a

# now the include dirs for the custom libraries
# if you use full paths in the source files, only the following is necessary
INCLUDE_DIRS += -I. 


.PHONY: clean

all: make_build_dir ${APP2BUILD}

make_build_dir:
	-mkdir build

clean:
	-rm -fr build
	-rm ${APP2BUILD}
######################################################
################# object files ########################
# define a suffix rule for .c -> .o
# we could use .c.o :
# but %.o: %.c is more logical !!!
# $@ has the value of the target
# $< has the value of the first dependency file name.
# $^ expands to a space delimited list of the prerequisites

build/%.o: %.c
	gcc -o $@ -c ${CFLAGS} ${INCLUDE_DIRS} $<
	
################ generated c files ####################
%.c: %.cxx
	cxx.cmd $<

#################### dependencies on pure header files #########>
: 

#######################################################
################# executables ########################

OBJFILES := $(patsubst %.cxx,build/%.o,$(wildcard *.cxx))
.PRECIOUS: %.c

ifeq ($(OBJFILES),)
	OBJFILES := $(patsubst %.cxx,build/%.o,$(wildcard *.cxx))
endif



${APP2BUILD}: testDerivedClass_example2.c $(OBJFILES) ${FULLPATH_OBJ_DEPENDENCIES}
	gcc -o $@ $^ ${STATICLIBS} ${CFLAGS} ${LIB_DIRS} ${LIBS}  

################################################
help :
	@echo ""
	@echo "make		 - builds library"
	@echo "make clean	- remove *.o files and build directory"
	@echo "make help	- this info"
	@echo ""

