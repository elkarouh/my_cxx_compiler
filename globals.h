
#ifndef _GLOBALS_H
#define _GLOBALS_H


// header files required by global struct


// enums and defines


#ifndef _MAIN_C_
#define EXTERN extern
#else
#define EXTERN
#define INITIALIZE
#endif

// global data appropriately packaged in a struct
EXTERN struct GG { // should become namespace G
	int x;
	float y;
	};

struct G G;

#ifdef INITIALIZE

#endif
;

#undef EXTERN
#undef INITIALIZE
#endif

