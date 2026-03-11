// Author: HEK
/* Heap queue algorithm (a.k.a. priority queue).*/

private struct q_elem_t:
	void* data
	int pri

private class Heap:
	q_elem_t *elems  // array of q_elem_t
	int num_elems // actual number of elements
	int capacity // allocated memory
	def __init__(self, uint16_t size):
		if size < 4:
			size = 4
		self.capacity = size
		self.num_elems = 0
		self.elems = new q_elem_t[size]
		if self.elems == NULL:
			free self
			return NULL
	def __del__(self):
		free self.elems
	bool empty(self):
		return self.num_elems==0
	private void _siftdown(self, int startpos, int pos):
		q_elem_t newitem = self.elems[pos]
		while pos > startpos:
			int parentpos = (pos-1) >> 1
			q_elem_t parent = self.elems[parentpos]
			if parent.pri <= newitem.pri:
				break
			self.elems[pos] = parent
			pos = parentpos
		self.elems[pos] = newitem
	private void _siftup(self, int pos):
		int endpos = self.num_elems
		int startpos = pos
		q_elem_t newitem = self.elems[pos]
		int childpos = 2*pos + 1	//leftmost child position
		while childpos < endpos:
			int rightpos = childpos+1
			if rightpos < endpos and self.elems[rightpos].pri <= self.elems[childpos].pri:
				childpos = rightpos
			self.elems[pos] = self.elems[childpos]
			pos = childpos
			childpos = 2*pos + 1
		self.elems[pos] = newitem
		self._siftdown(startpos, pos) 
	private void push(self, void* item, int pri):
		self.elems[self.num_elems] = (q_elem_t) { item, pri }
		self.num_elems++
		// TODO CHECK FOR AVAILABLE SPACE, SEE PriorityQueue.cxx
		self._siftdown(0, self.num_elems-1)	
	private void* pop(self):
		q_elem_t lastelt = self.elems[self.num_elems-1]	// raises appropriate IndexError if heap is empty
		self.num_elems--
		q_elem_t returnitem
		if self.num_elems >= 0:
			returnitem = self.elems[0]
			self.elems[0] = lastelt
			self._siftup(0)
		else:
			returnitem = lastelt
		return returnitem.data
	private void* next(self):
		forever:
			if self.empty():
				return NULL
			yield self.pop()

def main():	// Simple sanity test
	heap:=new Heap(10)
	int data[] =:
		11, 33, 55, 77, 99, 22, 44, 66, 88, 0
	for int i=0;i<10;i++:
		heap->push(data[i], data[i])
	for int i in heap:
		print "elem=%d\n",i
	delete heap
