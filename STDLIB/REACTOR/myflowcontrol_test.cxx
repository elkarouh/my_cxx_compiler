#include "epoll_reactor.h"
#include "date.h"
/////////////////////////////////////////////////////////////////

class MyPeriodicTask(PeriodicTask_f):
	int count=0
	def __init__(self, Reactor* reactor_engine,double init_delay_ms, double period_ms):
		super.__init__(self, reactor_engine, init_delay_ms, period_ms)
		print "Initializing my periodic task: %ld\n", get_time().tv_sec
	@override
	private void run(self):
		print "IT WORKS: %ld\n", get_time().tv_sec
		if self.count++ > 10:
			print "Periodic Task exiting\n"
			self.terminated=true
			Reactor::stop(self.reactor_engine)
		
#define STDIN 0
class StdinObject:
	uint64_t bytes_received
	uint64_t init_time
	float average_rate	
	def __init__(self, Reactor* reactor_engine):
		self.bytes_received= 0
		reactor_engine->schedule_read_fileobject(STDIN,StdinObject::run,self) 
	private void run(self):
		printf "DATA RECEIVED\n"
		char buffer[1024]
		if self.bytes_received==0:
			struct timeval now= get_time()
			self.init_time= TIMEVAL2MSEC(&now)
		while true:
			size_t num = fread(buffer, 1, sizeof(buffer), stdin)
			if num>0:
				self.bytes_received += num
				fwrite(buffer, 1, num, stdout) // send to standard output
			else:
				return
			struct timeval now= get_time()			
			uint64_t elapsed= TIMEVAL2MSEC(&now) - self.init_time
			if elapsed> 5000:
				self.average_rate=self.bytes_received/elapsed*8/1000.0
				print"bytes received: %lld\n", self.bytes_received
				print"\t\taverage rate in Mbps= %f\r", self.average_rate 

			
///////////////////////////////////////////////////////
		
class MyReactor(Reactor):
	StdinObject* mystdin
	MyPeriodicTask* myperiodictask
	TCP_Server* tcp_server
	def __init__(self):
		super.__init__(self) 
	@override
	private void setup(self):
		printf "INITIALIZING REACTOR\n"
		self.mystdin= new StdinObject(self)
		self.myperiodictask= new MyPeriodicTask(self,1555,3333)

///////////////////////////////////////////////////////
class MainThread(Thread):
	int a
	int b
	def __init__(self, int arg1, int arg2):
		super.__init__(self)
		self.a = arg1
		self.b = arg2
	@override
	void run(self, void* arg):	
		assert self
		char* msg= (char *)arg
		print "%s %d %d\n", msg, self.a, self.b
		myreactor:= new MyReactor()
		myreactor->run()	

class Producer(Thread):
	FlowControlAgent* flowcontrol
	int counter=0
	char* name
	def __init__(self, char* name, FlowControlAgent* agent):
		super.__init__(self)
		self.flowcontrol=agent
		self.name=strdup(name)
	def __del__(self):
		delete self.name
		// delete self.flowcontrol  WE DON'T OWN IT !!!
		super.__del__(self)		
	@override
	def run(self):
		print "%s started\n", self.name
		forever:
			uint8_t* buf=self.flowcontrol->request_free_buffer()
			// produce the buffer
			uint32_t size;
			uint8_t* produced_buffer=self.produce_buffer(buf,&size)
			// release it to the consumer
			print "Produced filled in buffer: %p of size %d\n", produced_buffer,size
			self.flowcontrol->put_filled_in_free_buffer(produced_buffer,size)
			if self._stop:
				break
		print "Producer stopped"
	uint8_t* produce_buffer(self,uint8_t* empty_buffer, uint32_t* sizep):
		sleep(2) // SLOW PRODUCER
		self.counter++
		//memset(buf,i,BUFSIZE)
		strcpy(empty_buffer,"IT WORKS: ")
		*sizep=strlen("IT WORKS: ")
		return empty_buffer

		
class Consumer(Thread):
	FlowControlAgent* flowcontrol
	int counter=0
	char* name	
	def __init__(self, char* name, FlowControlAgent* agent):
		super.__init__(self)
		self.flowcontrol=agent
		self.name=strdup(name)
	def __del__(self):
		delete self.name
		// delete self.flowcontrol  WE DON'T OWN IT !!!
		super.__del__(self)		
	@override
	def run(self):
		print "%s started\n", self.name
		forever:
			int size 
			uint8_t* buf=self.flowcontrol->request_filled_in_buffer(&size)
			print "Got filled in buffer %p of size %d\n", buf, size
			// consume the buffer
			self.consume_buffer(buf)
			// release it back to the producer
			self.flowcontrol->release_filled_in_buffer(buf) 
			if self._stop:
				break
		print "Consumer stopped"
	def consume_buffer(self,uint8_t* full_buffer):
		print "%d==> %s\n",self.counter++, full_buffer
		//delay(2) // SLOW CONSUMER

class G:
	enum:
		BUF_MIN_ALIGNMENT= 64
		BUFSIZE=100
	uint8_t dummy=10 // THERE MUST BE AT LEAST ONE INITIALISATION (bug in my compiler!)
	def __init__(int argc, char *argv[]):
		G::init_app()
		G::run()
	def init_app():
		print "Application started\n"
	def run():
		a:= new MainThread(444,555)
		assert a
		a->start("hello hassan:")
		a->join()
		delete a
		flowcontrol_agent:= new FlowControlAgent(2,500)
		producer:= new Producer("producer",flowcontrol_agent)
		consumer:= new Consumer("consumer",flowcontrol_agent)
		producer->start("HHH")
		consumer->start("jjj")
		sleep(10)
		consumer->stop()
		producer->stop()
		delete flowcontrol_agent
		delete consumer
		delete producer
		print "IT IS DONE\n"
	def __del__():
		print "Application stopped\n"

////////////////////////////////////////////////////////

