/*
 * this is a simple linked list implementation
 * Use it when you want to preserver order of insertion
 * often need to remove elements (if not, use a straight array!)  
 */
private class Node:
	Node* next
	void* val
	int key  // used for Schwartzian sort
	def __init__(self, void* v,int key):
		self.val=v
		self.key=key
		self.next=NULL

class List:
	Node* head
	uint16_t length
	Node* p  // for the generator
	def __init__(self):
		self.head=NULL
		self.length=0
	def __del__(self):
		Node* p = self.head
		while p:
			Node* nextNode = p->next
			Node::free(p)
			p = nextNode
	def append(self, void* x):
		ni := new Node(x, -1) 
		if not self.head: // append to NULL = new 
			self.head=ni
		else:
			Node* p=self.head
			while p->next:
				p=p->next
			p->next= ni
		self.length++
	def prepend(self, void* x): // this is faster than append but reverse order!
		ni := new Node(x, -1)
		ni->next=self.head
		self.head=ni
		self.length++
	def insert(self, void* x, int key): // sorted insertion!!!
		ni := new Node(x, key)
		Node* p= self.head
		Node* prev=NULL
		while p:
			if p->key>ni->key: // we found insert place
				break
			prev= p
			p= p->next
		if prev:
			prev->next=ni
		else: 
			self.head=ni
		ni->next=p
		self.length++		
	bool remove(self, void* x):
		for Node *p=self.head,*prev=NULL; p; prev=p,p=p->next:
			if p->val==x: // we found it, let us delete it
				if prev:
					prev->next=p->next
				else: // we delete the first element !!!
					self.head=p->next
				Node::free(p)
				self.length--
				return true
		return false
	void* next(self):
		self.p= self.head
		while self.p:
			yield self.p->val
			self.p = self.p->next
		return NULL


def main():
	q := new List()
	q->insert((void*)5,999)
	q->insert((void*)89,998)
	q->insert((void*)8,997)
	q->insert((void*)18,996)
	q->remove((void*)8)
	for int x in q:
		print "elem=%d\n", x

