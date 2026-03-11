public typedef uint8_t* TYPE
/* Compute the snapped size for a given requested size. By snapping to powers
of 2 like this, repeated reallocations are avoided. */
#define snapUpSize(x) (--(x), (x)|=(x)>>1, (x)|=(x)>>2, (x)|=(x)>>4, (x)|=(x)>>8, (x)|=(x)>>16, ++(x))


//////////////////////////////////////////////////////////////////////////
// THIS IS A SELF-STARTING THREAD (function to be run is dynamic)
public typedef void* (*func_t)(void *) // needed to avoid bug in compiler!!!
public class Thread:
	pthread_attr_t attr    // thread attributes 
	pthread_t threadid     // the thread id 
	def __init__(self, func_t func, void *argument):
		// disable swapping out our memory (code/stack/ and so one) 
		mlockall(MCL_CURRENT | MCL_FUTURE)
		// initialise the attributes of the thread 
		assert not pthread_attr_init(&self.attr)
		// on Windows, you should return here !
		//assert not pthread_attr_setschedpolicy(&self.attr, SCHED_OTHER)
		assert not pthread_attr_setschedpolicy(&self.attr, SCHED_RR) 
		assert not pthread_attr_setdetachstate(&self.attr, 
												PTHREAD_CREATE_JOINABLE)
		assert not pthread_attr_setscope(&self.attr, PTHREAD_SCOPE_SYSTEM)
		// derive from parent 
		//assert not pthread_attr_setinheritsched(&self.attr, 
		//												PTHREAD_INHERIT_SCHED)
		// stack default is 2Mbytes on Linux, which should be enough !!! 
		// assert not pthread_attr_setstacksize(&self.attr, 0x200000) 		
		// start the thread 
		assert not pthread_create(&self.threadid, &self.attr, func, argument)
	def __del__(self):
		assert not pthread_cancel(self.threadid)
		assert not pthread_join(self.threadid, NULL)						
	void join(self): // should be called from the spawning thread
		assert not pthread_join(self.threadid, NULL)

// THIS IS A JAVA-LIKE THREAD where the run method has to be overridden 
public class Task:
	pthread_attr_t attr    // thread attributes 
	pthread_t threadid     // the thread id 
	void* arg
	bool running=false
	bool detached=false
	public def __init__(self):
		// disable swapping out our memory (code/stack/ and so one) 
		mlockall(MCL_CURRENT | MCL_FUTURE)
		/* initialise the attributes of the thread */
		assert not pthread_attr_init(&self.attr)
		// on Windows, you should return here !
		assert !pthread_attr_setschedpolicy(&self.attr, SCHED_OTHER)
		//assert not pthread_attr_setschedpolicy(&self.attr, SCHED_RR) 
		assert not pthread_attr_setdetachstate(&self.attr, 
													PTHREAD_CREATE_JOINABLE)
		assert not pthread_attr_setscope(&self.attr, PTHREAD_SCOPE_SYSTEM)
		// stack default is 2Mbytes on Linux, which should be enough !!!		
		//assert not pthread_attr_setstacksize(&self.attr, 0x200000) 
	def __del__(self):
		if self.running:
			if not self.detached:
				pthread_detach(self.threadid) 
			pthread_cancel(self.threadid)	
	public def start(self,void* arg):
		self.arg=arg 
		int rc= pthread_create(&self.threadid, &self.attr, Task::callback,self)
		if rc==EAGAIN:
			print "The system lacked the necessary resources to create another "
			print "thread, or the system-imposed limit on the total number of "
			print "threads in a process {PTHREAD_THREADS_MAX} would be exceeded"
			print "\n"
		elif rc== EINVAL: 
			print "The value specified by attr is invalid.\n"
		elif rc==EPERM: 
			print "The caller does not have appropriate permission to set the "
			print "required scheduling parameters or scheduling policy.\n"
		elif rc!=0:
			print "RC=%d\n",rc 		
		assert rc==0
		self.running=true
	public void callback(self):
		self.run(self.arg)		
	@virtual
	void run(self, void* arg):
		print "Please override the Task::run method\n"
	public void join0(self):
		assert not pthread_join(self.threadid, NULL)
	public int join(self):
		int result = -1
		if self.running:
			result = pthread_join(self.threadid, NULL)
			if result==0:
				self.detached=true
		return result
	int make_realtime(self):
		assert not pthread_attr_setschedpolicy(&self.attr, SCHED_RR)
	int detach(self):
		int result = -1
		if self.running:
			if not self.detached:
				result = pthread_detach(self.threadid)
				if result == 0:
					self.detached=true
		return result

class Semaphore:
	sem_t  sem
	def __init__(self, uint32_t initial_count):
		assert not sem_init(&self.sem,0,initial_count)
	def __del__(self):
		assert not sem_destroy(&self.sem)
	void sem_p(self):
		while sem_wait(&self.sem):
			if errno==EINTR:
				continue
			else:
				perror("OSAL: Error in sem_wait call: ")
				exit(-1)
	void sem_v(self):
		int rc=sem_post(&self.sem)
		if rc != 0:
			print "errno=%d\n",errno
			perror("error while posting\n")
	int getvalue(self):
		int sval
		int rc=sem_getvalue(&self.sem, &sval)
		if rc==0:
			return sval
		perror("getvalue error:")


class Mutex:
	pthread_mutex_t* mutex
	pthread_mutexattr_t attr
	def __init__(self):
		self.mutex = new pthread_mutex_t
		assert not pthread_mutexattr_init(&self.attr)
		assert not pthread_mutexattr_setprotocol(&self.attr, 
												PTHREAD_PRIO_INHERIT)
		assert not pthread_mutex_init(self.mutex, &self.attr)
	def __del__(self):
		assert not pthread_mutex_destroy(self.mutex)
		free self.mutex
	void lock(self):
		assert not pthread_mutex_lock(self.mutex)
	void unlock(self):
		assert not pthread_mutex_unlock(self.mutex)

/////////////////////////////////////////////////////////////////////////
private class CircularBuffer: // SIMPLE WORKING VERSION !!!
	TYPE* buf
	long head= 0
	long tail= 0 
	bool empty= true
	bool full= false
	long capacity
	def __init__(self, int capacity):
		self.capacity=capacity
		self.buf= new TYPE[capacity]
	def __del__(self):
		free self.buf
	int push(self, TYPE in):
		if self.full:
			return -1	
		self.buf[self.tail] = in
		self.tail = (self.tail+1) % self.capacity
		if self.tail == self.head:
			self.full = true
		self.empty = false
		return 0
	int pop(self, TYPE* val):
		if self.empty:
			return -1
		TYPE out = self.buf[self.head]
		self.head = (self.head+1) % self.capacity
		if self.head == self.tail:
			self.empty = true
		self.full = false
		*val=out
		return 0
	bool is_full(self):
		return self.full		
	bool is_empty(self):
		return self.empty		

class CircularBuffer0: // BUGGY VERSION
	volatile uint32_t mask               /* mask for quick check (alignment) */
	uint32_t read_counter=0       /* read position in buffer (pointer index) */
	uint32_t write_counter=0      /* write position in buffer (pointer index) */	
	void*  pbuffer[]   			/* buffer itself as flex array member */
	def __init__(self, uint32_t ptr_qty):
		/* smallish buffers do not make sense... */
		if ptr_qty < 4:
			ptr_qty = 4
		// round up to the next power of 2
		ptr_qty *= sizeof(void*)
		ptr_qty <<= 1
		//print "PTR QTY=%d\n", ptr_qty
		unsigned int round_size = 2
		while round_size < 0x8000000 and round_size < ptr_qty:
			round_size <<= 1
		round_size >>= 1
		print "ROUND SIZE=%d\n",round_size
		self = realloc(self,sizeof(CircularBuffer)+round_size)
		if not self:
			return NULL
		/* fill in header */
		self.mask           = round_size-1
	def __del__(self):
		int i=0
		forever:
			uint8_t* pbuf;int ret= self.pop(&pbuf)
			if ret<0:
				break
			if pbuf:
				free pbuf
				print "freeing output buf: %p, ", pbuf
				if ((++i) % 8) == 0:
					 print "\n" 				
		print "\n"	
	uint32_t get_size(self):
		return self.mask + 1
	uint32_t get_space_used(self):
		return self.write_counter - self.read_counter
	uint32_t get_space_left(self):
		uint32_t spaceused=self.get_space_used()
		return self.get_size() - spaceused
	int push(self, void *buf):
		/* check params and if space left.... */
		if self.get_space_left()==0:
			return -1
		self.pbuffer[self.write_counter & self.mask] = buf
		self.write_counter++
		self.write_counter = self.write_counter % 32
		return 0
	int pop(self, void **buf):
		/* check params and if something to read.... */
		if not buf or not self.get_space_used():
			return -1
		print "read counter=%lu, mask=%lu\n",self.read_counter, self.mask
		print "write counter=%lu, mask=%lu\n",self.write_counter, self.mask
		*buf = self.pbuffer[self.read_counter & self.mask]
		self.read_counter++
		self.read_counter = self.read_counter % 32
		assert self.read_counter<=self.write_counter
		return 0
	int peek(self, void **buf):
		/* check params and if something to read.... */
		if not buf or not self.get_space_used():
			return -1
		*buf = self.pbuffer[self.read_counter & self.mask]
		return 0

class ProducerConsumerChannel:	
	CircularBuffer* tx_empty_buffers_list
	CircularBuffer* tx_filled_buffers_list
	CircularBuffer* tx_filled_buffers_size_list
	Semaphore* tx_full_sem
	Semaphore* tx_empty_sem
	Mutex* tx_buf_mutex
	def __init__(self, int number_buffers, int buffer_size):
		self.tx_empty_buffers_list=  new CircularBuffer(number_buffers)
		self.tx_filled_buffers_list= new CircularBuffer(number_buffers)
		self.tx_filled_buffers_size_list= new CircularBuffer(number_buffers)
		for uint8_t i=0; i< number_buffers; i++:
			uint8_t* free_buffer = memalign(BUF_MIN_ALIGNMENT, buffer_size) 
			if not free_buffer:
				print "Unable to allocate mem at line %d\n",__LINE__
				exit(-1)
			else:
				print "memory allocated at address %p\n",free_buffer
			self.tx_empty_buffers_list->push(free_buffer)
		self.tx_full_sem= new Semaphore(0)
		self.tx_full_sem->sem_v()
		self.tx_full_sem->sem_p()
		self.tx_empty_sem= new Semaphore(number_buffers)
		self.tx_empty_sem->sem_p()
		self.tx_empty_sem->sem_v()
		self.tx_buf_mutex= new Mutex()
	def __del__(self):
		delete self.tx_full_sem
		delete self.tx_empty_sem
		delete self.tx_buf_mutex
		delete self.tx_empty_buffers_list
		delete self.tx_filled_buffers_list
		free self.tx_filled_buffers_size_list // don't call the destructor !
	// THESE ARE BLOCKING CALLS !!!
	// First 2 methods for the PRODUCER, last 2 for the CONSUMER
	uint8_t* get_empty_buffer(self): 
		self.tx_empty_sem->sem_p()
		self.tx_buf_mutex->lock()
		uint8_t* buf; self.tx_empty_buffers_list->pop(&buf)
		self.tx_buf_mutex->unlock()
		return buf
	void release_filled_in_buffer(self, uint8_t* buf, uint32_t buffer_len): 
		self.tx_buf_mutex->lock()
		self.tx_filled_buffers_size_list->push(buffer_len)
		self.tx_filled_buffers_list->push(buf) 
		self.tx_buf_mutex->unlock()
		//int count= self.tx_full_sem->getvalue()
		//print "Semaphore count=%ld\n",count
		assert self
		assert self.tx_full_sem 
		self.tx_full_sem->sem_v() // tell consumer it can consume one more
	uint8_t* get_filled_in_buffer(self, uint32_t* size_p): // CONSUMER
		self.tx_full_sem->sem_p()
		self.tx_buf_mutex->lock() 
		uint8_t* buf; self.tx_filled_buffers_list->pop(&buf)
		self.tx_filled_buffers_size_list->pop(size_p)
		self.tx_buf_mutex->unlock()
		return buf
	void release_emptied_buffer(self, uint8_t* buf): // CONSUMER
		self.tx_buf_mutex->lock()
		self.tx_empty_buffers_list->push(buf)
		self.tx_buf_mutex->unlock() 
		self.tx_empty_sem->sem_v() // tell producer it can produce one more


class Producer(Task):
	def __init__(self):
		super.__init__(self)
	@override
	void run(self,void* args):
		for int i=0;i<10;i++:
			uint8_t* buf=ProducerConsumerChannel::get_empty_buffer(G.ch)
			//memset(buf,i,BUFSIZE)
			print "Releasing filled in buffer: %p\n", buf
			ProducerConsumerChannel::release_filled_in_buffer(G.ch,buf,BUFSIZE)

class Consumer(Task):
	def __init__(self):
		super.__init__(self)
	@override
	void run(self,void* args):
		forever:
			int size 
			uint8_t* buf=ProducerConsumerChannel::get_filled_in_buffer(G.ch,&size)
			print "Got filled in buffer %p of size %d\n", buf, size
			sleep(0.1)
			ProducerConsumerChannel::release_emptied_buffer(G.ch,buf)


class G:
	enum:
		BUF_MIN_ALIGNMENT= 64
		BUFSIZE=100
	ProducerConsumerChannel* ch
	def __init__():
		G.ch= new ProducerConsumerChannel(5,BUFSIZE)
		pr := new Producer()
		co := new Consumer()
		Task::start(pr,NULL)
		Task::start(co,NULL)
		Task::join(pr)
		Task::join(co)
	def __del__():
		print "Application stopped\n"
