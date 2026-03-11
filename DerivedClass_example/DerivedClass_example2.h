#ifndef _DERIVEDCLASS_EXAMPLE2_H_
#define _DERIVEDCLASS_EXAMPLE2_H_


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



#ifndef _DERIVEDCLASS_EXAMPLE2_C_
#define EXTERN extern
#else
#define EXTERN
#endif

typedef struct Hello Hello;
typedef struct DerivedHello DerivedHello;
struct Hello { 
	int a;
	int b;
	void (*process_msg)(Hello* this);// virtual method
	};
extern int Hello_my_class_variable;
Hello* Hello_new(int arg1, int arg2);

void Hello_free(Hello* this);

void Hello_process_msg(Hello* this);

void Hello_printme(Hello* this);

struct DerivedHello { 
	Hello;
	int c;
	int d;
	};
DerivedHello* DerivedHello_new(int arg1, int arg2,int arg3, int arg4);

void DerivedHello_free(DerivedHello* this);

void DerivedHello_process_msg(DerivedHello* this);

void DerivedHello_printme(DerivedHello* this);


#ifdef _cplusplus // if compiled with C++ compiler
} // end of extern "C" block
#endif


#undef EXTERN
#endif
