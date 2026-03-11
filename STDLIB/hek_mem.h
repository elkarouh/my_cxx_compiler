#ifndef _HEK_MEM_H_
#define _HEK_MEM_H_


#ifdef _cplusplus // if compiled with C++ compiler.  Note that this is not
// standard, check your compiler's docs and other header files to find out
// the correct macro it uses for c++ versus C compilations.
extern "C" {
#endif
/************************************************/
/*   Standard Header Files includes             */

#include <stdio.h>
#include <stddef.h>
#include <time.h>
#include <locale.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

/************************************************/



#ifndef _HEK_MEM_C_
#define EXTERN extern
#else
#define EXTERN
#endif

#define malloc(s) fmalloc((s), __FILE__, __LINE__)
#define calloc(c, s) fcalloc((c), (s), __FILE__, __LINE__)
#define realloc(p, s) frealloc((p), (s), __FILE__, __LINE__)
#define recalloc(p, s) frecalloc((p), (s), __FILE__, __LINE__)
#define free(p) ffree((p), __FILE__, __LINE__)

void* fmalloc(size_t size, const char* file, const unsigned int line);

void* fcalloc(size_t count, size_t size, const char* file, const unsigned int line);

void* frealloc(void* ptr, size_t size, const char* file, const unsigned int line);

void* frecalloc(void* ptr, size_t size, const char* file, const unsigned int line);

void ffree(void* ptr, const char* file, const unsigned int line);

void checkmem();// call this in the app destructor or with atexit()

/***************************************************/
/*   inline functions h*/

static inline void nullfree(void **pptr) {if (*pptr == NULL) abort();free(*pptr); *pptr=NULL;};


#ifdef _cplusplus // if compiled with C++ compiler
} // end of extern "C" block
#endif


#undef EXTERN
#endif
