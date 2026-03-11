#define _DATE_C_
#include "date.h"


/************************************************/
/*   FORWARD DECLARATION OF STATIC FUNCTIONS    */

static uint32_t get_days_since_2000(Date mydate);
static Date get_date(int32_t number_days_since_2000);

/************************************************/


Date* Date_new() { 
	Date* this= malloc(sizeof(*this));
	if (!this) { 
		return NULL;
		}
	return this;
	}

void Date_free(Date* this) { 
	free(this);
	}


/***********************************************************************/
time_t get_year_start() { 
	time_t currentTime; time(&currentTime);
	struct tm *gmtTime= gmtime(&currentTime);
	struct tm start_of_year= { 
		.tm_sec=0,
		.tm_min=0,
		.tm_hour=0,
		.tm_mday=1,// first of
		.tm_mon=0,// january
		.tm_year=gmtTime->tm_year,// years since 1900
		.tm_wday= 1,// ignored by mktime
		.tm_yday= 1,// ignored by mktime 
		.tm_isdst= false,
		};
	/*
	for char* buf=malloc(255);buf;free(buf),buf=0:
		strftime(buf, 255, 
			"Start of current year=%d %b %Y %H:%M", &start_of_year)
	*/ 
	return mktime(&start_of_year);
	};
	
bool greater_or_equal(struct timeval t1, struct timeval t2) { 
	if (t1.tv_sec > t2.tv_sec) { 
		return true;
		}
	else if (t1.tv_sec < t2.tv_sec) { 
		return false;
		}
	else { 
		if (t1.tv_usec >= t2.tv_usec) { 
			return true;
			}
		else { 
			return false;
			}
		}
	}

uint64_t  diff_time(struct timeval t1, struct timeval t2) { 
	long sec = t1.tv_sec-t2.tv_sec;// WHAT IF THIS IS NEGATIVE???
	long usec = t1.tv_usec-t2.tv_usec;
	if (usec < 0L) { 
		--sec;
		usec += 1000000L;
		}
	return sec*1000+(usec/1000);// in msec
	//return (struct timeval) {sec,usec}
	}

struct timeval add_time(struct timeval t1, struct timeval t2) { 
	long sec = t1.tv_sec+t2.tv_sec;
	long usec = t1.tv_usec+t2.tv_usec;
	if (usec >= 1000000L) { 
		++sec;
		usec -= 1000000L;
		};
	//return sec*1000+(usec/1000)  // in msec		
	return (struct timeval) {sec,usec};
	}

struct timeval get_time(void) { 
	struct timeval now;
	gettimeofday(&now,NULL);
	return now;
	};
/**********************************************************************/

static uint32_t get_days_since_2000(Date mydate) { 
	if (mydate.month <=2) { 
		mydate.month += 12;
		mydate.year -= 1;
		}
	uint16_t C= mydate.year/100;
	uint16_t B=2-C+C/4;
	return 365*mydate.year + mydate.year/4 + B + 153*(mydate.month+1)/5 + mydate.day -730550;
	}

static Date get_date(int32_t number_days_since_2000) { 
	number_days_since_2000 += 730550;
	int32_t C = (4 * number_days_since_2000 - 497) / 146097;
	int32_t B = 2 - C + (C / 4);
	number_days_since_2000 -= B;
	int32_t Y = (4 * number_days_since_2000 - 489) / 1461;
	number_days_since_2000 -= 365 * Y + (Y / 4);
	int32_t M = ((5 * number_days_since_2000 - 1) / 153) - 1;
	number_days_since_2000 -= 153 * (M + 1) / 5;
	int32_t D = number_days_since_2000;
	if (M > 12) { 
		M = M - 12;
		Y = Y + 1;
		}
	return (Date) {Y, M, D};
	}
	
uint32_t get_days_since_beginning_of_year(int32_t number_days_since_2000) { 
	Date mydate=get_date(number_days_since_2000);
	return number_days_since_2000-get_days_since_2000((Date){mydate.year,1,1});
	}



///////////////////////////////////////////////////////////////////////////
/*  tm struct to time_t formula
tm_sec + tm_min*60 + tm_hour*3600 + tm_yday*86400 +  (tm_year-70)*31536000 + 
((tm_year-69)/4)*86400 - ((tm_year-1)/100)*86400 + ((tm_year+299)/400)*86400
*/	

