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

/************************************************/
/*   Application-specific Header Files includes */


/************************************************/


/************************************************/
/*   FORWARD DECLARATION OF STATIC FUNCTIONS    */

typedef struct Node Node; // opaque type
typedef struct List List; // opaque type
static Node* Node_constructor(Node* self, void* v,int key);
static Node* Node_new(void* v,int key);
static void Node_free(Node* self);
static List* List_constructor(List* self);
static List* List_new();
static void List_free(List* self);
static void List_destructor(List* self);
static void List_append(List* self, void* x);
static void List_prepend(List* self, void* x);
static void List_insert(List* self, void* x, int key);
static bool List_remove(List* self, void* x);
static void* List_next(List* self);

/************************************************/

/*
 * this is a simple linked list implementation
 * Use it when you want to preserver order of insertion
 * often need to remove elements (if not, use a straight array!)  
 */
struct Node { 
	Node* next;
	void* val;
	int key;// used for Schwartzian sort
	};

Node* Node_constructor(Node* this, void* v,int key) { 
	this->val=v;
	this->key=key;
	this->next=NULL;
	return this;
	}
static Node* Node_new(void* v,int key) { 
	Node* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Node_constructor(this, v, key);
	}

static void Node_free(Node* this) { 
	free(this);
	}



struct List { 
	int _state;
	bool _exhausted;
	bool _valid_output;
	Node* head;
	uint16_t length;
	Node* p;// for the generator
	};

List* List_constructor(List* this) { 
	this->_state=0;
	this->_exhausted=false;
	this->_valid_output=true;
	this->head=NULL;
	this->length=0;
	return this;
	}

static List* List_new() { 
	List* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return List_constructor(this);
	}

static void List_free(List* this) { 
	List_destructor(this);
	free(this);
	}

void List_destructor(List* this) { 
	Node* p = this->head;
	while (p) { 
		Node* nextNode = p->next;
		Node_free(p);
		p = nextNode;
		}
	}
void List_append(List* this, void* x) { 
	Node* ni =  Node_new(x, -1);
	if (!this->head) { // append to NULL = new 
		this->head=ni;
		}
	else { 
		Node* p=this->head;
		while (p->next) { 
			p=p->next;
			}
		p->next= ni;
		}
	this->length++;
	}
void List_prepend(List* this, void* x) { // this is faster than append but reverse order!
	Node* ni =  Node_new(x, -1);
	ni->next=this->head;
	this->head=ni;
	this->length++;
	}
void List_insert(List* this, void* x, int key) { // sorted insertion!!!
	Node* ni =  Node_new(x, key);
	Node* p= this->head;
	Node* prev=NULL;
	while (p) { 
		if (p->key>ni->key) { // we found insert place
			break;
			}
		prev= p;
		p= p->next;
		}
	if (prev) { 
		prev->next=ni;
		}
	else { 
		this->head=ni;
		}
	ni->next=p;
	this->length++;
	}
bool List_remove(List* this, void* x) { 
	for (Node *p=this->head,*prev=NULL; p; prev=p,p=p->next) { 
		if (p->val==x) { // we found it, let us delete it
			if (prev) { 
				prev->next=p->next;
				}
			else { // we delete the first element !!!
				this->head=p->next;
				}
			Node_free(p);
			this->length--;
			return true;
			}
		}
	return false;
	}
void* List_next(List* this) { 
	switch (this->_state) { 
		case 0: goto LABEL0;
		case 1: goto LABEL1;
		}
	LABEL0: //start of generator;
	this->p= this->head;
	while (this->p) { 
		//start of yield #1
		this->_state=1;
		this->_valid_output=true;
		return this->p->val;
		LABEL1:;
		//end of yield #1

		this->p = this->p->next;
		}
	this->_valid_output=false;
	this->_exhausted=true;
	return NULL;
	}



int main() { 
	List* q =  List_new();
	List_insert(q,(void*)5,999);
	List_insert(q,(void*)89,998);
	List_insert(q,(void*)8,997);
	List_insert(q,(void*)18,996);
	List_remove(q,(void*)8);
	while (true)  { 
		int x =List_next(q); if (q->_exhausted) break;
		fprintf (stderr, "elem=%d\n", x);
		}
	}


