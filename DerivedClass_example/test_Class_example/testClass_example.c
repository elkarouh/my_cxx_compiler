#include "../Class_example.h"
int main() { 
	Hello* my =  Hello_new(777,888);
	my =  Hello_new(777,888);
	Hello_printme(my);
	Hello_my_public_class_variable++;
	Hello_my_private_class_variable++;
	fprintf (stderr, "This is a class variable %d\n", Hello_my_public_class_variable);
	fprintf (stderr, "This is a private class variable %d\n", Hello_my_private_class_variable);
	Hello_free(my);
	return 0;
	}

