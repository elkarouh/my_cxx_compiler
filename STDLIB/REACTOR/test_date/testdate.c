#include "../date.h"
int main(void) { 
	// Date my_test_date2= {2012,6,11}
	uint16_t mydays= get_days_since_2000((Date){2012,6,11});
	assert (mydays == 4545);
	Date mydate= get_date(mydays);
	assert (memcmp(&mydate, &(Date){2012,6,11}, sizeof(Date))==0);
	uint16_t mydays_since_year_begin=get_days_since_beginning_of_year(mydays);
	assert (mydays_since_year_begin == 162);
	//
	time_t start_of_year_in_sec= get_year_start();
	time_t currentTime; time(&currentTime);
	fprintf (stderr, "start of year in sec=%ld\n", start_of_year_in_sec);
	fprintf (stderr, "current time in sec=%ld\n", currentTime);
	fprintf (stderr, "Seconds since year start=%ld\n",currentTime- start_of_year_in_sec);
	fprintf (stderr, "Days since year start=%ld\n",(currentTime- start_of_year_in_sec)/86400);
	}

