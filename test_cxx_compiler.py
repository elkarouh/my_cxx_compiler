from hek_test_utils import setup_unittest, unittest, main, NullObject,stdout_redirected
from cxx_compiler import process_lines
import sys
# print sys.version
# print "hello"
def idx_first_mismatch(str1,str2):
	for i in range(min(len(str1),len(str2))):
		if str1[i] != str2[i]:
			return i
	return 9999999
# SETUP THE TEST ENVIRONMENT
@setup_unittest
def verify(sourcetext,targettext,*args,**kwargs):
	DEBUG=kwargs.get("DEBUG",False)
	FAILS=kwargs.get("FAILS",False) #
	lines=sourcetext.split("\n")
	publics, privates,forward_declarations,inline_functions,imported_modules=process_lines(lines)
	from StringIO import StringIO
	with stdout_redirected(StringIO()) as f:
		if publics:
			print "PUBLIC=\n","".join(publics)
		if privates:
			print "PRIVATE=\n","".join(privates)
		if forward_declarations:
			try:
				print "FORWARD DECLARATIONS=\n", "\n".join(forward_declarations)
			except:
				print '>>>>>>>>>>><<<<<',forward_declarations
		if inline_functions:
			print "INLINE FUNCTIONS=\n",    "\n".join(inline_functions)
		if imported_modules:
			print "IMPORTED MODULES\n", "\n".join(imported_modules)
	if targettext:
		try:
			assert targettext.strip() == f.getvalue().strip()
		except AssertionError:
			if privates: print "______", privates[-1]
			print "expected======",len(targettext.strip())
			print "got     ======",len(f.getvalue().strip())
			myidx=idx_first_mismatch(targettext.strip(),f.getvalue().strip())
			print "first mismatch at index ",myidx
			print f.getvalue().strip()[:myidx]+'!!!'+f.getvalue().strip()[myidx:]
			raise
		#print "HEK TEST SUCCESSFUL"
	else:
		print f.getvalue()
	if DEBUG: # WE CAN PASS ARGUMENTS TO THE RUNNER                 #
		sys.stdout=NullObject # WE STOP FOR ALL FOLLOWING TESTS     #
	assert not FAILS

#########################################################################

#########################################################################
@unittest
def test_new2222():
	"""
class AAAA:
	int a
	float b
	def __init__(self):
		self.a=555
	inline int max(self,int a, int b):
		return a>b?a:b


def main():
	a:= new AAAA()
	print "A+b=%d\n", a->max(10,5)
EXPECTED:
PRIVATE=

struct AAAA {
	int a;
	float b;
	};

AAAA* AAAA_constructor(AAAA* this) {
	this->a=555;
	return this;
	}

static AAAA* AAAA_new() {
	AAAA* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return AAAA_constructor(this);
	}

static void AAAA_free(AAAA* this) {
	free(this);
	}




STATIC int main() {
	AAAA* a=  AAAA_new();
	fprintf (stderr, "A+b=%d\n", AAAA_max(a,10,5));
	}


FORWARD DECLARATIONS=
typedef struct AAAA AAAA; // opaque type
static AAAA* AAAA_constructor(AAAA* self);
static AAAA* AAAA_new();
static void AAAA_free(AAAA* self);
INLINE FUNCTIONS=
static inline int AAAA_max(AAAA* self,int a, int b) {
	return a>b?a:b;
	}
"""

@unittest
def test_new2222():
	"""
Memory::head =new Memory(p, size, file, line)
EXPECTED:
PRIVATE=

Memory_head = Memory_new(p, size, file, line);
"""

@unittest
def test_parentheses():
	"""
volatile Vector* myslice= myvector->get_slice(1,(int32_t)NULL)
while (m = num_elems * 2) < self.num_elems :
	pass
if (n1==n2) or (n3==n4):
	if !*G.pattern_file:
		new Memory()
		Memory::head =new Memory(p, size, file, line)
EXPECTED:
PRIVATE=

Vector* myslice __attribute__((cleanup(free_Vector)))= myvector->get_slice(1,(int32_t)NULL);
while ((m = num_elems * 2) < this->num_elems ) {
	// empty statement !!!;
	}
if ((n1==n2)  ||  (n3==n4)) {
	if (!*G.pattern_file) {
		 Memory_new();
		Memory_head = Memory_new(p, size, file, line);
		}
	}


INLINE FUNCTIONS=
static inline void free_Vector(Vector **fp) { if (*fp) Vector_free(*fp); }
"""

@unittest
def test_with_statement():
	'''
void fun():
	with new double as buf:
		print buf
	with new uint8_t[255] as buf:
		print buf
	with new uint8_t=unhexlify("7844aa99") as inv:
		assert inv[3]==0x99
EXPECTED:
PRIVATE=

void fun() {
	for (double* buf=malloc(sizeof(*buf)) , enter=1; enter; free(buf), enter=0) {
		fprintf (stderr, buf);
		}
	for (uint8_t* buf=calloc(255,sizeof(uint8_t)), enter=1; enter; free(buf), enter=0) {
		fprintf (stderr, buf);
		}
	for (uint8_t* inv=unhexlify("7844aa99"), enter=1; enter; free(inv), enter=0) {
		assert (inv[3]==0x99);
		}
	}


FORWARD DECLARATIONS=
static void fun();
'''

#@unittest
def test_multiline_strings():
	'''
char * ok_response =
	QHTTP/1.0 200 OKQ
	QContent-type: text/htmlQ
	QsssQ
EXPECTED:
PRIVATE=

char * ok_response =
	QHTTP/1.0 200 OKQ
	QContent-type: text/htmlQ
	QsssQ;
'''

@unittest
def test_polymorphic_calls():
	"""
for DrawingObject* c in collectibles:
	c=>draw()
	c=>draw(param)
EXPECTED:
PRIVATE=

for (int i=1;i<=collectibles[0];i++ ) {
	DrawingObject* c = collectibles[i];
	c->draw(c);
	c->draw(c,param);
	}


FORWARD DECLARATIONS=
#define append(sp, n) sp[++*(int*)sp] = (n)
#define pop(sp) sp[--*(int*)sp+1]
#define insert(sp,n,i) (*(((void**)memmove(&sp[i+1],&sp[i],sizeof(void*)*(1-i+(*(int*)sp)++)))-1))=(n)
#define remove(sp,i) (*(((void**)memmove(&sp[i],&sp[i+1],sizeof(void*)*(1-i+(*(int*)sp)--)))-1))
"""

@unittest
def test_public_constructors():
	"""
public class EEEE:
	int x
	public def __init__(self):
		self.x=4
EXPECTED:
PUBLIC=
typedef struct EEEE EEEE;
struct EEEE {
	int x;
	};
EEEE* EEEE_constructor(EEEE* this);

EEEE* EEEE_new();

void EEEE_free(EEEE* this);


PRIVATE=


EEEE* EEEE_constructor(EEEE* this) {
	this->x=4;
	return this;
	}
EEEE* EEEE_new() {
	EEEE* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return EEEE_constructor(this);
	}

void EEEE_free(EEEE* this) {
	free(this);
	}
"""


@unittest
def test_annotated_arrays():
	'''
array:= new char*[30]
append(array,"hello")
append(array,"world")
for char* str in array:
	print "string=%s\n", str
for char* str in array.reversed:
	print "\nreversed string=%s", str
print "\nsize=%d\n",array[0]
print "el=%s\n", pop(array)
EXPECTED:
PRIVATE=

char** array= calloc(30,sizeof(char*));
append(array,"hello");
append(array,"world");
for (int i=1;i<=array[0];i++ ) {
	char* str = array[i];
	fprintf (stderr, "string=%s\n", str);
	}
for (int i= array[0];i>0;i-- ) {
	char* str = array[i];
	fprintf (stderr, "\nreversed string=%s", str);
	}
fprintf (stderr, "\nsize=%d\n",array[0]);
fprintf (stderr, "el=%s\n", pop(array));


FORWARD DECLARATIONS=
#define append(sp, n) sp[++*(int*)sp] = (n)
#define pop(sp) sp[--*(int*)sp+1]
#define insert(sp,n,i) (*(((void**)memmove(&sp[i+1],&sp[i],sizeof(void*)*(1-i+(*(int*)sp)++)))-1))=(n)
#define remove(sp,i) (*(((void**)memmove(&sp[i],&sp[i+1],sizeof(void*)*(1-i+(*(int*)sp)--)))-1))
'''


@unittest
def test_annotated_arrays2():
	'''
gen := new GenObj(444)
array:= new Object*[30]
array.append("hello")
Object* a= array.pop()
for Object* str in array:
	print "string=%s\n", str
for int val in gen:
	print val
EXPECTED:
PRIVATE=

GenObj* gen =  GenObj_new(444);
Object** array= calloc(30,sizeof(Object*));
append(array,"hello");
Object* a= pop(array);
for (int i=1;i<=array[0];i++ ) {
	Object* str = array[i];
	fprintf (stderr, "string=%s\n", str);
	}
while (true)  {
	int val =GenObj_next(gen); if (gen->_exhausted) break;
	fprintf (stderr, val);
	}


FORWARD DECLARATIONS=
#define append(sp, n) sp[++*(int*)sp] = (n)
#define pop(sp) sp[--*(int*)sp+1]
#define insert(sp,n,i) (*(((void**)memmove(&sp[i+1],&sp[i],sizeof(void*)*(1-i+(*(int*)sp)++)))-1))=(n)
#define remove(sp,i) (*(((void**)memmove(&sp[i],&sp[i+1],sizeof(void*)*(1-i+(*(int*)sp)--)))-1))
'''


@unittest
def test_enum0():
	"""
struct X:
	ADAS_Hdr hdr
	U32 updatedFields
	U32 refClockFre
enum X:
	QUEUESIZE = 10
enum :
	QUEUESIZE = 10
private struct G:
	uint32_t global1
	uint32_t global2
G=:
	.global1=6 // comment
	.global2=7
struct Preamble:
	int x
	int y
EXPECTED:
PRIVATE=

struct X {
	ADAS_Hdr hdr;
	U32 updatedFields;
	U32 refClockFre;
	};
enum X {
	QUEUESIZE = 10,
	};
enum  {
	QUEUESIZE = 10,
	};
struct G {
	uint32_t global1;
	uint32_t global2;
	}
G= {
	.global1=6,// comment
	.global2=7,
	};
struct Preamble {
	int x;
	int y;
	};


FORWARD DECLARATIONS=
typedef struct X X; // opaque type
typedef enum X X; // opaque type
typedef struct Preamble Preamble; // opaque type
"""

@unittest
def test_enum2():
	"""
int get():
	for char inZ line:
		if char == DOUBLE_QUOTE:
			within_double_quote=True
			output_string+= REPLACER
			continue
		output_string+= char
	return output_string
	for x inZ a:
		for y inZ b:
			for x inZ e:
				print
	print
EXPECTED:
PRIVATE=

int get() {
	for (char inZ line) {
		if (char == DOUBLE_QUOTE) {
			within_double_quote=True;
			output_string+= REPLACER;
			continue;
			}
		output_string+= char;
		}
	return output_string;
	for (x inZ a) {
		for (y inZ b) {
			for (x inZ e) {
				fprintf (stderr,);
				}
			}
		}
	fprintf (stderr,);
	}


FORWARD DECLARATIONS=
static int get();
"""

@unittest
def test_class():
	"""
class Preamble:
	int x
	int y
	def __init__(self, int x, int y):
		self.x=x
		self.y=y
	def __del__(self):
		free(self)
	void move(self, int dx,
					int dy):
		int d
		self.x += dx
int s
int myfunc(int d,
	int f):
	print "ddd"

void move2(self, int dx,
				int dy):
	int d
	self.x += dx
EXPECTED:
PRIVATE=

struct Preamble {
	int x;
	int y;
	};

Preamble* Preamble_constructor(Preamble* this, int x, int y) {
	this->x=x;
	this->y=y;
	return this;
	}

static Preamble* Preamble_new(int x, int y) {
	Preamble* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Preamble_constructor(this, x, y);
	}

static void Preamble_free(Preamble* this) {
	Preamble_destructor(this);
	free(this);
	}

void Preamble_destructor(Preamble* this) {
	free(this);
	}
void Preamble_move(Preamble* this, int dx,
					int dy) {
	int d;
	this->x += dx;
	}

int s;
int myfunc(int d,
	int f) {
	fprintf (stderr, "ddd");
	}

void move2(this, int dx,
				int dy) {
	int d;
	this->x += dx;
	}


FORWARD DECLARATIONS=
typedef struct Preamble Preamble; // opaque type
static Preamble* Preamble_constructor(Preamble* self, int x, int y);
static Preamble* Preamble_new(int x, int y);
static void Preamble_free(Preamble* self);
static void Preamble_destructor(Preamble* self);
static void Preamble_move(Preamble* self, int dx,
					int dy);
static int myfunc(int d,
	int f);
static void move2(self, int dx,
				int dy);
"""

@unittest
def test_generators1():
	"""
class Count:
	int step
	int count
	def __init__(self, int start, int step):
		self.step=step
		self.count=start
	int next(self, int anumber):
		while true:
			yield self.count + anumber
			self.count += self.step
			if a==2:
				yield None
			else:
				return 6
		return 0
EXPECTED:
PRIVATE=

struct Count {
	int _state;
	bool _exhausted;
	bool _valid_output;
	int step;
	int count;
	};

Count* Count_constructor(Count* this, int start, int step) {
	this->_state=0;
	this->_exhausted=false;
	this->_valid_output=true;
	this->step=step;
	this->count=start;
	return this;
	}

static Count* Count_new(int start, int step) {
	Count* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Count_constructor(this, start, step);
	}

static void Count_free(Count* this) {
	free(this);
	}

int Count_next(Count* this, int anumber) {
	switch (this->_state) {
		case 0: goto LABEL0;
		case 1: goto LABEL1;
		case 2: goto LABEL2;
		}
	LABEL0: //start of generator;
	while (true) {
		//start of yield #1
		this->_state=1;
		this->_valid_output=true;
		return this->count + anumber;
		LABEL1:;
		//end of yield #1

		this->count += this->step;
		if (a==2) {
			//start of yield #2
			this->_state=2;
			this->_valid_output=false;
			return NULL;
			LABEL2:;
			//end of yield #2
			}
		else {
			this->_valid_output=false;
			this->_exhausted=true;
			return 6;
			}
		}
	this->_valid_output=false;
	this->_exhausted=true;
	return 0;
	}



FORWARD DECLARATIONS=
typedef struct Count Count; // opaque type
static Count* Count_constructor(Count* self, int start, int step);
static Count* Count_new(int start, int step);
static void Count_free(Count* self);
static int Count_next(Count* self, int anumber);

"""

@unittest
def test_new_type_inference():
	"""
print(new Count(2))
self.tcp_server:= new TCP_Server(self,"MY TCP SERVER", "0.0.0.0", 8080,MyTCP_Client_SS::new)
notif:= new Notification(START_PURE_CARRIER,new PureCarrier(frequency,tx_level))
EXPECTED:
PRIVATE=

fprintf (stderr,( Count_new(2)));
TCP_Server* this->tcp_server=  TCP_Server_new(this,"MY TCP SERVER", "0.0.0.0", 8080,MyTCP_Client_SS_new);
Notification* notif=  Notification_new(START_PURE_CARRIER,new PureCarrier(frequency,tx_level));
"""

@unittest
def test_generators3():
	"""
class Count:
	int count
	def __init__(self, int start, int step):
		self.count=start
	int next(self):
		while true:
			yield self.count
			self.count += self.step
			yield None
			if self.count>10:
				return 0
int main():
	mycount:= new Count(2,5)
	for int res in mycount:
		print "+++=%d\n",res
	delete mycount
EXPECTED:
PRIVATE=

struct Count {
	int _state;
	bool _exhausted;
	bool _valid_output;
	int count;
	};

Count* Count_constructor(Count* this, int start, int step) {
	this->_state=0;
	this->_exhausted=false;
	this->_valid_output=true;
	this->count=start;
	return this;
	}

static Count* Count_new(int start, int step) {
	Count* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Count_constructor(this, start, step);
	}

static void Count_free(Count* this) {
	free(this);
	}

int Count_next(Count* this) {
	switch (this->_state) {
		case 0: goto LABEL0;
		case 1: goto LABEL1;
		case 2: goto LABEL2;
		}
	LABEL0: //start of generator;
	while (true) {
		//start of yield #1
		this->_state=1;
		this->_valid_output=true;
		return this->count;
		LABEL1:;
		//end of yield #1

		this->count += this->step;
		//start of yield #2
		this->_state=2;
		this->_valid_output=false;
		return NULL;
		LABEL2:;
		//end of yield #2

		if (this->count>10) {
			this->_valid_output=false;
			this->_exhausted=true;
			return 0;
			}
		}
	}

STATIC int main() {
	Count* mycount=  Count_new(2,5);
	while (true)  {
		int res =Count_next(mycount); if (mycount->_exhausted) break;
		fprintf (stderr, "+++=%d\n",res);
		}
	Count_free(mycount);
	}


FORWARD DECLARATIONS=
typedef struct Count Count; // opaque type
static Count* Count_constructor(Count* self, int start, int step);
static Count* Count_new(int start, int step);
static void Count_free(Count* self);
static int Count_next(Count* self);
"""

@unittest
def test_generators2():
	"""
class Count:
	int step
	int count
	def __init__(self, int start, int step):
		self.step=step
		self.count=start
	void next(self, int anumber):
		while true:
			yield
			self.count += self.step
		return
EXPECTED:
PRIVATE=

struct Count {
	int _state;
	bool _exhausted;
	bool _valid_output;
	int step;
	int count;
	};

Count* Count_constructor(Count* this, int start, int step) {
	this->_state=0;
	this->_exhausted=false;
	this->_valid_output=true;
	this->step=step;
	this->count=start;
	return this;
	}

static Count* Count_new(int start, int step) {
	Count* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Count_constructor(this, start, step);
	}

static void Count_free(Count* this) {
	free(this);
	}

void Count_next(Count* this, int anumber) {
	switch (this->_state) {
		case 0: goto LABEL0;
		case 1: goto LABEL1;
		}
	LABEL0: //start of generator;
	while (true) {
		//start of yield #1
		this->_state=1;
		return;
		LABEL1:;
		//end of yield #1

		this->count += this->step;
		}
	this->_valid_output=false;
	this->_exhausted=true;
	return;
	}



FORWARD DECLARATIONS=
typedef struct Count Count; // opaque type
static Count* Count_constructor(Count* self, int start, int step);
static Count* Count_new(int start, int step);
static void Count_free(Count* self);
static void Count_next(Count* self, int anumber);
"""

@unittest
def test_generator_without_constructor():
	"""
class Fibonacci:
	int a = 0
	int b = 1
	int tmp
	int next(self):
		forever:
			yield self.a
			self.tmp= self.a
			self.a = self.b
			self.b += self.tmp
EXPECTED:
PRIVATE=

struct Fibonacci {
	int _state;
	bool _exhausted;
	bool _valid_output;
	int a;
	int b;
	int tmp;
	};

Fibonacci* Fibonacci_constructor(Fibonacci* this) {
	this->_state=0;
	this->_exhausted=false;
	this->_valid_output=true;
	return this;
	}
static Fibonacci* Fibonacci_new() {
	Fibonacci* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Fibonacci_constructor(this);
	}

static void Fibonacci_free(Fibonacci* this) {
	free(this);
	}

int Fibonacci_next(Fibonacci* this) {
	switch (this->_state) {
		case 0: goto LABEL0;
		case 1: goto LABEL1;
		}
	LABEL0: //start of generator;
	for (;;) {
		//start of yield #1
		this->_state=1;
		this->_valid_output=true;
		return this->a;
		LABEL1:;
		//end of yield #1

		this->tmp= this->a;
		this->a = this->b;
		this->b += this->tmp;
		}
	}



FORWARD DECLARATIONS=
typedef struct Fibonacci Fibonacci; // opaque type
static Fibonacci* Fibonacci_constructor(Fibonacci* self);
static Fibonacci* Fibonacci_new();
static void Fibonacci_free(Fibonacci* self);
static int Fibonacci_next(Fibonacci* self);

"""

@unittest
def test_func_pointers_as_attributes():
	"""
class Hello:
	int (*funpointer)(void*)
	def __init__(self,int arg1, int arg2):
		self.a = arg1
		self.b = arg2
	@virtual
	public void process_msg(self, char* msg):
		print "Hello is processing message!\n"
	public void printme(self):
		self.process_msg()
		self.funpointer(888)
		print "a=%d, b=%d\n", self.a, self.b
	public void meth_inher(self):
		print "meth inher a=%d, b=%d\n", self.a, self.b
EXPECTED:
PUBLIC=
void Hello_process_msg(Hello* this, char* msg);

void Hello_printme(Hello* this);

void Hello_meth_inher(Hello* this);


PRIVATE=

struct Hello {
	int (*funpointer)(void*);
	void (*process_msg)(Hello* this, char* msg);// virtual method
	};

Hello* Hello_constructor(Hello* this,int arg1, int arg2) {
	this->a = arg1;
	this->b = arg2;
	this->process_msg=Hello_process_msg;// virtual method
	return this;
	}

static Hello* Hello_new(int arg1, int arg2) {
	Hello* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Hello_constructor(this, arg1, arg2);
	}

static void Hello_free(Hello* this) {
	free(this);
	}

void Hello_process_msg(Hello* this, char* msg) {
	fprintf (stderr, "Hello is processing message!\n");
	}
void Hello_printme(Hello* this) {
	this->process_msg(this);
	this->funpointer(888);
	fprintf (stderr, "a=%d, b=%d\n", this->a, this->b);
	}
void Hello_meth_inher(Hello* this) {
	fprintf (stderr, "meth inher a=%d, b=%d\n", this->a, this->b);
	}



FORWARD DECLARATIONS=
typedef struct Hello Hello; // opaque type
static Hello* Hello_constructor(Hello* self,int arg1, int arg2);
static Hello* Hello_new(int arg1, int arg2);
static void Hello_free(Hello* self);
"""

@unittest
def test_dcdcdc():
	"""
private int func1(int x):
	int x
	int y
	print a
	print b
	print c
public void function(int x,int y):
	int x
	int y
public void function2(int x,
			int y):
	int xc
	int yc
EXPECTED:
PUBLIC=
void function(int x,int y);

void function2(int x,
			int y);


PRIVATE=

static int func1(int x) {
	int x;
	int y;
	fprintf (stderr, a);
	fprintf (stderr, b);
	fprintf (stderr, c);
	}
void function(int x,int y) {
	int x;
	int y;
	}
void function2(int x,
			int y) {
	int xc;
	int yc;
	}


FORWARD DECLARATIONS=
static int func1(int x);
"""

@unittest
def test_namespaces1():
	'''
namespace G:
	uint16_t raw_input_cadu_size=1000 // comment 1
	char filename[10]="hello" // comment 2
	char *x = "ffffff"  // comment 3
	namespace:
		int a = 888 // this is an
		int b= 777
	namespace HHH:
		float ddd
	namespace JJ:
		char *x=44444
EXPECTED:
PRIVATE=

struct G {
	uint16_t raw_input_cadu_size;// comment 1
	char filename[10];// comment 2
	char *x;// comment 3
	struct {
		int a;// this is an
		int b;
		};
	struct HHH {
		float ddd;
		};
	struct JJ {
		char *x;
		};
	}
G= {
	.raw_input_cadu_size=1000,
	.filename="hello",
	.x= "ffffff",
		{ // NAMESPACE,
		.a= 888,
		.b= 777,
		},
		{ // NAMESPACE  HHH,
		},
		{ // NAMESPACE  JJ,
		.x=44444,
		},
	};
'''

@unittest
def test_class2222():
	"""
public class Vector:
	v_elem_t* elems
	size_t num_elems
	size_t num_alloc_elems
	def __init__(self,size_t init_size):
		self.num_alloc_elems = init_size
		self.num_elems = 0
		self.elems = new v_elem_t[init_size]
		if self.elems == NULL:
			print "Unable to allocate memory"
			exit(-1)
EXPECTED:
PUBLIC=
typedef struct Vector Vector;
struct Vector {
	v_elem_t* elems;
	size_t num_elems;
	size_t num_alloc_elems;
	};
Vector* Vector_new(size_t init_size);

void Vector_free(Vector* this);


PRIVATE=


Vector* Vector_constructor(Vector* this,size_t init_size) {
	this->num_alloc_elems = init_size;
	this->num_elems = 0;
	this->elems = calloc(init_size,sizeof(v_elem_t));
	if (this->elems == NULL) {
		fprintf (stderr, "Unable to allocate memory");
		exit(-1);
		}
	return this;
	}
Vector* Vector_new(size_t init_size) {
	Vector* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Vector_constructor(this, init_size);
	}

void Vector_free(Vector* this) {
	free(this);
	}




FORWARD DECLARATIONS=
static Vector* Vector_constructor(Vector* self,size_t init_size);
"""

@unittest
def test_func_decl_on_several_lines():
	"""
public void function(int x,int y):
	int x
	int y
public void function2(int x,
			int y):
	int xc
	int yc
EXPECTED:
PUBLIC=
void function(int x,int y);

void function2(int x,
			int y);


PRIVATE=

void function(int x,int y) {
	int x;
	int y;
	}
void function2(int x,
			int y) {
	int xc;
	int yc;
	}
"""

@unittest
def test_function_pointer_argument():
	"""
class Test:
	int x
	public void sortGOOD(self, int x):
		print
	public void sort(self, int (*cmp_func)(const void *, const void *)):
		qsort(self.elems, self.num_elems, sizeof(v_elem_t), cmp_func)
EXPECTED:
PUBLIC=
void Test_sortGOOD(Test* this, int x);

void Test_sort(Test* this, int (*cmp_func)(const void *, const void *));


PRIVATE=

struct Test {
	int x;
	};

static Test* Test_new() {
	Test* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

static void Test_free(Test* this) {
	free(this);
	}

void Test_sortGOOD(Test* this, int x) {
	fprintf (stderr,);
	}
void Test_sort(Test* this, int (*cmp_func)(const void *, const void *)) {
	qsort(this->elems, this->num_elems, sizeof(v_elem_t), cmp_func);
	}



FORWARD DECLARATIONS=
typedef struct Test Test; // opaque type
static Test* Test_new();
static void Test_free(Test* self);
"""

@unittest
def test_derived_class():
	"""
public class DerivedQueue(Queue):
	int z
	def __init__(self, int myx, int myy, int myz):
		super.__init__(self,myx, myy)
		self.z=z
	def __del__(self):
		release resources allocated in constructor
		super.__del__(self)
q :=new DerivedQueue(1,2,3)
EXPECTED:
PUBLIC=
typedef struct DerivedQueue DerivedQueue;
struct DerivedQueue {
	Queue;
	int z;
	};
DerivedQueue* DerivedQueue_new(int myx, int myy, int myz);

void DerivedQueue_free(DerivedQueue* this);


PRIVATE=


DerivedQueue* DerivedQueue_constructor(DerivedQueue* this, int myx, int myy, int myz) {
	Queue_constructor((Queue*)this,myx, myy);
	this->z=z;
	return this;
	}

DerivedQueue* DerivedQueue_new(int myx, int myy, int myz) {
	DerivedQueue* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return DerivedQueue_constructor(this, myx, myy, myz);
	}

void DerivedQueue_free(DerivedQueue* this) {
	DerivedQueue_destructor(this);
	free(this);
	}

void DerivedQueue_destructor(DerivedQueue* this) {
	release resources allocated in constructor;
	Queue_destructor(this);
	}

DerivedQueue* q = DerivedQueue_new(1,2,3);


FORWARD DECLARATIONS=
static DerivedQueue* DerivedQueue_constructor(DerivedQueue* self, int myx, int myy, int myz);
static void DerivedQueue_destructor(DerivedQueue* self);
"""

@unittest
def test_multiline_args():
	"""
public int func1(int x):
	int x
	int y
private float func2(int w,
			int t):
	print
EXPECTED:
PUBLIC=
int func1(int x);


PRIVATE=

int func1(int x) {
	int x;
	int y;
	}
static float func2(int w,
			int t) {
	fprintf (stderr,);
	}


FORWARD DECLARATIONS=
static float func2(int w,
			int t);
"""

@unittest
def test_class4():
	"""
#include fsync.h
#include mymath.h
public class Preamble:
	int a
	int b
EXPECTED:
PUBLIC=
typedef struct Preamble Preamble;
struct Preamble {
	int a;
	int b;
	};
Preamble* Preamble_new();

void Preamble_free(Preamble* this);


PRIVATE=


Preamble* Preamble_new() {
	Preamble* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

void Preamble_free(Preamble* this) {
	free(this);
	}



IMPORTED MODULES
#include fsync.h
#include mymath.h
"""

@unittest
def test_class5():
	"""
public int func1(int x):
	int x
	int y
private float func2(int w,
			int t):
	print
EXPECTED:
PUBLIC=
int func1(int x);


PRIVATE=

int func1(int x) {
	int x;
	int y;
	}
static float func2(int w,
			int t) {
	fprintf (stderr,);
	}


FORWARD DECLARATIONS=
static float func2(int w,
			int t);
"""

@unittest
def test_class25():
	"""
while true:
	if actually_read>0:
		print "\nCh %d: input channel closed\n",G.tm_channel
		if G.tm_channel<2:
			goto restart
		else:
			break
	// this is for the next output_buffer
	self.buffer_write_idx= 0
EXPECTED:
PRIVATE=

while (true) {
	if (actually_read>0) {
		fprintf (stderr, "\nCh %d: input channel closed\n",G.tm_channel);
		if (G.tm_channel<2) {
			goto restart;
			}
		else {
			break;
			}
		}
	// this is for the next output_buffer
	this->buffer_write_idx= 0;
	}
"""


@unittest
def testDoWhile():
	"""
do:
	printf
while true
sys.exit()
EXPECTED:
PRIVATE=

do {
	printf;
	}
while (true);
sys.exit();

"""


@unittest
def testBidimensionalAllocation():
	"""
arr:= new double[ROWS][COLS]
vec:= new double[100]
EXPECTED:
PRIVATE=

double* arr_p= calloc(ROWS*COLS,sizeof(double));
double (*arr)[COLS]=(double(*)[COLS])arr_p;
double* vec= calloc(100,sizeof(double));
"""


@unittest
def test_virtual_methods():
	"""
public class Hello:
	int a
	int b
	float ff=999.999
	char* name= "hello"
	public static int my_class_variable = 990  // class variable, notice the initialisation!!!
	private static int my_private_class_variable = 999  // notice the initialisation!!!
	def __init__(self,int arg1, int arg2):
		self.a = arg1
		self.b = arg2
	@virtual
	public void process_msg(self, char* msg):
		print "Hello is processing message!\n"
	public void printme(self):
		self.process_msg()
		print "a=%d, b=%d\n", self.a, self.b
EXPECTED:
PUBLIC=
typedef struct Hello Hello;
struct Hello {
	int a;
	int b;
	float ff;
	char* name;
	void (*process_msg)(Hello* this, char* msg);// virtual method
	};
extern int Hello_my_class_variable;// class variable, notice the initialisation!!!
Hello* Hello_new(int arg1, int arg2);

void Hello_free(Hello* this);

void Hello_process_msg(Hello* this, char* msg);

void Hello_printme(Hello* this);


PRIVATE=


Hello* Hello_constructor(Hello* this,int arg1, int arg2) {
	this->ff=999.999;
	strcpy(this->name, "hello");
	this->a = arg1;
	this->b = arg2;
	this->process_msg=Hello_process_msg;// virtual method
	return this;
	}

int Hello_my_class_variable = 990;// class variable, notice the initialisation!!!
Hello* Hello_new(int arg1, int arg2) {
	Hello* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Hello_constructor(this, arg1, arg2);
	}

void Hello_free(Hello* this) {
	free(this);
	}

void Hello_process_msg(Hello* this, char* msg) {
	fprintf (stderr, "Hello is processing message!\n");
	}
void Hello_printme(Hello* this) {
	this->process_msg(this);
	fprintf (stderr, "a=%d, b=%d\n", this->a, this->b);
	}



FORWARD DECLARATIONS=
static Hello* Hello_constructor(Hello* self,int arg1, int arg2);
static int Hello_my_private_class_variable = 999  ;

"""

@unittest
def testMultiLineCondition():
	"""
while true:
	printf
while (sxdio_dma_running and
	(test_dma_continuous || (n_transactions < test_n_transactions))):
	void *     pbuf
	int        len
label:
code
EXPECTED:
PRIVATE=

while (true) {
	printf;
	}
while (sxdio_dma_running  &&
	(test_dma_continuous || (n_transactions < test_n_transactions))) {
	void *     pbuf;
	int        len;
	}
label:
code;
"""


@unittest
def test_multiline_declarations(): # fwd decl buggy
	"""
public void Preamble::init(
	Preamble* self,
	int size,
	void param
	):
	printf
// this is a comment
public void Preamble::new(Preamble* self,
	int size,
	void param
	):
	printf
EXPECTED:
PUBLIC=
void Preamble_init(
	Preamble* this,
	int size,
	void param
	);

void Preamble_new(Preamble* this,
	int size,
	void param
	);


PRIVATE=

void Preamble_init(
	Preamble* this,
	int size,
	void param
	) {
	printf;
	}
// this is a comment
void Preamble_new(Preamble* this,
	int size,
	void param
	) {
	printf;
	}
"""


#########################################################################

@unittest
def test_array_initialisation():
	"""
private uint8_t tm_ack[]=:
	0x49, 0x96, 0x02, 0xD2, 0x00, 0x00, 0x00, 0x14
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
	0xB6, 0x69, 0xFD, 0x2E
EXPECTED:
PRIVATE=

static uint8_t tm_ack[]= {
	0x49, 0x96, 0x02, 0xD2, 0x00, 0x00, 0x00, 0x14,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0xB6, 0x69, 0xFD, 0x2E,
	};
"""

@unittest
def test_implicit_union_struct_class():
	"""
union my_implict_union:
	int c
	int d
struct my_implict_struct:
	int c
	int d
class Implicit_class:
	int fd
	callback_t file_callback
	void* callback_args
EXPECTED:
PRIVATE=

union my_implict_union {
	int c;
	int d;
	};
struct my_implict_struct {
	int c;
	int d;
	};
struct Implicit_class {
	int fd;
	callback_t file_callback;
	void* callback_args;
	};

static Implicit_class* Implicit_class_new() {
	Implicit_class* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

static void Implicit_class_free(Implicit_class* this) {
	free(this);
	}



FORWARD DECLARATIONS=
typedef union my_implict_union my_implict_union; // opaque type
typedef struct my_implict_struct my_implict_struct; // opaque type
typedef struct Implicit_class Implicit_class; // opaque type
static Implicit_class* Implicit_class_new();
static void Implicit_class_free(Implicit_class* self);
"""

@unittest
def test_public_union_struct_class():
	"""
public union my_public_union:
	int c
	int d
public struct my_public_struct:
	int c
	int d
public class Public_class:
	int fd
	callback_t file_callback
	void* callback_args
EXPECTED:
PUBLIC=
typedef union my_public_union my_public_union;
typedef struct my_public_struct my_public_struct;
typedef struct Public_class Public_class;
union my_public_union {
	int c;
	int d;
	};
struct my_public_struct {
	int c;
	int d;
	};
struct Public_class {
	int fd;
	callback_t file_callback;
	void* callback_args;
	};
Public_class* Public_class_new();

void Public_class_free(Public_class* this);


PRIVATE=


Public_class* Public_class_new() {
	Public_class* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

void Public_class_free(Public_class* this) {
	free(this);
	}
"""

@unittest
def test_private_union_struct_class():
	"""
private union my_private_union:
	int c
	int d
private struct my_private_struct:
	int c
	int d
private class Private_class:
	int fd
	callback_t file_callback
	void* callback_args
EXPECTED:
PRIVATE=

union my_private_union {
	int c;
	int d;
	};
struct my_private_struct {
	int c;
	int d;
	};
struct Private_class {
	int fd;
	callback_t file_callback;
	void* callback_args;
	};

static Private_class* Private_class_new() {
	Private_class* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

static void Private_class_free(Private_class* this) {
	free(this);
	}



FORWARD DECLARATIONS=
typedef union my_private_union my_private_union; // opaque type
typedef struct my_private_struct my_private_struct; // opaque type
typedef struct Private_class Private_class; // opaque type
static Private_class* Private_class_new();
static void Private_class_free(Private_class* self);
"""
@unittest
def test_protected_class():
	"""
protected class Protected_class:
	int fd
	callback_t file_callback
	void* callback_args
EXPECTED:
PUBLIC=
typedef struct Protected_class Protected_class;// opaque type
Protected_class* Protected_class_new();

void Protected_class_free(Protected_class* this);


PRIVATE=

struct Protected_class {
	int fd;
	callback_t file_callback;
	void* callback_args;
	};

Protected_class* Protected_class_new() {
	Protected_class* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

void Protected_class_free(Protected_class* this) {
	free(this);
	}
"""

@unittest
def test_struct_initialisation():
	"""
struct G:
	uint32_t global1
	uint32_t global2
G=:
	.global1=6 // comment
	.global2=7
EXPECTED:
PRIVATE=

struct G {
	uint32_t global1;
	uint32_t global2;
	}
G= {
	.global1=6,// comment
	.global2=7,
	};
"""

@unittest
def test_enum():
	"""
enum X:
	QUEUESIZE = 10
enum :
	QUEUESIZE = 20
EXPECTED:
PRIVATE=

enum X {
	QUEUESIZE = 10,
	};
enum  {
	QUEUESIZE = 20,
	};


FORWARD DECLARATIONS=
typedef enum X X; // opaque type
"""

@unittest
def test_nested_anonymous_struct():
	"""
struct Foo:
	int a
	union:
		int b
		float c
	int d
Foo foo = {15, {3.2}, 13}
EXPECTED:
PRIVATE=

struct Foo {
	int a;
	union {
		int b;
		float c;
		};
	int d;
	}
Foo foo = {15, {3.2}, 13};


FORWARD DECLARATIONS=
typedef struct Foo Foo; // opaque type
"""

@unittest
def test_parenless_functions():
	"""
assert x==7
print "fdjkfd",rr
int x
EXPECTED:
PRIVATE=

assert (x==7);
fprintf (stderr, "fdjkfd",rr);
int x;
"""

@unittest
def testCommentAtWrongPlace():
	"""
if len < 0:
	break
/* set up the pusher read length */
sxdio_reg_write (test_fd, DDR_RD_LENGTH, test_buf_size)
EXPECTED:
PRIVATE=

if (len < 0) {
	break;
	}
/* set up the pusher read length */
sxdio_reg_write (test_fd, DDR_RD_LENGTH, test_buf_size);

"""

@unittest
def test_change_self():
	"""
void QUEUE_init(Queue *self, int size):
	self.first= 0
	self.last= size-1
	if self.count= 0:
		printf
EXPECTED:
PRIVATE=

void QUEUE_init(Queue *this, int size) {
	this->first= 0;
	this->last= size-1;
	if (this->count= 0) {
		printf;
		}
	}


FORWARD DECLARATIONS=
static void QUEUE_init(Queue *self, int size);
"""

@unittest
def testCommentBreakIdentation(DEBUG=0):
	"""
int main (int argc, char * argv[]):
	int result = 0
	/*
	 * process the command line options
	 */
	if test_options_get (argc, argv) != 0:
		print_usage ()
		return 1
	elif len == 0:
		break
EXPECTED:
PRIVATE=

int main (int argc, char * argv[]) {
	int result = 0;
	/*
	 * process the command line options
	 */
	if (test_options_get (argc, argv) != 0) {
		print_usage ();
		return 1;
		}
	else if (len == 0) {
		break;
		}
	}


FORWARD DECLARATIONS=
static int main (int argc, char * argv[]);
	"""

@unittest
def testUnmatchedSingleQuote():
	"""
	if line_of_code.count("'") %2: // unmatched single quote
		printf
EXPECTED:
PRIVATE=

if (line_of_code.count("'") %2) { // unmatched single quote
	printf;
	}
	"""

@unittest
def testWithinParentheses():
	"""
result = pthread_create (&sxdio_dma_rx_thread_id,
	NULL,
	sxdio_dma_rx_thread,
	NULL)
EXPECTED:
PRIVATE=

result = pthread_create (&sxdio_dma_rx_thread_id,
	NULL,
	sxdio_dma_rx_thread,
	NULL);

"""

@unittest
def testGotoLabel(debug=False):
	"""
while true:
	printf
label:
code
if a:
	goto label
EXPECTED:
PRIVATE=

while (true) {
	printf;
	}
label:
code;
if (a) {
	goto label;
	}
	"""


@unittest
def testSwitchStatement():# works if AFTER THE 'case', you use SPACES iso TABS !!!
	"""
switch opt:
	case 'h':
	  print_usage ()
	  exit (0)
	  break
	default:
	  fprintf stderr, "Error processing command line options\n"
	  bad_args = 1
	  break
EXPECTED:
PRIVATE=

switch (opt) {
	case 'h':
	  print_usage ();
	  exit (0);
	  break;
	default:
	  fprintf (stderr, "Error processing command line options\n");
	  bad_args = 1;
	  break;
	}
"""

@unittest
def testMultilineCommentAfterAfunction():
	"""void test_buf_free (void):
	for i = 0; i < test_n_bufs; ++i:
		if pbuf != 0:
			PDEBUG ("freeing buf: %p\\n", pbuf)
			free (pbuf)
/*
 * test_options_get - get user options from the command line
 *
 */
EXPECTED:
PRIVATE=
void test_buf_free (void) {
	for (i = 0; i < test_n_bufs; ++i) {
		if (pbuf != 0) {
			PDEBUG ("freeing buf: %p\\n", pbuf);
			free (pbuf);
			}
		}
	}
/*
 * test_options_get - get user options from the command line
 *
 */


FORWARD DECLARATIONS=
static void test_buf_free (void);
"""


@unittest
def test_standalone_public_function(DEBUG=False, FAILS=False):
	"""
public void test_getters_and_setters():
	pppp
typedef enum State =:
	QUEUESIZE = 10
	QUEUE = 11
uint8_t data[]=:
	0x0c,0x3b,0x02,0x96,0x71,0x11,0x00,0x4b // TIME CODE FIELD
	0xa0,0x00,0x03,0xff,0x85,0x5e,0x85,0x5e // FS STATUS FIELD
	0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff // RS STATUS FIELD
	0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff
	0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff
	0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff
Status *self = (Status*)data
public int a= 7
if a and b or c:
	if not dandornot:
		printf
EXPECTED:
PUBLIC=
void test_getters_and_setters();

extern int a;

PRIVATE=

void test_getters_and_setters() {
	pppp;
	}
typedef enum State = {
	QUEUESIZE = 10,
	QUEUE = 11,
	};
uint8_t data[]= {
	0x0c,0x3b,0x02,0x96,0x71,0x11,0x00,0x4b,// TIME CODE FIELD
	0xa0,0x00,0x03,0xff,0x85,0x5e,0x85,0x5e,// FS STATUS FIELD
	0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,// RS STATUS FIELD
	0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
	0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
	0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
	};
Status *this = (Status*)data;
int a= 7;
if (a  &&  b  ||  c) {
	if (!dandornot) {
		printf;
		}
	}


"""

@unittest
def testNestedStruct(): # BUG ; after struct def
	"""
struct Outer:
	struct Inner:        // Nested structure declaration
		int         a
		float       f
	in
	enum E:              // Nested enum type declaration
		UKNOWN
		OFF
		ON
	state
EXPECTED:
PRIVATE=

struct Outer {
	struct Inner { // Nested structure declaration
		int         a;
		float       f;
		};
	in;
	enum E { // Nested enum type declaration
		UKNOWN,
		OFF,
		ON,
		};
	state;
	}


FORWARD DECLARATIONS=
typedef struct Outer Outer; // opaque type
"""



@unittest
def test_multiline_params(DEBUG=False):
	"""
	void FRAMEBUFFER_init(FrameBuffer* self,
		uint32_t telemetry_channel,
		uint32_t sync_word_length,
		uint32_t tm_block_size):
		print Hello

EXPECTED:
PRIVATE=

void FRAMEBUFFER_init(FrameBuffer* this,
	uint32_t telemetry_channel,
	uint32_t sync_word_length,
	uint32_t tm_block_size) {
	fprintf (stderr, Hello);
	}


FORWARD DECLARATIONS=
static void FRAMEBUFFER_init(FrameBuffer* self,
	uint32_t telemetry_channel,
	uint32_t sync_word_length,
	uint32_t tm_block_size);
	"""

@unittest
def test_standalone_double_colon(DEBUG=False, FAILS=False):
	"""
	FrameBuffer* FRAMEBUFFER_new(
		uint32_t telemetry_channel,
		uint32_t sync_word_length,
		uint32_t tm_block_size,
		uint32_t number_tm_blocks
		):
		// this is a -style comment
		FrameBuffer* self= (FrameBuffer*)malloc(sizeof(FrameBuffer))
EXPECTED:
PRIVATE=

FrameBuffer* FRAMEBUFFER_new(
	uint32_t telemetry_channel,
	uint32_t sync_word_length,
	uint32_t tm_block_size,
	uint32_t number_tm_blocks
	) {
	// this is a -style comment
	FrameBuffer* this= (FrameBuffer*)malloc(sizeof(FrameBuffer));
	}


FORWARD DECLARATIONS=
static FrameBuffer* FRAMEBUFFER_new(
	uint32_t telemetry_channel,
	uint32_t sync_word_length,
	uint32_t tm_block_size,
	uint32_t number_tm_blocks
	);
	"""

@unittest
def test_return_struct(DEBUG=False, FAILS=False): # bug in fwd declarations
	"""
// MINOR BUG, this function returns a struct ==> get a ; at the end !!!
struct closure * foo(int x):
	struct closure * closure = (struct closure *)malloc(sizeof(struct closure))
	closure->x = x
	printf "x is %d\n",closure->x
	closure->call = &block
	return closure
EXPECTED:
PRIVATE=

// MINOR BUG, this function returns a struct ==> get a ; at the end !!!
struct closure * foo(int x) {
	struct closure * closure = (struct closure *)malloc(sizeof(struct closure));
	closure->x = x;
	printf ("x is %d\n",closure->x);
	closure->call = &block;
	return closure;
	};


FORWARD DECLARATIONS=
static struct closure * foo(int x);
	"""

@unittest
def test_var_initialisation0():
	"""
public bool Hash::zero_value_is_valid = true
public uint8_t arr[]= {1,2,3,4}
EXPECTED:
PUBLIC=
extern bool Hash_zero_value_is_valid;
extern uint8_t arr[];

PRIVATE=

bool Hash_zero_value_is_valid = true;
uint8_t arr[]= {1,2,3,4};
"""


@unittest
def test_var_initialisation(DEBUG=False, FAILS=False):
	"""
public int a= 7
if a and b or c:
	if not dandornot:
		printf
private uint32_t a_private_var
public int public
private long privatelong
public typedef int a
private void test_buf_free (void):
	for i = 0; i < test_n_bufs; ++i:
		if pbuf != 0:
			PDEBUG ("freeing buf: %p\n", pbuf)
			free (pbuf)
protected class tree_el:
	int val
	tree_el* right
	tree_el* left
	tree_el* insert(tree_el* self, int item):
		if not self:
			self.val=item
			self.left=new tree_el()
			self.right=new tree_el()
			return self
		if item < self.val:
			insert(self.left, item)
		else:
			insert(self.right, item)
		return self
EXPECTED:
PUBLIC=
typedef int a;
typedef struct tree_el tree_el;// opaque type
extern int a;
int public;
tree_el* tree_el_new();

void tree_el_free(tree_el* this);


PRIVATE=

int a= 7;
if (a  &&  b  ||  c) {
	if (!dandornot) {
		printf;
		}
	}
static uint32_t a_private_var;
static long privatelong;
static void test_buf_free (void) {
	for (i = 0; i < test_n_bufs; ++i) {
		if (pbuf != 0) {
			PDEBUG ("freeing buf: %p\n", pbuf);
			free (pbuf);
			}
		}
	}
struct tree_el {
	int val;
	tree_el* right;
	tree_el* left;
	};

tree_el* tree_el_new() {
	tree_el* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

void tree_el_free(tree_el* this) {
	free(this);
	}

tree_el* tree_el_insert(tree_el* this, int item) {
	if (!this) {
		this->val=item;
		this->left= tree_el_new();
		this->right= tree_el_new();
		return this;
		}
	if (item < this->val) {
		insert(this->left, item);
		}
	else {
		insert(this->right, item);
		}
	return this;
	}



FORWARD DECLARATIONS=
static void test_buf_free (void);
static tree_el* tree_el_insert(tree_el* self, int item);

	"""

@unittest
def test_nested_enums():
	"""
class Hello:
	enum:
		e=5
		f=9
	int x
	def __init__(self):
		self.x=888
EXPECTED:
PRIVATE=

struct Hello {
	enum {
		e=5,
		f=9,
		};
	int x;
	};

Hello* Hello_constructor(Hello* this) {
	this->x=888;
	return this;
	}
static Hello* Hello_new() {
	Hello* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Hello_constructor(this);
	}

static void Hello_free(Hello* this) {
	free(this);
	}




FORWARD DECLARATIONS=
typedef struct Hello Hello; // opaque type
static Hello* Hello_constructor(Hello* self);
static Hello* Hello_new();
static void Hello_free(Hello* self);

"""



@unittest
def test_linked_list(DEBUG=False, FAILS=False):
	"""
#include "../COMMON/utils.h"
#include "../OSAL/osal.h"
/*
 * this is a linked list implementation
 */
protected class list:
	void *val
	list *next
	def __init__(self, void* v):
		self.val=v
		self.next=NULL
	list* append(self, void *v):
		ni :=new list(v)
		if not self: // append to NULL = new
			return ni
		for list* curr = self; curr->next ; curr = curr->next:
			doit
		curr->next = ni
		return self
	list* delete(self,void* v):
		list* prev=NULL
		for list* curr = self; curr->next ; prev=curr, curr = curr->next:
			if curr->val==v: // we found it, let us delete it
				if prev:
					prev->next=curr->next
				else: // we deleted the only element !!!
					self=NULL
				break
		return self
	int foreach(self, int(*func)(void*,void*),void *args):
		for list* curr = self; curr->next ; curr = curr->next:
			(*func)(curr->val, args)
EXPECTED:
PUBLIC=
typedef struct list list;// opaque type
list* list_new(void* v);

void list_free(list* this);


PRIVATE=

/*
 * this is a linked list implementation
 */
struct list {
	void *val;
	list *next;
	};

list* list_constructor(list* this, void* v) {
	this->val=v;
	this->next=NULL;
	return this;
	}

list* list_new(void* v) {
	list* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return list_constructor(this, v);
	}

void list_free(list* this) {
	free(this);
	}

list* list_append(list* this, void *v) {
	list* ni = list_new(v);
	if (!this) { // append to NULL = new
		return ni;
		}
	for (list* curr = this; curr->next ; curr = curr->next) {
		doit;
		}
	curr->next = ni;
	return this;
	}
list* list_delete(list* this,void* v) {
	list* prev=NULL;
	for (list* curr = this; curr->next ; prev=curr, curr = curr->next) {
		if (curr->val==v) { // we found it, let us delete it
			if (prev) {
				prev->next=curr->next;
				}
			else { // we deleted the only element !!!
				this=NULL;
				}
			break;
			}
		}
	return this;
	}
int list_foreach(list* this, int(*func)(void*,void*),void *args) {
	for (list* curr = this; curr->next ; curr = curr->next) {
		(*func)(curr->val, args);
		}
	}



FORWARD DECLARATIONS=
static list* list_constructor(list* self, void* v);
static list* list_append(list* self, void *v);
static list* list_delete(list* self,void* v);
static int list_foreach(list* self, int(*func)(void*,void*),void *args);
IMPORTED MODULES
#include "../COMMON/utils.h"
#include "../OSAL/osal.h"

"""

@unittest
def test_function_pointer_decl():
	"""
public typedef void (*free_func_t)(v_elem_t) // THIS IS THE CULPRIT !!!!
public class Vector:
	v_elem_t* elems
	size_t num_elems
EXPECTED:
PUBLIC=
typedef void (*free_func_t)(v_elem_t);// THIS IS THE CULPRIT !!!!
typedef struct Vector Vector;
struct Vector {
	v_elem_t* elems;
	size_t num_elems;
	};
Vector* Vector_new();

void Vector_free(Vector* this);


PRIVATE=


Vector* Vector_new() {
	Vector* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

void Vector_free(Vector* this) {
	free(this);
	}
"""

@unittest
def test_new_keyword():
	'''
obj1:=new  Object1(params)
obj2:= new  Object2(params)
obj3:=new Object1(.a=10,.b=77)
for a1 := new int[12];a1;a1++:
	printttt
for f :=new int[12];f;f++:
	printttt
for f:=new FileChecker(G.cadu_filename,G.input_filename ); f; FileChecker::free(f),f=NULL:
	FileChecker::check(f)
fileobj :=new FileObject
intpointer := new int
EXPECTED:
PRIVATE=

Object1* obj1=  Object1_new(params);
Object2* obj2=   Object2_new(params);
Object1* obj3= D_NEW( Object1,.a=10,.b=77);
for (int* a1 = calloc(12,sizeof(int));a1;a1++) {
	printttt;
	}
for (int* f =calloc(12,sizeof(int));f;f++) {
	printttt;
	}
for (FileChecker* f= FileChecker_new(G.cadu_filename,G.input_filename ); f; FileChecker_free(f),f=NULL) {
	FileChecker_check(f);
	}
FileObject* fileobj =malloc(sizeof(*fileobj));
int* intpointer = malloc(sizeof(*intpointer));
'''
@unittest
def test_hhhhhhhh():
	"""
result = pthread_create (&sxdio_dma_rx_thread_id,
	NULL,
	sxdio_dma_rx_thread,
	NULL)
EXPECTED:
PRIVATE=

result = pthread_create (&sxdio_dma_rx_thread_id,
	NULL,
	sxdio_dma_rx_thread,
	NULL);
"""

@unittest
def test_static_init():
	"""
class Hello:
	int x = 8
	int y
	char* z="hello"
	volatile bool write_to_socket= false
	def __init__(self,my):
		self.y=y
// we have a bug here, the second 'and' is not replaced
if not self.raw_mode and not tmreq:
	print
EXPECTED:
PRIVATE=

struct Hello {
	int x;
	int y;
	char* z;
	volatile bool write_to_socket;
	};

Hello* Hello_constructor(Hello* this,my) {
	this->x= 8;
	strcpy(this->z,"hello");
	this->write_to_socket= false;
	this->y=y;
	return this;
	}
static Hello* Hello_new(my) {
	Hello* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Hello_constructor(this, my);
	}

static void Hello_free(Hello* this) {
	free(this);
	}


// we have a bug here, the second 'and' is not replaced
if (!this->raw_mode  &&  !tmreq) {
	fprintf (stderr,);
	}


FORWARD DECLARATIONS=
typedef struct Hello Hello; // opaque type
static Hello* Hello_constructor(Hello* self,my);
static Hello* Hello_new(my);
static void Hello_free(Hello* self);
"""

@unittest
def test_assert222():
	"""
assert ((uint8_t*)dma_buff)[i]==0x45
EXPECTED:
PRIVATE=

assert (((uint8_t*)dma_buff)[i]==0x45);
"""

@unittest
def test_static_class_member_init():
	"""
class Hello:
	int x
	public static int public_count=888
	private static int private_count=999
	static int c=8
EXPECTED:
PUBLIC=
extern int Hello_public_count;

PRIVATE=

struct Hello {
	int x;
	};

int Hello_public_count=888;
static Hello* Hello_new() {
	Hello* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

static void Hello_free(Hello* this) {
	free(this);
	}



FORWARD DECLARATIONS=
typedef struct Hello Hello; // opaque type
static int Hello_private_count=999;
int Hello_c=8;
static Hello* Hello_new();
static void Hello_free(Hello* self);
"""

@unittest
def test_static_class_member_init2():
	"""
public class Preamble:
	uint32_t version
	public static uint32_t size= sizeof(Preamble) // =76
EXPECTED:
PUBLIC=
typedef struct Preamble Preamble;
struct Preamble {
	uint32_t version;
	};
extern uint32_t Preamble_size;// =76
Preamble* Preamble_new();

void Preamble_free(Preamble* this);


PRIVATE=


uint32_t Preamble_size= sizeof(Preamble);// =76
Preamble* Preamble_new() {
	Preamble* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return this;
	}

void Preamble_free(Preamble* this) {
	free(this);
	}
"""

@unittest
def test_new_keyword2():
	"""
public struct timeval get_time(void):
	struct timeval now
	gettimeofday(&now,NULL)
	return now
struct closure * foo(int x):
	closure := new struct closure
	a:= new struct {int x;int y;}
	closure->x = x
	printf "x is %d\n",closure->x
	closure->call = &block
	return closure
EXPECTED:
PUBLIC=
struct timeval get_time(void);


PRIVATE=

struct timeval get_time(void) {
	struct timeval now;
	gettimeofday(&now,NULL);
	return now;
	};
struct closure * foo(int x) {
	 struct closure* closure = malloc(sizeof(*closure));
	 struct {int x;int y;}* a= malloc(sizeof(*a));
	closure->x = x;
	printf ("x is %d\n",closure->x);
	closure->call = &block;
	return closure;
	};


FORWARD DECLARATIONS=
static struct closure * foo(int x);
"""

@unittest
def test_class_111111111():
	"""
class Preamble:
	int x
	int y
	def __init__(self, int x, int y):
		self.x=x
		self.y=y
		self.move(3,9)
	def __del__(self):
		free(self)
	void move(self, int dx,int dy):
		int d
		self.x += dx
EXPECTED:
PRIVATE=

struct Preamble {
	int x;
	int y;
	};

Preamble* Preamble_constructor(Preamble* this, int x, int y) {
	this->x=x;
	this->y=y;
	Preamble_move(this,3,9);
	return this;
	}

static Preamble* Preamble_new(int x, int y) {
	Preamble* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Preamble_constructor(this, x, y);
	}

static void Preamble_free(Preamble* this) {
	Preamble_destructor(this);
	free(this);
	}

void Preamble_destructor(Preamble* this) {
	free(this);
	}
void Preamble_move(Preamble* this, int dx,int dy) {
	int d;
	this->x += dx;
	}



FORWARD DECLARATIONS=
typedef struct Preamble Preamble; // opaque type
static Preamble* Preamble_constructor(Preamble* self, int x, int y);
static Preamble* Preamble_new(int x, int y);
static void Preamble_free(Preamble* self);
static void Preamble_destructor(Preamble* self);
static void Preamble_move(Preamble* self, int dx,int dy);
"""

@unittest
def test_foreach_construct1():
	"""
class Count:
	int step
	int count
	def __init__(self, int start, int step):
		self.step=step
		self.count=start
	int next(self):
		while true:
			yield self.count
			self.count += self.step
			yield None
			if self.count>10:
				return 0
int main():
	mycount:= new Count(2,5)
	for int res in mycount:
		print "+++=%d\n",res
	delete mycount
EXPECTED:
PRIVATE=

struct Count {
	int _state;
	bool _exhausted;
	bool _valid_output;
	int step;
	int count;
	};

Count* Count_constructor(Count* this, int start, int step) {
	this->_state=0;
	this->_exhausted=false;
	this->_valid_output=true;
	this->step=step;
	this->count=start;
	return this;
	}

static Count* Count_new(int start, int step) {
	Count* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Count_constructor(this, start, step);
	}

static void Count_free(Count* this) {
	free(this);
	}

int Count_next(Count* this) {
	switch (this->_state) {
		case 0: goto LABEL0;
		case 1: goto LABEL1;
		case 2: goto LABEL2;
		}
	LABEL0: //start of generator;
	while (true) {
		//start of yield #1
		this->_state=1;
		this->_valid_output=true;
		return this->count;
		LABEL1:;
		//end of yield #1

		this->count += this->step;
		//start of yield #2
		this->_state=2;
		this->_valid_output=false;
		return NULL;
		LABEL2:;
		//end of yield #2

		if (this->count>10) {
			this->_valid_output=false;
			this->_exhausted=true;
			return 0;
			}
		}
	}

STATIC int main() {
	Count* mycount=  Count_new(2,5);
	while (true)  {
		int res =Count_next(mycount); if (mycount->_exhausted) break;
		fprintf (stderr, "+++=%d\n",res);
		}
	Count_free(mycount);
	}


FORWARD DECLARATIONS=
typedef struct Count Count; // opaque type
static Count* Count_constructor(Count* self, int start, int step);
static Count* Count_new(int start, int step);
static void Count_free(Count* self);
static int Count_next(Count* self);

"""
@unittest
def test_class_derived_class():
	"""
class Hello:
	int a
	int b
	float ff=999.999
	char* name= "hello"
	public static int my_class_variable = 990  // class variable, notice the initialisation!!!
	private static int my_private_class_variable = 999  // notice the initialisation!!!
	def __init__(self,int arg1, int arg2):
		self.a = arg1
		self.b = arg2
	@virtual
	public void process_msg(self, char* msg):
		print "Hello is processing message!\n"
	public void printme(self):
		self.process_msg()
		print "a=%d, b=%d\n", self.a, self.b
	public void meth_inher(self):
		print "meth inher a=%d, b=%d\n", self.a, self.b
class DerivedHello(Hello):
	int c
	int d
	def __init__(self,int arg1, int arg2,int arg3, int arg4):
		super.__init__(self,arg1,arg2)
		self.c = arg3
		self.d = arg4
	@override
	public void process_msg(self):
		print "DerivedHello is processing message!\n"
	public void printme(self):
		Hello::printme(self)
		print "c=%d, d=%d\n", self.c, self.d
int main():
	my:= new Hello(777)
	my->printme()
	my->meth_inher()
	my->process_msg()
	my2:= new DerivedHello(1777,1888, 1999, 2000)
	my2->printme()
	my2->process_msg()
	my2->meth_inher()
	Hello::my_class_variable++
	Hello::my_private_class_variable++
	print "This is a class variable %d\n", Hello::my_class_variable
	print "This is a private class variable %d\n", Hello::my_private_class_variable
	delete my
	delete my2
EXPECTED:
PUBLIC=
extern int Hello_my_class_variable;// class variable, notice the initialisation!!!
void Hello_process_msg(Hello* this, char* msg);

void Hello_printme(Hello* this);

void Hello_meth_inher(Hello* this);

void DerivedHello_process_msg(DerivedHello* this);

void DerivedHello_printme(DerivedHello* this);


PRIVATE=

struct Hello {
	int a;
	int b;
	float ff;
	char* name;
	void (*process_msg)(Hello* this, char* msg);// virtual method
	};

Hello* Hello_constructor(Hello* this,int arg1, int arg2) {
	this->ff=999.999;
	strcpy(this->name, "hello");
	this->a = arg1;
	this->b = arg2;
	this->process_msg=Hello_process_msg;// virtual method
	return this;
	}

int Hello_my_class_variable = 990;// class variable, notice the initialisation!!!
static Hello* Hello_new(int arg1, int arg2) {
	Hello* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Hello_constructor(this, arg1, arg2);
	}

static void Hello_free(Hello* this) {
	free(this);
	}

void Hello_process_msg(Hello* this, char* msg) {
	fprintf (stderr, "Hello is processing message!\n");
	}
void Hello_printme(Hello* this) {
	this->process_msg(this);
	fprintf (stderr, "a=%d, b=%d\n", this->a, this->b);
	}
void Hello_meth_inher(Hello* this) {
	fprintf (stderr, "meth inher a=%d, b=%d\n", this->a, this->b);
	}

struct DerivedHello {
	Hello;
	int c;
	int d;
	};

DerivedHello* DerivedHello_constructor(DerivedHello* this,int arg1, int arg2,int arg3, int arg4) {
	Hello_constructor((Hello*)this,arg1,arg2);
	this->c = arg3;
	this->d = arg4;
	this->process_msg=DerivedHello_process_msg;// virtual method
	return this;
	}

static DerivedHello* DerivedHello_new(int arg1, int arg2,int arg3, int arg4) {
	DerivedHello* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return DerivedHello_constructor(this, arg1, arg2, arg3, arg4);
	}

static void DerivedHello_free(DerivedHello* this) {
	Hello_free(this);
	}

void DerivedHello_process_msg(DerivedHello* this) {
	fprintf (stderr, "DerivedHello is processing message!\n");
	}
void DerivedHello_printme(DerivedHello* this) {
	Hello_printme(this);
	fprintf (stderr, "c=%d, d=%d\n", this->c, this->d);
	}

STATIC int main() {
	Hello* my=  Hello_new(777);
	Hello_printme(my);
	Hello_meth_inher(my);
	my->process_msg(my);
	DerivedHello* my2=  DerivedHello_new(1777,1888, 1999, 2000);
	DerivedHello_printme(my2);
	my2->process_msg(my2);
	Hello_meth_inher((Hello*)my2);
	Hello_my_class_variable++;
	Hello_my_private_class_variable++;
	fprintf (stderr, "This is a class variable %d\n", Hello_my_class_variable);
	fprintf (stderr, "This is a private class variable %d\n", Hello_my_private_class_variable);
	Hello_free(my);
	DerivedHello_free(my2);
	}


FORWARD DECLARATIONS=
typedef struct Hello Hello; // opaque type
typedef struct DerivedHello DerivedHello; // opaque type
static Hello* Hello_constructor(Hello* self,int arg1, int arg2);
static int Hello_my_private_class_variable = 999  ;
static Hello* Hello_new(int arg1, int arg2);
static void Hello_free(Hello* self);
static DerivedHello* DerivedHello_constructor(DerivedHello* self,int arg1, int arg2,int arg3, int arg4);
static DerivedHello* DerivedHello_new(int arg1, int arg2,int arg3, int arg4);
static void DerivedHello_free(DerivedHello* self);

"""
@unittest
def test_new_delete():
	"""
int main():
	my:= new Hello(777,888)
	my->printme()
	my2:= new DerivedHello(1777,1888, 1999, 2000)
	my2->printme()
	a:=new int[100]
	delete my
	delete my2
	delete a
	return 0
EXPECTED:
PRIVATE=

STATIC int main() {
	Hello* my=  Hello_new(777,888);
	Hello_printme(my);
	DerivedHello* my2=  DerivedHello_new(1777,1888, 1999, 2000);
	DerivedHello_printme(my2);
	int* a=calloc(100,sizeof(int));
	Hello_free(my);
	DerivedHello_free(my2);
	free(a);
	return 0;
	}

"""

@unittest
def test_methods_default_parameters():
	"""
class FFFF:
	int x
	def __init__(self, int first, float second=8.8):
		self.x=first
		print "second=%f\n",second
	void cpp_function(self, float p2=444.333, const char* s="dddddd"):
		print "params: %f %s\n", p2,  s

def main():
	f := new FFFF(3)
	f->cpp_function()
	f->cpp_function(787.4545)
	f->cpp_function(999.55, "hello world")
	delete f
EXPECTED:
PRIVATE=

struct FFFF {
	int x;
	};

FFFF* FFFF_constructor(FFFF* this, int first, float second) {
	this->x=first;
	fprintf (stderr, "second=%f\n",second);
	return this;
	}

static FFFF* FFFF_new(int first, float second) {
	FFFF* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return FFFF_constructor(this, first, second);
	}

static void FFFF_free(FFFF* this) {
	free(this);
	}

void FFFF_cpp_function(FFFF* this, float p2, const char* s) {
	fprintf (stderr, "params: %f %s\n", p2,  s);
	}


STATIC int main() {
	FFFF* f =  FFFF_new(3);
	FFFF_cpp_function(f);
	FFFF_cpp_function(f,787.4545);
	FFFF_cpp_function(f,999.55, "hello world");
	FFFF_free(f);
	}


FORWARD DECLARATIONS=
typedef struct FFFF FFFF; // opaque type
#ifndef OVERLOADED_MACROS_DEFINED
#define OVERLOADED_MACROS_DEFINED
#define MKFN(fn,...) MKFN_N(fn,##__VA_ARGS__,9,8,7,6,5,4,3,2,1,0)(__VA_ARGS__)
#define MKFN_N(fn,n0,n1,n2,n3,n4,n5,n6,n7,n8,n,...) fn##n
#endif

static FFFF* FFFF_constructor(FFFF* self, int first, float second);
static FFFF* FFFF_new(int first, float second);

/********* start of declarations for overloaded function *****/
#define FFFF_new2( A,B ) FFFF_new( A, B  )
#define FFFF_new1( A ) FFFF_new( A , 8.8 )
#define FFFF_new(...) MKFN(FFFF_new,##__VA_ARGS__)
/*********  end of declarations for overloaded function *****/


static void FFFF_free(FFFF* self);
static void FFFF_cpp_function(FFFF* self, float p2, const char* s);

/********* start of declarations for overloaded function *****/
#define FFFF_cpp_function3( A,B,C ) FFFF_cpp_function( A, B, C  )
#define FFFF_cpp_function2( A,B ) FFFF_cpp_function( A, B , "dddddd" )
#define FFFF_cpp_function1( A ) FFFF_cpp_function( A , 444.333, "dddddd" )
#define FFFF_cpp_function(...) MKFN(FFFF_cpp_function,##__VA_ARGS__)
/*********  end of declarations for overloaded function *****/



"""

@unittest
def test_rrrrrrrty():
	"""
public struct AS_status: // only valid for little-endian!
	uint8_t reserved[5]     // bytes 0 to 4
EXPECTED:
PUBLIC=
typedef struct AS_status AS_status;
struct AS_status { // only valid for little-endian!
	uint8_t reserved[5];// bytes 0 to 4
	};

PRIVATE=
"""

@unittest
def test_namespace222():
	"""
// no initialiser within nested namespace
namespace KKKKK:
	char cadu_filename[256]= "ccsds1204"
	char input_filename[256]= ""
	namespace nested:
		int x
		int y
EXPECTED:
PRIVATE=

// no initialiser within nested namespace
struct KKKKK {
	char cadu_filename[256];
	char input_filename[256];
	struct nested {
		int x;
		int y;
		};
	}
KKKKK= {
	.cadu_filename= "ccsds1204",
	.input_filename= "",
		{ // NAMESPACE  nested,
		},
	};


FORWARD DECLARATIONS=
typedef struct KKKKK KKKKK; // opaque type
"""

@unittest
def test_namespace333():
	"""
namespace KKKKK:
	char cadu_filename[256]= "ccsds1204"
	char input_filename[256]= ""
	namespace nested:
		int x=8
		int y
EXPECTED:
PRIVATE=

struct KKKKK {
	char cadu_filename[256];
	char input_filename[256];
	struct nested {
		int x;
		int y;
		};
	}
KKKKK= {
	.cadu_filename= "ccsds1204",
	.input_filename= "",
		{ // NAMESPACE  nested,
		.x=8,
		},
	};


FORWARD DECLARATIONS=
typedef struct KKKKK KKKKK; // opaque type

"""

@unittest
def test_default_arguments_public():
	"""
public void myfunction(self, int w, int x=111,int y=444, int z=888):
	int a
	int b
EXPECTED:
PUBLIC=
void myfunction(this, int w, int x,int y, int z);


PRIVATE=

#ifndef OVERLOADED_MACROS_DEFINED
#define OVERLOADED_MACROS_DEFINED
#define MKFN(fn,...) MKFN_N(fn,##__VA_ARGS__,9,8,7,6,5,4,3,2,1,0)(__VA_ARGS__)
#define MKFN_N(fn,n0,n1,n2,n3,n4,n5,n6,n7,n8,n,...) fn##n
#endif


/********* start of declarations for overloaded function *****/;
#define myfunction5( A,B,C,D,E ) myfunction( A, B, C, D, E  )
#define myfunction4( A,B,C,D ) myfunction( A, B, C, D , 888 )
#define myfunction3( A,B,C ) myfunction( A, B, C , 444, 888 )
#define myfunction2( A,B ) myfunction( A, B , 111, 444, 888 )
#define myfunction(...) MKFN(myfunction,##__VA_ARGS__)
/*********  end of declarations for overloaded function *****/;


void myfunction(this, int w, int x,int y, int z) {
	int a;
	int b;
	}

"""

@unittest
def test_default_arguments_private():
	"""
private void myfunction(self, int w, int x=111,int y=444, int z=888):
	int a
	int b
EXPECTED:
PRIVATE=

static void myfunction(this, int w, int x,int y, int z) {
	int a;
	int b;
	}


FORWARD DECLARATIONS=
#ifndef OVERLOADED_MACROS_DEFINED
#define OVERLOADED_MACROS_DEFINED
#define MKFN(fn,...) MKFN_N(fn,##__VA_ARGS__,9,8,7,6,5,4,3,2,1,0)(__VA_ARGS__)
#define MKFN_N(fn,n0,n1,n2,n3,n4,n5,n6,n7,n8,n,...) fn##n
#endif

static void myfunction(self, int w, int x,int y, int z);

/********* start of declarations for overloaded function *****/
#define myfunction5( A,B,C,D,E ) myfunction( A, B, C, D, E  )
#define myfunction4( A,B,C,D ) myfunction( A, B, C, D , 888 )
#define myfunction3( A,B,C ) myfunction( A, B, C , 444, 888 )
#define myfunction2( A,B ) myfunction( A, B , 111, 444, 888 )
#define myfunction(...) MKFN(myfunction,##__VA_ARGS__)
/*********  end of declarations for overloaded function *****/

"""

@unittest
def test_dssssssssss():
	"""
class CurriedFunction:
	void (*f)()
	int a
	def __init__(self,void (*f)(), int *x, int *y):
		unsigned char myArgListArray[48]
		tokens[i]= new char[len]
EXPECTED:
PRIVATE=

struct CurriedFunction {
	void (*f)();
	int a;
	};

CurriedFunction* CurriedFunction_constructor(CurriedFunction* this,void (*f)(), int *x, int *y) {
	unsigned char myArgListArray[48];
	tokens[i]= calloc(len,sizeof(char));
	return this;
	}
static CurriedFunction* CurriedFunction_new(void (*f)(), int *x, int *y) {
	CurriedFunction* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return CurriedFunction_constructor(this,f, x, y);
	}

static void CurriedFunction_free(CurriedFunction* this) {
	free(this);
	}




FORWARD DECLARATIONS=
typedef struct CurriedFunction CurriedFunction; // opaque type
static CurriedFunction* CurriedFunction_constructor(CurriedFunction* self,void (*f)(), int *x, int *y);
static CurriedFunction* CurriedFunction_new(void (*f)(), int *x, int *y);
static void CurriedFunction_free(CurriedFunction* self);
"""

@unittest
def test_improved_switch():
	"""
switch a:
	case 5::
		doit
		break
	case 6::
		dont
		break
	default::
		doit
EXPECTED:
PRIVATE=

switch (a) {
	case 5:  {
		doit;
		break;
		}
	case 6:  {
		dont;
		break;
		}
	default:  {
		doit;
		}
	}
"""

@unittest
def test_new_initialised():
	"""
myobj := new Obj = {.a=1,.b=5}
myobj := new float = 5.555
q:= new int[a][b]
EXPECTED:
PRIVATE=

Obj* myobj = malloc(sizeof(*myobj))  ; *myobj=(Obj) {.a=1,.b=5};
float* myobj = malloc(sizeof(*myobj))  ; *myobj=(float) 5.555;
int* q_p= calloc(a*b,sizeof(int));
int (*q)[b]=(int(*)[b])q_p;

"""


@unittest
def test_fun_pointers_arguments():
	"""
public class TCP_Server:
	uint16_t port_number
	int server_socket_fd
	def __init__(self, int port_number, void (*serve_client)(int), void (*sig_handler)(int)):
		pass
EXPECTED:
PUBLIC=
typedef struct TCP_Server TCP_Server;
struct TCP_Server {
	uint16_t port_number;
	int server_socket_fd;
	};
TCP_Server* TCP_Server_new(int port_number, void (*serve_client)(int), void (*sig_handler)(int));

void TCP_Server_free(TCP_Server* this);


PRIVATE=


TCP_Server* TCP_Server_constructor(TCP_Server* this, int port_number, void (*serve_client)(int), void (*sig_handler)(int)) {
	// empty statement !!!;
	return this;
	}
TCP_Server* TCP_Server_new(int port_number, void (*serve_client)(int), void (*sig_handler)(int)) {
	TCP_Server* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return TCP_Server_constructor(this, port_number,serve_client,sig_handler);
	}

void TCP_Server_free(TCP_Server* this) {
	free(this);
	}




FORWARD DECLARATIONS=
static TCP_Server* TCP_Server_constructor(TCP_Server* self, int port_number, void (*serve_client)(int), void (*sig_handler)(int));

"""
@unittest
def test_docstrings():
	"""
public bool Hash::zero_value_is_valid = true
public uint8_t arr[]= {1,2,3,4}
public typedef void* elem_t
int func(in x,
		int y):
	''' this is a doc string
	this is the second line of a doc string
	this is the third line of a doc string
	'''
	statements
int func2(in x,int y):
	''' this is a doc string
	'''
	statements2
EXPECTED:
PUBLIC=
typedef void* elem_t;
extern bool Hash_zero_value_is_valid;
extern uint8_t arr[];

PRIVATE=

bool Hash_zero_value_is_valid = true;
uint8_t arr[]= {1,2,3,4};
/* this is a doc string */
/* this is the second line of a doc string */
/* this is the third line of a doc string */
int func(in x,
		int y) {
	statements;
	}
/* this is a doc string */
int func2(in x,int y) {
	statements2;
	}


FORWARD DECLARATIONS=
static int func(in x,
		int y);
static int func2(in x,int y);
"""

@unittest
def test_scope_bug():
	"""
def main():
	if parent.pri <= newitem.pri:
		break
	h:= new Heap(10)  // SCOPE BUG AFTER THE BREAK, fixed !!!!
	for int i=0;i<10;i++:
		print "%d==elem=%d\n",i,*(int *)h->pop()
EXPECTED:
PRIVATE=

STATIC int main() {
	if (parent.pri <= newitem.pri) {
		break;
		}
	Heap* h=  Heap_new(10);// SCOPE BUG AFTER THE BREAK, fixed !!!!
	for (int i=0;i<10;i++) {
		fprintf (stderr, "%d==elem=%d\n",i,*(int *)Heap_pop(h));
		}
	}
"""

@unittest
def test_threaded_decorator():
	"""
@threaded
void worker(Queue* q):
	while true:
		int item = Queue::get(q)
		int item = q->get()
		print "Got item %d\n",item
		Queue::task_done(q)
		q->task_done()
EXPECTED:
PRIVATE=

void worker(Queue* q) {
	while (true) {
		int item = Queue_get(q);
		int item = Queue_get(q);
		fprintf (stderr, "Got item %d\n",item);
		Queue_task_done(q);
		Queue_task_done(q);
		}
	}


FORWARD DECLARATIONS=
#include "cxx_thread.h"
static void worker(Queue* q);
#define worker(...)  Thread_new(worker,__VA_ARGS__)
"""
@unittest
def test_delegate_objects():
	"""
def direction():
	int a = 1

class Map:
	Snake* snake=NULL
	Snake2* snake2
	def __init__(self):
		pass
	def __del__(self):
		delete self.snake
	int draw(self):
		self.snake->containsPoint(x,y)
		self.snake2->containsPoint(x,y)
EXPECTED:
PRIVATE=

def direction() {
	int a = 1;
	}

struct Map {
	Snake* snake;
	Snake2* snake2;
	};

Map* Map_constructor(Map* this) {
	this->snake=NULL;
	// empty statement !!!;
	return this;
	}

static Map* Map_new() {
	Map* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Map_constructor(this);
	}

static void Map_free(Map* this) {
	Map_destructor(this);
	free(this);
	}

void Map_destructor(Map* this) {
	Snake_free(this->snake);
	}
int Map_draw(Map* this) {
	Snake_containsPoint(this->snake,x,y);
	Snake2_containsPoint(this->snake2,x,y);
	}



FORWARD DECLARATIONS=
typedef struct Map Map; // opaque type
static def direction();
static Map* Map_constructor(Map* self);
static Map* Map_new();
static void Map_free(Map* self);
static void Map_destructor(Map* self);
static int Map_draw(Map* self);

"""
@unittest
def test_cosmetic_empty_lines():
	"""
int func2(in x,int y):
	''' this is a doc string
	'''
	statements2

	statement3
EXPECTED:
PRIVATE=

/* this is a doc string */
int func2(in x,int y) {
	statements2;

	statement3;
	}


FORWARD DECLARATIONS=
static int func2(in x,int y);
"""
@unittest
def test_raii():
	"""
volatile fp:= new File()
volatile fp:= new double
volatile myobj := new Obj = {.a=1,.b=5}
volatile myobj := new float = 5.555
volatile x
if self.coords[0].x <= MAP_HEIGHT/2 and self.coords[0].y <= MAP_HEIGHT/2:
	print
volatile a :=new int[ROWS][COLS]
EXPECTED:
PRIVATE=

File* fp __attribute__((cleanup(free_File)))=  File_new();
double* fp __attribute__((cleanup(free_double)))= malloc(sizeof(*fp));
Obj* myobj  __attribute__((cleanup(free_Obj)))= malloc(sizeof(*myobj))  ; *myobj=(Obj) {.a=1,.b=5};
float* myobj  __attribute__((cleanup(free_float)))= malloc(sizeof(*myobj))  ; *myobj=(float) 5.555;
volatile x;
if (this->coords[0].x <= MAP_HEIGHT/2  &&  this->coords[0].y <= MAP_HEIGHT/2) {
	fprintf (stderr,);
	}
int* a_p  __attribute__((cleanup(free_int)))=calloc(ROWS*COLS,sizeof(int));
int (*a)[COLS]=(int(*)[COLS])a_p;


INLINE FUNCTIONS=
static inline void free_File(File **fp) { if (*fp) File_free(*fp); }
static inline void free_double(double **fp) { if (*fp) free(*fp); }
static inline void free_Obj(Obj **fp) { if (*fp) Obj_free(*fp); }
static inline void free_float(float **fp) { if (*fp) free(*fp); }
static inline void free_int(int **fp) { if (*fp) free(*fp); }

"""

@unittest
def test_constructor_on_several_lines():
	"""
class Parent:
	int x
	int y
	def __init__(self, int x,
		int y):
		print "x=",d
	def move(self):
		pass
EXPECTED:
PRIVATE=

struct Parent {
	int x;
	int y;
	};

Parent* Parent_constructor(Parent* this, int x,
		int y) {
	fprintf (stderr, "x=",d);
	return this;
	}

static Parent* Parent_new(int x,
		int y) {
	Parent* this= malloc(sizeof(*this));
	if (!this) {
		return NULL;
		}
	return Parent_constructor(this, x, y);
	}

static void Parent_free(Parent* this) {
	free(this);
	}

void Parent_move(Parent* this) {
	// empty statement !!!;
	}



FORWARD DECLARATIONS=
typedef struct Parent Parent; // opaque type
static Parent* Parent_constructor(Parent* self, int x,
		int y);
static Parent* Parent_new(int x,
		int y);
static void Parent_free(Parent* self);
static void Parent_move(Parent* self);

"""
@unittest
def test_hhhhjjj():
	"""
int main():
	mycount= new Count(2,5)
	for int res in mycount:
		print "+++=%d\n",res
	delete mycount
uint32_t rotl32c (uint32_t x, uint32_t n):
	assert (n<32)
	return (x<<n) | (x>>(-n&31))
EXPECTED:
PRIVATE=

STATIC int main() {
	mycount=  Count_new(2,5);
	while (true)  {
		int res =Count_next(mycount); if (mycount->_exhausted) break;
		fprintf (stderr, "+++=%d\n",res);
		}
	Count_free(mycount);
	}
uint32_t rotl32c (uint32_t x, uint32_t n) {
	assert (n<32);
	return (x<<n) | (x>>(-n&31));
	}


FORWARD DECLARATIONS=
static uint32_t rotl32c (uint32_t x, uint32_t n);
"""

#@unittest
def test_hhhhhhhhhhh():
	"""
class ClassName:
	def __init__(self, int arg):
		self.arg = arg
	// BUG:problem with space after the :
	@virtual
	private void timeout_cb(self):
		print "Please override this function:Reactor::timeout_cb\n"
	@virtual
	private void teardown(self):
		print "Please override this function:Reactor::teardown\n"
EXPECTED:
hyyyyuiii
"""
@unittest
def test_frfrr():
	'''
int function():
	if parent.pri <= newitem.pri:
		break
	h:= new Heap(10)
	for int i=0;i<10;i++:
		print "%d==elem=%d\n",i,*(int *)h->pop()
	myreactor:= new MyReactor(argv[1],10000)
	a := new File(argv[0])
EXPECTED:
PRIVATE=

int function() {
	if (parent.pri <= newitem.pri) {
		break;
		}
	Heap* h=  Heap_new(10);
	for (int i=0;i<10;i++) {
		fprintf (stderr, "%d==elem=%d\n",i,*(int *)Heap_pop(h));
		}
	MyReactor* myreactor=  MyReactor_new(argv[1],10000);
	File* a =  File_new(argv[0]);
	}


FORWARD DECLARATIONS=
static int function();
'''
#@unittest
def test_hhhhhhhhhhh():
	"""
if (a>b or (c==0 and d==255)):
	//if (current_slot_time>requested_slot_time or (current_fr_id==0 and fr_id==255)):
	print
EXPECTED:
hyyyyuiii
"""
@unittest
def test_multiple_returnBUGGY():
	"""
myobj := new Obj = {.a=1,.b=5}
myobj := new float = 5.555
def fun():
	// bug, size is missing in the memcpy
	res := new int[2]={max_length, longest}
	return new int[2]={max_length, longest}
	return new Obj = {.a=1,.b=5}
EXPECTED:
PRIVATE=

Obj* myobj = malloc(sizeof(*myobj))  ; *myobj=(Obj) {.a=1,.b=5};
float* myobj = malloc(sizeof(*myobj))  ; *myobj=(float) 5.555;
def fun() {
	// bug, size is missing in the memcpy
	int* res = calloc(2,sizeof(int));memcpy(res, (int[]){max_length, longest}, 2*sizeof(int));
	return memcpy( calloc(2,sizeof(int)), (int[]){max_length, longest}, 2*sizeof(int));
	return malloc(sizeof(*))  ; *=(Obj) {.a=1,.b=5};
	}


FORWARD DECLARATIONS=
static def fun();
"""
@unittest
def test_buggy111():
	"""
#define MBYTES (1<<20)
#define KBYTES (1<<10)
print "this is a very long line",4,88
print ("this is a very long line",4,88)
EXPECTED:
PRIVATE=

#define MBYTES (1<<20)
#define KBYTES (1<<10)
fprintf (stderr, "this is a very long line",4,88);
fprintf (stderr, ("this is a very long line",4,88));


"""

###########################################################################
############## THESE ARE ADVANCED FEATURES TO BE IMPLEMENTED LATER ########
#@unittest
def test_lambda_function():
	"""
	Vector* gevonden=Vector::search(mysvector,
		lambda bool,(char *elem):
			printf "Hello"
			return strcmp(elem,"WORLD")==0
		)
	if not (index>=0 and index<self.num_elems):
		return NULL
	if not a:
		pass
EXPECTED:
	********************************************************************************
	PUBLIC STUFF
	********************************************************************************
	PRIVATE STUFF
	Vector* gevonden=Vector_search(mysvector,
		lambda (bool,(char *elem) {
			printf ("Hello");
			return strcmp(elem,"WORLD")==0;
		} )
		);
	if (!(index>=0  &&  index<this->num_elems)) {
		return NULL;
		}
	if (!a) {
		}
	"""

#@unittest
def testPrivatePublic():
	"""
class Complex: // Represents imaginary numbers
	private: /* NO PARENTHESES ! */
		double re, im  // Data members, represents re + im * sqrt(-1)
	public: /* NO PARENTHESES ! */
		void set(double r, double i):
			re=r; im=i  // Inlined member function definition
		double real() const:
			return re   // const - does not modify data members
		double imag() const:
			return im   // const - does not modify data members
	"""

#@unittest
def testWITH_MACRO(DEBUG=False):
	"""
	IMPORT_WITH_STATEMENT
	WITH a,b,c:
		printf
		BREAK(-1)
		RETURN
	EXCEPT:
		printf
EXPECTED:
	********************************************************************************
	PUBLIC STUFF
	********************************************************************************
	PRIVATE STUFF
	IMPORT_WITH_STATEMENT;
	WITH (a,b,c) {
		printf;
		BREAK(-1);
		RETURN;
		}
	EXCEPT {
		printf;
		}
	"""

source_text0=r"""
	if sig == SIGPIPE:
		print "Channel %d stopped\n", G.tm_channel
		exit(2)
	elif sig == SIGALRM:
		print "Channel %d: lack of input detected\n", G.tm_channel
		G.no_input_detected= true
		G.output_just_enabled= true // when we restart, we skip incomplete msg
	elif sig== SIGCHLD:
		print "Parent received SIGCHLD: "
		int status
		pid_t return_pid
"""

source_text0=r"""
	struct sockaddr_in addr =:
		.sin_family = AF_INET
		.sin_port = htons(port_number)
		.sin_addr.s_addr = INADDR_ANY
	err = bind(server_socket_fd, (struct sockaddr *) &addr, sizeof(struct sockaddr))
	if err == -1 :
		print "bind error: %d\n", errno
		perror("bind")
		exit(3)
	print "Socket Bind successful\n"
	err = listen(server_socket_fd, 5) // we allow  up to 5 clients at a time
	if err == -1 :
		print "listen error: %d\n", errno
		perror("listen")
		exit(3)
	print "Socket Listen successful\n"
"""

source_text0=r"""
while true:
	print "==============>Waiting for connection on port %d<==============\n", self.port_number
	struct sockaddr_in *client_addr= malloc(sizeof(*client_addr))
	socklen_t client_addr_size = sizeof(struct sockaddr)
	int client_socket_fd = accept(server_socket_fd,
		(struct sockaddr *)client_addr,
		&client_addr_size)
	osal_thread_create(TCP_Server::serve_client_request, client_socket_fd)
// extraneous trailing tab!!!
private class FrameProc:
	uint32_t chunksize_to_read  // how much to read into the input buffer
#define HELLO (1<<2)
"""

source_text0=r"""
enum State:
	open=1
	close=2
"""

source_text0=r"""
for x in fff:
	dothis
	do that
	for y in s:
		for z in ddd:
			print 'dd'
			//print 'rr'
"""

source_text0=r"""
public void Deque::push(self, int n):
	Deque::method(self)
	ptr->n = n
"""

source_text0=r"""
public class DDD:
	int x
	int y
	def __init__(self,int x):
		x=7
	public void publicmethod(self):
		r=8
"""

source_text0=r"""
private enum:
	open=1
	close=2
"""


source_text0=r"""
class CRectangle:
	int *width
	int *height
	public:
		def __init__(self,int a,int b): // CRectangle(int a,int b)
			width := new int
			height := new int
			*width = a
			*height = b
		def __del__(self): // ~CRectangle()
			delete width
			delete height
		int area (self):
			return *width * *height
"""


source_text0=r"""
class CRectangle:
	int *width
	int *height
	public:
		def __init__(self,int a,int b): // CRectangle(int a,int b)
			width := new int
			height := new int
			*width = a
			*height = b
		def __del__(self): // ~CRectangle()
			delete width
			delete height
		int area (self):
			return *width * *height
"""

'''
At least for the people who send me mail about a new language that they're designing, the general advice is: do it to learn about how to write a compiler. Don't have any expectations that anyone will use it, unless you hook up with some sort of organization in a position to push it hard. It's a lottery, and some can buy a lot of the tickets. There are plenty of beautiful languages (more beautiful than C) that didn't catch on. But someone does win the lottery, and doing a language at least teaches you something.
Dennis Ritchie (1941-2011) Creator of the C programming language and of UNIX
'''

'''
def makebold(fn):
	def wrapped():
		 return "<b>" + fn() + "</b>"
	return wrapped


# this decorated definition of hello1 function
# is equivalent to hello2() defined in terms of a helper function below.
@makebold
def hello1():
	return "hello world"

print hello1()

def hello_helper():
	return "hello world"
hello2 = makebold(hello_helper)
print hello2()
'''
'''
class CRectangle {
	int *width, *height;
  public:
	CRectangle (int,int);
	~CRectangle ();
	int area () {return (*width * *height);}
};

CRectangle::CRectangle (int a, int b) {
  width = new int;
  height = new int;
  *width = a;
  *height = b;
}

CRectangle::~CRectangle () {
  delete width;
  delete height;
}

int main () {
  CRectangle rect (3,4), rectb (5,6);
  cout << "rect area: " << rect.area() << endl;
  cout << "rectb area: " << rectb.area() << endl;
  return 0;
}

///////////////////////////////////////
class Calc
{
private:
	int m_nValue;

public:
	Calc() { m_nValue = 0; }

	void Add(int nValue);
	void Sub(int nValue);
	void Mult(int nValue);

	int GetValue() { return m_nValue; }
};

void Calc::Add(int nValue)
{
	m_nValue += nValue;
}

void Calc::Sub(int nValue)
{
	m_nValue -= nValue;
}

void Calc::Mult(int nValue)
{
	m_nValue *= nValue;
}
//////////////////////////////////////////
class CPolygon {
  protected:
	int width, height;
  public:
	void set_values (int a, int b)
	  { width=a; height=b;}
  };

class CRectangle: public CPolygon {
  public:
	int area ()
	  { return (width * height); }
  };

  namespace G
{
  int var = 5;
}

'''

