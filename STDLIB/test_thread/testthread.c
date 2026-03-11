#include "../thread.h"
int main() { 
	atexit(G_destructor);//comment
	G.ch=  ProducerConsumerChannel_new(5,BUFSIZE);
	Producer* pr =  Producer_new();
	Consumer* co =  Consumer_new();
	Task_start(pr,NULL);
	Task_start(co,NULL);
	Task_join(pr);
	Task_join(co);
	}
void G_destructor(void) { 
	fprintf (stderr, "Application stopped\n");
	}


