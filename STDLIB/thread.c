#define _THREAD_C_
#include "thread.h"

#include "globals.h"

/************************************************/
/*   FORWARD DECLARATION OF STATIC FUNCTIONS    */

typedef struct Semaphore Semaphore; // opaque type
typedef struct Mutex Mutex; // opaque type
typedef struct CircularBuffer CircularBuffer; // opaque type
typedef struct CircularBuffer0 CircularBuffer0; // opaque type
typedef struct ProducerConsumerChannel ProducerConsumerChannel; // opaque type
typedef struct Producer Producer; // opaque type
typedef struct Consumer Consumer; // opaque type
#include "globals.h" 
static Thread* Thread_constructor(Thread* self, func_t func, void *argument);
static void Thread_destructor(Thread* self);
static void Thread_join(Thread* self);
static void Task_destructor(Task* self);
static void Task_run(Task* self, void* arg);
static int Task_make_realtime(Task* self);
static int Task_detach(Task* self);
static Semaphore* Semaphore_constructor(Semaphore* self, uint32_t initial_count);
static Semaphore* Semaphore_new(uint32_t initial_count);
static void Semaphore_free(Semaphore* self);
static void Semaphore_destructor(Semaphore* self);
static void Semaphore_sem_p(Semaphore* self);
static void Semaphore_sem_v(Semaphore* self);
static int Semaphore_getvalue(Semaphore* self);
static Mutex* Mutex_constructor(Mutex* self);
static Mutex* Mutex_new();
static void Mutex_free(Mutex* self);
static void Mutex_destructor(Mutex* self);
static void Mutex_lock(Mutex* self);
static void Mutex_unlock(Mutex* self);
static CircularBuffer* CircularBuffer_constructor(CircularBuffer* self, int capacity);
static CircularBuffer* CircularBuffer_new(int capacity);
static void CircularBuffer_free(CircularBuffer* self);
static void CircularBuffer_destructor(CircularBuffer* self);
static int CircularBuffer_push(CircularBuffer* self, TYPE in);
static int CircularBuffer_pop(CircularBuffer* self, TYPE* val);
static bool CircularBuffer_is_full(CircularBuffer* self);
static bool CircularBuffer_is_empty(CircularBuffer* self);
static CircularBuffer0* CircularBuffer0_constructor(CircularBuffer0* self, uint32_t ptr_qty);
static CircularBuffer0* CircularBuffer0_new(uint32_t ptr_qty);
static void CircularBuffer0_free(CircularBuffer0* self);
static void CircularBuffer0_destructor(CircularBuffer0* self);
static uint32_t CircularBuffer0_get_size(CircularBuffer0* self);
static uint32_t CircularBuffer0_get_space_used(CircularBuffer0* self);
static uint32_t CircularBuffer0_get_space_left(CircularBuffer0* self);
static int CircularBuffer0_push(CircularBuffer0* self, void *buf);
static int CircularBuffer0_pop(CircularBuffer0* self, void **buf);
static int CircularBuffer0_peek(CircularBuffer0* self, void **buf);
static ProducerConsumerChannel* ProducerConsumerChannel_constructor(ProducerConsumerChannel* self, int number_buffers, int buffer_size);
static ProducerConsumerChannel* ProducerConsumerChannel_new(int number_buffers, int buffer_size);
static void ProducerConsumerChannel_free(ProducerConsumerChannel* self);
static void ProducerConsumerChannel_destructor(ProducerConsumerChannel* self);
static uint8_t* ProducerConsumerChannel_get_empty_buffer(ProducerConsumerChannel* self);
static void ProducerConsumerChannel_release_filled_in_buffer(ProducerConsumerChannel* self, uint8_t* buf, uint32_t buffer_len);
static uint8_t* ProducerConsumerChannel_get_filled_in_buffer(ProducerConsumerChannel* self, uint32_t* size_p);
static void ProducerConsumerChannel_release_emptied_buffer(ProducerConsumerChannel* self, uint8_t* buf);
static Producer* Producer_constructor(Producer* self);
static Producer* Producer_new();
static void Producer_free(Producer* self);
static void Producer_run(Producer* self,void* args);
static Consumer* Consumer_constructor(Consumer* self);
static Consumer* Consumer_new();
static void Consumer_free(Consumer* self);
static void Consumer_run(Consumer* self,void* args);
static void G_destructor(void);

/************************************************/

/* Compute the snapped size for a given requested size. By snapping to powers
of 2 like this, repeated reallocations are avoided. */
#define snapUpSize(x) (--(x), (x)|=(x)>>1, (x)|=(x)>>2, (x)|=(x)>>4, (x)|=(x)>>8, (x)|=(x)>>16, ++(x))


//////////////////////////////////////////////////////////////////////////
// THIS IS A SELF-STARTING THREAD (function to be run is dynamic)

Thread* Thread_constructor(Thread* this, func_t func, void *argument) { 
	// disable swapping out our memory (code/stack/ and so one) 
	mlockall(MCL_CURRENT | MCL_FUTURE);
	// initialise the attributes of the thread 
	assert (!pthread_attr_init(&this->attr));
	// on Windows, you should return here !
	//assert not pthread_attr_setschedpolicy(&self.attr, SCHED_OTHER)
	assert (!pthread_attr_setschedpolicy(&this->attr, SCHED_RR));
	assert (!pthread_attr_setdetachstate(&this->attr, 
												PTHREAD_CREATE_JOINABLE));
	assert (!pthread_attr_setscope(&this->attr, PTHREAD_SCOPE_SYSTEM));
	// derive from parent 
	
		//assert not pthread_attr_setinheritsched(&self.attr, 
//												PTHREAD_INHERIT_SCHED)
	// stack default is 2Mbytes on Linux, which should be enough !!! 
	// assert not pthread_attr_setstacksize(&self.attr, 0x200000) 		
	// start the thread 
	assert (!pthread_create(&this->threadid, &this->attr, func, argument));
	return this;
	}

Thread* Thread_new(func_t func, void *argument) { 
	Thread* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Thread_constructor(this, func, argument);
	}

void Thread_free(Thread* this) { 
	Thread_destructor(this);
	free(this);
	}

void Thread_destructor(Thread* this) { 
	assert (!pthread_cancel(this->threadid));
	assert (!pthread_join(this->threadid, NULL));
	}
void Thread_join(Thread* this) { // should be called from the spawning thread
	assert (!pthread_join(this->threadid, NULL));
	}


// THIS IS A JAVA-LIKE THREAD where the run method has to be overridden 

Task* Task_constructor(Task* this) { 
	this->running=false;
	this->detached=false;
	// disable swapping out our memory (code/stack/ and so one) 
	mlockall(MCL_CURRENT | MCL_FUTURE);
	/* initialise the attributes of the thread */
	assert (!pthread_attr_init(&this->attr));
	// on Windows, you should return here !
	assert (!pthread_attr_setschedpolicy(&this->attr, SCHED_OTHER));
	//assert not pthread_attr_setschedpolicy(&self.attr, SCHED_RR) 
	assert (!pthread_attr_setdetachstate(&this->attr, 
													PTHREAD_CREATE_JOINABLE));
	assert (!pthread_attr_setscope(&this->attr, PTHREAD_SCOPE_SYSTEM));
	// stack default is 2Mbytes on Linux, which should be enough !!!		
	//assert not pthread_attr_setstacksize(&self.attr, 0x200000) 
	this->run=Task_run;// virtual method
	return this;
	}

Task* Task_new() { 
	Task* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Task_constructor(this);
	}

void Task_free(Task* this) { 
	Task_destructor(this);
	free(this);
	}

void Task_destructor(Task* this) { 
	if (this->running) { 
		if (!this->detached) { 
			pthread_detach(this->threadid);
			}
		pthread_cancel(this->threadid);
		}
	}
void Task_start(Task* this,void* arg) { 
	this->arg=arg;
	int rc= pthread_create(&this->threadid, &this->attr, Task_callback,this);
	if (rc==EAGAIN) { 
		fprintf (stderr, "The system lacked the necessary resources to create another ");
		fprintf (stderr, "thread, or the system-imposed limit on the total number of ");
		fprintf (stderr, "threads in a process {PTHREAD_THREADS_MAX} would be exceeded");
		fprintf (stderr, "\n");
		}
	else if (rc== EINVAL) { 
		fprintf (stderr, "The value specified by attr is invalid.\n");
		}
	else if (rc==EPERM) { 
		fprintf (stderr, "The caller does !have appropriate permission to set the ");
		fprintf (stderr, "required scheduling parameters or scheduling policy.\n");
		}
	else if (rc!=0) { 
		fprintf (stderr, "RC=%d\n",rc);
		}
	assert (rc==0);
	this->running=true;
	}
void Task_callback(Task* this) { 
	this->run(this,this->arg);
	}
void Task_run(Task* this, void* arg) { 
	fprintf (stderr, "Please override the Task_run method\n");
	}
void Task_join0(Task* this) { 
	assert (!pthread_join(this->threadid, NULL));
	}
int Task_join(Task* this) { 
	int result = -1;
	if (this->running) { 
		result = pthread_join(this->threadid, NULL);
		if (result==0) { 
			this->detached=true;
			}
		}
	return result;
	}
int Task_make_realtime(Task* this) { 
	assert (!pthread_attr_setschedpolicy(&this->attr, SCHED_RR));
	}
int Task_detach(Task* this) { 
	int result = -1;
	if (this->running) { 
		if (!this->detached) { 
			result = pthread_detach(this->threadid);
			if (result == 0) { 
				this->detached=true;
				}
			}
		}
	return result;
	}


struct Semaphore { 
	sem_t  sem;
	};

Semaphore* Semaphore_constructor(Semaphore* this, uint32_t initial_count) { 
	assert (!sem_init(&this->sem,0,initial_count));
	return this;
	}

static Semaphore* Semaphore_new(uint32_t initial_count) { 
	Semaphore* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Semaphore_constructor(this, initial_count);
	}

static void Semaphore_free(Semaphore* this) { 
	Semaphore_destructor(this);
	free(this);
	}

void Semaphore_destructor(Semaphore* this) { 
	assert (!sem_destroy(&this->sem));
	}
void Semaphore_sem_p(Semaphore* this) { 
	while (sem_wait(&this->sem)) { 
		if (errno==EINTR) { 
			continue;
			}
		else { 
			perror("OSAL: Error in sem_wait call: ");
			exit(-1);
			}
		}
	}
void Semaphore_sem_v(Semaphore* this) { 
	int rc=sem_post(&this->sem);
	if (rc != 0) { 
		fprintf (stderr, "errno=%d\n",errno);
		perror("error while (posting\n"));
		}
	}
int Semaphore_getvalue(Semaphore* this) { 
	int sval;
	int rc=sem_getvalue(&this->sem, &sval);
	if (rc==0) { 
		return sval;
		}
	perror("getvalue error:");
	}



struct Mutex { 
	pthread_mutex_t* mutex;
	pthread_mutexattr_t attr;
	};

Mutex* Mutex_constructor(Mutex* this) { 
	this->mutex = malloc(sizeof(*this->mutex));
	assert (!pthread_mutexattr_init(&this->attr));
	assert (!pthread_mutexattr_setprotocol(&this->attr, 
												PTHREAD_PRIO_INHERIT));
	assert (!pthread_mutex_init(this->mutex, &this->attr));
	return this;
	}

static Mutex* Mutex_new() { 
	Mutex* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Mutex_constructor(this);
	}

static void Mutex_free(Mutex* this) { 
	Mutex_destructor(this);
	free(this);
	}

void Mutex_destructor(Mutex* this) { 
	assert (!pthread_mutex_destroy(this->mutex));
	free (this->mutex);
	}
void Mutex_lock(Mutex* this) { 
	assert (!pthread_mutex_lock(this->mutex));
	}
void Mutex_unlock(Mutex* this) { 
	assert (!pthread_mutex_unlock(this->mutex));
	}


/////////////////////////////////////////////////////////////////////////
struct CircularBuffer { // SIMPLE WORKING VERSION !!!
	TYPE* buf;
	long head;
	long tail;
	bool empty;
	bool full;
	long capacity;
	};

CircularBuffer* CircularBuffer_constructor(CircularBuffer* this, int capacity) { 
	this->head= 0;
	this->tail= 0;
	this->empty= true;
	this->full= false;
	this->capacity=capacity;
	this->buf= calloc(capacity,sizeof(TYPE));
	return this;
	}

static CircularBuffer* CircularBuffer_new(int capacity) { 
	CircularBuffer* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return CircularBuffer_constructor(this, capacity);
	}

static void CircularBuffer_free(CircularBuffer* this) { 
	CircularBuffer_destructor(this);
	free(this);
	}

void CircularBuffer_destructor(CircularBuffer* this) { 
	free (this->buf);
	}
int CircularBuffer_push(CircularBuffer* this, TYPE in) { 
	if (this->full) { 
		return -1;
		}
	this->buf[this->tail] = in;
	this->tail = (this->tail+1) % this->capacity;
	if (this->tail == this->head) { 
		this->full = true;
		}
	this->empty = false;
	return 0;
	}
int CircularBuffer_pop(CircularBuffer* this, TYPE* val) { 
	if (this->empty) { 
		return -1;
		}
	TYPE out = this->buf[this->head];
	this->head = (this->head+1) % this->capacity;
	if (this->head == this->tail) { 
		this->empty = true;
		}
	this->full = false;
	*val=out;
	return 0;
	}
bool CircularBuffer_is_full(CircularBuffer* this) { 
	return this->full;
	}
bool CircularBuffer_is_empty(CircularBuffer* this) { 
	return this->empty;
	}


struct CircularBuffer0 { // BUGGY VERSION
	volatile uint32_t mask;/* mask for quick check (alignment) */
	uint32_t read_counter;/* read position in buffer (pointer index) */
	uint32_t write_counter;/* write position in buffer (pointer index) */	
	void*  pbuffer[];/* buffer itself as flex array member */
	};

CircularBuffer0* CircularBuffer0_constructor(CircularBuffer0* this, uint32_t ptr_qty) { 
	this->read_counter=0;/* read position in buffer (pointer index) */
	this->write_counter=0;/* write position in buffer (pointer index) */	
	/* smallish buffers do not make sense... */
	if (ptr_qty < 4) { 
		ptr_qty = 4;
		}
	// round up to the next power of 2
	ptr_qty *= sizeof(void*);
	ptr_qty <<= 1;
	//print "PTR QTY=%d\n", ptr_qty
	unsigned int round_size = 2;
	while (round_size < 0x8000000  &&  round_size < ptr_qty) { 
		round_size <<= 1;
		}
	round_size >>= 1;
	fprintf (stderr, "ROUND SIZE=%d\n",round_size);
	this = realloc(this,sizeof(CircularBuffer)+round_size);
	if (!this) { 
		return NULL;
		}
	/* fill in header */
	this->mask           = round_size-1;
	return this;
	}

static CircularBuffer0* CircularBuffer0_new(uint32_t ptr_qty) { 
	CircularBuffer0* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return CircularBuffer0_constructor(this, ptr_qty);
	}

static void CircularBuffer0_free(CircularBuffer0* this) { 
	CircularBuffer0_destructor(this);
	free(this);
	}

void CircularBuffer0_destructor(CircularBuffer0* this) { 
	int i=0;
	for (;;) { 
		uint8_t* pbuf;int ret= CircularBuffer0_pop(this,&pbuf);
		if (ret<0) { 
			break;
			}
		if (pbuf) { 
			free (pbuf);
			fprintf (stderr, "freeing output buf: %p, ", pbuf);
			if (((++i) % 8) == 0) { 
				 fprintf (stderr, "\n");
				}
			}
		}
	fprintf (stderr, "\n");
	}
uint32_t CircularBuffer0_get_size(CircularBuffer0* this) { 
	return this->mask + 1;
	}
uint32_t CircularBuffer0_get_space_used(CircularBuffer0* this) { 
	return this->write_counter - this->read_counter;
	}
uint32_t CircularBuffer0_get_space_left(CircularBuffer0* this) { 
	uint32_t spaceused=CircularBuffer0_get_space_used(this);
	return CircularBuffer0_get_size(this) - spaceused;
	}
int CircularBuffer0_push(CircularBuffer0* this, void *buf) { 
	/* check params and if space left.... */
	if (CircularBuffer0_get_space_left(this)==0) { 
		return -1;
		}
	this->pbuffer[this->write_counter & this->mask] = buf;
	this->write_counter++;
	this->write_counter = this->write_counter % 32;
	return 0;
	}
int CircularBuffer0_pop(CircularBuffer0* this, void **buf) { 
	/* check params and if something to read.... */
	if (!buf  ||  !CircularBuffer0_get_space_used(this)) { 
		return -1;
		}
	fprintf (stderr, "read counter=%lu, mask=%lu\n",this->read_counter, this->mask);
	fprintf (stderr, "write counter=%lu, mask=%lu\n",this->write_counter, this->mask);
	*buf = this->pbuffer[this->read_counter & this->mask];
	this->read_counter++;
	this->read_counter = this->read_counter % 32;
	assert (this->read_counter<=this->write_counter);
	return 0;
	}
int CircularBuffer0_peek(CircularBuffer0* this, void **buf) { 
	/* check params and if something to read.... */
	if (!buf  ||  !CircularBuffer0_get_space_used(this)) { 
		return -1;
		}
	*buf = this->pbuffer[this->read_counter & this->mask];
	return 0;
	}


struct ProducerConsumerChannel { 
	CircularBuffer* tx_empty_buffers_list;
	CircularBuffer* tx_filled_buffers_list;
	CircularBuffer* tx_filled_buffers_size_list;
	Semaphore* tx_full_sem;
	Semaphore* tx_empty_sem;
	Mutex* tx_buf_mutex;
	};

ProducerConsumerChannel* ProducerConsumerChannel_constructor(ProducerConsumerChannel* this, int number_buffers, int buffer_size) { 
	this->tx_empty_buffers_list=   CircularBuffer_new(number_buffers);
	this->tx_filled_buffers_list=  CircularBuffer_new(number_buffers);
	this->tx_filled_buffers_size_list=  CircularBuffer_new(number_buffers);
	for (uint8_t i=0; i< number_buffers; i++) { 
		uint8_t* free_buffer = memalign(BUF_MIN_ALIGNMENT, buffer_size);
		if (!free_buffer) { 
			fprintf (stderr, "Unable to allocate mem at line %d\n",__LINE__);
			exit(-1);
			}
		else { 
			fprintf (stderr, "memory allocated at address %p\n",free_buffer);
			}
		CircularBuffer_push(this->tx_empty_buffers_list,free_buffer);
		}
	this->tx_full_sem=  Semaphore_new(0);
	Semaphore_sem_v(this->tx_full_sem);
	Semaphore_sem_p(this->tx_full_sem);
	this->tx_empty_sem=  Semaphore_new(number_buffers);
	Semaphore_sem_p(this->tx_empty_sem);
	Semaphore_sem_v(this->tx_empty_sem);
	this->tx_buf_mutex=  Mutex_new();
	return this;
	}

static ProducerConsumerChannel* ProducerConsumerChannel_new(int number_buffers, int buffer_size) { 
	ProducerConsumerChannel* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return ProducerConsumerChannel_constructor(this, number_buffers, buffer_size);
	}

static void ProducerConsumerChannel_free(ProducerConsumerChannel* this) { 
	ProducerConsumerChannel_destructor(this);
	free(this);
	}

void ProducerConsumerChannel_destructor(ProducerConsumerChannel* this) { 
	Semaphore_free(this->tx_full_sem);
	Semaphore_free(this->tx_empty_sem);
	Mutex_free(this->tx_buf_mutex);
	CircularBuffer_free(this->tx_empty_buffers_list);
	CircularBuffer_free(this->tx_filled_buffers_list);
	free (this->tx_filled_buffers_size_list);// don't call the destructor !
	}
// THESE ARE BLOCKING CALLS !!!
// First 2 methods for the PRODUCER, last 2 for the CONSUMER
uint8_t* ProducerConsumerChannel_get_empty_buffer(ProducerConsumerChannel* this) { 
	Semaphore_sem_p(this->tx_empty_sem);
	Mutex_lock(this->tx_buf_mutex);
	uint8_t* buf; CircularBuffer_pop(this->tx_empty_buffers_list,&buf);
	Mutex_unlock(this->tx_buf_mutex);
	return buf;
	}
void ProducerConsumerChannel_release_filled_in_buffer(ProducerConsumerChannel* this, uint8_t* buf, uint32_t buffer_len) { 
	Mutex_lock(this->tx_buf_mutex);
	CircularBuffer_push(this->tx_filled_buffers_size_list,buffer_len);
	CircularBuffer_push(this->tx_filled_buffers_list,buf);
	Mutex_unlock(this->tx_buf_mutex);
	//int count= self.tx_full_sem->getvalue()
	//print "Semaphore count=%ld\n",count
	assert (this);
	assert (this->tx_full_sem);
	Semaphore_sem_v(this->tx_full_sem);// tell consumer it can consume one more
	}
uint8_t* ProducerConsumerChannel_get_filled_in_buffer(ProducerConsumerChannel* this, uint32_t* size_p) { // CONSUMER
	Semaphore_sem_p(this->tx_full_sem);
	Mutex_lock(this->tx_buf_mutex);
	uint8_t* buf; CircularBuffer_pop(this->tx_filled_buffers_list,&buf);
	CircularBuffer_pop(this->tx_filled_buffers_size_list,size_p);
	Mutex_unlock(this->tx_buf_mutex);
	return buf;
	}
void ProducerConsumerChannel_release_emptied_buffer(ProducerConsumerChannel* this, uint8_t* buf) { // CONSUMER
	Mutex_lock(this->tx_buf_mutex);
	CircularBuffer_push(this->tx_empty_buffers_list,buf);
	Mutex_unlock(this->tx_buf_mutex);
	Semaphore_sem_v(this->tx_empty_sem);// tell producer it can produce one more
	}



struct Producer { 
	Task;
	};

Producer* Producer_constructor(Producer* this) { 
	Task_constructor((Task*)this);
	this->run=Producer_run;// virtual method
	return this;
	}

static Producer* Producer_new() { 
	Producer* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Producer_constructor(this);
	}

static void Producer_free(Producer* this) { 
	Task_free(this);
	}

void Producer_run(Producer* this,void* args) { 
	for (int i=0;i<10;i++) { 
		uint8_t* buf=ProducerConsumerChannel_get_empty_buffer(G.ch);
		//memset(buf,i,BUFSIZE)
		fprintf (stderr, "Releasing filled in buffer: %p\n", buf);
		ProducerConsumerChannel_release_filled_in_buffer(G.ch,buf,BUFSIZE);
		}
	}


struct Consumer { 
	Task;
	};

Consumer* Consumer_constructor(Consumer* this) { 
	Task_constructor((Task*)this);
	this->run=Consumer_run;// virtual method
	return this;
	}

static Consumer* Consumer_new() { 
	Consumer* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Consumer_constructor(this);
	}

static void Consumer_free(Consumer* this) { 
	Task_free(this);
	}

void Consumer_run(Consumer* this,void* args) { 
	for (;;) { 
		int size;
		uint8_t* buf=ProducerConsumerChannel_get_filled_in_buffer(G.ch,&size);
		fprintf (stderr, "Got filled in buffer %p of size %d\n", buf, size);
		sleep(0.1);
		ProducerConsumerChannel_release_emptied_buffer(G.ch,buf);
		}
	}



