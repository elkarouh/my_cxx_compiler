class Hello:
	int a
	int b = 0
	public static int my_public_class_variable = 990
	private static int my_private_class_variable = 999
	public static int my_public_class_variable2
	private static int my_private_class_variable2
	def __init__(self,int arg1, int arg2):
		self.a = arg1
		self.b = arg2
	def __del__(self):
		//release resources allocated in constructor
		pass
	@virtual
	void process_msg(self):
		print "Hello is processing message!\n"	
	void printme(self):
		self.process_msg() // virtual method call
		print "a=%d, b=%d\n", self.a, self.b
		my := new Hello(777,888)
		my = new Hello(777,888)
		my->printme() 
////////////////////////////////////////
	
def main():
	my := new Hello(777,888)
	my = new Hello(777,888)
	my->printme() 
	Hello::my_public_class_variable++
	Hello::my_private_class_variable++
	print "This is a class variable %d\n", Hello::my_public_class_variable
	print "This is a private class variable %d\n", Hello::my_private_class_variable
	delete my
	return 0
