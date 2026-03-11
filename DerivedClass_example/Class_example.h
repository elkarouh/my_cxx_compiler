#ifndef _CLASS_EXAMPLE_H_
#define _CLASS_EXAMPLE_H_


#ifdef _cplusplus // if compiled with C++ compiler.  Note that this is not
// standard, check your compiler's docs and other header files to find out
// the correct macro it uses for c++ versus C compilations.
extern "C" {
#endif
/************************************************/
/*   Standard Header Files includes             */

#include <stdlib.h>
#include <stdio.h>

/************************************************/



#ifndef _CLASS_EXAMPLE_C_
#define EXTERN extern
#else
#define EXTERN
#endif

extern int Hello_my_public_class_variable;
int Hello_my_public_class_variable2;

#ifdef _cplusplus // if compiled with C++ compiler
} // end of extern "C" block
#endif


#undef EXTERN
#endif
