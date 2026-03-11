#define _DERIVEDCLASS_EXAMPLE2_C_
#include "DerivedClass_example2.h"


/************************************************/
/*   FORWARD DECLARATION OF STATIC FUNCTIONS    */

static Hello* Hello_constructor(Hello* self,int arg1, int arg2);
static int Hello_my_private_class_variable = 999;
static void Hello_destructor(Hello* self);
static DerivedHello* DerivedHello_constructor(DerivedHello* self,int arg1, int arg2,int arg3, int arg4);
static void DerivedHello_destructor(DerivedHello* self);

/************************************************/


Hello* Hello_constructor(Hello* this,int arg1, int arg2) { 
	this->a = arg1;
	this->b = arg2;
	this->process_msg=Hello_process_msg;// virtual method
	return this;
	}

int Hello_my_class_variable = 990;
Hello* Hello_new(int arg1, int arg2) { 
	Hello* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Hello_constructor(this, arg1, arg2);
	}

void Hello_free(Hello* this) { 
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
	}


// class variable in the c++ way
//public int Hello::my_class_variable = 990
//private int Hello::my_private_class_variable = 999


//////////////////////////////

DerivedHello* DerivedHello_constructor(DerivedHello* this,int arg1, int arg2,int arg3, int arg4) { 
	//Hello::__init__(self,arg1,arg2)
	Hello_constructor((Hello*)this,arg1,arg2);
	this->c = arg3;
	this->d = arg4;
	this->process_msg=DerivedHello_process_msg;// virtual method
	return this;
	}

DerivedHello* DerivedHello_new(int arg1, int arg2,int arg3, int arg4) { 
	DerivedHello* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return DerivedHello_constructor(this, arg1, arg2, arg3, arg4);
	}

void DerivedHello_free(DerivedHello* this) { 
	DerivedHello_destructor(this);
	free(this);
	}

void DerivedHello_destructor(DerivedHello* this) { 
	//release resources allocated in derived constructor
	Hello_destructor(this);
	fprintf (stderr,);
	}
/* this is a doc string */
/* input parameter:.... */
void DerivedHello_process_msg(DerivedHello* this) { 
	DerivedHello_printme(this);
	fprintf (stderr, "DerivedHello is processing message!\n");
	}
void DerivedHello_printme(DerivedHello* this) { 
	Hello_printme(this);
	fprintf (stderr, "a=%d, b=%d\n", this->a, this->b);
	fprintf (stderr, "c=%d, d=%d\n", this->c, this->d);
	}


////////////////////////////////////////
	
