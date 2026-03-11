#ifndef _DATE_H_
#define _DATE_H_


#ifdef _cplusplus // if compiled with C++ compiler.  Note that this is not
// standard, check your compiler's docs and other header files to find out
// the correct macro it uses for c++ versus C compilations.
extern "C" {
#endif
/************************************************/
/*   Standard Header Files includes             */

#include <assert.h>
#include <sys/time.h>
#include <stdio.h>
#include <stddef.h>
#include <time.h>
#include <locale.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

/************************************************/



#ifndef _DATE_C_
#define EXTERN extern
#else
#define EXTERN
#endif

typedef struct Date Date;
#define TIMEVAL2MSEC(t) (((t)->tv_sec*1000)+((t)->tv_usec/1000))

struct Date { 
	uint16_t year;
	uint16_t month;
	uint16_t day;
	};
Date* Date_new();

void Date_free(Date* this);

time_t get_year_start();

bool greater_or_equal(struct timeval t1, struct timeval t2);

uint64_t  diff_time(struct timeval t1, struct timeval t2);

struct timeval add_time(struct timeval t1, struct timeval t2);

struct timeval get_time(void);

uint32_t get_days_since_beginning_of_year(int32_t number_days_since_2000);


#ifdef _cplusplus // if compiled with C++ compiler
} // end of extern "C" block
#endif


#undef EXTERN
#endif
