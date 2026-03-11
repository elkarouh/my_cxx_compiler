// TODO: add a real hash function
// TODO: try linear search with sentinel

#define SIZE 1024

uint32_t hash_fun(const char *str):
	uint32_t hash= 5381
	int32_t c
	while c=*str++:
		hash = ((hash << 5) + hash) + c
	return hash

class Node:
	void* key
	void* val
	Node* next
	def __init__(self, void* key,void* val, Node* next):
		self.val=val
		self.key=key
		self.next=next

class List:
	Node* head=NULL
	uint16_t length=0
	def __del__(self):
		Node* p = self.head
		while p:
			Node* nextNode = p->next
			Node::free(p)
			p = nextNode
	def prepend(self, void* key, void* val):
		ni := new Node(key, val, self.head)
		self.head=ni
		self.length++
	Node* find(self, void* key):
		for Node *p=self.head,*prev=NULL; p; prev=p,p=p->next:
			if p->key==key: // we found it, let us delete it
				return p
		return NULL
	bool remove(self, void* key):
		for Node *p=self.head,*prev=NULL; p; prev=p,p=p->next:
			if p->key==key: // we found it, let us delete it
				if prev:
					prev->next=p->next
				else: // we delete the first element !!!
					self.head=p->next
				Node::free(p)
				self.length--
				return true
		return false

class Dict:
	List** table
	int size
	def __init__(self,int size):
		self.table= new List*[size]
		self.size=size
	def __del__(self):
		for int i=0; i<self.size; i++:
			if self.table[i]:
				List::free(self.table[i])
		free self.table
	List* _find_bucket(self, void* key):
		int hash=(int)key & (self.size-1)
		List* bucket=self.table[hash]
		if not bucket:
			bucket=self.table[hash]= new List()
		return bucket
	void* hget(self, void* key):
		List* bucket= Dict::_find_bucket(self,key)
		Node* node= List::find(bucket,key)
		if node:
			return node->val
		return NULL 
	void hset(self, void* key, void*value):
		List* bucket= Dict::_find_bucket(self,key)
		List::prepend(bucket,key,value)		
	void hdel(self, void* key):
		List* bucket= Dict::_find_bucket(self,key)
		List::remove(bucket,key)
		
// TEST DRIVER
int main():
	t := new Dict(1000)
	Dict::hset(t, (void*)10, (void*)20)
	Dict::hset(t, (void*)10, (void*)25)	// overwrite possible
	Dict::hset(t, (void*)20, (void*)30)
	Dict::hset(t, (void*)30, (void*)40)
	Dict::hdel(t, (void*)20)
	void* a = Dict::hget(t, (void*)10)
	void* b = Dict::hget(t, (void*)20)
	void* c = Dict::hget(t, (void*)30)
	print "10:%d\n", (int)a
	if b:
		print "20:%d\n", (int)b
	print "30:%d\n", (int)c
	free t
//////////////////////////////////////////
