// CAVEAT: keys and values are only char* 
// TODO: the value should be void* !!!!!!!!!!
public class Pair:
	Pair* next
	char *key
	char *value
	def __init__(self, char *key, char *value): 
		self.key = strdup(key)
		self.value = strdup(value)
		self.next=NULL
	def __del__(self):
		free self.key
		free self.value

#define CMP_EQ(a,b) (strcmp(a->key,b)==0)  // for the retrieval !!!
public class Bucket: // =List of Pairs
	Pair *head
	uint16_t length
	def __del__(self):
		Pair* p=self.head
		while p:
			Pair* nextNode = p->next
			Pair::free(p)
			p = nextNode
	def append(self, const char *key, const char *value):
		ni :=new Pair(key, value)
		if not self.head: // append to NULL = new 
			self.head=ni
		else:
			Pair* p=self.head
			while p->next:
				p=p->next
			p->next= ni
		self.length++
	def remove_key(self, const char *key):
		if not self.head:
			return // empty list, nothing to do
		if not self.head->next: // only one element
			Pair::free(self.head)
			self.head=NULL
			self.length=0
			return
		Pair* prev=NULL
		for Pair* p= self.head; p->next; prev=p, p=p->next:
			if CMP_EQ(p,key): // we found it, let us delete it
				if prev:
					prev->next=p->next
				else: // we delete the first element !!!
					self.head=p->next
				Pair::free(p)
				self.length--
				return
		print "NOT FOUND\n"
	Pair* get_pair(self, const char *key):
		if not self.head:
			return NULL	
		if not self.head->next: // only one element
			if CMP_EQ(self.head,key):
				return self.head
			return NULL
		for Pair* p= self.head; p->next; p=p->next:
			if CMP_EQ(p,key): // we found it, let us delete it
				return p
		return NULL
	bool add_pair(self, const char *key, const char *value):
		/* Check if we can handle insertion by simply replacing
		 * an existing value in a key-value pair in the bucket.*/
		Pair* pair = self.get_pair(key)
		if pair:
			/* The bucket contains a pair that matches the provided key,
			 * change the value for that pair to the new value.*/
			if strlen(pair->value) < strlen(value):
				/* If the new value is larger than the old value, re-allocate
				 * space for the new larger value.*/
				char* tmp_value= realloc(pair->value,
											(strlen(value)+1)*sizeof(char))
				if not tmp_value:
					return false
				pair->value = tmp_value
			/* Copy the new value into the pair that matches the key */
			strcpy(pair->value, value)
			return true			
		/* Create a key-value pair */
		self.append(key,value)
		return true

public class Dict:
	uint16_t capacity
	Bucket* buckets
	// for the iterator !!!
	Bucket* bucket_pointer
	Pair* pair_pointer
	int i,j
	def __init__(self,uint32_t capacity):
		self.capacity = capacity
		self.buckets = new Bucket[capacity]  //THIS DOESN'T USE THE CONSTRUCTOR!
		if not self.buckets:
			return NULL
	def __del__(self):
		Bucket* bucket= self.buckets
		for uint16_t i = 0;i<self.capacity;i++:
			Bucket::free(bucket)
			bucket++
		free self.buckets
	private Bucket* get_bucket(self,const char *key):
		assert key
		uint32_t index = hash(key) % self.capacity
		return &(self.buckets[index])
	public bool get(self, const char *key, char *out_buf, uint32_t n_out_buf):
		Bucket* bucket= self.get_bucket(key)
		Pair* pair = Bucket::get_pair(bucket, key)
		if not pair or not out_buf:
			return false
		if strlen(pair->value) >= n_out_buf:
			return false
		strcpy(out_buf, pair->value)
		return true
	public bool contains(self, const char *key):
		assert key
		Bucket* bucket= self.get_bucket(key)
		Pair* pair = Bucket::get_pair(bucket, key)
		if not pair:
			return false
		return true	
	public bool put(self, const char *key, const char *value):
		if not key or not value:
			return false
		//Get a pointer to the bucket the key string hashes to
		Bucket* bucket= self.get_bucket(key)
		return Bucket::add_pair(bucket, key, value)			
	public int get_count(self):
		int count=0
		Bucket* bucket = self.buckets
		for uint16_t i=0;i<self.capacity;i++,bucket++:
			count+=bucket->length
		return count
	public bool remove_entry(self,const char* key):
		assert key
		Bucket* bucket= self.get_bucket(key)
		Bucket::remove_key(bucket,key)
		return true	
	public Pair* next(self):
		self.bucket_pointer = self.buckets
		for self.i=0;self.i<self.capacity;self.i++,self.bucket_pointer++:
			self.pair_pointer= self.bucket_pointer->head
			while self.pair_pointer:
				yield self.pair_pointer
				self.pair_pointer = self.pair_pointer->next
		return NULL

private uint32_t hash(const char *str):
	uint32_t hash= 5381
	int32_t c
	while c=*str++:
		hash = ((hash << 5) + hash) + c
	return hash

def main():
	a := new Dict(20)
	a->put("hello", "world1")
	a->put("hello2", "world2")
	a->put("hello3", "world3")
	a->put("hello", "new world")
	a->remove_entry("hello2")
	char buf[256]
	bool succ= a->get("hello",buf,256)
	if succ:
		print "string=%s\n",buf
	succ= a->get("hello2",buf,256)
	if succ:
		print "string=%s\n",buf
	succ= a->get("hello3",buf,256)
	if succ:
		print "string=%s\n",buf
	print "count=%d\n", a->get_count()
	for Pair* p in a: 
		print "+++%s=%s\n",p->key,p->value
	delete a	
