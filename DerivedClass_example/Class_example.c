#define _CLASS_EXAMPLE_C_
#include "Class_example.h"


/************************************************/
/*   FORWARD DECLARATION OF STATIC FUNCTIONS    */

typedef struct Hello Hello; // opaque type
static Hello* Hello_constructor(Hello* self,int arg1, int arg2);
static int Hello_my_private_class_variable = 999;
static int Hello_my_private_class_variable2;
static Hello* Hello_new(int arg1, int arg2);
static void Hello_free(Hello* self);
static void Hello_destructor(Hello* self);
static void Hello_process_msg(Hello* self);
static void Hello_printme(Hello* self);

/************************************************/

struct Hello { 
	int a;
	int b;
	void (*process_msg)(Hello* this);// virtual method
	};

Hello* Hello_constructor(Hello* this,int arg1, int arg2) { 
	this->b= 0;
	this->a = arg1;
	this->b = arg2;
	this->process_msg=Hello_process_msg;// virtual method
	return this;
	}

int Hello_my_public_class_variable = 990;
static Hello* Hello_new(int arg1, int arg2) { 
	Hello* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Hello_constructor(this, arg1, arg2);
	}

static void Hello_free(Hello* this) { 
	Hello_destructor(this);
	free(this);
	}

void Hello_destructor(Hello* this) { 
	//release resources allocated in constructor
	// empty statement !!!;
	}
void Hello_process_msg(Hello* this) { 
	fprintf (stderr, "Hello is processing message!\n");
	}
void Hello_printme(Hello* this) { 
	this->process_msg(this);// virtual method call
	fprintf (stderr, "a=%d, b=%d\n", this->a, this->b);
	Hello* my =  Hello_new(777,888);
	my =  Hello_new(777,888);
	Hello_printme(my);
	}

////////////////////////////////////////
	
