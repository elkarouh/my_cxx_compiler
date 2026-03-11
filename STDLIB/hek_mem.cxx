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

public #define malloc(s) fmalloc((s), __FILE__, __LINE__)
public #define calloc(c, s) fcalloc((c), (s), __FILE__, __LINE__)
public #define realloc(p, s) frealloc((p), (s), __FILE__, __LINE__)
public #define recalloc(p, s) frecalloc((p), (s), __FILE__, __LINE__)
public #define free(p) ffree((p), __FILE__, __LINE__)

// Because we want to be able to call the REAL functions now
#undef malloc
#undef calloc
#undef realloc
#undef free

class Memory:
	void* p	// The actual memory
	size_t size	// The size of the requested block
	const char* file	// The name of the file where the memory was allocated
	unsigned int line	// The actual line of code that allocated the memory
	Memory* next // Pointer to the next block Memory
	static Memory* head = NULL // Our linked list of blocks
	def __init__(self,void* p,size_t size,const char* file,const uint16_t line):
		self.p = p
		self.size = size
		self.file = file
		self.line = line
		self.next = Memory::head

// LinkedList prepend element
public void* fmalloc(size_t size, const char* file, const unsigned int line):
	void* p = malloc(size)
	if not p:
		print "Fatal: could not allocate %d bytes at %s, line %d\n", size, file, line
		return
	// Keep track of this allocation
	Memory::head =new Memory(p, size, file, line)
	return p

// LinkedList prepend element
public void* fcalloc(size_t count, size_t size, const char* file, const unsigned int line):
	void* p = calloc(count, size)
	if not p :
		print "Fatal: could not allocate %d chunks of %d bytes at %s, line %d\n", count, size, file, line
		return NULL
	// Keep track of this allocation
	Memory::head =new Memory(p, count*size, file, line)
	return p

// LinkedList find element
public void* frealloc(void* ptr, size_t size, const char* file, const unsigned int line):
	void *np = realloc(ptr, size)
	if not np:
		print "Fatal: could not reallocate %d bytes at %s, line %d\n", size, file, line
		return NULL
	for Memory* curr=Memory::head;curr;curr=curr->next:
		if curr->p==ptr:
			curr->size= size
			curr->p= np
			return np
	// This should NEVER happen
	print "Fatal: attempted to locate previous block for realloc in %s, line %d, but failed\n", file, line
	exit(1)

// NEW implementation of recalloc !!!!!!!!!!!!!
public void* frecalloc(void* ptr, size_t size, const char* file, const unsigned int line):
	void *np = realloc(ptr, size)
	if not np:
		print "Fatal: could not reallocate %d bytes at %s, line %d\n", size, file, line
		return NULL
	for Memory* curr=Memory::head;curr;curr=curr->next:
		if curr->p==ptr:
			int old_size=curr->size
			curr->size= size
			if size>old_size:
				memset(np+old_size, 0, size-old_size)
			curr->p= np
			return np
	// This should NEVER happen
	print "Fatal: attempted to locate previous block for realloc in %s, line %d, but failed\n", file, line
	exit(1)


// LinkedList remove element
public void ffree(void* ptr, const char* file, const unsigned int line):
	if not ptr:
		return
	free ptr // free the pointer as usual
	// now free the block in the linked list
	for Memory *curr=Memory::head,*prev=NULL;curr;prev=curr,curr=curr->next:
		if curr->p==ptr:
			if prev: // Break the link in the chain
				prev->next = curr->next
			else: // This is the first, replace the head pointer
				Memory::head = curr->next				
			free curr
			return
	print "NOT FOUND!!!\n"

// LinkedList traverse
public void checkmem():  // call this in the app destructor or with atexit()
	if not Memory::head: // Congratulations, you have no memory leaks!
		return
	print "\nYOU HAVE MEMORY LEAKS\n"
	for Memory *curr=Memory::head;curr;curr=curr->next:
		print "\t%d bytes at %p, allocated in %s at line %d\n", curr->size, curr->p, curr->file, curr->line
		
static inline void nullfree(void **pptr) {if (*pptr == NULL) abort();free(*pptr); *pptr=NULL;}

	
