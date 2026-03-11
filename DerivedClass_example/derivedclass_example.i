
%module derivedclass_example
%{
#include "derivedclass_example.h"
%}



%include "stdint.i"

%typemap(in) (char *str, int len) {
$1 = PyString_AsString($input);
$2 = PyString_Size($input);
};

%typemap(in) (uint8_t *data, int len) {
$1 = PyString_AsString($input);
$2 = PyString_Size($input);
};

%typemap(in) uint8_t * {
	$1 = PyString_AsString($input);
}
%typemap(in) uint8_t []  {
	$1 = PyString_AsString($input);
}

%feature("autodoc", "1");

%include "derivedclass_example.h" // Just grab original C header file
