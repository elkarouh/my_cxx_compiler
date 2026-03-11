#include "../DerivedClass_example.h"
int main() { 
	Hello* my =  Hello_new(777,888);
	Hello_printme(my);
	DerivedHello* my2 =  DerivedHello_new(1777,1888, 1999, 2000);
	DerivedHello_printme(my2);
	Hello_my_class_variable++;
	Hello_my_private_class_variable++;
	fprintf (stderr, "This is a class variable %d\n", Hello_my_class_variable);
	fprintf (stderr, "This is a private class variable %d\n", Hello_my_private_class_variable);
	Hello_free(my);
	DerivedHello_free(my2);
	return 0;
	}

