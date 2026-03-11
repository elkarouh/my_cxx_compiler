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

typedef struct q_elem_t q_elem_t; // opaque type
typedef struct Heap Heap; // opaque type
static Heap* Heap_constructor(Heap* self, uint16_t size);
static Heap* Heap_new(uint16_t size);
static void Heap_free(Heap* self);
static void Heap_destructor(Heap* self);
static bool Heap_empty(Heap* self);
static void Heap__siftdown(Heap* self, int startpos, int pos);
static void Heap__siftup(Heap* self, int pos);
static void Heap_push(Heap* self, void* item, int pri);
static void* Heap_pop(Heap* self);
static void* Heap_next(Heap* self);

/************************************************/

// Author: HEK
/* Heap queue algorithm (a.k.a. priority queue).*/

struct q_elem_t { 
	void* data;
	int pri;
	};

struct Heap { 
	int _state;
	bool _exhausted;
	bool _valid_output;
	q_elem_t *elems;// array of q_elem_t
	int num_elems;// actual number of elements
	int capacity;// allocated memory
	};

Heap* Heap_constructor(Heap* this, uint16_t size) { 
	this->_state=0;
	this->_exhausted=false;
	this->_valid_output=true;
	if (size < 4) { 
		size = 4;
		}
	this->capacity = size;
	this->num_elems = 0;
	this->elems = calloc(size,sizeof(q_elem_t));
	if (this->elems == NULL) { 
		free (this);
		return NULL;
		}
	return this;
	}
static Heap* Heap_new(uint16_t size) { 
	Heap* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Heap_constructor(this, size);
	}

static void Heap_free(Heap* this) { 
	Heap_destructor(this);
	free(this);
	}

void Heap_destructor(Heap* this) { 
	free (this->elems);
	}
bool Heap_empty(Heap* this) { 
	return this->num_elems==0;
	}
static void Heap__siftdown(Heap* this, int startpos, int pos) { 
	q_elem_t newitem = this->elems[pos];
	while (pos > startpos) { 
		int parentpos = (pos-1) >> 1;
		q_elem_t parent = this->elems[parentpos];
		if (parent.pri <= newitem.pri) { 
			break;
			}
		this->elems[pos] = parent;
		pos = parentpos;
		}
	this->elems[pos] = newitem;
	}
static void Heap__siftup(Heap* this, int pos) { 
	int endpos = this->num_elems;
	int startpos = pos;
	q_elem_t newitem = this->elems[pos];
	int childpos = 2*pos + 1;//leftmost child position
	while (childpos < endpos) { 
		int rightpos = childpos+1;
		if (rightpos < endpos  &&  this->elems[rightpos].pri <= this->elems[childpos].pri) { 
			childpos = rightpos;
			}
		this->elems[pos] = this->elems[childpos];
		pos = childpos;
		childpos = 2*pos + 1;
		}
	this->elems[pos] = newitem;
	Heap__siftdown(this,startpos, pos);
	}
static void Heap_push(Heap* this, void* item, int pri) { 
	this->elems[this->num_elems] = (q_elem_t) { item, pri };
	this->num_elems++;
	// TODO CHECK FOR AVAILABLE SPACE, SEE PriorityQueue.cxx
	Heap__siftdown(this,0, this->num_elems-1);
	}
static void* Heap_pop(Heap* this) { 
	q_elem_t lastelt = this->elems[this->num_elems-1];// raises appropriate IndexError if heap is empty
	this->num_elems--;
	q_elem_t returnitem;
	if (this->num_elems >= 0) { 
		returnitem = this->elems[0];
		this->elems[0] = lastelt;
		Heap__siftup(this,0);
		}
	else { 
		returnitem = lastelt;
		}
	return returnitem.data;
	}
static void* Heap_next(Heap* this) { 
	switch (this->_state) { 
		case 0: goto LABEL0;
		case 1: goto LABEL1;
		}
	LABEL0: //start of generator;
	for (;;) { 
		if (Heap_empty(this)) { 
			this->_valid_output=false;
			this->_exhausted=true;
			return NULL;
			}
		//start of yield #1
		this->_state=1;
		this->_valid_output=true;
		return Heap_pop(this);
		LABEL1:;
		//end of yield #1
		}
	}


int main() { // Simple sanity test
	Heap* heap= Heap_new(10);
	int data[] = { 
		11, 33, 55, 77, 99, 22, 44, 66, 88, 0,
		};
	for (int i=0;i<10;i++) { 
		Heap_push(heap,data[i], data[i]);
		}
	while (true)  { 
		int i =Heap_next(heap); if (heap->_exhausted) break;
		fprintf (stderr, "elem=%d\n",i);
		}
	Heap_free(heap);
	}

