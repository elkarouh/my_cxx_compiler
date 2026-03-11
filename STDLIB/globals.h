
#ifndef _GLOBALS_H
#define _GLOBALS_H


// header files required by global struct


// enums and defines
enum {
		BUF_MIN_ALIGNMENT= 64,
		BUFSIZE=100,
};


#ifndef _MAIN_C_
#define EXTERN extern
#else
#define EXTERN
#define INITIALIZE
#endif

// global data appropriately packaged in a struct
EXTERN struct GG {
	ProducerConsumerChannel* ch;
	};

struct G G;

#ifdef INITIALIZE

#endif
;

#undef EXTERN
#undef INITIALIZE
#endif

