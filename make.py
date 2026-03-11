#################################################################################
MAKEFILE_TEMPLATE_FOR_EXECUTABLES=\
"""
APP2BUILD = {0}
FULLPATH_OBJ_DEPENDENCIES= {1}
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
STATICLIBS =  {2}
#STATICLIBS += asn1clib/libasn1clib.a

# now the include dirs for the custom libraries
# if you use full paths in the source files, only the following is necessary
INCLUDE_DIRS += -I. 


.PHONY: clean

all: make_build_dir ${{APP2BUILD}}

make_build_dir:
	-mkdir build

clean:
	-rm -fr build
	-rm ${{APP2BUILD}}
######################################################
################# object files ########################
# define a suffix rule for .c -> .o
# we could use .c.o :
# but %.o: %.c is more logical !!!
# $@ has the value of the target
# $< has the value of the first dependency file name.
# $^ expands to a space delimited list of the prerequisites

build/%.o: %.c
	gcc -o $@ -c ${{CFLAGS}} ${{INCLUDE_DIRS}} $<
	
################ generated c files ####################
%.c: %.cxx
	cxx.cmd $<

#################### dependencies on pure header files #########>
{4}: {3}

#######################################################
################# executables ########################

OBJFILES := $(patsubst %.cxx,build/%.o,$(wildcard *.cxx))
.PRECIOUS: %.c

ifeq ($(OBJFILES),)
	OBJFILES := $(patsubst %.cxx,build/%.o,$(wildcard *.cxx))
endif



${{APP2BUILD}}: {5} $(OBJFILES) ${{FULLPATH_OBJ_DEPENDENCIES}}
	gcc -o $@ $^ ${{STATICLIBS}} ${{CFLAGS}} ${{LIB_DIRS}} ${{LIBS}}  

################################################
help :
	@echo ""
	@echo "make		 - builds library"
	@echo "make clean	- remove *.o files and build directory"
	@echo "make help	- this info"
	@echo ""

"""
################################################################################
MAKEFILE_TEMPLATE_FOR_LIBRARY=\
"""
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

all: makebuild_dir lib${{MODULE2BUILD}}.a maketest

makebuild_dir:
	-mkdir build

clean:
	-rm -fr build
	-rm lib${{MODULE2BUILD}}.a

maketest:
	$(foreach testdir,$(patsubst %.cxx,test_%,$(wildcard *.cxx)), -make -C $(testdir) &)
	-swig {0}.i
	-python setup.py build_ext --inplace



# run the unit tests
run:
	-test_{0}/test{0}
	-test_{0}/test{0}.exe

#######################################################
################# executables ########################
OBJDIR = build
OBJFILES := $(patsubst %.cxx,build/%.o,$(wildcard *.cxx))
ifeq ($(OBJFILES),)
	OBJFILES := $(patsubst %.c,build/%.o,$(wildcard *.c))	 
endif

.PRECIOUS: %.c


lib${{MODULE2BUILD}}.a: $(OBJFILES)
	ar crus $@ $^
	{2}
	
######################################################
################# object files ########################
# define a suffix rule for .c -> .o
# we could use .c.o :
# but %.o: %.c is more logical !!!
# $@ has the value of the target
# $< has the value of the first dependency file name.
# $^ expands to a space delimited list of the prerequisites

build/%.o: %.c
	gcc -o $@ -c ${{CFLAGS}} ${{INCLUDE_DIRS}} ${{LIB_DIRS}}  $<
	

################ generated c files from cxx ####################
%.c: %.cxx
	cxx.cmd $<
#################### dependencies on pure header files #########
{0}.c: {1}

################################################
help :
	@echo ""
	@echo "make		    - builds library"	
	@echo "make clean	- remove build directory"
	@echo "make help	- this info"
	@echo ""

""" 

################################################################################
SWIG_INTERFACE_FILE_FOR_LIBRARY=\
"""
%module {0}
%{{
#include "{0}.h"
%}}



%include "stdint.i"

%typemap(in) (char *str, int len) {{
$1 = PyString_AsString($input);
$2 = PyString_Size($input);
}};

%typemap(in) (uint8_t *data, int len) {{
$1 = PyString_AsString($input);
$2 = PyString_Size($input);
}};

%typemap(in) uint8_t * {{
	$1 = PyString_AsString($input);
}}
%typemap(in) uint8_t []  {{
	$1 = PyString_AsString($input);
}}

%feature("autodoc", "1");

%include "{0}.h" // Just grab original C header file
"""

aaa="""
%extend {1} {{ // Attach these functions to struct {1}
	{2} 
	}};
"""

def make_swig_file_library(input_file):
	print "GENERATING SWIG file"
	base=os.path.basename(input_file)[:-4].lower()
	print "module name=",base
	Base=base.upper()[0]+base[1:]
	print "class name=",Base
	if __name__=="__main__":
		output_file=sys.stdout
	else:
		output_file=file("{}.i".format(base),"w")
	output_file.write(SWIG_INTERFACE_FILE_FOR_LIBRARY.format(base)
	#			Base,
	#			"this is the interface !!!"
	#				)
		)	
	if output_file!=sys.stdout:
		output_file.close()
SETUP_FILE_FOR_LIBRARY=\
"""
#!/usr/bin/env python
from distutils.core import setup, Extension
from glob import glob
my_source_files = ['{0}.c','{0}_wrap.c']
my_extension = Extension('_{0}',sources=my_source_files,
						library_dirs=['.'],
						libraries = ["{1}"],
						extra_compile_args=['-std=c99'])

setup (name = '{0}',
       version = '0.2',
       author      = "HEK",
       description = "Simple swig example from docs",
       ext_modules = [my_extension],
       py_modules = ['{0}'],
       )
"""
def make_swig_setup_file(input_file):
	print "GENERATING SETUP.py"
	base=os.path.basename(input_file)[:-4].lower()
	libname=os.path.split(os.path.dirname(input_file))[1].lower()
	if __name__=="__main__":
		sys.stdout.write(SETUP_FILE_FOR_LIBRARY.format(base,libname))
	else:
		output_file=file("setup.py","w")
		with output_file as fout:
			fout.write(SETUP_FILE_FOR_LIBRARY.format(base,libname))	
		output_file.close()
	with open("__init__.py","w"):
		pass
############################################################################
import sys, os, glob
from cxx_utils import SINGLE_QUOTE, DOUBLE_QUOTE

def make_makefile(input_file,headerfiles,pure_headerfiles,imported_objects, main_app=True):
	print "GENERATING Makefile"
	print "main input file=",os.path.basename(input_file)[:-4]
	print "imported_objects=",imported_objects	
	print "header files=",headerfiles
	print "pure header files=",pure_headerfiles
	#static_libs= [direct.strip("\\/") for direct in glob.glob('*/') if not direct.startswith('test_')]
	static_lib_paths= [direct.strip(os.sep) for direct in glob.glob('*'+os.sep) 
											if not direct.startswith(('test_','build'))
											]
	exe_static_libs=" ".join([os.path.join(path,"lib"+path+".a") for path in static_lib_paths])
	lib_static_libs=[]
	for path in static_lib_paths:
		lib_static_libs.extend(["ar crus $@ "+obj for obj in glob.glob(os.path.join(path,"build","*.o"))])
	lib_static_libs="\n\t".join(lib_static_libs)
	print "exe STATIC LIBS=", exe_static_libs
	print "lib STATIC LIBS=", lib_static_libs
	if __name__=="__main__":
		output_file=sys.stdout
	else:
		output_file=file("Makefile","w")
	with output_file as fout:
		if main_app:# no .h file, this must be an application 
			makefile=MAKEFILE_TEMPLATE_FOR_EXECUTABLES
			mathlib_needed= "math.h" in headerfiles
			pthreadlib_needed="pthread.h" in headerfiles # CAVEAT, OSAL makes use of pthread!!!	
			if os.name=='posix':
				target=os.path.basename(input_file)[:-4]
			else:
				target=os.path.basename(input_file)[:-4]+'.exe'
			fout.write(makefile.format(target,
										make_imported_objs(imported_objects),
										make_imported_libs(imported_objects)+exe_static_libs,
										" ".join(pure_headerfiles),
										os.path.basename(input_file)[:-4]+".c",
										""
			))
		else: # .h file, this must be a library
			makefile= MAKEFILE_TEMPLATE_FOR_LIBRARY
			fout.write(makefile.format(os.path.basename(input_file)[:-4],
										" ".join(pure_headerfiles),
										lib_static_libs
										))
			make_swig_file_library(input_file)
			make_swig_setup_file(input_file)
			
	
def make_imported_objs(imported_objects):
	return " ".join(imported_objects).replace(SINGLE_QUOTE,"").replace(DOUBLE_QUOTE,'')
		
def make_imported_libs(imported_objects):
	objlist=[]
	for obj in imported_objects:
		print "OBJ=",obj
		path=obj.replace(SINGLE_QUOTE,"").replace(DOUBLE_QUOTE,'').rsplit("/",1)
		print "PATH=",path
		if path[:-1]:
			print "PATH=",path[:-1]
			objlist.append(path[-2]+'/lib' +path[-2].rsplit('/',1)[-1].lower()+'.a')
	return " ".join(objlist)

cpp_preamble= """
#ifdef _cplusplus // if compiled with C++ compiler.  Note that this is not
// standard, check your compiler's docs and other header files to find out
// the correct macro it uses for c++ versus C compilations.
extern "C" {
#endif
"""
cpp_postamble="""
#ifdef _cplusplus // if compiled with C++ compiler
} // end of extern "C" block
#endif
"""

def make_h_file(h_output_file,c_output_file,public_lines,headerfiles,app_specific_headerfiles, inline_destructors):
	if __name__=="__main__":
		output_file=sys.stdout
	else:
		output_file=file(h_output_file,"w")
	print "output file=", h_output_file
	with output_file as h_file:
		FILE_NAME_VAR=os.path.basename(h_output_file).replace(".","_").upper()
		h_file.write("#ifndef _{0}_\n#define _{0}_\n\n".format(FILE_NAME_VAR))
		###
		h_file.write(cpp_preamble)
		h_file.write("/************************************************/\n")
		h_file.write("/*   Standard Header Files includes             */\n\n")
		for headerfile in headerfiles:
			h_file.write('#include <{}>\n'.format(headerfile))
		h_file.write("\n/************************************************/\n\n")
		#THE INCLUDE DIRECTIVES SHOULD BE FIRST IN THE FILE !!!!
		if app_specific_headerfiles:
			h_file.write("/***************************************************/\n")
			h_file.write("/*   Application-specific Header Files includes    */\n\n")	
			for line in app_specific_headerfiles: # own include directive, goes to .h file !
				h_file.write(line+'\n')
			h_file.write("\n/**************************************************/\n\n")
		### THIS SHOULD BE AFTER THE LAST INCLUDE !!!
		h_file.write("\n")						
		h_file.write("\n#ifndef _{0}_\n".format(os.path.basename(c_output_file).replace(".","_").upper()))
		h_file.write("#define EXTERN extern\n")
		h_file.write("#else\n")
		h_file.write("#define EXTERN\n")
		h_file.write("#endif\n\n")
		for line in public_lines:				
			h_file.write(line)
			#if '* this' in line or '_new' in line:	
			#	print "LINE=",line,
		if inline_destructors:
			h_file.write("/***************************************************/\n")
			h_file.write("/*   inline functions h*/\n\n")
			for line in inline_destructors:
				h_file.write(line)								
		h_file.write(cpp_postamble)
		h_file.write("\n\n#undef EXTERN")
		h_file.write("\n#endif\n")
	os.startfile(h_output_file)




def make_c_file(h_output_file,c_output_file,private_lines, forward_declarations,
				 headerfiles,imported_modules, inline_destructors,
				 						main_app=False,global_file=None):
	if __name__=="__main__":
		output_file=sys.stdout
	else:
		output_file=file(c_output_file,"w")
	testdir="test_"+os.path.splitext(os.path.basename(c_output_file))[0]
	if not main_app: # test dir for library
		if not os.path.exists(testdir):
			os.mkdir(testdir)
	with output_file as c_file:
		#c_file.write("#define D_NEW(T,...) memcpy(malloc(sizeof(T)),&(T const){__VA_ARGS__},sizeof(T))\n")
		if not main_app: # this is a library
			c_file.write("#define _{0}_\n".format(os.path.basename(c_output_file).replace(".","_").upper()))
			c_file.write('#include "{0}"\n\n'.format(os.path.basename(h_output_file)))
			for imported_module in imported_modules:
				if "globals.h" in imported_module:
					c_file.write(imported_module+"\n")
		else:
			if global_file: 
				c_file.write("#define _MAIN_C_\n")
			# these should be in the .h file but since it doesn't exist, it has to be here
			c_file.write("/************************************************/\n")
			c_file.write("/*   Standard Header Files includes             */\n\n")
			for headerfile in headerfiles:
				c_file.write('#include <{}>\n'.format(headerfile))
			c_file.write("\n/************************************************/\n\n")
			c_file.write("/************************************************/\n")
			c_file.write("/*   Application-specific Header Files includes */\n\n")
			for headerfile in imported_modules:
				c_file.write('{}\n'.format(headerfile))
			c_file.write("\n/************************************************/\n\n")
		if forward_declarations: # ONLY IF MAIN_APP ?????????????????? zzz 
			c_file.write("\n/************************************************/\n")
			c_file.write("/*   FORWARD DECLARATION OF STATIC FUNCTIONS    */\n\n")
			for func in forward_declarations:
				c_file.write(func+'\n')
			c_file.write("\n/************************************************/\n\n")
		if main_app:
			if inline_destructors:
				c_file.write("/***************************************************/\n")
				c_file.write("/*   inline functions c*/\n\n")
				for line in inline_destructors:
					c_file.write(line)			
		in_test_dir=False
		for line in private_lines:
			if 'STATIC ' in line:
				line=line.replace('STATIC ','')	
				if not main_app:
					#c_file.write("#ifdef UNITTEST\n")
					in_test_dir=True
					c_test_filename=os.path.join(testdir,"test"+os.path.basename(c_output_file))
					c_test_file=file(c_test_filename,"w")
					c_test_file.write('#include "../{}"\n'.format(os.path.splitext(os.path.basename(c_output_file))[0]+'.h'))
			if in_test_dir:
				c_test_file.write(line)
			else:
				c_file.write(line)				
		if in_test_dir:
			c_test_file.close()
			makefile=MAKEFILE_TEMPLATE_FOR_EXECUTABLES
			parentdir=os.path.basename(os.path.abspath('.'))
			libname="../lib"+parentdir.lower()+".a"
			test_makefile_name=os.path.join(testdir,'Makefile')			
			build_target=os.path.basename(c_test_filename)[:-2]
			c_filename=os.path.basename(c_test_filename)
			if not os.path.exists(test_makefile_name):
				with open(test_makefile_name,"w") as fout:
					fout.write(makefile.format(build_target+'.exe'*(os.name!='posix'),
											"",
											libname,
											"",
											"",
											c_filename))
	os.startfile(c_output_file)
    
if __name__=="__main__":
	from hek_c_symbols import needed_header_files
	input_file=r"c:\users\elkarouh\cxx_compiler\test\New1.cxx"
	c_output_file=input_file[:-3]+'c'
	h_output_file=input_file[:-3]+'h'		
	headerfiles=needed_header_files("socket, printf, sin, thread")
	imported_modules=["#include ../COMMON/utils.h","#include ../OSAL/osal.h"]
	imported_objects=[line.rstrip().replace("#include ","")
										 .replace(".h",".o") for line in imported_modules]	
	print "Imported objects=", imported_objects	
	#print headerfiles
		
	#make_makefile(input_file,headerfiles, [],imported_objects, main_app=False)
	#make_makefile(input_file,headerfiles, [],imported_objects, main_app=True)

	public_lines=['int doit();']
	private_lines=['int doit() {','}']
	forward_declarations=[]	
	headerfiles=needed_header_files("socket, printf, sin, thread")
	#make_h_file(h_output_file,c_output_file,public_lines,headerfiles,imported_modules)
	#make_c_file(h_output_file,c_output_file,private_lines, forward_declarations,headerfiles,imported_modules, main_app=True)
	#print '===========',make_imported_libs([os.path.abspath("/test/mylib.c")])
	make_swig_file_library(input_file)
	make_swig_setup_file(input_file)
