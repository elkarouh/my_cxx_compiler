#ifndef _THREAD_H_
#define _THREAD_H_


#ifdef _cplusplus // if compiled with C++ compiler.  Note that this is not
// standard, check your compiler's docs and other header files to find out
// the correct macro it uses for c++ versus C compilations.
extern "C" {
#endif
/************************************************/
/*   Standard Header Files includes             */

#include <pthread.h>
#include <assert.h>
#include <stdio.h>
#include <malloc.h>
#include <stddef.h>
#include <time.h>
#include <locale.h>
#include <errno.h>
#include <stdbool.h>
#include <string.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <semaphore.h>

/************************************************/



#ifndef _THREAD_C_
#define EXTERN extern
#else
#define EXTERN
#endif

typedef uint8_t* TYPE;
typedef void* (*func_t)(void *);// needed to avoid bug in compiler!!!
typedef struct Thread Thread;
typedef struct Task Task;
struct Thread { 
	pthread_attr_t attr;// thread attributes 
	pthread_t threadid;// the thread id 
	};
Thread* Thread_new(func_t func, void *argument);

void Thread_free(Thread* this);

struct Task { 
	pthread_attr_t attr;// thread attributes 
	pthread_t threadid;// the thread id 
	void* arg;
	bool running;
	bool detached;
	void (*run)(Task* this, void* arg);// virtual method
	};
Task* Task_constructor(Task* this);

Task* Task_new();

void Task_free(Task* this);

void Task_start(Task* this,void* arg);

void Task_callback(Task* this);

void Task_join0(Task* this);

int Task_join(Task* this);


#ifdef _cplusplus // if compiled with C++ compiler
} // end of extern "C" block
#endif


#undef EXTERN
#endif
