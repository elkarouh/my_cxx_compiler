public class Hello:
	int a
	int b
	public static int my_class_variable = 990
	private static int my_private_class_variable = 999
	def __init__(self,int arg1, int arg2):
		self.a = arg1
		self.b = arg2
	def __del__(self):
		//release resources allocated in constructor
		pass
	@virtual
	public void process_msg(self):
		print "Hello is processing message!\n"	
	public void printme(self):
		self.process_msg() // virtual method call
		print "a=%d, b=%d\n", self.a, self.b

// class variable in the c++ way
//public int Hello::my_class_variable = 990
//private int Hello::my_private_class_variable = 999


//////////////////////////////
public class DerivedHello(Hello):
	int c
	int d
	def __init__(self,int arg1, int arg2,int arg3, int arg4):
		//Hello::__init__(self,arg1,arg2)
		super.__init__(self,arg1,arg2)
		self.c = arg3
		self.d = arg4
	def __del__(self):
		//release resources allocated in derived constructor
		super.__del__(self)	
		print
	@override
	public void process_msg(self):
		""" this is a doc string
		'input parameter:....
		"""
		self.printme()
		print "DerivedHello is processing message!\n"
	public void printme(self):
		Hello::printme(self)
		print "a=%d, b=%d\n", self.a, self.b
		print "c=%d, d=%d\n", self.c, self.d

////////////////////////////////////////
	
def main():
	my := new Hello(777,888)
	my->printme() 
	my2 := new DerivedHello(1777,1888, 1999, 2000)
	my2->printme()
	Hello::my_class_variable++
	Hello::my_private_class_variable++
	print "This is a class variable %d\n", Hello::my_class_variable
	print "This is a private class variable %d\n", Hello::my_private_class_variable
	delete my
	delete my2
	return 0
