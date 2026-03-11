#define _EPOLL_REACTOR_C_
#include "epoll_reactor.h"


/************************************************/
/*   FORWARD DECLARATION OF STATIC FUNCTIONS    */

static int timer_set_expiry(int timer, time_t sec, long nsec, time_t intsec, long intnsec);
static void Reactor_setup(Reactor* self);
static void PeriodicTask_f_process_time_event(PeriodicTask_f* self);
static void Task_run(Task* self, void* arg);
static void Task_stop(Task* self);
static void Thread_run(Thread* self, void* arg);
static void *get_in_addr(struct sockaddr *sa);
static void UDP_server_process_data(UDP_server* self);
static void UDP_server_process_message(UDP_server* self, uint8_t* message, int len );
static void UDP_server_setup_udp_server_socket(UDP_server* self, char* PORT);
static uint16_t TCP_Client_parse_message(TCP_Client* self,uint8_t* message, int len);
static void TCP_Client_tear_down(TCP_Client* self);
static TCP_Server* TCP_Server_constructor(TCP_Server* self, Reactor* reactor_engine,char* name, char* ip_address_dot, int port_number,TCP_Client* (*client_constructor)(void*,int));
static void UDP_client_process_data(UDP_client* self);
static void UDP_client_process_message(UDP_client* self, uint8_t* message, int len );
static int UDP_client_setup_udp_client_socket(UDP_client* self,char* ip_address, char* SERVERPORT);
static Channel* Channel_constructor(Channel* self, int maxsize);
static void Channel_destructor(Channel* self);
static void Channel_push(Channel* self, void* in);
static void* Channel_pop(Channel* self);
static void timespec_add(struct timespec* a, struct timespec* b, struct timespec* out);
static Buffer* Buffer_constructor(Buffer* self,buffer_size);
static void Buffer_destructor(Buffer* self);
static FlowControlAgent2* FlowControlAgent2_constructor(FlowControlAgent2* self,int buffer_count,int buffer_size);
static void FlowControlAgent2_destructor(FlowControlAgent2* self);
static FlowControlAgent* FlowControlAgent_constructor(FlowControlAgent* self,int buffer_count,int buffer_size);
static void FlowControlAgent_destructor(FlowControlAgent* self);

/************************************************/


#define MAXEVENTS 64

int setNonBlocking(int fd) { 
	int flags=fcntl(fd, F_GETFL, 0);
	if (flags == -1) { 
		flags = 0;
		}
	return fcntl(fd, F_SETFL, flags | O_NONBLOCK);
	}


static int timer_set_expiry(int timer, time_t sec, long nsec, time_t intsec, long intnsec) { 
	struct itimerspec timerSpec;
	memset(&timerSpec, 0, sizeof(timerSpec));
	timerSpec.it_value.tv_sec = sec;
	timerSpec.it_value.tv_nsec = nsec;
	timerSpec.it_interval.tv_sec = intsec;
	timerSpec.it_interval.tv_nsec = intnsec;
	struct itimerspec oldSpec;
	return timerfd_settime(timer, 0, &timerSpec, &oldSpec);
	}


Reactor* Reactor_constructor(Reactor* this) { 
	this->_stop=false;
	this->epoll_fd = epoll_create1(0);
	memset(this->fd_repository,0, sizeof this->fd_repository);
	this->setup=Reactor_setup;// virtual method
	return this;
	}

Reactor* Reactor_new() { 
	Reactor* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Reactor_constructor(this);
	}

void Reactor_free(Reactor* this) { 
	free(this);
	}

static void Reactor_setup(Reactor* this) { 
	fprintf (stderr, "Please override this function:Reactor_setup\n");
	}
void Reactor_run(Reactor* this) { 
	this->setup(this);
	struct epoll_event* events=calloc(MAXEVENTS,sizeof *events);
	for (;;) { 
		int nfds = epoll_wait (this->epoll_fd, events, MAXEVENTS, -1);
		if (nfds==-1) { 
			if (errno == EINTR) { 
				continue;
				}
			else { 
				perror("EPOLL ERROR:");
				abort();
				}
			}
		for (int i=0; i<nfds; i++) { 
			Callback* action = (Callback*) events[i].data.ptr;
			if (!action) { 
				continue;
				}
			if (events[i].events & EPOLLERR) { 
				fprintf (stderr, "epoll error\n");
				close(action->fd);
				continue;
				}
			if (events[i].events & EPOLLHUP) { 
				fprintf (stderr, "epoll error\n");
				close(action->fd);
				continue;
				}
			if (events[i].events & EPOLLIN) { 
				//print "Event ready for reading\n"
				action->action_handler(action->arg);
				}
			if (events[i].events & EPOLLOUT) { 
				fprintf (stderr, "Event ready for writing\n");
				}
			}
		if (this->_stop) { 
			fprintf (stderr, "Exiting reactor\n");
			break;
			}
		}
	}
void Reactor_stop(Reactor* this) { 
	this->_stop=true;
	}
void Reactor_schedule_read_fileobject(Reactor* this, int fd, void (*callback)(void*), void* args) { 
	assert (this->fd_repository[fd]==NULL);
	Callback* action = malloc(sizeof(*action));
	this->fd_repository[fd]= action;
	*action= (Callback){.fd=fd,.action_handler=callback,.arg=args};
	setNonBlocking(fd);
	epoll_ctl(this->epoll_fd,EPOLL_CTL_ADD,fd,(struct epoll_event[]){{.data.fd=fd,.data.ptr = action,.events=EPOLLIN | EPOLLET}});
	}
void Reactor_schedule_write_fileobject(Reactor* this, int fd, void (*callback)(void*), void* args) { 
	Callback* action = malloc(sizeof(*action));
	this->fd_repository[fd]= action;
	*action= (Callback){.fd=fd,.action_handler=callback,.arg=args};
	setNonBlocking(fd);
	epoll_ctl(this->epoll_fd,EPOLL_CTL_ADD,fd,(struct epoll_event[]){{.data.fd=fd,.data.ptr = action,.events=EPOLLOUT | EPOLLET}});
	}
void Reactor_remove_fileobject(Reactor* this, int fd) { 
	int ret = epoll_ctl(this->epoll_fd, EPOLL_CTL_DEL, fd, NULL);
	Callback* cb=this->fd_repository[fd];
	if (cb) { 
		free (cb);
		}
	this->fd_repository[fd]=NULL;
	}
int Reactor_schedule_timed_event(Reactor* this,void (*callback)(void*), void* args, time_t sec, long nsec, time_t intsec, long intnsec) { 
	int fd=timerfd_create(CLOCK_REALTIME, 0);// TFD_NONBLOCK  iso 0 
	Callback* action = malloc(sizeof(*action));
	action->fd = fd;
	action->action_handler = callback;
	action->arg = args;
	this->fd_repository[fd]= action;
	int rc=epoll_ctl(this->epoll_fd,EPOLL_CTL_ADD,fd,(struct epoll_event[]){{.data.ptr = action,.events=EPOLLIN | EPOLLET}});
	//print "Scheduling time event, rc= %d %d %d %d %d\n", rc,sec, nsec, intsec, intnsec
	int res=timer_set_expiry(action->fd, sec, nsec, intsec, intnsec);
	//fcntl(tfd, F_SETFL, fcntl(tfd, F_GETFL, 0) | O_NONBLOCK)
	return fd;
	}
void Reactor_remove_timed_event(Reactor* this, int fd) { 
	Callback* cb=this->fd_repository[fd];
	if (cb) { 
		free (cb);
		}
	int ret = epoll_ctl(this->epoll_fd, EPOLL_CTL_DEL, fd, NULL);
	//print "set timer expiry: %d\n",fd
	int res=timer_set_expiry(fd, 0, 0, 0, 0);
	//print "closing timer fd: %d\n",fd
	close(fd);
	fprintf (stderr, "timer closed, fd= %d\n",fd);
	this->fd_repository[fd]=NULL;
	}


/***************************************************************************/
// MAY NOT BE OPAQUE IF YOU WANT INHERITANCE!


PeriodicTask_f* PeriodicTask_f_constructor(PeriodicTask_f* this, Reactor* reactor_engine, double initial_delay_ms,double period_ms) { 
	this->terminated=false;
	double period_nsec= period_ms*1000000;
	uint64_t sec= period_nsec/1000000000;
	uint64_t nsec=period_nsec-sec*1000000000;
	//
	double initial_delay_nsec= initial_delay_ms*1000000;
	uint64_t sec0= initial_delay_nsec/1000000000;
	uint64_t nsec0=initial_delay_nsec-sec0*1000000000;
	//print "timer started with period: %llu sec, %llu nsec ",sec, nsec
	//print "and initial delay: %llu sec, %llu nsec\n",sec0, nsec0
	this->fd=Reactor_schedule_timed_event(reactor_engine,
											PeriodicTask_f_process_time_event,
											this,
											sec0,nsec0,sec,nsec);
	this->reactor_engine= reactor_engine;
	this->period=period_ms;
	this->counter=0;
	this->run=PeriodicTask_f_run;// virtual method
	return this;
	}

PeriodicTask_f* PeriodicTask_f_new(Reactor* reactor_engine, double initial_delay_ms,double period_ms) { 
	PeriodicTask_f* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return PeriodicTask_f_constructor(this, reactor_engine, initial_delay_ms, period_ms);
	}

void PeriodicTask_f_free(PeriodicTask_f* this) { 
	PeriodicTask_f_destructor(this);
	free(this);
	}

void PeriodicTask_f_destructor(PeriodicTask_f* this) { 
	this->terminated=true;
	Reactor_remove_timed_event(this->reactor_engine,this->fd);
	}
void PeriodicTask_f_process_time_event(PeriodicTask_f* this) { 
	if (this->terminated) { 
		return;
		}
	uint8_t buf[512];
	ssize_t count = read(this->fd, buf, sizeof buf);// THIS MUST HAPPEN !!!
	//print "COUNT= %d\n", count
	this->run(this);
	}
void PeriodicTask_f_run(PeriodicTask_f* this) { 
	fprintf (stderr, "please OVERRIDE\n");
	}
int PeriodicTask_f_update_timer(PeriodicTask_f* this,double initial_delay_ms,double period_ms) { 
	double period_nsec= period_ms*1000000;
	uint64_t sec= period_nsec/1000000000;
	uint64_t nsec=period_nsec-sec*1000000000;
	double initial_delay_nsec= initial_delay_ms*1000000;
	uint64_t sec0= initial_delay_nsec/1000000000;
	uint64_t nsec0=initial_delay_nsec-sec0*1000000000;
	if (sec0==0  &&  nsec0==0) { 
		nsec0=1000;// don't disable the timer !!!
		}
	int res=timer_set_expiry(this->fd, sec0,nsec0,sec,nsec);
	uint64_t value; read(this->fd, &value, 8);
	return res;
	}

/////////////////////////////////////////////////////////////////////////////
// if you want to see all threads, do 
// ps -eTo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,wchan:14,comm
// ps -eLo pid, pcpu, args


Task* Task_constructor(Task* this) { 
	this->_stop=false;
	assert (!pthread_attr_init(&this->attr));
	assert (!pthread_attr_setschedpolicy(&this->attr, SCHED_RR));
	assert (!pthread_attr_setdetachstate(&this->attr, PTHREAD_CREATE_JOINABLE));
	assert (!pthread_attr_setscope(&this->attr, PTHREAD_SCOPE_SYSTEM));
	//assert not pthread_attr_setstacksize(attr, 0x200000) // 2MB stack default 
	assert (!pthread_attr_setinheritsched(&this->attr, PTHREAD_EXPLICIT_SCHED));
	this->max_prio=sched_get_priority_max(SCHED_RR);// should be 99
	this->min_prio=sched_get_priority_min(SCHED_RR);// should be 1	
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
	pthread_attr_destroy(&this->attr);
	}
void Task_start(Task* this,void* arg) { 
	this->arg=arg;
	struct sched_param param;
	// GIVE A NON-NULL PARAMETER IF YOU WANT HIGHEST PRIORITY !!!
	if (arg) { 
		param.sched_priority= this->max_prio-10;
		}
	else { 
		param.sched_priority= this->min_prio+10;
		}
	assert (!pthread_attr_setschedparam(&this->attr,&param));
	int rc= pthread_create(&this->threadid, &this->attr, Task_callback,this);
	if (rc==EAGAIN) { 
		fprintf (stderr, "The system lacked the necessary resources to create another thread, or the system-imposed limit on the total number of threads in a process {PTHREAD_THREADS_MAX} would be exceeded.\n");
		}
	else if (rc== EINVAL) { 
		fprintf (stderr, "The value specified by attr is invalid.\n");
		}
	else if (rc==EPERM) { 
		fprintf (stderr, "The caller does !have appropriate permission to set the required scheduling parameters or scheduling policy.\n");
		}
	else if (rc!=0) { 
		fprintf (stderr, "RC=%d\n",rc);
		}
	assert (rc==0);
	}
void Task_callback(Task* this) { 
	this->run(this,this->arg);
	}
void Task_run(Task* this, void* arg) { 
	fprintf (stderr, "Please override the Task_run method\n");
	}
void Task_join(Task* this) { 
	int rc= pthread_join(this->threadid, NULL);
	assert (rc==0);
	}
void Task_cancel(Task* this) { 
	int rc= pthread_cancel(this->threadid);
	assert (rc=0);
	rc=pthread_join(this->threadid, NULL);
	assert (rc=0);
	}
void Task_stop(Task* this) { 
	this->_stop=true;
	}


//public class Task_non_rt:

Thread* Thread_constructor(Thread* this) { 
	this->_stop=false;
	assert (!pthread_attr_init(&this->attr));
	assert (!pthread_attr_setschedpolicy(&this->attr, SCHED_OTHER));
	assert (!pthread_attr_setdetachstate(&this->attr, PTHREAD_CREATE_JOINABLE));
	assert (!pthread_attr_setscope(&this->attr, PTHREAD_SCOPE_SYSTEM));
	//assert not pthread_attr_setstacksize(attr, 0x200000) // 2MB stack default 
	this->run=Thread_run;// virtual method
	return this;
	}

Thread* Thread_new() { 
	Thread* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Thread_constructor(this);
	}

void Thread_free(Thread* this) { 
	Thread_destructor(this);
	free(this);
	}

void Thread_destructor(Thread* this) { 
	pthread_attr_destroy(&this->attr);
	}
void Thread_start(Thread* this,void* arg) { 
	this->arg=arg;
	int rc= pthread_create(&this->threadid, &this->attr, Task_callback,this);
	if (rc==EAGAIN) { 
		fprintf (stderr, "The system lacked the necessary resources to create another thread, or the system-imposed limit on the total number of threads in a process {PTHREAD_THREADS_MAX} would be exceeded.\n");
		}
	else if (rc== EINVAL) { 
		fprintf (stderr, "The value specified by attr is invalid.\n");
		}
	else if (rc==EPERM) { 
		fprintf (stderr, "The caller does !have appropriate permission to set the required scheduling parameters or scheduling policy.\n");
		}
	else if (rc!=0) { 
		fprintf (stderr, "RC=%d\n",rc);
		}
	assert (rc==0);
	}
void Thread_callback(Thread* this) { 
	this->run(this,this->arg);
	}
void Thread_run(Thread* this, void* arg) { 
	fprintf (stderr, "Please override the Task_run method\n");
	}
void Thread_join(Thread* this) { 
	int rc= pthread_join(this->threadid, NULL);
	assert (rc==0);
	}
void Thread_cancel(Thread* this) { 
	int rc= pthread_cancel(this->threadid);
	assert (rc=0);
	rc=pthread_join(this->threadid, NULL);
	assert (rc=0);
	}
void Thread_stop(Thread* this) { 
	this->_stop=true;
	}

////////////////////////////////////////////////////////////////////////////
/***************************************************************************/
/* get sockaddr, IPv4  ||  IPv6 */
void *get_in_addr(struct sockaddr *sa) { 
	if (sa->sa_family == AF_INET) { 
		return &(((struct sockaddr_in*)sa)->sin_addr);
		}
	return &(((struct sockaddr_in6*)sa)->sin6_addr);
	}


UDP_server* UDP_server_constructor(UDP_server* this, Reactor* reactor_engine, char* MYPORT) { 
	UDP_server_setup_udp_server_socket(this,MYPORT);
	this->reactor_engine= reactor_engine;
	 Reactor_schedule_read_fileobject(reactor_engine,this->sockfd,UDP_server_process_data,this);
	//print "UDP listener: waiting to recv on port %s...\n", MYPORT
	this->process_message=UDP_server_process_message;// virtual method
	return this;
	}

UDP_server* UDP_server_new(Reactor* reactor_engine, char* MYPORT) { 
	UDP_server* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return UDP_server_constructor(this, reactor_engine, MYPORT);
	}

void UDP_server_free(UDP_server* this) { 
	UDP_server_destructor(this);
	free(this);
	}

void UDP_server_destructor(UDP_server* this) { 
	close(this->sockfd);
	Reactor_remove_fileobject(this->reactor_engine,this->sockfd);
	}
static void UDP_server_process_data(UDP_server* this) { 
	for (;;) { 
		bool close_it = false;
		char s[INET6_ADDRSTRLEN];
		socklen_t addr_len = sizeof this->cliaddr;
		int numbytes = recvfrom(this->sockfd, this->rx_buffer, 0xFFFE , 
			                0, (struct sockaddr *)&this->cliaddr, &addr_len);
		if (numbytes== -1) { 
			// If errno == EAGAIN, that means we have read all
			// data. So go back to the main loop.
			if (errno == EAGAIN) { 
				return;
				}
			perror ("recvfrom");
			close_it= true;
			}
		else if (numbytes== 0) { 
			// End of file. The remote has closed the connection.
			fprintf (stderr, "END OF FILE DETECTED !!!!!!\n");
			close_it = true;
			}
		else { 
			// call the callback function !!!
			char* client_address=inet_ntop(this->cliaddr.ss_family,
			                 get_in_addr((struct sockaddr *)&this->cliaddr), 
							 s, 
							 sizeof s);
			this->process_message(this,this->rx_buffer,numbytes);
			}
		if (close_it) { 
			fprintf (stderr, "Closed connection on descriptor %d\n", this->sockfd);
			// Closing the descriptor will make epoll remove it
			// from the set of descriptors which are monitored.
			close(this->sockfd);
			Reactor_remove_fileobject(this->reactor_engine,this->sockfd);
			return;
			}
		}
	}
void UDP_server_process_message(UDP_server* this, uint8_t* message, int len ) { 
	fprintf (stderr, "Please override !!!\n");
	}
static void UDP_server_setup_udp_server_socket(UDP_server* this, char* PORT) { 
	struct addrinfo hints, *servinfo, *p;
	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;// set to AF_INET to force IPv4
	hints.ai_socktype = SOCK_DGRAM;
	hints.ai_flags = AI_PASSIVE;// use my IP
	int rv = getaddrinfo(NULL, PORT, &hints, &servinfo);
	if (rv != 0) { 
		//print "getaddrinfo: %s\n", gai_strerror(rv)
		perror ("getaddrinfo");
		exit(-2);
		}
	// loop through all the results and bind to the first we can
	int sockfd;
	for (p = servinfo; p != NULL; p = p->ai_next) { 
		sockfd = socket(p->ai_family, p->ai_socktype,p->ai_protocol);
		if (sockfd == -1) { 
			perror ("listener: socket");
			continue;
			}
		if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) { 
			close(sockfd);
			perror ("listener: bind");
			continue;
			}
		break;
		}
	if (p == NULL) { 
		perror ("listener: failed to bind socket\n");
		exit(-2);
		}
	freeaddrinfo(servinfo);// free the linked-list
	this->sockfd=sockfd;
	}
int UDP_server_send_data(UDP_server* this, uint8_t* message, int len) { 
	int rc=sendto(this->sockfd, message, len, 0, 
						(struct sockaddr*)&this->cliaddr,sizeof(this->cliaddr));
	return rc;
	}



TCP_Client* TCP_Client_constructor(TCP_Client* this, Reactor* engine,int fd) { 
	this->read_idx=0;
	this->fd=fd;
	this->reactor_engine= engine;
	this->parse_message=TCP_Client_parse_message;// virtual method
	return this;
	}

TCP_Client* TCP_Client_new(Reactor* engine,int fd) { 
	TCP_Client* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return TCP_Client_constructor(this, engine, fd);
	}

void TCP_Client_free(TCP_Client* this) { 
	free(this);
	}

void TCP_Client_receive_data(TCP_Client* this) { 
	int bytes_read= recv(this->fd,
							this->read_buffer+this->read_idx, 
							sizeof(this->read_buffer)-this->read_idx,0);
	if (bytes_read==-1) { 
		fprintf (stderr, "Error\n");
		}
	else if (bytes_read==0) { 
		// connection lost
		TCP_Client_tear_down(this);
		}
	else { 
		uint16_t bytes_to_process= this->read_idx+bytes_read;
		uint16_t idx=this->parse_message(this,this->read_buffer,bytes_to_process);
		uint16_t unprocessed_len= bytes_to_process-idx;
		if (unprocessed_len) { // could not process everything
			memmove(this->read_buffer,this->read_buffer+idx,unprocessed_len);
			}
		this->read_idx= unprocessed_len;
		}
	}
/* returns the index of the processed data. */
uint16_t TCP_Client_parse_message(TCP_Client* this,uint8_t* message, int len) { 
	fprintf (stderr, "Please override TCP_Client_parse_message\n");
	return len;
	}
static void TCP_Client_tear_down(TCP_Client* this) { 
	close(this->fd);
	}




TCP_Server* TCP_Server_constructor(TCP_Server* this, Reactor* reactor_engine,char* name, char* ip_address_dot, int port_number,TCP_Client* (*client_constructor)(void*,int)) { 
	this->client_constructor=client_constructor;
	this->reactor_engine= reactor_engine;
	strcpy(this->name, name);
	strcpy(this->ip_address_dot, ip_address_dot);
	this->port_number= port_number;
	int server_socket_fd = socket(AF_INET, SOCK_STREAM, 0);
	if (server_socket_fd == -1 ) { 
		fprintf (stderr, "Error creating socket: %d\n", errno);
		perror ("socket create");
		exit(3);
		}
	this->server_socket_fd= server_socket_fd;
	fprintf (stderr, "Server socket successfully created\n");
	// Allow address reuse
	int err = setsockopt(server_socket_fd, SOL_SOCKET, SO_REUSEADDR, &(int){1}, sizeof(int));
	if (err == -1 ) { 
		fprintf (stderr, "Error setting SO_REUSEADDR on socket: %d\n", errno);
		perror ("setsockopt");
		exit(3);
		}
	fprintf (stderr, "Socket Reuse Address option successfully set\n");
	// bind
	struct sockaddr_in addr = { 
		.sin_family = AF_INET,
		.sin_port = htons(port_number),
		.sin_addr.s_addr = INADDR_ANY,
		};
	err =bind(server_socket_fd,(struct sockaddr *) &addr, sizeof(struct sockaddr));
	if (err == -1 ) { 
		fprintf (stderr, "bind error: %d\n", errno);
		perror ("bind");
		exit(3);
		};
	fprintf (stderr, "Socket Bind successful\n");
	err = listen(server_socket_fd, 5);// we allow  up to 5 clients at a time
	if (err == -1 ) { 
		fprintf (stderr, "listen error: %d\n", errno);
		perror ("listen");
		exit(3);
		}
	fprintf (stderr, "Socket Listen successful\n");
	fprintf (stderr, "Waiting for connection on port %d\n", this->port_number);
	Reactor_schedule_read_fileobject(reactor_engine, 
			server_socket_fd, 
			TCP_Server_accept, 
			this);
	return this;
	}

TCP_Server* TCP_Server_new(Reactor* reactor_engine,char* name, char* ip_address_dot, int port_number,TCP_Client* (*client_constructor)(void*,int)) { 
	TCP_Server* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return TCP_Server_constructor(this, reactor_engine, name, ip_address_dot, port_number,client_constructor);
	}

void TCP_Server_free(TCP_Server* this) { 
	free(this);
	}

void TCP_Server_accept(TCP_Server* this) { 
	struct sockaddr_in *client_addr= malloc(sizeof(*client_addr));
	socklen_t client_addr_size = sizeof(struct sockaddr);
	int client_fd = accept(this->server_socket_fd, 
										(struct sockaddr *)client_addr, 
										&client_addr_size);
	fprintf (stderr, "Client successfully accepted\n");
	TCP_Client* client= this->client_constructor(this->reactor_engine,client_fd);
	assert (client);
	Reactor_schedule_read_fileobject(this->reactor_engine,
											client_fd,
											TCP_Client_receive_data,
											client);
	}
void TCP_Server_teardown(TCP_Server* this) { 
	close(this->server_socket_fd);
	}



UDP_client* UDP_client_constructor(UDP_client* this, Reactor* reactor_engine, char* SERV_ADDR,char* SERV_PORT) { 
	UDP_client_setup_udp_client_socket(this,SERV_ADDR,SERV_PORT);
	if (reactor_engine) { 
		 Reactor_schedule_read_fileobject(reactor_engine,this->sockfd,
												UDP_client_process_data,this);
		}
	this->process_message=UDP_client_process_message;// virtual method
	return this;
	}
UDP_client* UDP_client_new(Reactor* reactor_engine, char* SERV_ADDR,char* SERV_PORT) { 
	UDP_client* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return UDP_client_constructor(this, reactor_engine, SERV_ADDR, SERV_PORT);
	}

void UDP_client_free(UDP_client* this) { 
	free(this);
	}

static void UDP_client_process_data(UDP_client* this) { 
	for (;;) { 
		bool close_it = false;
		int numbytes = recvfrom(this->sockfd, this->rx_buffer,0xFFFE, 0, NULL, NULL);
		if (numbytes== -1) { 
			// If errno == EAGAIN, that means we have read all
			// data. So go back to the main loop.
			if (errno == EAGAIN) { 
				return;
				}
			perror ("recvfrom");
			close_it= true;
			}
		else if (numbytes== 0) { 
			// End of file. The remote has closed the connection.
			fprintf (stderr, "END OF FILE DETECTED !!!!!!\n");
			close_it = true;
			}
		else { 
			// call the callback function !!!
			this->process_message(this,this->rx_buffer,numbytes);
			}
		if (close_it) { 
			fprintf (stderr, "Closed connection on descriptor %d\n", this->sockfd);
			// Closing the descriptor will make epoll remove it
			// from the set of descriptors which are monitored.
			close (this->sockfd);
			}
		}
	}
void UDP_client_process_message(UDP_client* this, uint8_t* message, int len ) { 
	fprintf (stderr, "Please override !!!\n");
	}
static int UDP_client_setup_udp_client_socket(UDP_client* this,char* ip_address, char* SERVERPORT) { 
	struct addrinfo hints, *servinfo, *p;
	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_DGRAM;
	int rv = getaddrinfo(ip_address, SERVERPORT, &hints, &servinfo);
	if (rv != 0) { 
		//print "getaddrinfo: %s\n", gai_strerror(rv)
		perror ("getaddrinfo");
		exit(-2);
		}
	// loop through all the results and make a socket
	int sockfd;
	for (p = servinfo; p != NULL; p = p->ai_next) { 
		sockfd = socket(p->ai_family, p->ai_socktype,p->ai_protocol);
		if (sockfd == -1) { 
			perror ("client: socket");
			continue;
			}
		break;
		}
	if (p == NULL) { 
		fprintf (stderr, "client: failed to bind socket\n");
		exit(-2);
		}
	this->sockfd=sockfd;
	this->servaddr= *(struct sockaddr_in*)(p->ai_addr);
	// let us free the memory
	freeaddrinfo(servinfo);
	return 0;
	}
int UDP_client_send_data(UDP_client* this, uint8_t* message, int len) { 
	int rc=sendto(this->sockfd, message, len, 0, 
						(struct sockaddr*)&this->servaddr, sizeof(this->servaddr));
	return rc;
	}


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

Channel* Channel_constructor(Channel* this, int maxsize) { 
	this->head= 0;
	this->tail= 0;
	this->full= false;
	this->empty= true;
	this->unfinished_tasks= 0;
	this->maxsize=maxsize;
	this->buf= calloc(maxsize,sizeof(void*));
	// mutex must be held whenever the channel is mutating.  All methods
	// that acquire mutex must release it before returning.  mutex
	// is shared between the three conditions, so acquiring and
	// releasing the conditions also acquires and releases mutex.	
	this->mutex1 = malloc(sizeof(*this->mutex1));
	pthread_mutex_init (this->mutex1, NULL);
	this->mutex2 = malloc(sizeof(*this->mutex2));
	pthread_mutex_init (this->mutex2, NULL);
	// Notify not_full whenever an item is removed from the channel;
	// a thread waiting to put is notified then.		
	this->notFull = malloc(sizeof(*this->notFull));
	pthread_cond_init (this->notFull, NULL);
	// Notify not_empty whenever an item is added to the channel; a
	// thread waiting to get is notified then.		
	this->notEmpty = malloc(sizeof(*this->notEmpty));
	pthread_cond_init (this->notEmpty, NULL);
	//Notify all_tasks_done whenever the number of unfinished tasks
	// drops to zero; thread waiting to join() is notified to resume
	this->all_tasks_done= malloc(sizeof(*this->all_tasks_done));
	pthread_cond_init (this->all_tasks_done, NULL);
	return this;
	}

Channel* Channel_new(int maxsize) { 
	Channel* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Channel_constructor(this, maxsize);
	}

void Channel_free(Channel* this) { 
	Channel_destructor(this);
	free(this);
	}

void Channel_destructor(Channel* this) { 
	pthread_mutex_destroy (this->mutex1);
	free (this->mutex1);
	pthread_mutex_destroy (this->mutex2);
	free (this->mutex2);
	pthread_cond_destroy (this->notFull);
	free (this->notFull);
	pthread_cond_destroy (this->notEmpty);
	free (this->notEmpty);
	pthread_cond_destroy (this->all_tasks_done);
	free (this->all_tasks_done);
	free (this->buf);
	}
static void Channel_push(Channel* this, void* in) { 
	this->buf[this->tail] = in;
	this->tail = (this->tail+1) % this->maxsize;
	if (this->tail == this->head) { 
		this->full = true;
		}
	this->empty = false;
	}
static void* Channel_pop(Channel* this) { 
	void* out = this->buf[this->head];
	this->head = (this->head + 1) % this->maxsize;
	if (this->head == this->tail) { 
		this->empty = true;
		}
	this->full = false;
	return out;
	}
/* Put an item into the channel. */
void Channel_put(Channel* this, void* i) { 
	pthread_mutex_lock(this->mutex1);
	while (this->full) { 
		fprintf (stderr, "producer: channel FULL.\n");
		pthread_cond_wait (this->notFull, this->mutex1);
		}
	Channel_push(this,i);
	this->unfinished_tasks += 1;
	pthread_mutex_unlock(this->mutex1);
	pthread_cond_signal(this->notEmpty);
	}
/* Remove  &&  return an item from the channel. */
void* Channel_get(Channel* this) { 
	pthread_mutex_lock(this->mutex1);
	while (this->empty) { 
		//print "consumer: channel EMPTY.\n"
		pthread_cond_wait (this->notEmpty, this->mutex1);
		}
	void* res= Channel_pop(this);
	pthread_mutex_unlock(this->mutex1);
	pthread_cond_signal(this->notFull);
	//print "consumer: received %d.\n", (int)res     
	return res;
	}
/* Remove  &&  return an item from the channel. */
/* If 'timeout' is 0, return an item if (one is immediately) */
/* available. Is timeout' is a positive number, it blocks at most */
/* timeout secs  &&  returns NULL if (no item was available within that time) */
void* Channel_get_with_timeout(Channel* this, uint32_t TIMEOUT_IN_MILLISECONDS) { 
	pthread_mutex_lock(this->mutex1);
	///////////
	uint32_t SECONDS= TIMEOUT_IN_MILLISECONDS/1000;
	uint32_t NANOSECONDS= (TIMEOUT_IN_MILLISECONDS%1000) * 1000000;
	/////////////
	struct timespec ts0, ts1, ts;
	clock_gettime(CLOCK_REALTIME, &ts0);// needs link with -lrt			
	ts1.tv_sec = SECONDS;
	ts1.tv_nsec = NANOSECONDS;
	timespec_add(&ts0,&ts1,&ts);
	/////////
	int rc = 0;
	while (this->empty  &&  rc==0) { 
		//print "consumer: channel EMPTY.\n"
		if (TIMEOUT_IN_MILLISECONDS==0) { // we don't wait if timeout is 0
			rc= 1;// set it to a non NULL value !!!
			break;
			}
		rc=pthread_cond_timedwait(this->notEmpty, this->mutex1, &ts);
		}
	void* res;
	if (rc != 0) { 
		res= NULL;
		}
	else { 
		res= Channel_pop(this);
		}
	pthread_mutex_unlock(this->mutex1);
	if (res) { 
		pthread_cond_signal(this->notFull);
		}
	return res;
	}
void* Channel_get_nowait(Channel* this) { 
	char* res;
	pthread_mutex_lock(this->mutex1);
	if (this->empty) { 
		res= NULL;
		}
	else { 
		res= Channel_pop(this);
		}
	pthread_mutex_unlock(this->mutex1);
	if (res) { 
		pthread_cond_signal(this->notFull);
		}
	return res;
	}
/* Indicate that a formerly enqueued task is complete. */
/* Used by Channel consumer threads.  For each get() used to fetch a task, */
/* a subsequent call to task_done() tells the channel that the processing */
/* on the task is complete. */
/* If a join() is currently blocking, it will resume when all items */
/* have been processed (meaning that a task_done() call was received */
/* for every item that had been put() into the channel). */
void Channel_task_done(Channel* this) { 
	pthread_mutex_lock(this->mutex2);// Shall we use the same mutex ???		
	this->unfinished_tasks--;
	if (this->unfinished_tasks == 0) { 
		pthread_cond_broadcast(this->all_tasks_done);
		}
	if (this->unfinished_tasks < 0) { 
		 assert (false  ||  "task_done() called too many times");
		}
	pthread_mutex_unlock(this->mutex2);
	}
/* Blocks until all items in the Channel have been gotten and processed. */
/* The count of unfinished tasks goes up whenever an item is added to the */
/* channel. The count goes down whenever a consumer thread calls task_done() */
/* to indicate the item was retrieved  &&  all work on it is complete. */
/* When the count of unfinished tasks drops to zero, join() unblocks. */
void Channel_join(Channel* this) { 
	pthread_mutex_lock(this->mutex2);// Shall we use the same mutex ???
	while (this->unfinished_tasks) { 
		pthread_cond_wait (this->all_tasks_done, this->mutex2);
		}
	pthread_mutex_unlock(this->mutex2);
	}



static void timespec_add(struct timespec* a, struct timespec* b, struct timespec* out) { 
	time_t sec = a->tv_sec + b->tv_sec;
	long nsec = a->tv_nsec + b->tv_nsec;
	sec += nsec / 1000000000L;
	nsec = nsec % 1000000000L;
	out->tv_sec = sec;
	out->tv_nsec = nsec;
	}


Buffer* Buffer_constructor(Buffer* this,buffer_size) { 
	this->buf = memalign (64, buffer_size);
	if (!this->buf) { 
		fprintf (stderr, "Unable to allocate mem at line %d\n",__LINE__);
		return NULL;
		}
	this->size=buffer_size;
	return this;
	}

Buffer* Buffer_new(buffer_size) { 
	Buffer* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return Buffer_constructor(this, buffer_size);
	}

void Buffer_free(Buffer* this) { 
	Buffer_destructor(this);
	free(this);
	}

void Buffer_destructor(Buffer* this) { 
	free (this->buf);
	}



FlowControlAgent2* FlowControlAgent2_constructor(FlowControlAgent2* this,int buffer_count,int buffer_size) { 
	this->free_queue=  Channel_new(buffer_count);
	this->filled_queue=  Channel_new(buffer_count);
	for (uint8_t i=0; i< buffer_count; i++) { 
		Buffer* free_buffer =  Buffer_new(buffer_size);
		if (!free_buffer) { 
			fprintf (stderr, "Unable to allocate mem at line %d\n",__LINE__);
			return NULL;
			}
		Channel_put(this->free_queue,free_buffer);
		}
	return this;
	}
FlowControlAgent2* FlowControlAgent2_new(int buffer_count,int buffer_size) { 
	FlowControlAgent2* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return FlowControlAgent2_constructor(this, buffer_count, buffer_size);
	}

void FlowControlAgent2_free(FlowControlAgent2* this) { 
	FlowControlAgent2_destructor(this);
	free(this);
	}

void FlowControlAgent2_destructor(FlowControlAgent2* this) { 
	int i=0;
	while (true) { 
		Buffer* pbuf=Channel_get_nowait(this->free_queue);
		if (!pbuf) { 
			break;
			}
		delete pbuf;
		fprintf (stderr, "freeing output buf: %p, ", pbuf->buf);
		if (((++i) % 8) == 0) { 
			 fprintf (stderr, "\n");
			}
		}
	while (true) { 
		Buffer* pbuf=Channel_get_nowait(this->filled_queue);
		if (!pbuf) { 
			break;
			}
		delete pbuf;
		fprintf (stderr, "freeing output buf: %p, ", pbuf->buf);
		if (((++i) % 8) == 0) { 
			 fprintf (stderr, "\n");
			}
		}
	fprintf (stderr, "\n");
	Channel_free(this->free_queue);
	Channel_free(this->filled_queue);
	}
// PRODUCER API			
uint8_t* FlowControlAgent2_request_free_buffer(FlowControlAgent2* this) { 
	return Channel_get(this->free_queue);
	}
void FlowControlAgent2_put_filled_in_free_buffer(FlowControlAgent2* this,Buffer* filled_in_buffer) { 
	Channel_put(this->filled_queue,filled_in_buffer);
	}
// CONSUMER API		
uint8_t* FlowControlAgent2_request_filled_in_buffer(FlowControlAgent2* this) { 
	return Channel_get(this->filled_queue);
	}
void FlowControlAgent2_release_filled_in_buffer(FlowControlAgent2* this,Buffer* free_buffer) { 
	Channel_put(this->free_queue,free_buffer);
	}
void FlowControlAgent2_flush_control_buffer(FlowControlAgent2* this) { // FLUSH, DON'T FREE !!!
	while (true) { 
		Buffer* pbuf=Channel_get_nowait(this->filled_queue);
		if (!pbuf) { 
			break;
			}
		}
	}



FlowControlAgent* FlowControlAgent_constructor(FlowControlAgent* this,int buffer_count,int buffer_size) { 
	this->free_queue=  Channel_new(buffer_count);
	this->filled_queue=  Channel_new(buffer_count);
	this->size_queue=  Channel_new(buffer_count);
	for (uint8_t i=0; i< buffer_count; i++) { 
		uint8_t* free_buffer = memalign (64, buffer_size);
		if (!free_buffer) { 
			fprintf (stderr, "Unable to allocate mem at line %d\n",__LINE__);
			return NULL;
			}
		Channel_put(this->free_queue,free_buffer);
		}
	return this;
	}
FlowControlAgent* FlowControlAgent_new(int buffer_count,int buffer_size) { 
	FlowControlAgent* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return FlowControlAgent_constructor(this, buffer_count, buffer_size);
	}

void FlowControlAgent_free(FlowControlAgent* this) { 
	FlowControlAgent_destructor(this);
	free(this);
	}

void FlowControlAgent_destructor(FlowControlAgent* this) { 
	int i=0;
	while (true) { 
		uint8_t* pbuf=Channel_get_nowait(this->free_queue);
		if (!pbuf) { 
			break;
			}
		free (pbuf);
		fprintf (stderr, "freeing output buf: %p, ", pbuf);
		if (((++i) % 8) == 0) { 
			 fprintf (stderr, "\n");
			}
		}
	while (true) { 
		uint8_t* pbuf=Channel_get_nowait(this->filled_queue);
		if (!pbuf) { 
			break;
			}
		free (pbuf);
		fprintf (stderr, "freeing output buf: %p, ", pbuf);
		if (((++i) % 8) == 0) { 
			 fprintf (stderr, "\n");
			}
		}
	while (true) { 
		uint32_t size=Channel_get_nowait(this->size_queue);
		if (!size) { 
			break;
			}
		}
	fprintf (stderr, "\n");
	Channel_free(this->free_queue);
	Channel_free(this->filled_queue);
	Channel_free(this->size_queue);
	}
// PRODUCER API			
uint8_t* FlowControlAgent_request_free_buffer(FlowControlAgent* this) { 
	return Channel_get(this->free_queue);
	}
void FlowControlAgent_put_filled_in_free_buffer(FlowControlAgent* this,uint8_t* filled_in_buffer,uint32_t size) { 
	Channel_put(this->filled_queue,filled_in_buffer);
	Channel_put(this->size_queue,size);
	}
// CONSUMER API		
uint8_t* FlowControlAgent_request_filled_in_buffer(FlowControlAgent* this,uint32_t* size_p) { 
	*size_p=Channel_get(this->size_queue);
	return Channel_get(this->filled_queue);
	}
void FlowControlAgent_release_filled_in_buffer(FlowControlAgent* this,uint8_t* free_buffer) { 
	Channel_put(this->free_queue,free_buffer);
	}
void FlowControlAgent_flush_control_buffer(FlowControlAgent* this) { // FLUSH, DON'T FREE !!!
	while (true) { 
		uint8_t* pbuf=Channel_get_nowait(this->filled_queue);
		uint32_t size=Channel_get_nowait(this->size_queue);
		if (!pbuf) { 
			break;
			}
		}
	}


