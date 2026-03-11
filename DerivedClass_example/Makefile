
lowercase = $(subst A,a,$(subst B,b,$(subst C,c,$(subst D,d,$(subst E,e,$(subst F,f,$(subst G,g,$(subst H,h,$(subst I,i,$(subst J,j,$(subst K,k,$(subst L,l,$(subst M,m,$(subst N,n,$(subst O,o,$(subst P,p,$(subst Q,q,$(subst R,r,$(subst S,s,$(subst T,t,$(subst U,u,$(subst V,v,$(subst W,w,$(subst X,x,$(subst Y,y,$(subst Z,z,$1))))))))))))))))))))))))))
# get the directory basename (lastword is used to skip spaces indir names!!!)
MODULE2BUILD0=$(notdir $(lastword $(shell pwd)))
# convert to lowercase
MODULE2BUILD  = $(call lowercase,$(MODULE2BUILD0))

CFLAGS += -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64
CFLAGS += -fms-extensions -std=c99 -fno-strict-aliasing -g -O3 
CFLAGS += -DLINUX -D_REENTRANT -Wall -Wextra -Wno-write-strings

# full path custom libraries
LIB_DIRS =  
STATICLIBS = 


# now the include dirs
# since we use full paths in the source files, we only need the current dir
INCLUDE_DIRS += -I.

.PHONY: clean

all: makebuild_dir lib${MODULE2BUILD}.a maketest

makebuild_dir:
	-mkdir build

clean:
	-rm -fr build
	-rm lib${MODULE2BUILD}.a

maketest:
	$(foreach testdir,$(patsubst %.cxx,test_%,$(wildcard *.cxx)), -make -C $(testdir) &)
	-swig DerivedClass_example.i
	-python setup.py build_ext --inplace



# run the unit tests
run:
	-test_DerivedClass_example/testDerivedClass_example
	-test_DerivedClass_example/testDerivedClass_example.exe

#######################################################
################# executables ########################
OBJDIR = build
OBJFILES := $(patsubst %.cxx,build/%.o,$(wildcard *.cxx))
ifeq ($(OBJFILES),)
	OBJFILES := $(patsubst %.c,build/%.o,$(wildcard *.c))	 
endif

.PRECIOUS: %.c


lib${MODULE2BUILD}.a: $(OBJFILES)
	ar crus $@ $^
	
	
######################################################
################# object files ########################
# define a suffix rule for .c -> .o
# we could use .c.o :
# but %.o: %.c is more logical !!!
# $@ has the value of the target
# $< has the value of the first dependency file name.
# $^ expands to a space delimited list of the prerequisites

build/%.o: %.c
	gcc -o $@ -c ${CFLAGS} ${INCLUDE_DIRS} ${LIB_DIRS}  $<
	

################ generated c files from cxx ####################
%.c: %.cxx
	cxx.cmd $<
#################### dependencies on pure header files #########
DerivedClass_example.c: 

################################################
help :
	@echo ""
	@echo "make		    - builds library"	
	@echo "make clean	- remove build directory"
	@echo "make help	- this info"
	@echo ""

