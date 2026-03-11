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
typedef struct Dict Dict; // opaque type
static uint32_t hash_fun(const char *str);
static Node* Node_constructor(Node* self, void* key,void* val, Node* next);
static Node* Node_new(void* key,void* val, Node* next);
static void Node_free(Node* self);
static List* List_new();
static void List_free(List* self);
static void List_destructor(List* self);
static void List_prepend(List* self, void* key, void* val);
static Node* List_find(List* self, void* key);
static bool List_remove(List* self, void* key);
static Dict* Dict_constructor(Dict* self,int size);
static Dict* Dict_new(int size);
static void Dict_free(Dict* self);
static void Dict_destructor(Dict* self);
static List* Dict__find_bucket(Dict* self, void* key);
static void* Dict_hget(Dict* self, void* key);
static void Dict_hset(Dict* self, void* key, void*value);
static void Dict_hdel(Dict* self, void* key);

/************************************************/

// TODO: add a real hash function
// TODO: try linear search with sentinel

#define SIZE 1024

uint32_t hash_fun(const char *str) { 
	uint32_t hash= 5381;
	int32_t c;
	while (c=*str++) { 
		hash = ((hash << 5) + hash) + c;
		}
	return hash;
	}

struct Node { 
	void* key;
	void* val;
	Node* next;
	};

Node* Node_constructor(Node* this, void* key,void* val, Node* next) { 
	this->val=val;
	this->key=key;
	this->next=next;
	return this;
	}
static Node* Node_new(void* key,void* val, Node* next) { 
	Node* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Node_constructor(this, key, val, next);
	}

static void Node_free(Node* this) { 
	free(this);
	}



struct List { 
	Node* head;
	uint16_t length;
	};

static List* List_new() { 
	List* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return this;
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
void List_prepend(List* this, void* key, void* val) { 
	Node* ni =  Node_new(key, val, this->head);
	this->head=ni;
	this->length++;
	}
Node* List_find(List* this, void* key) { 
	for (Node *p=this->head,*prev=NULL; p; prev=p,p=p->next) { 
		if (p->key==key) { // we found it, let us delete it
			return p;
			}
		}
	return NULL;
	}
bool List_remove(List* this, void* key) { 
	for (Node *p=this->head,*prev=NULL; p; prev=p,p=p->next) { 
		if (p->key==key) { // we found it, let us delete it
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


struct Dict { 
	List** table;
	int size;
	};

Dict* Dict_constructor(Dict* this,int size) { 
	this->table= calloc(size,sizeof(List*));
	this->size=size;
	return this;
	}

static Dict* Dict_new(int size) { 
	Dict* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Dict_constructor(this, size);
	}

static void Dict_free(Dict* this) { 
	Dict_destructor(this);
	free(this);
	}

void Dict_destructor(Dict* this) { 
	for (int i=0; i<this->size; i++) { 
		if (this->table[i]) { 
			List_free(this->table[i]);
			}
		}
	free (this->table);
	}
List* Dict__find_bucket(Dict* this, void* key) { 
	int hash=(int)key & (this->size-1);
	List* bucket=this->table[hash];
	if (!bucket) { 
		bucket=this->table[hash]=  List_new();
		}
	return bucket;
	}
void* Dict_hget(Dict* this, void* key) { 
	List* bucket= Dict__find_bucket(this,key);
	Node* node= List_find(bucket,key);
	if (node) { 
		return node->val;
		}
	return NULL;
	}
void Dict_hset(Dict* this, void* key, void*value) { 
	List* bucket= Dict__find_bucket(this,key);
	List_prepend(bucket,key,value);
	}
void Dict_hdel(Dict* this, void* key) { 
	List* bucket= Dict__find_bucket(this,key);
	List_remove(bucket,key);
	}

		
// TEST DRIVER
int main() { 
	Dict* t =  Dict_new(1000);
	Dict_hset(t, (void*)10, (void*)20);
	Dict_hset(t, (void*)10, (void*)25);// overwrite possible
	Dict_hset(t, (void*)20, (void*)30);
	Dict_hset(t, (void*)30, (void*)40);
	Dict_hdel(t, (void*)20);
	void* a = Dict_hget(t, (void*)10);
	void* b = Dict_hget(t, (void*)20);
	void* c = Dict_hget(t, (void*)30);
	fprintf (stderr, "10:%d\n", (int)a);
	if (b) { 
		fprintf (stderr, "20:%d\n", (int)b);
		}
	fprintf (stderr, "30:%d\n", (int)c);
	free (t);
	}
//////////////////////////////////////////

