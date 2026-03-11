#define _HEK_MEM_C_
#include "hek_mem.h"


/************************************************/
/*   FORWARD DECLARATION OF STATIC FUNCTIONS    */

typedef struct Memory Memory; // opaque type
static Memory* Memory_constructor(Memory* self,void* p,size_t size,const char* file,const uint16_t line);
Memory* Memory_head = NULL ;
static Memory* Memory_new(void* p,size_t size,const char* file,const uint16_t line);
static void Memory_free(Memory* self);

/************************************************/

// todo, implement a reference counter !!!
// todo, implement memory pool
// p=calloc(n, m) is equivalent to p=malloc(n*m); memset(p, 0, m * n)
// p=recalloc(old_p,size) should be implemented as p=realloc(old_p,size);memset(p+old_size, 0, size-old_size)
/* 
Memory management is a pain, yes, but there's a relatively straightforward way 
to make sure you don't leak too much memory without resorting to valgrind or 
other tool: declare a header file called hek_mem.h that redefines malloc, 
calloc, realloc, and free
In any of your source files, just #include "hek_mem.h"
And use malloc, realloc, calloc, and free as usual. Make sure to call checkmem()
 at the end of your program, or, since it's the right fptr signature anyway, 
 call atexit(checkmem);
*/

// Because we want to be able to call the REAL functions now
#undef malloc
#undef calloc
#undef realloc
#undef free

struct Memory { 
	void* p;// The actual memory
	size_t size;// The size of the requested block
	const char* file;// The name of the file where the memory was allocated
	unsigned int line;// The actual line of code that allocated the memory
	Memory* next;// Pointer to the next block Memory
	};

Memory* Memory_constructor(Memory* this,void* p,size_t size,const char* file,const uint16_t line) { 
	this->p = p;
	this->size = size;
	this->file = file;
	this->line = line;
	this->next = Memory_head;
	return this;
	}
static Memory* Memory_new(void* p,size_t size,const char* file,const uint16_t line) { 
	Memory* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Memory_constructor(this, p, size, file, line);
	}

static void Memory_free(Memory* this) { 
	free(this);
	}



// LinkedList prepend element
void* fmalloc(size_t size, const char* file, const unsigned int line) { 
	void* p = malloc(size);
	if (!p) { 
		fprintf (stderr, "Fatal: could !allocate %d bytes at %s, line %d\n", size, file, line);
		return;
		}
	// Keep track of this allocation
	Memory_head = Memory_new(p, size, file, line);
	return p;
	}

// LinkedList prepend element
void* fcalloc(size_t count, size_t size, const char* file, const unsigned int line) { 
	void* p = calloc(count, size);
	if (!p ) { 
		fprintf (stderr, "Fatal: could !allocate %d chunks of %d bytes at %s, line %d\n", count, size, file, line);
		return NULL;
		}
	// Keep track of this allocation
	Memory_head = Memory_new(p, count*size, file, line);
	return p;
	}

// LinkedList find element
void* frealloc(void* ptr, size_t size, const char* file, const unsigned int line) { 
	void *np = realloc(ptr, size);
	if (!np) { 
		fprintf (stderr, "Fatal: could !reallocate %d bytes at %s, line %d\n", size, file, line);
		return NULL;
		}
	for (Memory* curr=Memory_head;curr;curr=curr->next) { 
		if (curr->p==ptr) { 
			curr->size= size;
			curr->p= np;
			return np;
			}
		}
	// This should NEVER happen
	fprintf (stderr, "Fatal: attempted to locate previous block for realloc in %s, line %d, but failed\n", file, line);
	exit(1);
	}

// NEW implementation of recalloc !!!!!!!!!!!!!
void* frecalloc(void* ptr, size_t size, const char* file, const unsigned int line) { 
	void *np = realloc(ptr, size);
	if (!np) { 
		fprintf (stderr, "Fatal: could !reallocate %d bytes at %s, line %d\n", size, file, line);
		return NULL;
		}
	for (Memory* curr=Memory_head;curr;curr=curr->next) { 
		if (curr->p==ptr) { 
			int old_size=curr->size;
			curr->size= size;
			if (size>old_size) { 
				memset(np+old_size, 0, size-old_size);
				}
			curr->p= np;
			return np;
			}
		}
	// This should NEVER happen
	fprintf (stderr, "Fatal: attempted to locate previous block for realloc in %s, line %d, but failed\n", file, line);
	exit(1);
	}


// LinkedList remove element
void ffree(void* ptr, const char* file, const unsigned int line) { 
	if (!ptr) { 
		return;
		}
	free (ptr);// free the pointer as usual
	// now free the block in the linked list
	for (Memory *curr=Memory_head,*prev=NULL;curr;prev=curr,curr=curr->next) { 
		if (curr->p==ptr) { 
			if (prev) { // Break the link in the chain
				prev->next = curr->next;
				}
			else { // This is the first, replace the head pointer
				Memory_head = curr->next;
				}
			free (curr);
			return;
			}
		}
	fprintf (stderr, "NOT FOUND!!!\n");
	}

// LinkedList traverse
void checkmem() { // call this in the app destructor or with atexit()
	if (!Memory_head) { // Congratulations, you have no memory leaks!
		return;
		}
	fprintf (stderr, "\nYOU HAVE MEMORY LEAKS\n");
	for (Memory *curr=Memory_head;curr;curr=curr->next) { 
		fprintf (stderr, "\t%d bytes at %p, allocated in %s at line %d\n", curr->size, curr->p, curr->file, curr->line);
		}
	}
		

	

