#include <sys/timerfd.h>
#include <sys/epoll.h>

#define MAXEVENTS 64

public int setNonBlocking(int fd):
	int flags=fcntl(fd, F_GETFL, 0)
	if flags == -1:
		flags = 0
	return fcntl(fd, F_SETFL, flags | O_NONBLOCK)

public struct Callback:
	int fd
	void (*action_handler)(void*)
	void* arg  // pointer to the object

private int timer_set_expiry(int timer, time_t sec, long nsec, time_t intsec, long intnsec):
	struct itimerspec timerSpec
	memset(&timerSpec, 0, sizeof(timerSpec))
	timerSpec.it_value.tv_sec = sec
	timerSpec.it_value.tv_nsec = nsec
	timerSpec.it_interval.tv_sec = intsec
	timerSpec.it_interval.tv_nsec = intnsec
	struct itimerspec oldSpec
	return timerfd_settime(timer, 0, &timerSpec, &oldSpec)

public class Reactor:
	int epoll_fd
	Callback* fd_repository[0xFFFF] 
	bool _stop=false
	public def __init__(self):
		self.epoll_fd = epoll_create1(0)
		memset(self.fd_repository,0, sizeof self.fd_repository)
	@virtual
	private void setup(self):
		print "Please override this function:Reactor::setup\n"
	public void run(self):
		self.setup()
		struct epoll_event* events=calloc(MAXEVENTS,sizeof *events)
		forever:
			int nfds = epoll_wait (self.epoll_fd, events, MAXEVENTS, -1)
			if nfds==-1:
				if errno == EINTR:
					continue
				else:
					perror("EPOLL ERROR:")
					abort()	
			for int i=0; i<nfds; i++:
				Callback* action = (Callback*) events[i].data.ptr
				if not action:
					continue
				if events[i].events & EPOLLERR: 
					print "epoll error\n"
					close(action->fd)
					continue
				if events[i].events & EPOLLHUP:
					print "epoll error\n"
					close(action->fd)
					continue
				if events[i].events & EPOLLIN:
					//print "Event ready for reading\n"
					action->action_handler(action->arg)
				if events[i].events & EPOLLOUT:
					print "Event ready for writing\n"
			if self._stop:
				print "Exiting reactor\n"
				break
	public void stop(self):
		self._stop=true
	public void schedule_read_fileobject(self, int fd, void (*callback)(void*), void* args):
		assert self.fd_repository[fd]==NULL
		action := new Callback
		self.fd_repository[fd]= action 
		*action= (Callback){.fd=fd,.action_handler=callback,.arg=args}
		setNonBlocking(fd)
		epoll_ctl(self.epoll_fd,EPOLL_CTL_ADD,fd,(struct epoll_event[]){{.data.fd=fd,.data.ptr = action,.events=EPOLLIN | EPOLLET}})
	public void schedule_write_fileobject(self, int fd, void (*callback)(void*), void* args):
		action := new Callback
		self.fd_repository[fd]= action 
		*action= (Callback){.fd=fd,.action_handler=callback,.arg=args}
		setNonBlocking(fd)
		epoll_ctl(self.epoll_fd,EPOLL_CTL_ADD,fd,(struct epoll_event[]){{.data.fd=fd,.data.ptr = action,.events=EPOLLOUT | EPOLLET}})
	public void remove_fileobject(self, int fd):
		int ret = epoll_ctl(self.epoll_fd, EPOLL_CTL_DEL, fd, NULL)
		Callback* cb=self.fd_repository[fd]
		if cb:
			free cb
		self.fd_repository[fd]=NULL
	public int schedule_timed_event(self,void (*callback)(void*), void* args, time_t sec, long nsec, time_t intsec, long intnsec):
		int fd=timerfd_create(CLOCK_REALTIME, 0) // TFD_NONBLOCK  iso 0 
		action := new Callback
		action->fd = fd
		action->action_handler = callback
		action->arg = args
		self.fd_repository[fd]= action
		int rc=epoll_ctl(self.epoll_fd,EPOLL_CTL_ADD,fd,(struct epoll_event[]){{.data.ptr = action,.events=EPOLLIN | EPOLLET}})
		//print "Scheduling time event, rc= %d %d %d %d %d\n", rc,sec, nsec, intsec, intnsec
		int res=timer_set_expiry(action->fd, sec, nsec, intsec, intnsec)
		//fcntl(tfd, F_SETFL, fcntl(tfd, F_GETFL, 0) | O_NONBLOCK)
		return fd
	public def remove_timed_event(self, int fd):
		Callback* cb=self.fd_repository[fd]
		if cb:
			free cb
		int ret = epoll_ctl(self.epoll_fd, EPOLL_CTL_DEL, fd, NULL)
		//print "set timer expiry: %d\n",fd
		int res=timer_set_expiry(fd, 0, 0, 0, 0)
		//print "closing timer fd: %d\n",fd
		close(fd)
		print "timer closed, fd= %d\n",fd
		self.fd_repository[fd]=NULL

/***************************************************************************/
// MAY NOT BE OPAQUE IF YOU WANT INHERITANCE!

public class PeriodicTask_f:
	Reactor* reactor_engine
	uint16_t period
	uint16_t counter
	int fd
	bool terminated=false
	public def __init__(self, Reactor* reactor_engine, double initial_delay_ms,double period_ms):
		double period_nsec= period_ms*1000_000
		uint64_t sec= period_nsec/1000_000_000
		uint64_t nsec=period_nsec-sec*1000_000_000
		//
		double initial_delay_nsec= initial_delay_ms*1000_000
		uint64_t sec0= initial_delay_nsec/1000_000_000
		uint64_t nsec0=initial_delay_nsec-sec0*1000_000_000
		//print "timer started with period: %llu sec, %llu nsec ",sec, nsec
		//print "and initial delay: %llu sec, %llu nsec\n",sec0, nsec0
		self.fd=Reactor::schedule_timed_event(reactor_engine,
											PeriodicTask_f::process_time_event,
											self,
											sec0,nsec0,sec,nsec)
		self.reactor_engine= reactor_engine	
		self.period=period_ms
		self.counter=0
	public def __del__(self):
		self.terminated=true
		Reactor::remove_timed_event(self.reactor_engine,self.fd)
	def process_time_event(self):
		if self.terminated:
			return
		uint8_t buf[512]
		ssize_t count = read(self.fd, buf, sizeof buf) // THIS MUST HAPPEN !!!
		//print "COUNT= %d\n", count
		self.run()
	@virtual
	public void run(self):
		print "please OVERRIDE\n"
	public int update_timer(self,double initial_delay_ms,double period_ms):
		double period_nsec= period_ms*1000_000
		uint64_t sec= period_nsec/1000_000_000
		uint64_t nsec=period_nsec-sec*1000_000_000
		double initial_delay_nsec= initial_delay_ms*1000_000
		uint64_t sec0= initial_delay_nsec/1000_000_000
		uint64_t nsec0=initial_delay_nsec-sec0*1000_000_000
		if sec0==0 and nsec0==0:
			nsec0=1000 // don't disable the timer !!!
		int res=timer_set_expiry(self.fd, sec0,nsec0,sec,nsec)
		uint64_t value; read(self.fd, &value, 8)
		return res
/////////////////////////////////////////////////////////////////////////////
// if you want to see all threads, do 
// ps -eTo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,wchan:14,comm
// ps -eLo pid, pcpu, args

public class Task:
	pthread_attr_t attr    // thread attributes 
	pthread_t threadid     // the thread id 
	void* arg
	int max_prio
	int min_prio
	bool _stop=false	
	public def __init__(self):
		assert not pthread_attr_init(&self.attr)
		assert not pthread_attr_setschedpolicy(&self.attr, SCHED_RR) 
		assert not pthread_attr_setdetachstate(&self.attr, PTHREAD_CREATE_JOINABLE)
		assert not pthread_attr_setscope(&self.attr, PTHREAD_SCOPE_SYSTEM)
		//assert not pthread_attr_setstacksize(attr, 0x200000) // 2MB stack default 
		assert not pthread_attr_setinheritsched(&self.attr, PTHREAD_EXPLICIT_SCHED)
		self.max_prio=sched_get_priority_max(SCHED_RR) // should be 99
		self.min_prio=sched_get_priority_min(SCHED_RR) // should be 1	
	public def __del__(self):
		pthread_attr_destroy(&self.attr) 
	public def start(self,void* arg):
		self.arg=arg 
		struct sched_param param
		// GIVE A NON-NULL PARAMETER IF YOU WANT HIGHEST PRIORITY !!!
		if arg:			
			param.sched_priority= self.max_prio-10 
		else:
			param.sched_priority= self.min_prio+10
		assert not pthread_attr_setschedparam(&self.attr,&param)
		int rc= pthread_create(&self.threadid, &self.attr, Task::callback,self)
		if rc==EAGAIN:
			print "The system lacked the necessary resources to create another thread, or the system-imposed limit on the total number of threads in a process {PTHREAD_THREADS_MAX} would be exceeded.\n"
		elif rc== EINVAL: 
			print "The value specified by attr is invalid.\n"
		elif rc==EPERM: 
			print "The caller does not have appropriate permission to set the required scheduling parameters or scheduling policy.\n"
		elif rc!=0:
			print "RC=%d\n",rc
		assert rc==0
	public void callback(self):
		self.run(self.arg)		
	@virtual
	void run(self, void* arg):
		print "Please override the Task::run method\n"
	public void join(self):
		int rc= pthread_join(self.threadid, NULL)
		assert rc==0
	public void cancel(self):
		int rc= pthread_cancel(self.threadid)
		assert rc=0
		rc=pthread_join(self.threadid, NULL)
		assert rc=0
	def stop(self):
		self._stop=true

//public class Task_non_rt:
public class Thread:
	pthread_attr_t attr    // thread attributes 
	pthread_t threadid     // the thread id 
	void* arg
	int max_prio
	int min_prio
	bool _stop=false
	public def __init__(self):
		assert not pthread_attr_init(&self.attr)
		assert not pthread_attr_setschedpolicy(&self.attr, SCHED_OTHER) 
		assert not pthread_attr_setdetachstate(&self.attr, PTHREAD_CREATE_JOINABLE)
		assert not pthread_attr_setscope(&self.attr, PTHREAD_SCOPE_SYSTEM)
		//assert not pthread_attr_setstacksize(attr, 0x200000) // 2MB stack default 
	public def __del__(self):
		pthread_attr_destroy(&self.attr) 
	public def start(self,void* arg):
		self.arg=arg 
		int rc= pthread_create(&self.threadid, &self.attr, Task::callback,self)
		if rc==EAGAIN:
			print "The system lacked the necessary resources to create another thread, or the system-imposed limit on the total number of threads in a process {PTHREAD_THREADS_MAX} would be exceeded.\n"
		elif rc== EINVAL: 
			print "The value specified by attr is invalid.\n"
		elif rc==EPERM: 
			print "The caller does not have appropriate permission to set the required scheduling parameters or scheduling policy.\n"
		elif rc!=0:
			print "RC=%d\n",rc
		assert rc==0
	public void callback(self):
		self.run(self.arg)		
	@virtual
	void run(self, void* arg):
		print "Please override the Task::run method\n"
	public void join(self):
		int rc= pthread_join(self.threadid, NULL)
		assert rc==0
	public void cancel(self):
		int rc= pthread_cancel(self.threadid)
		assert rc=0
		rc=pthread_join(self.threadid, NULL)
		assert rc=0
	public void stop(self):
		self._stop=true		
////////////////////////////////////////////////////////////////////////////
/***************************************************************************/
void *get_in_addr(struct sockaddr *sa):
	"""
	'  get sockaddr, IPv4 or IPv6
	"""
	if sa->sa_family == AF_INET:
		return &(((struct sockaddr_in*)sa)->sin_addr)
	return &(((struct sockaddr_in6*)sa)->sin6_addr)

public class UDP_server:
	Reactor* reactor_engine
	int sockfd
	struct sockaddr_storage cliaddr
	uint8_t rx_buffer[0xFFFF]	
	public def __init__(self, Reactor* reactor_engine, char* MYPORT):
		self.setup_udp_server_socket(MYPORT)
		self.reactor_engine= reactor_engine
		reactor_engine->schedule_read_fileobject(self.sockfd,UDP_server::process_data,self)
		//print "UDP listener: waiting to recv on port %s...\n", MYPORT
	public def __del__(self):
		close(self.sockfd)	
		Reactor::remove_fileobject(self.reactor_engine,self.sockfd)		
	private void process_data(self):
		forever:
			bool close_it = false
			char s[INET6_ADDRSTRLEN]
			socklen_t addr_len = sizeof self.cliaddr
			int numbytes = recvfrom(self.sockfd, self.rx_buffer, 0xFFFE , 
			                0, (struct sockaddr *)&self.cliaddr, &addr_len)
			if numbytes== -1:
				// If errno == EAGAIN, that means we have read all
				// data. So go back to the main loop.
				if errno == EAGAIN:
					return
				perror "recvfrom"
				close_it= true
			elif numbytes== 0:
				// End of file. The remote has closed the connection.
				print "END OF FILE DETECTED !!!!!!\n"
				close_it = true
			else:
				// call the callback function !!!
				char* client_address=inet_ntop(self.cliaddr.ss_family,
			                 get_in_addr((struct sockaddr *)&self.cliaddr), 
							 s, 
							 sizeof s)
				self.process_message(self.rx_buffer,numbytes)
			if close_it:
				print "Closed connection on descriptor %d\n", self.sockfd
				// Closing the descriptor will make epoll remove it
				// from the set of descriptors which are monitored.
				close(self.sockfd)	
				Reactor::remove_fileobject(self.reactor_engine,self.sockfd)
				return		
	@virtual
	def process_message(self, uint8_t* message, int len ):
		print "Please override !!!\n"
	private void setup_udp_server_socket(self, char* PORT):
		struct addrinfo hints, *servinfo, *p
		memset(&hints, 0, sizeof hints)
		hints.ai_family = AF_UNSPEC // set to AF_INET to force IPv4
		hints.ai_socktype = SOCK_DGRAM
		hints.ai_flags = AI_PASSIVE // use my IP
		int rv = getaddrinfo(NULL, PORT, &hints, &servinfo)
		if rv != 0:
			//print "getaddrinfo: %s\n", gai_strerror(rv)
			perror "getaddrinfo"
			exit(-2)
		// loop through all the results and bind to the first we can
		int sockfd
		for p = servinfo; p != NULL; p = p->ai_next:
			sockfd = socket(p->ai_family, p->ai_socktype,p->ai_protocol)
			if sockfd == -1:
				perror "listener: socket"
				continue
			if bind(sockfd, p->ai_addr, p->ai_addrlen) == -1:
				close(sockfd)
				perror "listener: bind"
				continue
			break
		if p == NULL:
			perror "listener: failed to bind socket\n"
			exit(-2)
		freeaddrinfo(servinfo) // free the linked-list
		self.sockfd=sockfd
	public int send_data(self, uint8_t* message, int len):
		int rc=sendto(self.sockfd, message, len, 0, 
						(struct sockaddr*)&self.cliaddr,sizeof(self.cliaddr))
		return rc

public class TCP_Client:
	int fd
	uint8_t read_buffer[0xFFFF]
	Reactor* reactor_engine
	uint16_t read_idx=0
	public def __init__(self, Reactor* engine,int fd):
		self.fd=fd
		self.reactor_engine= engine
	public void receive_data(self):
		int bytes_read= recv(self.fd,
							self.read_buffer+self.read_idx, 
							sizeof(self.read_buffer)-self.read_idx,0)
		if bytes_read==-1:
			print "Error\n"
		elif bytes_read==0:
			// connection lost
			self.tear_down()
		else:
			uint16_t bytes_to_process= self.read_idx+bytes_read
			uint16_t idx=self.parse_message(self.read_buffer,bytes_to_process)
			uint16_t unprocessed_len= bytes_to_process-idx
			if unprocessed_len: // could not process everything
				memmove(self.read_buffer,self.read_buffer+idx,unprocessed_len)
			self.read_idx= unprocessed_len
	@virtual
	uint16_t parse_message(self,uint8_t* message, int len):
		"""
		'returns the index of the processed data.
		"""
		print "Please override TCP_Client::parse_message\n"
		return len

	private def tear_down(self):
		close(self.fd)


public class TCP_Server:
	Reactor* reactor_engine
	char name[256]
	char ip_address_dot[256]
	uint16_t port_number
	int server_socket_fd
	TCP_Client* (*client_constructor)(void*,int)
	def __init__(self, Reactor* reactor_engine,char* name, char* ip_address_dot, int port_number,TCP_Client* (*client_constructor)(void*,int)):
		self.client_constructor=client_constructor
		self.reactor_engine= reactor_engine
		strcpy(self.name, name)
		strcpy(self.ip_address_dot, ip_address_dot)
		self.port_number= port_number
		int server_socket_fd = socket(AF_INET, SOCK_STREAM, 0)
		if server_socket_fd == -1 :
			print "Error creating socket: %d\n", errno
			perror "socket create"
			exit(3)
		self.server_socket_fd= server_socket_fd
		print "Server socket successfully created\n"
		// Allow address reuse
		int err = setsockopt(server_socket_fd, SOL_SOCKET, SO_REUSEADDR, &(int){1}, sizeof(int))
		if err == -1 :
			print "Error setting SO_REUSEADDR on socket: %d\n", errno
			perror "setsockopt"
			exit(3)
		print "Socket Reuse Address option successfully set\n"
		// bind
		struct sockaddr_in addr =:	
			.sin_family = AF_INET
			.sin_port = htons(port_number)
			.sin_addr.s_addr = INADDR_ANY
		err =bind(server_socket_fd,(struct sockaddr *) &addr, sizeof(struct sockaddr))
		if err == -1 :
			print "bind error: %d\n", errno
			perror "bind"
			exit(3)
		print "Socket Bind successful\n"
		err = listen(server_socket_fd, 5) // we allow  up to 5 clients at a time
		if err == -1 :
			print "listen error: %d\n", errno
			perror "listen"
			exit(3)
		print "Socket Listen successful\n"
		print "Waiting for connection on port %d\n", self.port_number
		Reactor::schedule_read_fileobject(reactor_engine, 
			server_socket_fd, 
			TCP_Server::accept, 
			self)
	public void accept(self):
		struct sockaddr_in *client_addr= malloc(sizeof(*client_addr))
		socklen_t client_addr_size = sizeof(struct sockaddr)
		int client_fd = accept(self.server_socket_fd, 
										(struct sockaddr *)client_addr, 
										&client_addr_size)
		print "Client successfully accepted\n"
		TCP_Client* client= self.client_constructor(self.reactor_engine,client_fd)
		assert client
		Reactor::schedule_read_fileobject(self.reactor_engine,
											client_fd,
											TCP_Client::receive_data,
											client)
	public void teardown(self):
		close(self.server_socket_fd)

public class UDP_client:
	int sockfd
	struct sockaddr_in servaddr
	uint8_t rx_buffer[0xFFFF]
	public def __init__(self, Reactor* reactor_engine, char* SERV_ADDR,char* SERV_PORT):
		self.setup_udp_client_socket(SERV_ADDR,SERV_PORT)
		if reactor_engine:
			reactor_engine->schedule_read_fileobject(self.sockfd,
												UDP_client::process_data,self)
	private void process_data(self):
		forever:
			bool close_it = false
			int numbytes = recvfrom(self.sockfd, self.rx_buffer,0xFFFE, 0, NULL, NULL)		                
			if numbytes== -1:
				// If errno == EAGAIN, that means we have read all
				// data. So go back to the main loop.
				if errno == EAGAIN:
					return
				perror "recvfrom"
				close_it= true
			elif numbytes== 0:
				// End of file. The remote has closed the connection.
				print "END OF FILE DETECTED !!!!!!\n"
				close_it = true
			else:
				// call the callback function !!!
				self.process_message(self.rx_buffer,numbytes)
			if close_it:
				print "Closed connection on descriptor %d\n", self.sockfd
				// Closing the descriptor will make epoll remove it
				// from the set of descriptors which are monitored.
				close (self.sockfd)
	@virtual
	def process_message(self, uint8_t* message, int len ):
		print "Please override !!!\n"
	private int setup_udp_client_socket(self,char* ip_address, char* SERVERPORT):
		struct addrinfo hints, *servinfo, *p
		memset(&hints, 0, sizeof hints)
		hints.ai_family = AF_UNSPEC
		hints.ai_socktype = SOCK_DGRAM
		int rv = getaddrinfo(ip_address, SERVERPORT, &hints, &servinfo)	
		if rv != 0:
			//print "getaddrinfo: %s\n", gai_strerror(rv)
			perror "getaddrinfo"
			exit(-2)
		// loop through all the results and make a socket
		int sockfd
		for p = servinfo; p != NULL; p = p->ai_next:
			sockfd = socket(p->ai_family, p->ai_socktype,p->ai_protocol)
			if sockfd == -1:
				perror "client: socket"
				continue		
			break
		if p == NULL:
			print "client: failed to bind socket\n"
			exit(-2)
		self.sockfd=sockfd
		self.servaddr= *(struct sockaddr_in*)(p->ai_addr)
		// let us free the memory
		freeaddrinfo(servinfo)		
		return 0
	public int send_data(self, uint8_t* message, int len):
		int rc=sendto(self.sockfd, message, len, 0, 
						(struct sockaddr*)&self.servaddr, sizeof(self.servaddr))
		return rc

////////////////////////////////////////////////////////////////////////////
//"""A multi-producer, multi-consumer channel.
// for an accept/select implementation, you need
// one select channel of adequate size
// for each accept call, one shall post itself on the select channel and
// shall wait on a corresponding response channel of size 1
// the select construct shall wait on the select channel (possibly with
// timeout), retrieve the function to execute and
// then post the response on the corresponding response channel.
///////////////////////////////////////////////////////////////////////
public class Channel:
	void** buf
	long head= 0
	long tail= 0 
	bool full= false
	bool empty= true
	pthread_mutex_t *mutex1
	pthread_mutex_t *mutex2
	pthread_cond_t *notFull, *notEmpty, *all_tasks_done
	int maxsize
	int unfinished_tasks = 0
	def __init__(self, int maxsize):
		self.maxsize=maxsize
		self.buf= new void*[maxsize]
		// mutex must be held whenever the channel is mutating.  All methods
		// that acquire mutex must release it before returning.  mutex
		// is shared between the three conditions, so acquiring and
		// releasing the conditions also acquires and releases mutex.	
		self.mutex1 = new pthread_mutex_t
		pthread_mutex_init (self.mutex1, NULL)
		self.mutex2 = new pthread_mutex_t
		pthread_mutex_init (self.mutex2, NULL)
		// Notify not_full whenever an item is removed from the channel;
		// a thread waiting to put is notified then.		
		self.notFull = new pthread_cond_t
		pthread_cond_init (self.notFull, NULL)
		// Notify not_empty whenever an item is added to the channel; a
		// thread waiting to get is notified then.		
		self.notEmpty = new pthread_cond_t
		pthread_cond_init (self.notEmpty, NULL)
		//Notify all_tasks_done whenever the number of unfinished tasks
		// drops to zero; thread waiting to join() is notified to resume
		self.all_tasks_done= new pthread_cond_t
		pthread_cond_init (self.all_tasks_done, NULL)
	def __del__(self):
		pthread_mutex_destroy (self.mutex1)
		free (self.mutex1)
		pthread_mutex_destroy (self.mutex2)
		free (self.mutex2)
		pthread_cond_destroy (self.notFull)
		free (self.notFull)
		pthread_cond_destroy (self.notEmpty)
		free (self.notEmpty)
		pthread_cond_destroy (self.all_tasks_done)
		free (self.all_tasks_done)
		free (self.buf)
	private def push(self, void* in):
		self.buf[self.tail] = in
		self.tail = (self.tail+1) % self.maxsize
		if self.tail == self.head:
			self.full = true
		self.empty = false
	private void* pop(self):
		void* out = self.buf[self.head]
		self.head = (self.head + 1) % self.maxsize
		if self.head == self.tail:
			self.empty = true
		self.full = false
		return out
	public def put(self, void* i):
		"""
		'Put an item into the channel.
		"""	
		pthread_mutex_lock(self.mutex1)
		while self.full:
			print "producer: channel FULL.\n"
			pthread_cond_wait (self.notFull, self.mutex1)
		self.push(i)
		self.unfinished_tasks += 1
		pthread_mutex_unlock(self.mutex1)
		pthread_cond_signal(self.notEmpty)	
	public void* get(self):
		"""
		'Remove and return an item from the channel.
		"""	
		pthread_mutex_lock(self.mutex1)
		while self.empty:
			//print "consumer: channel EMPTY.\n"
			pthread_cond_wait (self.notEmpty, self.mutex1)
		void* res= self.pop()
		pthread_mutex_unlock(self.mutex1)
		pthread_cond_signal(self.notFull)
		//print "consumer: received %d.\n", (int)res     
		return res
	public void* get_with_timeout(self, uint32_t TIMEOUT_IN_MILLISECONDS):
		"""
		'Remove and return an item from the channel.
		"If 'timeout' is 0, return an item if one is immediately
		"available. Is timeout' is a positive number, it blocks at most 
		'timeout secs and returns NULL if no item was available within that time
		"""	
		pthread_mutex_lock(self.mutex1)
		///////////
		uint32_t SECONDS= TIMEOUT_IN_MILLISECONDS/1000
		uint32_t NANOSECONDS= (TIMEOUT_IN_MILLISECONDS%1000) * 1000000
		/////////////
		struct timespec ts0, ts1, ts
		clock_gettime(CLOCK_REALTIME, &ts0)  // needs link with -lrt			
		ts1.tv_sec = SECONDS
		ts1.tv_nsec = NANOSECONDS
		timespec_add(&ts0,&ts1,&ts)
		/////////
		int rc = 0		    
		while self.empty and rc==0:
			//print "consumer: channel EMPTY.\n"
			if TIMEOUT_IN_MILLISECONDS==0: // we don't wait if timeout is 0
				rc= 1  // set it to a non NULL value !!!
				break			
			rc=pthread_cond_timedwait(self.notEmpty, self.mutex1, &ts)
		void* res
		if rc != 0:
			res= NULL
		else:
			res= self.pop()
		pthread_mutex_unlock(self.mutex1)
		if res:
			pthread_cond_signal(self.notFull)        
		return res
	public void* get_nowait(self):
		char* res
		pthread_mutex_lock(self.mutex1)
		if self.empty:
			res= NULL
		else:
			res= self.pop()
		pthread_mutex_unlock(self.mutex1)
		if res:
			pthread_cond_signal(self.notFull)        
		return res			
	public def task_done(self):
		"""Indicate that a formerly enqueued task is complete.
		'Used by Channel consumer threads.  For each get() used to fetch a task,
		'a subsequent call to task_done() tells the channel that the processing
		'on the task is complete.
		'If a join() is currently blocking, it will resume when all items
		'have been processed (meaning that a task_done() call was received
		'for every item that had been put() into the channel).
		"""
		pthread_mutex_lock(self.mutex2) // Shall we use the same mutex ???		
		self.unfinished_tasks--
		if self.unfinished_tasks == 0:
			pthread_cond_broadcast(self.all_tasks_done)
		if self.unfinished_tasks < 0:
			 assert false or "task_done() called too many times"
		pthread_mutex_unlock(self.mutex2)
	public def join(self):
		"""Blocks until all items in the Channel have been gotten and processed.
		'The count of unfinished tasks goes up whenever an item is added to the
		'channel. The count goes down whenever a consumer thread calls task_done()
		'to indicate the item was retrieved and all work on it is complete.
		'When the count of unfinished tasks drops to zero, join() unblocks.
		"""
		pthread_mutex_lock(self.mutex2) // Shall we use the same mutex ???
		while self.unfinished_tasks:
			pthread_cond_wait (self.all_tasks_done, self.mutex2)			
		pthread_mutex_unlock(self.mutex2)


private void timespec_add(struct timespec* a, struct timespec* b, struct timespec* out):
	time_t sec = a->tv_sec + b->tv_sec
	long nsec = a->tv_nsec + b->tv_nsec
	sec += nsec / 1000000000L
	nsec = nsec % 1000000000L
	out->tv_sec = sec
	out->tv_nsec = nsec

public class Buffer:
	uint8_t* buf
	uint32_t size
	def __init__(self,buffer_size):
		self.buf = memalign (64, buffer_size) 
		if not self.buf:
			print "Unable to allocate mem at line %d\n",__LINE__
			return NULL
		self.size=buffer_size
	def __del__(self):
		free self.buf

public class FlowControlAgent2:
	Channel*  free_queue
	Channel* filled_queue  
	def __init__(self,int buffer_count,int buffer_size):
		self.free_queue= new Channel(buffer_count)
		self.filled_queue= new Channel(buffer_count)
		for uint8_t i=0; i< buffer_count; i++:
			free_buffer := new Buffer(buffer_size) 
			if not free_buffer:
				print "Unable to allocate mem at line %d\n",__LINE__
				return NULL
			self.free_queue->put(free_buffer)
	def __del__(self):
		int i=0
		while true:
			Buffer* pbuf=self.free_queue->get_nowait()
			if not pbuf:
				break
			delete pbuf
			print "freeing output buf: %p, ", pbuf->buf
			if ((++i) % 8) == 0:
				 print "\n" 				
		while true:
			Buffer* pbuf=self.filled_queue->get_nowait()
			if not pbuf:
				break
			delete pbuf
			print "freeing output buf: %p, ", pbuf->buf
			if ((++i) % 8) == 0:
				 print "\n" 	
		print "\n"
		delete self.free_queue
		delete self.filled_queue
	// PRODUCER API			
	public uint8_t* request_free_buffer(self):
		return Channel::get(self.free_queue)
	public def put_filled_in_free_buffer(self,Buffer* filled_in_buffer):
		Channel::put(self.filled_queue,filled_in_buffer)
	// CONSUMER API		
	public uint8_t* request_filled_in_buffer(self): 
		return Channel::get(self.filled_queue)
	public def release_filled_in_buffer(self,Buffer* free_buffer):
		Channel::put(self.free_queue,free_buffer)
	public def flush_control_buffer(self): // FLUSH, DON'T FREE !!!
		while true:
			Buffer* pbuf=self.filled_queue->get_nowait()
			if not pbuf:
				break

public class FlowControlAgent:
	Channel*  free_queue
	Channel* filled_queue 
	Channel* size_queue 
	def __init__(self,int buffer_count,int buffer_size):
		self.free_queue= new Channel(buffer_count)
		self.filled_queue= new Channel(buffer_count)
		self.size_queue= new Channel(buffer_count)
		for uint8_t i=0; i< buffer_count; i++:
			uint8_t* free_buffer = memalign (64, buffer_size) 
			if not free_buffer:
				print "Unable to allocate mem at line %d\n",__LINE__
				return NULL
			self.free_queue->put(free_buffer)
	def __del__(self):
		int i=0
		while true:
			uint8_t* pbuf=self.free_queue->get_nowait()
			if not pbuf:
				break
			free pbuf
			print "freeing output buf: %p, ", pbuf
			if ((++i) % 8) == 0:
				 print "\n" 				
		while true:
			uint8_t* pbuf=self.filled_queue->get_nowait()
			if not pbuf:
				break
			free pbuf
			print "freeing output buf: %p, ", pbuf
			if ((++i) % 8) == 0:
				 print "\n" 	
		while true:
			uint32_t size=self.size_queue->get_nowait()
			if not size:
				break
		print "\n"
		delete self.free_queue
		delete self.filled_queue
		delete self.size_queue
	// PRODUCER API			
	public uint8_t* request_free_buffer(self):
		return Channel::get(self.free_queue)
	public def put_filled_in_free_buffer(self,uint8_t* filled_in_buffer,uint32_t size):
		Channel::put(self.filled_queue,filled_in_buffer)
		Channel::put(self.size_queue,size)
	// CONSUMER API		
	public uint8_t* request_filled_in_buffer(self,uint32_t* size_p):
		*size_p=Channel::get(self.size_queue) 
		return Channel::get(self.filled_queue) 
	public def release_filled_in_buffer(self,uint8_t* free_buffer):
		Channel::put(self.free_queue,free_buffer)
	public def flush_control_buffer(self): // FLUSH, DON'T FREE !!!
		while true:
			uint8_t* pbuf=self.filled_queue->get_nowait()
			uint32_t size=self.size_queue->get_nowait()
			if not pbuf:
				break
