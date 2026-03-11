#ifndef _EPOLL_REACTOR_H_
#define _EPOLL_REACTOR_H_


#ifdef _cplusplus // if compiled with C++ compiler.  Note that this is not
// standard, check your compiler's docs and other header files to find out
// the correct macro it uses for c++ versus C compilations.
extern "C" {
#endif
/************************************************/
/*   Standard Header Files includes             */

#include <sys/types.h>
#include <malloc.h>
#include <time.h>
#include <errno.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/stat.h>
#include <sys/epoll.h>
#include <stdio.h>
#include <stddef.h>
#include <fcntl.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
#include <sys/time.h>
#include <netdb.h>
#include <locale.h>
#include <stdbool.h>
#include <sys/select.h>
#include <unistd.h>
#include <netinet/in.h>

/************************************************/

/***************************************************/
/*   Application-specific Header Files includes    */

#include <sys/timerfd.h>
#include <sys/epoll.h>

/**************************************************/



#ifndef _EPOLL_REACTOR_C_
#define EXTERN extern
#else
#define EXTERN
#endif

typedef struct Callback Callback;
typedef struct Reactor Reactor;
typedef struct PeriodicTask_f PeriodicTask_f;
typedef struct Task Task;
typedef struct Thread Thread;
typedef struct UDP_server UDP_server;
typedef struct TCP_Client TCP_Client;
typedef struct TCP_Server TCP_Server;
typedef struct UDP_client UDP_client;
typedef struct Channel Channel;
typedef struct Buffer Buffer;
typedef struct FlowControlAgent2 FlowControlAgent2;
typedef struct FlowControlAgent FlowControlAgent;
int setNonBlocking(int fd);

struct Callback { 
	int fd;
	void (*action_handler)(void*);
	void* arg;// pointer to the object
	};
struct Reactor { 
	int epoll_fd;
	Callback* fd_repository[0xFFFF];
	bool _stop;
	void (*setup)(Reactor* this);// virtual method
	};
Reactor* Reactor_constructor(Reactor* this);

Reactor* Reactor_new();

void Reactor_free(Reactor* this);

void Reactor_run(Reactor* this);

void Reactor_stop(Reactor* this);

void Reactor_schedule_read_fileobject(Reactor* this, int fd, void (*callback)(void*), void* args);

void Reactor_schedule_write_fileobject(Reactor* this, int fd, void (*callback)(void*), void* args);

void Reactor_remove_fileobject(Reactor* this, int fd);

int Reactor_schedule_timed_event(Reactor* this,void (*callback)(void*), void* args, time_t sec, long nsec, time_t intsec, long intnsec);

void Reactor_remove_timed_event(Reactor* this, int fd);

struct PeriodicTask_f { 
	Reactor* reactor_engine;
	uint16_t period;
	uint16_t counter;
	int fd;
	bool terminated;
	void (*run)(PeriodicTask_f* this);// virtual method
	};
PeriodicTask_f* PeriodicTask_f_constructor(PeriodicTask_f* this, Reactor* reactor_engine, double initial_delay_ms,double period_ms);

PeriodicTask_f* PeriodicTask_f_new(Reactor* reactor_engine, double initial_delay_ms,double period_ms);

void PeriodicTask_f_free(PeriodicTask_f* this);

void PeriodicTask_f_destructor(PeriodicTask_f* this);

void PeriodicTask_f_run(PeriodicTask_f* this);

int PeriodicTask_f_update_timer(PeriodicTask_f* this,double initial_delay_ms,double period_ms);

struct Task { 
	pthread_attr_t attr;// thread attributes 
	pthread_t threadid;// the thread id 
	void* arg;
	int max_prio;
	int min_prio;
	bool _stop;
	void (*run)(Task* this, void* arg);// virtual method
	};
Task* Task_constructor(Task* this);

Task* Task_new();

void Task_free(Task* this);

void Task_destructor(Task* this);

void Task_start(Task* this,void* arg);

void Task_callback(Task* this);

void Task_join(Task* this);

void Task_cancel(Task* this);

struct Thread { 
	pthread_attr_t attr;// thread attributes 
	pthread_t threadid;// the thread id 
	void* arg;
	int max_prio;
	int min_prio;
	bool _stop;
	void (*run)(Thread* this, void* arg);// virtual method
	};
Thread* Thread_constructor(Thread* this);

Thread* Thread_new();

void Thread_free(Thread* this);

void Thread_destructor(Thread* this);

void Thread_start(Thread* this,void* arg);

void Thread_callback(Thread* this);

void Thread_join(Thread* this);

void Thread_cancel(Thread* this);

void Thread_stop(Thread* this);

struct UDP_server { 
	Reactor* reactor_engine;
	int sockfd;
	struct sockaddr_storage cliaddr;
	uint8_t rx_buffer[0xFFFF];
	void (*process_message)(UDP_server* this, uint8_t* message, int len );// virtual method
	};
UDP_server* UDP_server_constructor(UDP_server* this, Reactor* reactor_engine, char* MYPORT);

UDP_server* UDP_server_new(Reactor* reactor_engine, char* MYPORT);

void UDP_server_free(UDP_server* this);

void UDP_server_destructor(UDP_server* this);

int UDP_server_send_data(UDP_server* this, uint8_t* message, int len);

struct TCP_Client { 
	int fd;
	uint8_t read_buffer[0xFFFF];
	Reactor* reactor_engine;
	uint16_t read_idx;
	uint16_t (*parse_message)(TCP_Client* this,uint8_t* message, int len);// virtual method
	};
TCP_Client* TCP_Client_constructor(TCP_Client* this, Reactor* engine,int fd);

TCP_Client* TCP_Client_new(Reactor* engine,int fd);

void TCP_Client_free(TCP_Client* this);

void TCP_Client_receive_data(TCP_Client* this);

struct TCP_Server { 
	Reactor* reactor_engine;
	char name[256];
	char ip_address_dot[256];
	uint16_t port_number;
	int server_socket_fd;
	TCP_Client* (*client_constructor)(void*,int);
	};
TCP_Server* TCP_Server_new(Reactor* reactor_engine,char* name, char* ip_address_dot, int port_number,TCP_Client* (*client_constructor)(void*,int));

void TCP_Server_free(TCP_Server* this);

void TCP_Server_accept(TCP_Server* this);

void TCP_Server_teardown(TCP_Server* this);

struct UDP_client { 
	int sockfd;
	struct sockaddr_in servaddr;
	uint8_t rx_buffer[0xFFFF];
	void (*process_message)(UDP_client* this, uint8_t* message, int len );// virtual method
	};
UDP_client* UDP_client_constructor(UDP_client* this, Reactor* reactor_engine, char* SERV_ADDR,char* SERV_PORT);

UDP_client* UDP_client_new(Reactor* reactor_engine, char* SERV_ADDR,char* SERV_PORT);

void UDP_client_free(UDP_client* this);

int UDP_client_send_data(UDP_client* this, uint8_t* message, int len);

struct Channel { 
	void** buf;
	long head;
	long tail;
	bool full;
	bool empty;
	pthread_mutex_t *mutex1;
	pthread_mutex_t *mutex2;
	pthread_cond_t *notFull, *notEmpty, *all_tasks_done;
	int maxsize;
	int unfinished_tasks;
	};
Channel* Channel_new(int maxsize);

void Channel_free(Channel* this);

void Channel_put(Channel* this, void* i);

void* Channel_get(Channel* this);

void* Channel_get_with_timeout(Channel* this, uint32_t TIMEOUT_IN_MILLISECONDS);

void* Channel_get_nowait(Channel* this);

void Channel_task_done(Channel* this);

void Channel_join(Channel* this);

struct Buffer { 
	uint8_t* buf;
	uint32_t size;
	};
Buffer* Buffer_new(buffer_size);

void Buffer_free(Buffer* this);

struct FlowControlAgent2 { 
	Channel*  free_queue;
	Channel* filled_queue;
	};
FlowControlAgent2* FlowControlAgent2_new(int buffer_count,int buffer_size);

void FlowControlAgent2_free(FlowControlAgent2* this);

uint8_t* FlowControlAgent2_request_free_buffer(FlowControlAgent2* this);

void FlowControlAgent2_put_filled_in_free_buffer(FlowControlAgent2* this,Buffer* filled_in_buffer);

uint8_t* FlowControlAgent2_request_filled_in_buffer(FlowControlAgent2* this);

void FlowControlAgent2_release_filled_in_buffer(FlowControlAgent2* this,Buffer* free_buffer);

void FlowControlAgent2_flush_control_buffer(FlowControlAgent2* this);// FLUSH, DON'T FREE !!!

struct FlowControlAgent { 
	Channel*  free_queue;
	Channel* filled_queue;
	Channel* size_queue;
	};
FlowControlAgent* FlowControlAgent_new(int buffer_count,int buffer_size);

void FlowControlAgent_free(FlowControlAgent* this);

uint8_t* FlowControlAgent_request_free_buffer(FlowControlAgent* this);

void FlowControlAgent_put_filled_in_free_buffer(FlowControlAgent* this,uint8_t* filled_in_buffer,uint32_t size);

uint8_t* FlowControlAgent_request_filled_in_buffer(FlowControlAgent* this,uint32_t* size_p);

void FlowControlAgent_release_filled_in_buffer(FlowControlAgent* this,uint8_t* free_buffer);

void FlowControlAgent_flush_control_buffer(FlowControlAgent* this);// FLUSH, DON'T FREE !!!


#ifdef _cplusplus // if compiled with C++ compiler
} // end of extern "C" block
#endif


#undef EXTERN
#endif
