#TODO: implement PEP 0531 (existential operator)
#TODO: demos "sunfish chess engine, tcl interpreter, google search engine"
#TODO: use qo to replace the makefiles (https://github.com/andlabs/qo )!!!
# TODO: include compile options and directives in the file itself !!!
#TODO: refactor the code to make use of the rxb module !!!
#todo: separate the transpiler from the Makefile generation
#todo: transform 'if sig in [SIGTERM,SIGINT]:'  INTO 'if sig== SIGTERM or sig==SIGINT:'
#todo: integrate SWIG
#todo: add swig type annotations to cxx files !!! //%INPUT
#todo: fixed makefile generation for splitted main functionality!
#TODO: extract python unittest code to a separate file !!!
#todo: use  :->  to indicate a polymorphic call !!!
#todo: fix the typedef bug (see currying file)
# todo: handle inline functions TO BE TESTED !!!!
#todo: finish off the standard library //// use cmake
# todo: add def __del__(self): super.__del__(self) when derived from class !!!
#todo: add "return 0;" to the main of the unittests !!!
# todo: add G pointers to symbol table !!!!
# todo: SYMBOL TABLE
# todo: implement symbol table, in order to do operations on strings(e.g. slicing)
# todo: populate symbol table with function definition parameters !!!
# todo: populate symbol table with function definition parameters for imported modules
#todo: the constructor(__init__) of a class to be derived must be public,
# especially a class of which one method is virtual !!!
# advice: use sdl for games, Qt for GUI's
#todo: test the insert macro (also make a get_and_delete macro) !!!
# add asserts after or before each use of array indexing (when using annotated arrays!)
#todo use std::list std::dict std::queue std::task std::string std::priorityQueue std::reactor std::channel
#todo: put standard lib in zip file and extract as needed:
#  linkedlist.cxx,preprocessor.h,CircularBuffer.cxx,hek_thread.cxx,hek_string.cxx, heapq.cxx,hek_mem.cxx
#  cxx_dict.cxx, epoll_reactor.cxx, Channel.cxx(merge with hek_thread.cxx!!!)
#todo; change case:: into case:
#TODO: integrate with C++ (also generate corresponding makefile!!!)
#todo: implement labeled break
#todo: replace 'for i in range(n)' in 'for int i=0;i<n;i++'
#todo include python interpreter into a cxx program !!!
#todo: Schwartzian transform for linked lists| implement heap, queue and dict!!!
#TODO: use nullfree in the destructor instead of free,
#    and enforce that only a NULL pointer can be used in a malloc !!!
# realloc() to only receive non-NULL pointers and for malloc() to only receive NULL ones !!!
# MAKE USE OF RECALLOC
#todo: incorporate plantUML (see plant.py)
#todo: replace delete[] with free (to please c++ users!)
#todo: implement David Beazley slides on generator tricks!
#todo : implement struct inheritance
#todo: in makefile, pkg-config as in stackoverflow.com/questions/19366064/how-to-compile-an-example-sdl-program-written-in-c
#TODO: implement smart pointer(with reference count)
#todo: write tetris game, pacman game
# TODO: introduce a foreach construct, also "for int i in [a:b]"
#  should become ==> for int i=a;i<b;i++
#todo: first comment in the file (between /* and */) should be considered as docstring !!!
#TODO: int {x,y} = function(...) ==> volatile int* res= function(...); int x=res[0],y=res[1];
# in the function, return (int[]) x,y ==> res= new int[2];return res;
#todo: delegate objects also for G class !!!
#todo: pod struct inheritance
#     in __init__ method, if self is assigned to, then add
#       ==> transform: self=SDL_SetVideoMode(width, height, bpp, flags)
#      into:
#       free self // we don't need it anymore
#       self=SDL_SetVideoMode(width, height, bpp, flags)
#       if not self:
#           return NULL
#       self=realloc(self,sizeof *self)
#       if not self:
#           return NULL
#       //
#todo: implement generics/templates e.g. List<int,10> mylist !!!
# example: Stack<int,10> mystack as  ==>NEW_LIST(int,mystack,10)
#       mystack.push(555)  ==>
#       mystack.pop()  ==>
#       mystack.size() =>
#       mystack.empty()  ==>
#       mystack.full()  ==>
#       for int i in mystack  ==>
# example: int myqueue[10] as Queue
#todo: convert uint16_t to uint_fast16_t (c99 feature!!!)
#todo: generate a default constructor in a derived class if not called !!!
#   def __init__(self):
#       super.__init__(self)
#   THE PROBLEM IS WHEN THERE ARE PARAMETERS. YOU HAVE TO GET THE CONSTRUCTOR
#   PARAMETERS FROM THE PARENT CLASS DEFINITION possibly IN ANOTHER FILE !!!
# todo: assert a>0 , "a must be positive" ==> replace ',' by '&&'
# todo: add a method to reset the generator !!!!
# todo: anonymous blocks
#       ::
#           print
#           print
#       this should trigger a { print; print''}
# TODO: properties for getters and setters
# class Cat:
#    char name[100]:
#        get:
#            return name
#        set:
#            strcpy(name,value)
#todo: data=yield from generator()
#    ==> data=generator->next()
#        if not generator->exhausted:
#             yield data
#todo: implement user-defined literals 1m 3s 4m_s
#todo: object method reset(self):
# ==>       HAL::destructor(self);HAL::constructor(self,self.tx_id, self.card_id, self.debug)
"""
The idea behind coroutines is that multiple functions can cooperate by yielding
control to one another. JavaScript's generators are more limited, in that they
can only pass control back to the caller. Still, this turns out to be enough,
because we can introduce a coordinator function to pass control from the caller
to any function we choose.
This cooperation, in turn, allows us to do multiple tasks concurrently.
"""
"""
transformers (pure functions)
filters (stateful generators)
newsource= source >> filter1 | transformer | filter2
for int x in source:
    int y= filter1->next(x)
    if not filter1->valid_output:
        continue
    if not filter1->exhausted:
        break
    int w= transformer(y)
    int z= filter2->next(w)
    if not filter2->valid_output:
        continue
    yield z
todo: combine with channels to exploit multicores !!!
"""
# todo: newsource= source >> processor1 | .... | processorN
# todo: int x= source >> sink --> int x= sink(source)
# todo: repeat until construct
# todo: valType myhash[keyType]
# becomes
# #include "uthash.h"
# struct myhashType:
#     keyType _key
#     valType _val
#     UT_hash_handle hh
# my_struct *myhash = NULL
# todo: add ADA constrained types: int x constraint 0 < x < 9
# TODO default parameters for virtual methods
# BUG, doc strings may not contain empty lines !!!
# todo implement clone method
# todo: write the c++ wrapper !!!
# todo: implement currying
# todo: handle overloaded functions !!!
# add a c++ mode
# BUG :/* a single quote in the comment ' spoils everything */
# add python-style comments
# TODO: implement an Either class, e.g. Either(int x, bool y)
# EXAMPLE: as a return value type
# private Either<Exception, int> myfunction(....)
############################    TODO's   ############################
# 1. anonymous blocks (for RAAI in C++) with block: construct
# 2. define constructor and destructor by this and ~this
# 3. define map in the D way !!!
#int b[char*];    // associative array b of ints that are
#                  // indexed by an array of characters.
#                  // The KeyType is char*
#b["hello"] = 3;   // set value associated with key "hello" to 3
#func(b["hello"]); // pass 3 as parameter to func()
#Particular keys in an associative array can be removed with the remove function:
#b.remove("hello");
#
#5. PYSTRING(yourstring)[2:4] ==> String::slice(yourstring,2,4)
#6. PYDICT(yourhash)[ww]=7
#7. PYLIST(yourlist)[1:8] ==> Vector::slice(yourlist,1,8)
#8. for char c in PYSTRING(yourstring):  ==> for int i=0;i<strlen(yourstring);i++: char c=yourstring[i]
#9. for int el in PYLIST(yourlist):  ==> for int i=0;i<Vector::len(yourlist);i++: int el=Vector::get(i)
#10.for int key,char*value in PYDICT(yourdict):  ==> for int i=0;i<Hash::len(yourdict);i++: int key=..
#
"""
try:
    SSLFreeBuffer(&hashCtx))
    ReadyHash(&SSLHashSHA1, &hashCtx))
    SSLHashSHA1.update(&hashCtx, &clientRandom))
    SSLHashSHA1.update(&hashCtx, &serverRandom))
    SSLHashSHA1.update(&hashCtx, &signedParams))
    SSLHashSHA1.final(&hashCtx, &hashOut)))
except:
    whatever
else:
    finish
====> translates into:
if !((err = SSLFreeBuffer(&hashCtx)) ||
    (err = ReadyHash(&SSLHashSHA1, &hashCtx)) ||
    (err = SSLHashSHA1.update(&hashCtx, &clientRandom)) ||
    (err = SSLHashSHA1.update(&hashCtx, &serverRandom)) ||
    (err = SSLHashSHA1.update(&hashCtx, &signedParams)) ||
    (err = SSLHashSHA1.final(&hashCtx, &hashOut))) {
   finish;
fail:
  whatever;
}

"""

"""
HOW A C++ program can make use of a CXX class?
THIS SHOULD BE A .hxx FILE THAT CREATES A .hpp FILE FOR C++ consumption
public extern "C":
    #include "buf.h"

public klass mybuf : public Buf:
    mybuf(int x, int y):
        Buf::constructor(self,x,y)
    void clear():
        Buf::clear(self)
    bool printit():
        return Buf::printit(self)
    bool append(const char* p, unsigned c):
        return Buf::append(self, p, c)

The code is clean-C, ie C99 but in order to be compatible with C++, this
means no designated initializers, no compound literals, and casting allocs.
To take advantage of these features when having to use C++ libraries,
i use extern "C" in all the generated c headers,
compile all C code with a c compiler into object files and then the c++ code and
the main with a c++ compiler and link it all together !!!
"""
"""
HOW A CXX program can make use of a C++ class, e.g. Qtclass, defined in qtklass.h?
Create qtklass_wrapper.h file, with the following contents

#include "qtklass.h"
struct Qtclass
extern "C" int Qtclass_new(int x) { return new Qtclass(x); }
extern "C" int Qtclass_foo(self, int i) { return self.foo(i); }
extern "C" int Qtclass_del(self) { return ~Qtclass(); }


"""

# regular expressions to parse html
# /(<.*?>|[^<]+)\s*/g    # get tags and text
# /(\w+)="(.*?)"/g       # get attibutes
##############################################################################
# MODULE INHERITANCE OVERRIDE SOME FUNCTIONS
'''
import cxx_compiler
orig_cxx_compiler = __import__('cxx_compiler')
class CPP_compiler(cxx_compiler):
    class __metaclass__(type):
        def __new__(cls, name, bases, dct):
            dct["__getattr__"] = lambda x, y: getattr(bases[0], y)
            return type.__new__(cls, name, (object,), dct)
    def lstat(self, arg):
        print orig_cxx_compiler.lstat(arg)
        return 6
    def rmdir(self, arg):
        raise self.error("No such file or directory: %r" % arg)
compiler = CPP_compiler()
'''
#############################################################################
globals_h_template="""
#ifndef _GLOBALS_H
#define _GLOBALS_H


// header files required by global struct
{0}

// enums and defines
{1}

#ifndef _MAIN_C_
#define EXTERN extern
#else
#define EXTERN
#define INITIALIZE
#endif

// global data appropriately packaged in a struct
EXTERN {2}
#ifdef INITIALIZE
{3}
#endif
;

#undef EXTERN
#undef INITIALIZE
#endif

"""
##############################################################################
import re, sys, copy, string, os
from hek_test_utils import stdout_redirected
from StringIO import StringIO
from cxx_utils import windows, get_indentation, get_sanitized_line, Pipe
from process_cpp import process_cpp_classes
from hek_c_symbols import needed_header_files
from make import make_makefile, make_c_file, make_h_file
SINGLE_TRIPLE_QUOTE="'''"
DOUBLE_TRIPLE_QUOTE='"""'
xsplit = lambda s,*seps:filter(None,re.split("("+"|".join(map(re.escape,seps))+")",s))
# interesting property: "".join(xsplit(s))==s
myxsplit=lambda s: xsplit(s,'.',',','(',')','[',']','*','->',' ')
xfind=lambda s,seps=".,()[]":re.findall(r"[\w]+|%s"%"|".join(map(re.escape,seps)+["->"]),s)
def is_sublist(sublist,list):
    list=[elem for elem in list if elem!=" "]
    #list=[elem for elem in list if elem in string.whitespace]
    return any(sublist==list[i:i+len(sublist)] for i in range(len(list)))

def remove_funpointer_parens(argvalues):
    if "(" not in argvalues:
        return argvalues
    balance=0
    output=[]
    curr_elem=[]
    for elem in argvalues.split(','):
        balance += elem.count('(')-elem.count(')')
        curr_elem.append(elem)
        if balance==0:
            new_elem=','.join(curr_elem)
            if '(*' in new_elem:
                new_elem=new_elem[new_elem.find('(*')+2:]
                new_elem=new_elem[:new_elem.find(')')]
            output.append(new_elem)
            curr_elem=[]
    return ','.join(output)
if __name__=="__main__":
    line=", port_number, (*serve_client)(int), char* (*sig_handler)(int,float)"
    #print remove_funpointer_parens(line)

class SymbolTable(list):
    push=list.append
    def enter_scope(self):
        self.push({})
    def leave_scope(self):
        self.pop()
    def add_symbol(self,symbol,value):
        #print ">>>", symbol, value
        self[-1][symbol]=value
    def get_symbol(self,sym):
        for sym_table in reversed(self):
            if sym in sym_table:
                return sym_table[sym]
        return None

if __name__=="__main__":
    a=SymbolTable()
    a.enter_scope()
    a.add_symbol('sym1',4)
    a.add_symbol('sym2',88)
    a.enter_scope()
    a.add_symbol('sym1',5)
    #print a
    assert a.get_symbol('sym1')==5
    assert a.get_symbol('sym2')==88
    assert a.get_symbol('sym3')==None
    a.leave_scope()
    assert a.get_symbol('sym1')==4
    assert a.get_symbol('sym2')==88

def determine_arguments(func_string):
    npar=0
    args=[]
    for x in myxsplit(func_string):
        if x=='(':
            npar += 1
            if npar>1:
                args.append(x)
            continue
        if x==')':
            npar -= 1
            if npar>=1:
                args.append(x)
            continue
        if npar==0:
            continue
        if npar==1:
            if x==',':
                if args and '(' not in args:
                    myvar=args[-1]
                    mytype="".join(args[:-1])
                    #print myvar,"==>",mytype
                    G.symbol_table.add_symbol(myvar,mytype)
                args=[]
                continue
        args.append(x)
    if args and '(' not in args:
        myvar=args[-1]
        mytype="".join(args[:-1])
        #print myvar,"==>",mytype
        G.symbol_table.add_symbol(myvar,mytype)

def is_function_declaration(line_of_code):
    # int func(dds)
    # int (*func)(dds)  ==> not a function but declaration of func pointer
    # void sort(Test* self, int (*cmp_func)(int, int)):
    ee=line_of_code.split()
    if ee and ee[0] in ('if','while','for','class','inline'):
        return False
    OPENPAR='('
    CLOSEPAR=')'
    if OPENPAR not in line_of_code:
        return False
    num_pars=0
    for i, char in enumerate(line_of_code):
        if char=='=' and num_pars==0:
            return False
        if char==OPENPAR:
            num_pars += 1
            within_paren=True
        if char==CLOSEPAR:
            num_pars -= 1
            if num_pars==0:
                if OPENPAR in line_of_code[i:]:
                    return False # int (*func)(dds)
    if num_pars==0 and not line_of_code.rstrip().endswith("):"):
        return False # avoid cl= new Class(par1,par2) or #define a (1<<2)
    return True

if __name__=="__main__":
    line="void sort(Test* self, int (*cmp_func)(int, int)):"
    line="if ggggg.startswith('kk'):"
    #print is_function_declaration(line)
    #raise SystemExit

def declare_default_arguments(function, default_arguments):
    if "__init__" in function:
        return function,[]
    func_name=function.split("(")[0].split()[-1]
    #print '55555555555 ', func_name
    try:
        arguments=function.split("(",1)[1].split(',') # caveat, argument can contains ','
    except:
        return function,[]
    #print 'func name=', func_name
    number_params=len(arguments)
    number_default_params=len(default_arguments)
    #print "NUMBER PARAMS=",number_params
    #print "NUMBER DEFAULT PARAMS=",number_default_params
    with stdout_redirected(StringIO()) as f1:
        if number_default_params==number_params:
            # the first alternative  entails including "preprocessor.h"
            #print '#include "preprocessor.h"'
            make_stdlib_files("DEFAULT PARAMETERS")
        else:
            # the following alternative is self-contained but does not work with 0 arguments (not in c99) !!!
            print "#ifndef OVERLOADED_MACROS_DEFINED"
            print "#define OVERLOADED_MACROS_DEFINED"
            print "#define MKFN(fn,...) MKFN_N(fn,##__VA_ARGS__,9,8,7,6,5,4,3,2,1,0)(__VA_ARGS__)"
            print "#define MKFN_N(fn,n0,n1,n2,n3,n4,n5,n6,n7,n8,n,...) fn##n"
            print "#endif"
    with stdout_redirected(StringIO()) as f2:
        print "\n/********* start of declarations for overloaded function *****/"
        #
        print '#define %s%d(' % (func_name,number_params),
        print ','.join(chr(65+k) for k in range(number_params)),
        print ')',
        print func_name+'(',
        print ', '.join(chr(65+k) for k in range(number_params)),
        print ', '.join(default_arguments[number_params:]),
        print ')'
        for i in range(number_default_params):
            print '#define %s%d(' % (func_name,number_params-i-1),
            if number_params-i-1:
                print ','.join(chr(65+k) for k in range(number_params-i-1)),
            print ')',
            print func_name+'(',
            if number_params-i-1:
                print ', '.join(chr(65+k) for k in range(number_params-i-1)),
                print ',',
            print ', '.join(default_arguments[number_default_params-i-1:]),
            print ')'
        if number_default_params==number_params:
            # the first alternative  entails including "preprocessor.h"
            print "#define {0}(...) TOKCAT({0}, VA_NUM_ARGS(__VA_ARGS__))(__VA_ARGS__)".format(func_name)
        else:
            # the following alternative is self-contained but does not work with 0 arguments (not in c99) !!!
            print "#define {0}(...) MKFN({0},##__VA_ARGS__)".format(func_name)
        print "/*********  end of declarations for overloaded function *****/\n"
    return f1.getvalue(), f2.getvalue().replace('::__init__(','_constructor(').replace('::','_')


def collect_default_arguments(fun):
    skip=False
    output=""
    current_default_val=""
    default_args=[]
    for i,char in enumerate(fun):
        if not skip:
            if char=='=':
                skip=True
        if skip:
            if char == ',' or fun[i:].startswith('):') or fun[i:]==")":
                skip=False
                default_args.append(current_default_val[1:].strip())
                current_default_val=""
        if skip:
            current_default_val += char
        else:
            output += char
    #print "eee ", default_args
    if "__init__" in fun:
        default_args=[]
    return output,default_args
############################################################################
def subDirPath(d='.'):
    return glob.glob('*/')
    #return filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)])
##############################################################################
class G:
    module_docstring=[] # STILL TO BE USED
    forward_declarations=[]
    global_declarations=[]  # enums and defines
    symbol_table=SymbolTable()
    class_symbol_table={}
    delegates_for_class={}
    imported_modules=[]
    defines=[]
    main_app= False # if false, we need a .h file
    h_output_file=""
    c_output_file=""
    override_methods=[]
    mode='c'
    ASSERT_MODE=False
    PUBLIC_MAIN_CONSTRUCTOR=False
def reset_globals(mode):
    G.module_docstring=[]
    G.forward_declarations=[]
    G.global_declarations=[]
    G.imported_modules=[]
    G.defines=[]
    G.main_app= False # if false, we need a .h file
    G.h_output_file=""
    G.c_output_file=""
    G.override_methods=[]
    G.mode=mode
    G.ASSERT_MODE=False
    G.PUBLIC_MAIN_CONSTRUCTOR=False
#########################################################################

@Pipe
def base_processing(lines): # this is the first level
    within_curly_braces, within_round_braces, within_square_braces= 0, 0, 0
    within_braces=False
    within_comment= False
    within_multiline_string=False
    previous_indentation=0
    line_in_construction=[]
    comment_in_construction=[]
    myiter=windows(lines)
    for previous_line, line, next_line in myiter:
        if not within_braces:
            current_indentation= get_indentation(line.rstrip())
        if next_line:
            next_indentation= get_indentation(next_line.rstrip())
        else:
            next_indentation=None
        if not line.strip():
            if next_indentation>0:
                # skip empty cosmetic lines
                yield previous_indentation, "", "",{}
                continue
        #################################################################
        sanitized_line=get_sanitized_line(line)
        if line.startswith("#include"): # this is a directive !!!
            # yield None, line, "",{}
            G.imported_modules.append(line.rstrip())
            previous_indentation=0
            continue
        if line.startswith("#define"): # this is a directive !!!
            # yield None, line, "",[dict(within_braces=False)]
            G.defines.append(line.rstrip())
            previous_indentation=0
            # continue  we want to preserve them at the place where they are defined!
        if within_comment:
            if '*/' in get_sanitized_line(line):
                within_comment=False
            yield None, "", line, {}
            continue
        comment_idx= None
        comment1_idx=sanitized_line.find('/*') # find the first occurrence, comment might contain /*
        comment2_idx=sanitized_line.find('//') # find the first occurrence, comment might contain //
        if comment2_idx>=0 and (comment1_idx<0 or comment2_idx<comment1_idx): # '//' is first
            comment_idx=comment2_idx
        elif comment1_idx >=0:
            if "*/" not in sanitized_line[comment1_idx:]:
                within_comment=True
            comment_idx=comment1_idx
        if comment_idx>=0:
            current_line=line[:comment_idx]
            current_comment=line[comment_idx:]
        else:
            current_line=line
            current_comment=""
        dedent= previous_indentation-current_indentation
        while dedent>1:
            yield current_indentation+dedent-1, "", "",{"dedenting":True}
            dedent -= 1
        previous_indentation= current_indentation # FIX THIS
        # THIS IS FOR MULTILINE STRINGS
        #QUOTE=('"','Q') # Q added as workaround for bug in test_cxx_compiler.py !!!
        #if current_line.strip().startswith(QUOTE) and current_line.strip().endswith(QUOTE):
        #   within_multiline_string=True
        #   if not (next_line.strip().startswith(QUOTE) and next_line.strip().endswith(QUOTE)):
        #       current_line +=';'
        #   yield (current_indentation-1,current_line,current_comment,{})
        #   continue
        #else:
        #   within_multiline_string=False # end of multiline string
        within_curly_braces+=sanitized_line.count("{")-sanitized_line.count("}")
        within_round_braces+=sanitized_line.count("(")-sanitized_line.count(")")
        within_square_braces+=sanitized_line.count("[")-sanitized_line.count("]")
        within_braces=(within_curly_braces+within_round_braces+within_square_braces)>0
        line_in_construction+=[current_line]
        if current_comment:comment_in_construction+=[current_comment]
        if not within_braces:
            yield (current_indentation,
                    "\n".join(line_in_construction),
                    "\n".join(comment_in_construction),
                    #current_comment,
                    {}
                    )
            line_in_construction=[]
            comment_in_construction=[]
@Pipe
def process_struct_union_enum(level):
    within_struct=False
    within_union=False
    within_enum=False
    name=""
    for indent,line_of_code,comment,other_info in level:
        if indent==0 and line_of_code.lstrip().startswith(("struct ","public struct ","private struct ")):
            if '(' not in line_of_code and ')' not in line_of_code:
                within_struct=True
                keyw='struct '
        if indent==0 and line_of_code.lstrip().startswith(("union ","public union ","private union ")):
            within_union=True
            keyw='union '
        if indent==0 and line_of_code.lstrip().startswith(("enum ","public enum ","private enum ")):
            within_enum=True
            keyw='enum '
        if within_struct or within_union or within_enum:
            within_struct=False
            within_union=False
            within_enum=False
            name=line_of_code.partition(keyw)[2].partition('(')[0].lstrip().split()[0].rstrip('):')
            ###############
            is_private= line_of_code.lstrip().startswith(('private',keyw))
            if is_private:
                opaque_comment= '// opaque type'
                if G.mode=='c':
                    opaque_declaration='typedef '+line_of_code.rstrip(': ')+' '+name
                else:
                    opaque_declaration=line_of_code.rstrip(': ')
                #print ')))))))) ', line_of_code
                if len(name)>0: # no need for anonymous enums
                    if name != 'G': # THIS IS A HACK !!!!
                        G.forward_declarations.append(opaque_declaration.replace('private ','',1)+'; '+opaque_comment)
                line_of_code= line_of_code.replace("protected ","",1).replace("private ","",1)
                #print "8888888888888888888888888888", line_of_code
            else:
                #line_of_code = "public typedef "+ line_of_code.replace("public ","")
                if G.mode=="c":
                    typedef_decl='typedef '+line_of_code.strip().rstrip(':')+' '+name
                else:
                    typedef_decl=line_of_code.strip().rstrip(':')
                yield indent,'public '+typedef_decl, "", {}
        yield indent,line_of_code,comment,other_info

REAL, OVERRIDE, VIRTUAL= range(3)
@Pipe
def process_classes(level):
    within_class=False
    within_methods=False
    classname=""
    parent_classname=""
    parent_argvalues=''
    argtypes=""
    argvalues=""
    constructor_defined=False
    destructor_defined=False
    within_constructor=False
    within_next_method=False
    prologue_generator_done=False
    generator_class=False
    return_this_added=False
    methods=[]
    init_lines=[]
    method_type= REAL
    for indent,line_of_code,comment,other_info in level:
        if indent==0:# state changes can only occur at indent 0
            if within_class: # current class ends
                within_class=False
                G.class_symbol_table[classname]= (methods,parent_classname)
                # we are done with the class
                yield instance_members[0]
                if generator_class:
                    yield 1,"\tint _state","",{}
                    yield 1,"\tbool _exhausted","",{}
                    yield 1,"\tbool _valid_output","",{}
                if not instance_members[1:]:
                    yield 1,"\tint dummy","//NO MEMBERS IN STRUCT!",{}
                for line in instance_members[1:]:
                    if line[1].lstrip().startswith('enum'):
                        for li in ([(0,line[1],'',{})] >> process_struct_union_enum):
                            #print "nnn ",li,G.forward_declarations
                            pass
                    yield line
                #print G.symbol_table
                # let us now add the virtual methods pointers !!
                for meth_name,meth_proto,meth_type in methods:
                    if meth_type==VIRTUAL:
                        #print "virtual method:", meth_name
                        yield 1,meth_proto,"// virtual method",{}
                yield (0, '', '', {})
                # we are done with the struct
                # let us now build the __init__()
                rlines=[]
                if init_lines:
                    yield init_lines[0]
                if generator_class:
                    if not init_lines:
                        yield (0, '{0}* {0}::__init__({0}* self):'.format(classname), '', {})
                    yield 1,"\tself._state=0","",{}
                    yield 1,"\tself._exhausted=false","",{}
                    yield 1,"\tself._valid_output=true","",{}
                    if not init_lines:
                        yield 1,"\treturn this","",{}
                for line in init_lines[1:]:
                    if 'return this' in line[1] or rlines:
                        rlines.append(line)
                    else:
                        #print "init line=", line
                        yield line
                init_lines=[] # reset it
                for meth_name,meth_proto,meth_type in methods:
                    if meth_type >= OVERRIDE:
                        yield 1,'\tself.{0}={1}::{0}'.format(meth_name,classname),"// virtual method",{}
                for rline in rlines:
                    rline=rline[0],rline[1],rline[2],{'mode':'PRIVATE'}
                    #print "eeeeeee ",rline
                    yield rline
                #yield (0, '', '', {})
                # generate constructor and destructor
                for line in static_members:
                    if line[1].startswith("public"):
                        yield line
                    else:
                        line=line[1].replace('private','static',1).replace('::','_')
                        G.forward_declarations.append(line+';')
                if is_private:
                    access='private'
                else:
                    access='public'
                # GENERATE THE CODE for the Object_new() method
                if G.mode=='c':
                    yield (0, '{2} {0}* {0}_new({1}):'.format(classname,argtypes,access),'', {})
                    yield (1, '\t{0}* self= malloc(sizeof(*self))'.format(classname), '', {})
                    yield (1, '\tif not self:', '', {})
                    yield (2, '\t\treturn NULL', '', {})
                    if parent_classname and not constructor_defined:
                        # we shoudl generate a default constructor with right args
                        # this means i need the signature of the parent class
                        #def __init__(self, args):
                        #   super.__init__(self,args)
                        print "WARNING: NO CONSTRUCTOR DEFINED IN DERIVED CLASS !!!"
                        pass
                    if constructor_defined:
                        argvalues=remove_funpointer_parens(argvalues)
                        argvalues=collect_default_arguments(argvalues)[0]
                        yield (1, '\treturn {0}::__init__(self{1})'.format(classname,argvalues), '', {})
                            #yield (1, '\treturn new {0}({1})'.format(classname,argvalues.lstrip(', ')), '', {})
                    elif generator_class:
                        yield (1, '\treturn {0}::__init__(self)'.format(classname), '', {})
                    else:
                        yield (1, '\treturn self', '', {})
                    yield (0, '', '', {})
                    # GENERATE THE CODE for the Object_free() method
                    # free
                    yield (0, '{1} void {0}_free({0}* self):'.format(classname,access), '', {})
                    if destructor_defined:
                        yield (1, '\t{0}::__del__(self)'.format(classname), '', {})
                    if parent_classname and not destructor_defined:
                        # TODO !!!! new new new to be tested zzzz
                        # we generate a default destructor with a call to the parent destructor
                        yield (1, '\t{0}_free(self)'.format(parent_classname), '', {})
                    else:
                        yield (1, '\tfree(self)', '', {})
                    yield (0, '', '', {})
                # NOW the methods
                do_prologue_generator=False
                for line in methods_lines:
                    inden,linecode,_,_=line
                    #print "jjjj ",linecode, inden
                    if inden==0 and '(' in linecode:
                        method_nam=linecode.split('(')[0].split()[-1]
                        if method_nam.endswith("next"):
                            #print "dddd ",method_nam, line_of_code
                            do_prologue_generator=True
                            yield line
                            continue
                    if do_prologue_generator:
                        yield inden,'\t'*inden+'switch self._state:','',{}
                        yield inden+1,'\t'*(inden+1)+'case 0: goto LABEL0','',{}
                        for i in range(yieldnum):
                            yield inden+1,'\t'*(inden+1)+'case {0}: goto LABEL{0}'.format(i+1),'',{}
                        yield inden,'\t'*inden+'LABEL0: //start of generator','',{}
                        do_prologue_generator=False
                    yield line
                ##########################################
                within_class=False
                within_methods=False
                classname=''
                argtypes=""
                argvalues=""
                parent_classname=""
                parent_argvalues=''
                constructor_defined=False
                destructor_defined=False
                within_constructor=False
                within_next_method=False
                do_prologue_generator=False
                generator_class=False
                return_this_added=False
            if not within_class:
                if line_of_code.lstrip().startswith(("class ","public class ","private class ","protected class ")):
                    within_class=True
                    methods=[]
                    methods_lines=[]
                    instance_members=[]
                    static_members=[]
                    initialized_members=[]
                    classname=line_of_code.strip().partition('class ')[2].partition('(')[0].lstrip().split()[0].rstrip('):')
                    if "(" in line_of_code and ")" in line_of_code:
                        parent_classname=line_of_code.strip().partition('(')[2].lstrip().split()[0].rstrip('):')
                        line_of_code=line_of_code.partition('(')[0].rstrip()+':'
                    #print "8888888888888888888888 ", line_of_code
                    G.symbol_table.add_symbol('self', classname)
                    ###############
                    is_private= line_of_code.lstrip().startswith(('private','class'))
                    is_protected= line_of_code.lstrip().startswith('protected')
                    if is_private or is_protected:
                        opaque_comment= '// opaque type'
                        if G.mode=='c':
                            opaque_declaration='typedef '+line_of_code.strip().rstrip(': ').replace("protected ","").replace('class','struct',1)+' '+classname
                        else:
                            opaque_declaration=line_of_code.strip().rstrip(': ')
                        if is_private:
                            G.forward_declarations.append(opaque_declaration.replace('private ','')+'; '+opaque_comment)
                        else:
                            yield 0,'public '+opaque_declaration, opaque_comment,{}
                        line_of_code= line_of_code.replace("protected ","",1).replace("private ","",1)
                    else:
                        #line_of_code = "public typedef "+ line_of_code.replace("public ","")
                        if G.mode=='c':
                            typedef_decl='typedef '+line_of_code.replace('class','struct',1).rstrip().rstrip(' :')+' '+classname
                        else:
                            typedef_decl=line_of_code.rstrip().rstrip(' :')
                        yield 0,'public '+typedef_decl, "",{}
                    if G.mode=="c":
                        line_of_code= line_of_code.replace("class","struct",1)
                    ###############
                    #yield 0,line_of_code,comment,other_info
                    instance_members.append((0,
                                            line_of_code,
                                            comment,
                                            other_info))
                    if parent_classname:
                        # anonymous struct for the parent class !
                        #yield (1, '\t{0} '.format(parent_classname), '', {}) # ANONYMOUS STRUCT !!!
                        instance_members.append((1,
                                             '\t{0} '.format(parent_classname),
                                            '',
                                            {}))
                    continue
        if indent==1:# state changes (for within_methods) can only occur at indent 1
            if within_class and 'self' in line_of_code and '(' in line_of_code:
                within_methods=True # we are done with the attributes
                #print '88', line_of_code
        # NOW THAT WE HAVE HANDLED THE STATE CHANGES, LET US PROCESS THE LINES
        if not within_class:
            yield indent,line_of_code,comment,other_info
        else: # we are within a class
            if not within_methods:
                # declaration of instance variables
                if 'static ' in line_of_code:
                    idx=line_of_code.find('=')
                    if idx==-1:
                        static_var_name=line_of_code.split()[-1]
                        newline=line_of_code.lstrip().replace('static ','')
                        vidx=newline.rfind(static_var_name)
                    else:
                        static_var_name=line_of_code[:idx].split()[-1]
                        newline=line_of_code.lstrip().replace('static ','')
                        vidx=newline[:newline.find('=')].rfind(static_var_name)
                    #print 'static varname=', static_var_name
                    #print '44444444', newline, vidx
                    #print '6666666 ', newline[:vidx]
                    #print '777 ', newline[vidx+len(static_var_name):]
                    newline=newline[:vidx]+classname+'::'+static_var_name+newline[vidx+len(static_var_name):]
                    #print '5555 ', newline
                    static_members.append((0,
                                        newline,
                                        comment,
                                        other_info))
                elif '=' in line_of_code and indent==1:
                    idx=line_of_code.find('=')
                    splitted_line=line_of_code[:idx].split()
                    identifier=splitted_line[-1]
                    type=" ".join(splitted_line[:-1])
                    initialiser=line_of_code[idx+1:]
                    #print "type=",type,
                    #print " identifier=",identifier
                    #print " initialiser=",initialiser
                    if type=="char*":
                        newline='\tstrcpy(self.%s,%s)'% (identifier,initialiser)
                    else:
                        #newline='\tself.'+line_of_code[:idx].split()[-1]+line_of_code[idx:]
                        newline='\tself.'+identifier+'='+initialiser
                    #print 'i am here ', newline
                    #yield indent,line_of_code[:idx],comment,other_info
                    instance_members.append((indent,
                                            line_of_code[:idx],
                                            comment,
                                            other_info))
                    initialized_members.append((1,
                                        newline,
                                        comment,
                                        other_info))
                    # initialized instance member
                    splittedline=line_of_code[:idx].split('*')
                    if splittedline[1:]:
                        #print "))))))))))))))", classname,G.class_symbol_table
                        klassname=splittedline[0].strip()
                        G.symbol_table.add_symbol('self.'+splittedline[1].strip(),klassname)
                        if classname not in G.delegates_for_class:
                            G.delegates_for_class[classname]={}
                        G.delegates_for_class[classname]['self.'+splittedline[1].strip()]=klassname
                else:
                    #yield indent,line_of_code,comment,other_info
                    instance_members.append((indent,
                                            line_of_code,
                                            comment,
                                            other_info))
                    # uninitialized instance member
                    splittedline=line_of_code.split('*')
                    if splittedline[1:]:
                        #print "))))))))))))))", classname,G.class_symbol_table, line_of_code
                        #print "))))))))))))))", classname, line_of_code
                        klassname=splittedline[0].strip()
                        #print "))) klassname", klassname
                        #print "SYMB=", G.symbol_table
                        G.symbol_table.add_symbol('self.'+splittedline[1].strip(),klassname)
                        if classname not in G.delegates_for_class:
                            G.delegates_for_class[classname]={}
                        G.delegates_for_class[classname]['self.'+splittedline[1].strip()]=klassname
                        #print 'wwwwwwwwwww ',G.symbol_table,line_of_code
            else: # we are within a method
                if line_of_code.lstrip().startswith(("def ","public def")) and "__del__" in line_of_code:
                    destructor_defined=True
                if line_of_code.lstrip().startswith(("def ","public def")) and "__init__" in line_of_code:
                    constructor_defined=True
                    argtypes=(line_of_code.replace("self","")
                                        .replace("public def","")
                                        .replace("def","")
                                        .replace("__init__","")
                                        .replace("(","",1)
                                        #.replace(")","")
                                        .replace(":","")
                                        .replace(",","",1)
                                        .strip()[:-1]
                                        )
                    #print "argtypes=", argtypes,  argtypes.split(',')
                    #print [arg.split()[-1] for arg in argtypes.split(',')]
                    # TODO handle the MULTILINE __init__ case !!!
                    if argtypes:
                        #print "====>argtypes=", argtypes
                        argvalues= ', '.join([arg.split()[-1].lstrip('*') for arg in argtypes.split(',')])
                        #print "argvalues=", argvalues
                        if argvalues:
                            argvalues=', '+argvalues
                if within_constructor and not return_this_added:
                    if other_info.get("dedenting",False) and indent <=2:
                        #yield 1,"\treturn this",comment,other_info
                        init_lines.append((1,"\treturn this",comment,other_info))
                        return_this_added=True
                if indent==1: # method declaration
                    if '@virtual' in line_of_code:
                        method_type= VIRTUAL
                        continue
                    if '@override' in line_of_code:
                        method_type= OVERRIDE
                        continue
                    if '(self' in line_of_code:
                        line_of_code=line_of_code.replace("self",classname+"* self")
                    line_of_code=line_of_code.replace("def ","void ")
                    if "__init__" in line_of_code:
                        within_constructor=True
                        init_lines=[]
                        line_of_code=line_of_code.replace("void ",classname+"* ",1)
                    elif within_constructor:
                        within_constructor=False
                        if not return_this_added:
                            init_lines.append((indent,"\treturn this",comment,other_info))
                            #yield indent,"\treturn this",comment,other_info
                            init_lines.append((0, '', '', {}))
                            #yield (0, '', '', {})
                            return_this_added=True
                    #print "####", line_of_code, len(line_of_code), ord(line_of_code[0])
                    if line_of_code.strip():
                        method_name=line_of_code.split('(')[0].split()[-1]
                        if method_name=="next":
                            within_next_method=True
                            yieldnum=0
                            prologue_generator_done=False
                            generator_class=True
                        prototype=(line_of_code.
                        replace(method_name,'(*%s)' % method_name,1).
                        replace('public ','',1).replace('private ','',1).rstrip().
                        strip(':'))
                        line_of_code=line_of_code.replace(method_name,classname+"::"+method_name)
                        #print "-----------------", method_name, prototype
                        methods.append((method_name,prototype,method_type))
                        method_type=REAL
                if indent>1:
                    if '__init__' in line_of_code: # call to parent constructor
                        line_of_code=(line_of_code.
                                replace("super.__init__(","{0}::__init__(({0}*)".format(parent_classname))
                        )
                    if '__del__' in line_of_code: # call to parent destructor
                        line_of_code=(line_of_code.
                                replace("super.__del__","{0}::__del__".format(parent_classname))
                        )
                if within_constructor:
                    if indent is not None:
                        #yield indent-1,line_of_code[1:],comment,other_info
                        init_lines.append((indent-1,line_of_code[1:],comment,other_info))
                        if "__init__" in line_of_code:
                            for line in initialized_members:
                                #yield line
                                init_lines.append(line)
                    else: # this is a continuation line for method declaration
                        #yield None,line_of_code[1:],comment,other_info
                        init_lines.append((None,line_of_code[1:],comment,other_info))
                else:
                    if indent is not None:
                        #yield indent-1,line_of_code[1:],comment,other_info
                        if not within_next_method:
                            methods_lines.append((indent-1,line_of_code[1:],comment,other_info))
                        else:
                            if 'yield' in line_of_code:
#                              'yield ttttt' should become
#                               self._state = 1; /* so we will come back to LABEL1 */
#                               return ttttt;
#                               LABEL1:; /* resume control straight after the return */
                                yieldnum +=1
                                methods_lines.append((indent-1,"","\t"*(indent-1)+"//start of yield #%d"% yieldnum,{}))
                                methods_lines.append((indent-1,"\t"*(indent-1)+"self._state=%d"% yieldnum,comment,other_info))
                                if line_of_code.split()[1:]:
                                    if line_of_code.split()[1]=='None':
                                        line_of_code=line_of_code.replace('None','NULL')
                                        methods_lines.append((indent-1,"\t"*(indent-1)+"self._valid_output=false","",{}))
                                    else:
                                        methods_lines.append((indent-1,"\t"*(indent-1)+"self._valid_output=true","",{}))
                                line_of_code=line_of_code.replace('yield','return')
                                methods_lines.append((indent-1,line_of_code[1:],"",other_info))
                                methods_lines.append((indent-1,"\t"*(indent-1)+"LABEL%d:"% yieldnum,";",other_info))
                                methods_lines.append((indent-1,"","\t"*(indent-1)+"//end of yield #%d\n"% yieldnum,{}))
                            elif 'return' in line_of_code:
#                              'return ttttt' should become
#                               self._exhausted = true; /* so we will not come back to LABEL1 */
#                               return ttttt;
                                methods_lines.append((indent-1,"\t"*(indent-1)+"self._valid_output=false","",other_info))
                                methods_lines.append((indent-1,"\t"*(indent-1)+"self._exhausted=true","",other_info))
                                methods_lines.append((indent-1,line_of_code[1:],"",other_info))
                            else:
                                methods_lines.append((indent-1,line_of_code[1:],comment,other_info))
                    else: # this is a continuation line for method declaration
                        #yield None,line_of_code[1:],comment,other_info
                        methods_lines.append((None,line_of_code[1:],comment,other_info))

@Pipe
def entering_scope(level):
    previous_indentation=0
    G.symbol_table.enter_scope()
    for indent,line_of_code,comment,other_info in level:
        #print "9999999999999999999999", line_of_code
        if indent is not None:
            if indent>previous_indentation:
                #print "entering scope ",line_of_code,G.symbol_table
                G.symbol_table.enter_scope()
            previous_indentation=indent
        yield indent,line_of_code,comment,other_info

@Pipe
def leaving_scope(level):
    previous_indentation=0
    #G.symbol_table.leave_scope()
    for indent,line_of_code,comment,other_info in level:
        if indent is not None:
            if indent<previous_indentation:
                #print "leaving scope ", line_of_code, indent, previous_indentation,G.symbol_table
                #print "leaving scope ", line_of_code, "|", G.symbol_table
                G.symbol_table.leave_scope()
            previous_indentation=indent
        yield indent,line_of_code,comment,other_info

def make_stdlib_files(feature):
    if feature=="DEFAULT PARAMETERS":
        stdlib_file="STDLIB/preprocessor.h"
    if feature=="std::linkedlist":
        stdlib_file="STDLIB/linkedlist.cxx"
    elif feature=="std::string":
        stdlib_file="STDLIB/string.cxx"
    elif feature=="std::dict":
        stdlib_file="STDLIB/dict.cxx"
    elif feature=="std::fifo":
        stdlib_file="STDLIB/fifo.cxx"
    elif feature=="std::file":
        stdlib_file="STDLIB/file.cxx"
    elif feature=="std::priorityqueue":
        stdlib_file="STDLIB/priorityqueue.cxx"
    elif feature=="std::reactor":
        stdlib_file="STDLIB/reactor.cxx"
    elif feature=="std::task":
        stdlib_file="STDLIB/task.cxx"
    elif feature=="std::channel":
        stdlib_file="STDLIB/channel.cxx"
    includefile=stdlib_file.replace('cxx','h')
    G.forward_declarations.append('#include "{}"'.format(includefile))
    if not os.path.exists(stdlib_file):
        write_stdlib_files_to_disk(stdlib_file)

def write_stdlib_files_to_disk(file):
    import zipfile
    from os.path import dirname, join
    mystdlib_in_same_directory=join(dirname(__file__), "STDLIB.zip")
    zf = zipfile.ZipFile(mystdlib_in_same_directory)
    #print zf.namelist()
    assert file in zf.namelist(), "file {} not found in STDLIB".format(file)
    zf.extract(file)

#feature=="DESIGNATED_NEW"
#define D_NEW(T,...) memcpy(malloc(sizeof(T)),&(T const){__VA_ARGS__},sizeof(T))


def transform(line):
    myxsplit22=lambda s: xsplit(s,'if','<<','<',"=",':',' ')
    mline=myxsplit22(line)
    #print mline
    if mline.count('<')==2:
        idx1=mline.index("<")
        idx2=mline.index("<",idx1+1)
        if 'and' in mline[idx1:idx2]:
            return line
        if 'or' in mline[idx1:idx2]:
            return line
        #print "idx1=",idx1
        #print "idx2=",idx2
        if mline[idx1+1]=='=':
            mline[idx2:idx2]=[' and ']+mline[idx1+2:idx2]
        else:
            mline[idx2:idx2]=[' and ']+mline[idx1+1:idx2]
        #print mline
        line= ''.join(mline)
    return line

if __name__=="__main__":
    line="if a < 5 < b:"
    #line="if a < 5  and c < b:"
    #line="if a << b:"
    #print transform(line)
    #raise SystemExit

@Pipe
def translate_keywords(level):
    threaded_decl=False
    myxsplit=lambda s: xsplit(s,',','.',':','=>','=',' ','\t','(',')','[',']','->')
    for indent,line_of_code,comment,other_info in level:
        #print '##############################'
        #print line_of_code
        line_of_code=transform(line_of_code)
        #print myxsplit(line_of_code)
        mysplitted_lineofcode=myxsplit(line_of_code)
        extraline=None
        extraline_indented=None
        volatile=False
        object_with_destructor=False
        # "with new File() as f:" construct
        if is_sublist(['with','new'],mysplitted_lineofcode):
            colon_idx=mysplitted_lineofcode.index(':')
            #print "============>",mysplitted_lineofcode[:colon_idx+1] #
            mysplitted_lineofcode= mysplitted_lineofcode[:colon_idx+1]
            with_idx=mysplitted_lineofcode.index('with')
            mysplitted_lineofcode[with_idx]='for'
            variable=mysplitted_lineofcode[-2]
            var_type=mysplitted_lineofcode[with_idx+4]
            if mysplitted_lineofcode[with_idx+5]=="=": # we have our own allocator 'with new int=mymalloc as var:'
                mysplitted_lineofcode[with_idx+2:with_idx+5]=[var_type+'* ',variable]
                mysplitted_lineofcode[-5:]=[', enter=1','; ','enter; ','free(',variable,'), enter=0',':']
            else: # the more general case
                mysplitted_lineofcode[with_idx+2:with_idx+2]=[variable]+[':','=']
                #mysplitted_lineofcode[-5:]=[';',variable,';','delete',' ',variable,',',variable,'=0',':']
                mysplitted_lineofcode[-5:]=[', enter=1','; ','enter; ','delete',' ',variable,', enter=0',':']
            #print "after-------->",mysplitted_lineofcode
        if G.mode=='c' and is_sublist(['new'],mysplitted_lineofcode) and not (
                        is_sublist([':',':','new'],mysplitted_lineofcode) and
                            not is_sublist(['=','new'],mysplitted_lineofcode)):
            type_inference=False
            if is_sublist([':','=','new'],mysplitted_lineofcode):
                type_inference=True
            idx=mysplitted_lineofcode.index('new')
            afternew=filter(lambda x:x not in string.whitespace,mysplitted_lineofcode[idx+1:])
            classname= afternew[0]
            #print "vvvvv ",classname,mysplitted_lineofcode
            if classname=="struct":
                classname= "".join(mysplitted_lineofcode[idx+1:])
                mysplitted_lineofcode[idx+1:]=[classname]
                #print "vvvvv ",classname
            #print 'CLASSNAME=', classname
            #print "rrrrr ",mysplitted_lineofcode
            if is_sublist([':',':'],mysplitted_lineofcode[:idx]):
                beforenew=filter(lambda x:x not in string.whitespace and x!='for',mysplitted_lineofcode[:idx])
            else:
                beforenew=filter(lambda x:x not in string.whitespace+':' and x!='for',mysplitted_lineofcode[:idx])
            if beforenew and beforenew[0]=='volatile':
                volatile=True
                theobject="".join(beforenew[1:-1])
            else:
                theobject="".join(beforenew[:-1])
            #print 'beforenew=', beforenew, theobject
            if theobject in mysplitted_lineofcode:
                object_idx=mysplitted_lineofcode.index(theobject)
            else:
                object_idx=0
            #print 'the object=', theobject
            #print 'before new=', beforenew
            #print 'after new=', afternew
            if afternew[1:] and ('[' in afternew[1:3]) and ']' in afternew:
                mtype= ' '.join(afternew[:afternew.index('[')])
                #print "ffff ",mysplitted_lineofcode
                mtypeidx=mysplitted_lineofcode.index(mtype)
                if afternew.count('[')==1:
                    # a=new int[100]  ==> a=malloc(100*sizeof(int))
                    # a=new int[100]  ==> a=calloc(100,sizeof(int))
                    msize_itv= afternew[afternew.index('[')+1:afternew.index(']')]
                    msize= "".join(msize_itv)
                    #print "msize=",msize
                    #print "msize_itv=",msize_itv
                    #print "###########################" # zzzzzzzzzzzzz
                    msizeidx1=mysplitted_lineofcode.index(msize_itv[0],mtypeidx)
                    msizeidx2=mysplitted_lineofcode.index(msize_itv[-1],mtypeidx)
                    mysplitted_lineofcode[msizeidx1-1:msizeidx2+1]=[]
                    #mysplitted_lineofcode[mtypeidx-2:mtypeidx+2]='malloc(%s*sizeof(%s))'%(msize,mtype)
                    mysplitted_lineofcode[mtypeidx-2:mtypeidx+2]=["calloc(%s,sizeof(%s))"%(msize,mtype)]
                    #print 'type and size=', 'malloc(%s*sizeof(%s))'%(msize,mtype)
                    # check if an initializer is present
                    #print 'kkkkk=',mysplitted_lineofcode[mtypeidx-1:]
                    if '=' in mysplitted_lineofcode[mtypeidx-1:]:
                        eq_idx=mysplitted_lineofcode.index('=',mtypeidx-1)
                        mysplitted_lineofcode[eq_idx]=", "
                        if 'return' in filter(lambda x:x!='\t',mysplitted_lineofcode)[0:1]:
                            retidx=mysplitted_lineofcode.index("return")
                            mysplitted_lineofcode[retidx]="return memcpy("
                            mysplitted_lineofcode[eq_idx+1:eq_idx+1]=['('+classname+'[])']
                        else:
                            mysplitted_lineofcode[eq_idx:eq_idx]=[';memcpy('+theobject]
                            mysplitted_lineofcode[eq_idx+2:eq_idx+2]=['('+classname+'[])']
                        mysplitted_lineofcode.append(", %s*sizeof(%s))"%(msize,mtype))
                else:
                    # a=new int[ROWS][COLS]  ==> int a=calloc(ROWS*COLS,sizeof(int))
                    #print 'after new=', afternew
                    #print "line of code=",mysplitted_lineofcode
                    sizes=[]
                    take=False
                    for tok in afternew:
                        if tok=='[':
                            take=True
                        elif tok==']':
                            take=False
                        elif take:
                            sizes.append(tok)
                    msize= '*'.join(sizes)
                    decl='calloc(%s,sizeof(%s))'%(msize,mtype)
                    #print "SIZES=",sizes, msize, decl
                    new_idx=mysplitted_lineofcode.index('new')
                    mysplitted_lineofcode[object_idx]= theobject+"_p"
                    mysplitted_lineofcode[new_idx:]=[decl]
                    extraline="\t"*indent+"{0} (*{1})[{2}]=({0}(*)[{2}]){1}_p".format(mtype,theobject,sizes[1])
            else:
                if is_sublist(['(','.'],mysplitted_lineofcode):
                    # obj=new Object(.a=10,.b=15)==>obj=D_NEW(Object,.a=10,.b=15)
                    new_idx=mysplitted_lineofcode.index('new')
                    mysplitted_lineofcode[new_idx:new_idx+1]=[' D_NEW(']
                    classname_idx=mysplitted_lineofcode.index(classname)
                    mysplitted_lineofcode[classname_idx:classname_idx+2]=[classname,',']
                elif '(' in afternew:
                    object_with_destructor=True
                    # obj=new Object(params) ==> obj= Object::new(params)
                    classname_idx=mysplitted_lineofcode.index(classname,idx)
                    mysplitted_lineofcode[classname_idx:classname_idx+1]=[classname,'::']
                    new_idx=mysplitted_lineofcode.index('new')
                    del mysplitted_lineofcode[new_idx]
                    mysplitted_lineofcode[classname_idx+1:classname_idx+1]=['new']
                    #print 'classname=',classname
                    #print "==================>", mysplitted_lineofcode
                else:
                    # fileobj =new FileObject ==> fileobj = malloc(sizeof(*fileobj))
                    new_idx=mysplitted_lineofcode.index('new')
                    #print 'theobject=', theobject, mysplitted_lineofcode
                    mysplitted_lineofcode[new_idx:new_idx+1]=['malloc(sizeof(*%s))'%theobject]
                    classname_idx=mysplitted_lineofcode.index(classname)
                    del mysplitted_lineofcode[classname_idx]
                    # check if an initializer is present
                    if '=' in mysplitted_lineofcode[new_idx:]:
                        eq_idx=mysplitted_lineofcode.index('=',new_idx)
                        mysplitted_lineofcode[eq_idx:eq_idx]=['; *'+theobject]
                        mysplitted_lineofcode[eq_idx+2:eq_idx+2]=['('+classname+')']
            # type inference
            #if not '.' in beforenew and not '[' in beforenew:
                # add the implicit type
            if type_inference:
                #print '====',mysplitted_lineofcode,object_idx,classname,theobject
                a="Y@R".join(mysplitted_lineofcode)
                b=a.replace(':Y@R=','Y@R=')
                mysplitted_lineofcode=b.split('Y@R')
                mysplitted_lineofcode[object_idx:object_idx]=[classname,'*',' ']
            #print 'Adding {0} of class {1} to symbol table'.format(theobject,classname), line_of_code
            G.symbol_table.add_symbol(theobject,classname)
            #print "symbol=%s, class=%s" % (theobject, G.symbol_table.get_symbol(theobject))
            #print G.symbol_table
            #print "==================>", mysplitted_lineofcode
        if G.mode=='cpp' and is_sublist(['new'],mysplitted_lineofcode) and not (
                        is_sublist([':',':','new'],mysplitted_lineofcode) and
                            not is_sublist(['=','new'],mysplitted_lineofcode)):
            type_inference=False
            idx=mysplitted_lineofcode.index('new')
            afternew=filter(lambda x:x not in string.whitespace,mysplitted_lineofcode[idx+1:])
            classname= afternew[0]
            if classname=="struct":
                classname= "".join(mysplitted_lineofcode[idx+1:])
                mysplitted_lineofcode[idx+1:]=[classname]
            #print 'CLASSNAME=', classname
            #print "rrrrr ",mysplitted_lineofcode
            if is_sublist([':',':'],mysplitted_lineofcode[:idx]):
                beforenew=filter(lambda x:x not in string.whitespace and x!='for',mysplitted_lineofcode[:idx])
            else:
                beforenew=filter(lambda x:x not in string.whitespace+':' and x!='for',mysplitted_lineofcode[:idx])
            if beforenew and beforenew[0]=='volatile':
                volatile=True
                theobject="".join(beforenew[1:-1])
            else:
                theobject="".join(beforenew[:-1])
            #print 'beforenew=', beforenew, theobject
            if theobject in mysplitted_lineofcode:
                object_idx=mysplitted_lineofcode.index(theobject)
            else:
                object_idx=0
            a="Y@R".join(mysplitted_lineofcode)
            b=a.replace(':Y@R=','Y@R=')
            mysplitted_lineofcode=b.split('Y@R')
            mysplitted_lineofcode[object_idx:object_idx]=[classname,'*',' ']

        if 'delete' in mysplitted_lineofcode and G.mode=='c':
            delegate_object=False
            # delete obj ==>  Object::free(obj)
            del_idx=mysplitted_lineofcode.index('delete')
            theobject=mysplitted_lineofcode[del_idx+2]
            if theobject=='self':
                theobject="".join(mysplitted_lineofcode[del_idx+2:del_idx+5])
                delegate_object=True
            if delegate_object:
                for klas in G.delegates_for_class:
                    if theobject in G.delegates_for_class[klas]:
                        klass=G.delegates_for_class[klas][theobject]
                        break
                else:
                    klass=None
            else:
                klass=G.symbol_table.get_symbol(theobject)
            #print "___",line_of_code, klass,theobject
            if klass is not None:
                klass=klass.rstrip(' *')
                if klass.islower():
                    mysplitted_lineofcode[del_idx:del_idx+2]=['free','(']
                else:
                    mysplitted_lineofcode[del_idx:del_idx+2]=[klass,'::','free','(']
                if delegate_object:
                    #print "dddd ", mysplitted_lineofcode
                    obj_idx=len(mysplitted_lineofcode) # NOT SURE, TEST IT !!!
                    #obj_idx=mysplitted_lineofcode.index(theobject,del_idx)
                    mysplitted_lineofcode[obj_idx:obj_idx+1]=[')']
                else:
                    obj_idx=mysplitted_lineofcode.index(theobject,del_idx)
                    mysplitted_lineofcode[obj_idx:obj_idx+1]=[theobject,')']
        polymorphic_call=False
        if '->' in mysplitted_lineofcode or ('=>' in mysplitted_lineofcode and 'print' not in mysplitted_lineofcode)or is_sublist(['self','.'],mysplitted_lineofcode):
            #print "IIIIIIIIIIIIIIIIII", G.symbol_table
            p_idx=9999
            obj=None
            delegate_object=False
            if '->' in mysplitted_lineofcode:
                # f->check() becomes FileChecker::check(f)
                p_idx=mysplitted_lineofcode.index('->')
                obj=mysplitted_lineofcode[p_idx-1]
                #print "OBJECT1=",obj,mysplitted_lineofcode,G.symbol_table #
            if '=>' in mysplitted_lineofcode and 'print' not in mysplitted_lineofcode: # POLYMORPHIC CALL !!!
                #print "OBJECT1=",obj,mysplitted_lineofcode,G.symbol_table #
                # f=>check() becomes f->check(f)
                p_idx=mysplitted_lineofcode.index('=>')
                obj=mysplitted_lineofcode[p_idx-1]
                #print "OBJECT1=",obj,mysplitted_lineofcode,G.symbol_table #
                polymorphic_call=True
            if is_sublist(['self','.'],mysplitted_lineofcode):
                p_idx2=mysplitted_lineofcode.index('self')+1
                if p_idx2< p_idx:
                    if obj:
                        obj = 'self.'+obj
                        delegate_object=True
                        #print "OBJ=",obj
                    else:
                        p_idx=p_idx2
                        obj='self'
            if delegate_object:
                pass
                #print "OBJECT2=",obj,mysplitted_lineofcode# zzzzzzzzzzzzzzz
                #print G.symbol_table
            #print "OBJECT2=",obj,mysplitted_lineofcode
            method=mysplitted_lineofcode[p_idx+1]
            #print "method=", method
            #print G.class_symbol_table
            #print "object=",obj, method
            if delegate_object:
                for klas in G.delegates_for_class:
                    if obj in G.delegates_for_class[klas]:
                        klass=G.delegates_for_class[klas][obj]
                        break
                else:
                    klass=None
            else:
                klass=G.symbol_table.get_symbol(obj)
            if klass:
                klass=klass.rstrip(' *')
            #print "klass=",klass,mysplitted_lineofcode[p_idx+2:],G.symbol_table
            #following is buggy if call is made with space as in "Z->encode ()"
            if klass is not None and mysplitted_lineofcode[p_idx+2:] and mysplitted_lineofcode[p_idx+2]=='(' :
                klass_methods,parent_klass=G.class_symbol_table.get(klass,([],None))
                #print "====",obj,klass,klass_methods,parent_klass
                found=False
                for meth_name,meth_proto,meth_type in klass_methods:
                    if meth_name==method:
                        found=True
                        break
                if not found:
                    meth_type=REAL
                #print "found=",found,meth_type
                if meth_type>=OVERRIDE or polymorphic_call: # only add param to polymorphic calls
                    # c->process() ==> c->process(c)
                    add_implicit_this=True
                    #print "_____________hhh"
                    myklass=None
                else:
                    if found or klass not in G.class_symbol_table: # found in the base class
                        myklass=klass
                    else: # assume it is in the parent class (NOT ROBUST!)
                        myklass=parent_klass
                    #print "ddddddddd", obj, mysplitted_lineofcode
                    #print "MYKLASS=", myklass,mysplitted_lineofcode,p_idx #zzzzzzzzzzz
                    if myklass:
                        if delegate_object:
                            mysplitted_lineofcode[p_idx-3:p_idx+1]=[myklass,'::']
                        else:
                            mysplitted_lineofcode[p_idx-1:p_idx+1]=[myklass,'::']
                        add_implicit_this=True
                    else:
                        add_implicit_this=False
                if add_implicit_this:
                    if myklass is not None and myklass!=klass:
                        casted_obj="({0}*){1}".format(myklass,obj)
                    else:
                        casted_obj=obj
                    lpar_idx=mysplitted_lineofcode.index('(',p_idx)
                    rpar_idx=mysplitted_lineofcode.index(')',p_idx)
                    if rpar_idx==lpar_idx+1:
                        mysplitted_lineofcode[lpar_idx+1:lpar_idx+1]=[casted_obj]
                    else:
                        mysplitted_lineofcode[lpar_idx+1:lpar_idx+1]=[casted_obj,',']
                    if polymorphic_call:
                        ass_idx=mysplitted_lineofcode.index('=>')
                        mysplitted_lineofcode[ass_idx]='->'
            elif polymorphic_call:
                # add implicit this
                #print "------------------------",mysplitted_lineofcode
                lpar_idx=mysplitted_lineofcode.index('(',p_idx)
                rpar_idx=mysplitted_lineofcode.index(')',p_idx)
                if rpar_idx==lpar_idx+1:
                    mysplitted_lineofcode[lpar_idx+1:lpar_idx+1]=[obj]
                else:
                    mysplitted_lineofcode[lpar_idx+1:lpar_idx+1]=[obj,',']
                ass_idx=mysplitted_lineofcode.index('=>')
                mysplitted_lineofcode[ass_idx]='->'

        #print mysplitted_lineofcode
        # Transforms string comparison into startswith construct !!!
        if is_sublist(['=','='],mysplitted_lineofcode):
            idx_st=mysplitted_lineofcode.index('=')
            idx = idx_st+1
            if mysplitted_lineofcode[idx]=='=':
                #print mysplitted_lineofcode, idx
                idx += 1
                while True:
                    next_word= mysplitted_lineofcode[idx]
                    if next_word in (' ','\t'):
                        idx += 1
                        continue
                    if next_word.startswith('"'):
                        mysplitted_lineofcode[idx_st:idx_st+idx-idx_st]=[".","startswith","("]
                        mysplitted_lineofcode[idx+2:idx+2]=[')']
                        #print mysplitted_lineofcode
                    break
        if is_sublist(['.','append','('],mysplitted_lineofcode):
            # array.append(xx) ==> append(array,xx)
            idx_st=mysplitted_lineofcode.index('append')
            mysplitted_lineofcode[idx_st-2:idx_st-2]=['append(']
            mysplitted_lineofcode[idx_st:idx_st+3]=[',']
        if is_sublist(['.','pop','('],mysplitted_lineofcode):
            # a=array.pop() ==> a=pop(array)
            idx_st=mysplitted_lineofcode.index('pop')
            mysplitted_lineofcode[idx_st-2:idx_st-2]=['pop(']
            mysplitted_lineofcode[idx_st:idx_st+3]=[]
        if is_sublist(['.','startswith','('],mysplitted_lineofcode):
            idx_st=mysplitted_lineofcode.index('startswith')
            mysplitted_lineofcode[idx_st-2:idx_st-2]=['strncmp(']
            mysplitted_lineofcode[idx_st:idx_st+3]=[',']
            mysplitted_lineofcode[idx_st+2:idx_st+3]=[',strlen({}))==0'.format(mysplitted_lineofcode[idx_st+1])]
        #print "==",mysplitted_lineofcode
        if 'volatile' in filter(lambda x:x!='\t',mysplitted_lineofcode)[0:1]:
            #print mysplitted_lineofcode
            volatile_idx=mysplitted_lineofcode.index('volatile')
            classname=mysplitted_lineofcode[volatile_idx+2]
            vol=classname.endswith('*')
            vol=vol or "*" in mysplitted_lineofcode[volatile_idx+3:volatile_idx+5]
            if vol and '=' in mysplitted_lineofcode:
                classname=classname.strip('*')
                object_idx=mysplitted_lineofcode.index('=',volatile_idx+2)
                #if is_sublist(['::','new'],mysplitted_lineofcode):
                #if classname.capitalize()==classname:  !!!!
                if classname[0].isupper(): # much better !!!!
                    object_with_destructor=True
                else:
                    object_with_destructor=False
                if object_with_destructor:
                    destructor=" __attribute__((cleanup(free_{})))".format(classname)
                    inline_destructor="static inline void free_{0}({0} **fp) {{ if (*fp) {0}_free(*fp); }}".format(classname)
                else:
                    destructor=" __attribute__((cleanup(free_{})))".format(classname)
                    inline_destructor="static inline void free_{0}({0} **fp) {{ if (*fp) free(*fp); }}".format(classname)
                #print "destructor=",destructor
                #print "inline destructor=", inline_destructor
                if inline_destructor not in G.forward_declarations:
                    G.forward_declarations.append(inline_destructor)
                mysplitted_lineofcode[object_idx:object_idx]=[destructor]
                mysplitted_lineofcode=mysplitted_lineofcode[2:]
                #print "dddddddddddddddddddddddddddddddd"
        if 'for' in filter(lambda x:x!='\t',mysplitted_lineofcode)[0:1]:
            for_idx=mysplitted_lineofcode.index('for')
            if 'in' in mysplitted_lineofcode[for_idx+1:]:
                in_idx=mysplitted_lineofcode.index('in',for_idx+1)
                #print 'iiiiii', mysplitted_lineofcode, for_idx,in_idx
                loop_var="".join(mysplitted_lineofcode[for_idx+1:in_idx]).lstrip()
                gen_var="".join(mysplitted_lineofcode[in_idx+1:]).rstrip().strip(':')
                #print "loop var=", loop_var
                gen_klass=G.symbol_table.get_symbol(gen_var.strip())
                #print "gen klass=",gen_klass #, gen_var
                #       for int x in gen:  ==>
                #       while not gen->exhausted:
                #           int x= gen->next()
                if gen_klass and gen_klass[0].isupper() and not gen_klass[-1]=='*':
                    mysplitted_lineofcode[for_idx:for_idx+1]=['while (true)']
                    mysplitted_lineofcode[for_idx+2:]=[':']
                    #print "loop var= ", loop_var,gen_klass, gen_var
                    extraline_indented="\t"*(indent+1)+loop_var+'='+gen_klass+'_next('+gen_var.strip()+')'
                    extraline_indented += "; if ({}->_exhausted) break".format(gen_var.strip())
                    #print 'newline=',extraline_indented
                else: # we assume an array
                    # for char* st in arr:
                    #      pass
                    # becomes
                    # for int i=1;i<=arr[0];i++:
                    #      char*st = arr[i]
                    decl1="#define append(sp, n) sp[++*(int*)sp] = (n)"
                    decl2="#define pop(sp) sp[--*(int*)sp+1]"
                    decl3="#define insert(sp,n,i) (*(((void**)memmove(&sp[i+1],&sp[i],sizeof(void*)*(1-i+(*(int*)sp)++)))-1))=(n)"
                    decl4="#define remove(sp,i) (*(((void**)memmove(&sp[i],&sp[i+1],sizeof(void*)*(1-i+(*(int*)sp)--)))-1))"
                    if decl1 not in G.forward_declarations:
                        G.forward_declarations.append(decl1)
                    if decl2 not in G.forward_declarations:
                        G.forward_declarations.append(decl2)
                    if decl3 not in G.forward_declarations:
                        G.forward_declarations.append(decl3)
                    if decl4 not in G.forward_declarations:
                        G.forward_declarations.append(decl4)
                    if gen_var.rstrip().endswith('.reversed'):
                        gen_var=gen_var.rstrip()[:-9]
                        mysplitted_lineofcode[for_idx:for_idx+1]=['for int i={}[0];i>0;i--'.format(gen_var)]
                    else:
                        mysplitted_lineofcode[for_idx:for_idx+1]=['for int i=1;i<={}[0];i++'.format(gen_var.strip())]
                    mysplitted_lineofcode[for_idx+2:]=[':']
                    #print "loop var= ", loop_var,gen_klass, gen_var
                    obj_klass=loop_var.split('*')[0:1]
                    if loop_var.split('*')[1:]:
                        obj_name=loop_var.split('*')[1].strip()
                        #print "zzzzzzzzz obj klass=", obj_klass[0],"!obj name=",obj_name
                        G.symbol_table.add_symbol(obj_name,obj_klass[0])
                    extraline_indented="\t"*(indent+1)+loop_var+'='+gen_var+'[i]'
        line_of_code="".join(mysplitted_lineofcode)
        #print "----------------", line_of_code
        if is_sublist([':','=','reshape'],mysplitted_lineofcode):
            # b := reshape(a,2,5) ==>int (*b)[5]=(int(*)[5])a_p
            #print "rrrrrrrrrrrrrrr",mysplitted_lineofcode
            filtered=filter(lambda x:x not in ' \t',mysplitted_lineofcode)
            #print filtered
            #print G.symbol_table
            ttype_idx1=mysplitted_lineofcode.index('reshape')
            ttype_idx2=mysplitted_lineofcode.index(',',ttype_idx1)
            ttype= filter(lambda x:x not in ' \t',mysplitted_lineofcode[ttype_idx1+2:ttype_idx2])
            var=filtered[0]
            coldim=filtered[-2]
            pointer=filtered[-6]
            mytype=G.symbol_table.get_symbol(pointer)
            line_of_code='\t'*mysplitted_lineofcode.count('\t')
            line_of_code+="{0} (*{1})[{2}]=({0}(*)[{2}]){3}_p".format(mytype,var,coldim,pointer)
            #print "====",line_of_code
        if "@threaded" in line_of_code:
            G.forward_declarations.append('#include "cxx_thread.h"')
            threaded_decl=True
            continue
        if threaded_decl:
            threaded_decl=False
            method_nam=line_of_code.split('(')[0].split()[-1]
            decl="#define {0}(...)  Thread_new({0},__VA_ARGS__)".format(method_nam)
            G.forward_declarations.append(decl)
        # nice numbers in the style 111_000_000+55_000
        nice_number_pattern= r'\b[1-9][0-9_]*[lL]?\b'
        #line_of_code= "value=111_000_000+55_000"
        matches= re.findall(nice_number_pattern, line_of_code)
        for m in matches:
            line_of_code=line_of_code.replace(m,m.replace("_",""))
        line_of_code=re.sub(r'\bpass\b', '// empty statement !!!',line_of_code)
        if G.mode=='c':
            line_of_code=re.sub(r'\bnamespace\b', 'struct',line_of_code)
        line_of_code=re.sub(r'\Aimport ', '#include ',line_of_code)
        line_of_code=re.sub(r'\b__init__\b', 'constructor',line_of_code)
        line_of_code=re.sub(r'\b__del__\b', 'destructor',line_of_code)
        line_of_code=re.sub(r'\bforever\b', 'for ;;',line_of_code)
        line_of_code=re.sub(r'\bklass\b', 'struct',line_of_code) # public inheritance by default
        # replace and, or and not by &&, || and !
        line_of_code=re.sub(r'\b not \b', ' !',line_of_code)
        line_of_code=re.sub(r' not [(]', ' !(',line_of_code)
        if "and" in line_of_code:
            idx=line_of_code.index("and")
            if line_of_code[:idx].count('"') % 2 ==0:
                line_of_code=re.sub(r'\band\b', ' && ',line_of_code)
        if "or" in line_of_code:
            idx=line_of_code.index("or")
            if line_of_code[:idx].count('"') % 2 ==0:
                line_of_code=re.sub(r'\bor\b', ' || ',line_of_code)
        line_of_code=re.sub(r'\bexhausted\b', '_exhausted',line_of_code)
        line_of_code=re.sub(r'\bvalid_output\b', '_valid_output',line_of_code)
        if line_of_code.strip().startswith(('case','default')):
            #if line_of_code.rstrip().endswith('::'):
            line_of_code=line_of_code.replace("::",": :")
            #else:
            #   line_of_code=line_of_code.replace(":",": :")
        else:
            if G.mode=='c':
                line_of_code=line_of_code.replace("::","_") #.replace('self.super.','this->super.')
        # ALTERNATIVE IS TO REPLACE self BY (*this)
        # ESPECIALLY FOR C++ code where self.attr becomes (*this).attr
        line_of_code=re.sub(r'\bself\b[.]', 'this->',line_of_code)
        #line_of_code=re.sub(r'\bsuper\b[.]', 'super->',line_of_code)
        line_of_code=re.sub(r'\bprint\b', 'fprintf stderr,',line_of_code)
        line_of_code=re.sub(r'\bself\b', 'this',line_of_code)
        line_of_code=re.sub(r'\bother\b[.]', 'other->',line_of_code)
        line_of_code=re.sub(r'\bTrue\b[.]', 'true',line_of_code)
        line_of_code=re.sub(r'\bFalse\b[.]', 'false',line_of_code)
        #if line_of_code.strip().startswith(("if ","else if ")):
        #   line_of_code=line_of_code.replace("if ","if (")
        #   line_of_code=line_of_code[::-1].replace(":",")",1)[::-1]
        if line_of_code.strip().startswith("elif "):
            line_of_code=line_of_code.replace("elif ","else if ")
        #   line_of_code=line_of_code[::-1].replace(":",")",1)[::-1]
        if line_of_code.strip().startswith("while "):
            if not line_of_code.strip().startswith("while ("):
                #print "1===>", line_of_code
                line_of_code=line_of_code.replace("while ","while (")
                #print "2===>", line_of_code
                if line_of_code.rstrip().endswith(":"):
                    line_of_code=line_of_code.rstrip().replace(":",")",1)
                else:
                    line_of_code=line_of_code.rstrip()+")"
                #line_of_code=line_of_code[::-1].replace(":",")",1)[::-1]
                #print "3===>", line_of_code
        if line_of_code.strip().startswith("for "):
            line_of_code=line_of_code.replace("for ","for (")
            line_of_code=line_of_code[::-1].replace(":",")",1)[::-1]
        if line_of_code.strip().startswith("switch "):
            line_of_code=line_of_code.replace("switch ","switch (")
            line_of_code=line_of_code[::-1].replace(":",")",1)[::-1]
        line_of_code=line_of_code.replace('int main(','STATIC int main(')
        line_of_code=line_of_code.replace('void main(','STATIC void main(')
        line_of_code=line_of_code.replace('def main(','STATIC int main(')
        # add assert for all pointer dereferencing
        if '->' in line_of_code:
            idx=-1
            while True:
                idx=line_of_code.find('->',idx+1)
                if idx==-1: break
                #print "idx=",idx
                obj_idx_space=line_of_code[:idx].find(' ')
                obj_idx_tab=line_of_code[:idx].find('\t')
                #obj_idx_paren=line_of_code[:idx].find('(')
                obj_idx_paren= -1
                #print obj_idx_space,obj_idx_tab,obj_idx_paren, line_of_code
                obj_idx=max(obj_idx_space,obj_idx_tab,obj_idx_paren)
                obj_idx=max(obj_idx,0)
                pointer_var=line_of_code[obj_idx:idx]
                #print "POINTER VAR=",pointer_var
                if G.ASSERT_MODE:
                    yield indent,'assert {} and "NULL POINTER DERERENCING"'.format(pointer_var.strip()),'',{}
        line_of_code=add_parens(line_of_code)
        yield indent,line_of_code,comment,other_info
        if extraline:
            yield indent,extraline,'',{}
        if extraline_indented:
            yield indent+1,extraline_indented,'',{}

def add_parens(line_of_code):
    # TODO: add for, switch
    myxsplit=lambda s: xsplit(s,',','.',':','=',' ','\t','(',')','[',']','->')
    splitted_line=myxsplit(line_of_code.rstrip())
    paren_less_functions=('printf','sprintf','vsprintf','snprintf','fflush','if',
        'fprintf','puts','assert','perror','YIELD','yield','STOP_YIELD','println',
        'RAISE', 'free','sscanf', 'exit', 'BREAK', "while")
    #print "BEFORE===>",splitted_line
    for fun_name in paren_less_functions:
        if fun_name in splitted_line: # printf without ()
            fun_idx=splitted_line.index(fun_name)
            if splitted_line[fun_idx+1:] and splitted_line[fun_idx+1]in '()':
                continue # avoid __attribute__((cleanup(free)))=... and free(..
            rest_of_line=filter(lambda x:x not in ' :',splitted_line[fun_idx+1:])
            if not rest_of_line:
                break
            if rest_of_line[0]=='(':
                stack=['(']
                exp_len=len(rest_of_line)-2
                for i,tok in enumerate(rest_of_line[1:]):
                    if tok=='(':
                        stack.append('(')
                    if tok==')':
                        stack.pop()
                        if len(stack)==0:
                            break
                #print "LEN STACK=",i, exp_len
                rline=''.join(rest_of_line[1:-1])
                if i==exp_len:
                    # no need to add parens
                    break
            splitted_line[fun_idx+1]=' ('
            if splitted_line[-1]==":":
                splitted_line[-1:-1]=[')']
            else:
                splitted_line.append(')')
            break
    else: # not found, return
        return line_of_code
    line_of_code="".join(splitted_line)
    #print "AFTER ===>",splitted_line
    return line_of_code

if __name__=="__main__":
    source_text='while (m = num_elems * 2) < self.num_elems :'
    #source_text="if (n1==n2) or (n3==n4):"
    #source_text='if (strcmp(arg,"-f") == 0) || (strcmp(arg,"-f1") == 0)'
    #source_text='if (a < b)'
    #print add_parens(source_text)
    #raise SystemExit

@Pipe
def process_MainClass(level):
    within_main_class=False
    within_methods=False
    within_enums=False
    within_defines=False
    main_class_lines=[] # these have to go at the beginning of the file
    enum_defines_lines=[] # # these have to go at the beginning of the file
    methods_lines=[] # these are the methods that have to go at the end of the file
    first_comment=None
    for indent,line_of_code,comment,other_info in level:
        if indent==0:# state changes can only occur at indent 0
            if within_main_class: # main class ends
                within_main_class=False
                # THESE SHOULD GO AT THE BEGINNING OF THE FILE
                G.global_declarations=process_enum(enum_defines_lines)
                g_enums_defines=process_enum(enum_defines_lines)
                #print G.global_declarations
                #print enum_defines_lines
                #print "========================"
                #print "main=====",main_class_lines
                main_class_lines.append( (0, '', '', {}))  # add an empty line
                g_struct_decl=[]
                g_struct_init=[]
                container=g_struct_decl
                for line in (main_class_lines>>process_namespaces>>add_braces):
                    #print "===>",line
                    if "struct G {" in line:
                        line= line.replace("struct G {","struct GG {")
                    if line.startswith("G="):
                        container.append("G")
                        container=g_struct_init
                        container.append("={")
                        G.global_declarations.append(line.rstrip())
                        continue
                    container.append(line.rstrip())
                    G.global_declarations.append(line.rstrip())
                #print "g_struct_decl=",g_struct_decl
                #print "g_struct_init=",g_struct_init
                headerfiles=needed_header_files("\n".join(g_struct_decl))
                headerfiles=['#include <{}>'.format(fil) for fil in headerfiles]
                #print "HEADER FILES=", "\n".join(headerfiles)
                globals_h_contents=globals_h_template.format(
                                    "\n".join(headerfiles),
                                    "\n".join(g_enums_defines),
                                    "\n".join(g_struct_decl),
                                    "\n".join(g_struct_init))
                #print globals_h_contents
                #print "========================"
                with file("globals.h",'w') as f:
                    f.write(globals_h_contents)
                I_WANT_TO_USE_GLOBALS_DOT_H_FILE=True
                if I_WANT_TO_USE_GLOBALS_DOT_H_FILE:
                    G.global_declarations=[]
                    # these have to appear AFTER the typedefs !!!
                    # #define _MAIN_C_ added in make.py
                    G.global_declarations.append('#include "globals.h" ')
                for line in methods_lines:
                    yield line
            if not within_main_class:
                if line_of_code.lstrip().startswith("class G:"):
                    within_main_class=True
                    ###############
                    main_class_lines.append((0,"namespace G:",comment,other_info))
                    continue
        if within_main_class and indent==1:# state changes (for within_methods) can only occur at indent 1
            if not line_of_code.lstrip() and comment:
                if not first_comment:
                    first_comment=(indent-1,line_of_code[1:],comment,other_info)
                    continue
            if line_of_code.lstrip().startswith('enum'):
                within_enums=True
            else:
                within_enums=False
            if line_of_code.lstrip().startswith('#'):
                within_defines=True
            elif not (not line_of_code.lstrip() and comment):
                within_defines=False
            if not within_enums and not within_defines:
                if  '(' in line_of_code and ')' in line_of_code:
                    within_methods=True # we are done with the attributes
        # NOW THAT WE HAVE HANDLED THE STATE CHANGES, LET US PROCESS THE LINES
        if not within_main_class:
            yield indent,line_of_code,comment,other_info
        else: # we are within the main class
            if not within_methods and not within_enums and not within_defines:
                if first_comment:
                    main_class_lines.append((first_comment[0]+1,'\t',
                                            first_comment[2],first_comment[3]))
                    first_comment=None
                # declaration of instance variables
                main_class_lines.append((indent,line_of_code,comment,other_info))
            elif within_enums or within_defines:
                if first_comment:
                    enum_defines_lines.append(first_comment)
                    first_comment=None
                enum_defines_lines.append((indent-1,line_of_code[1:],comment,other_info))
            elif within_methods:
                if indent==1: # we are in the declaration part of the method
                    in_constructor_decl=False
                    if line_of_code.lstrip().startswith("public def __init__("):
                        line_of_code=line_of_code.replace("public def __init__(","public int mainloop(")
                        in_constructor_decl=True
                        G.PUBLIC_MAIN_CONSTRUCTOR=True
                    elif "def __init__(" in line_of_code:
                        line_of_code=line_of_code.replace("def __init__(","int main(")
                        in_constructor_decl=True
                    if "def __del__(" in line_of_code:
                        line_of_code=line_of_code.replace("def __del__(","void G::destructor(void")
                    line_of_code=line_of_code.replace("def ","void G::")
                if indent:
                    methods_lines.append((indent-1,line_of_code[1:],comment,other_info))
                else:
                    methods_lines.append((None,'',comment,other_info))
                if in_constructor_decl:
                    methods_lines.append((1,"\tatexit(G::destructor)","//comment",{}))
                    in_constructor_decl=False

@Pipe
def process_namespaces(lines):
    within_namespace=False
    within_nested_namespace=False
    initialized_lines=[]
    name_of_namespace=None
    indent_str='\t'
    for indent,line_of_code,comment,other_info in lines:
        if indent==0:
            if within_namespace:
                within_namespace=False
                if initialized_lines:
                    yield 0, name_of_namespace.strip().replace(':','=:'),"", {}
                else:
                    yield 0, "struct {0} {0}".format(name_of_namespace.strip().replace(':','')),"", {}
                for line in initialized_lines:
                    if line.startswith("START_NAMESPACE"):
                        indent_str="\t\t"
                        message="{ // %s" % line.strip(':').replace("START_","")
                        yield 1,indent_str+message,"",{}
                        continue
                    if line=="END_NAMESPACE":
                        yield 1,indent_str+"}","",{}
                        indent_str="\t"
                        continue
                    yield 1,indent_str+line,"",{}
            else:
                if line_of_code.lstrip().startswith("namespace "):
                    within_namespace=True
                    name_of_namespace=line_of_code.partition('namespace')[2]
                    #print 'name=', name_of_namespace
                    yield indent,line_of_code.replace('namespace',"struct"),comment,other_info
                    continue
        if indent==1:
            if within_nested_namespace:
                within_nested_namespace=False
                initialized_lines.append("END_NAMESPACE")
            if not within_nested_namespace:
                if line_of_code.lstrip().startswith("namespace"):
                    _,_,nested_name=line_of_code.partition('namespace')
                    within_nested_namespace=True
                    initialized_lines.append("START_NAMESPACE %s" % nested_name.strip(':'))
        if within_namespace:
            sp=line_of_code.split('=')
            if len(sp)>1:
                #print '====>',sp
                line=(".{}={}".format(sp[0]
                                        .split()[-1]
                                        .split('[')[0]
                                        .lstrip()
                                        .lstrip('*'),sp[1]))
                #print 'QQ====>',line
                initialized_lines.append(line)
            yield indent,sp[0],comment,other_info
        else:
            yield indent,line_of_code,comment,other_info

@Pipe
def build_forward_declarations(level):
    """
    builds the forward declaration for private functions
    """
    previous_indentation=0
    within_function=False
    within_private_function_declaration=False
    within_doc_string=False
    function_name=""
    myiter=windows(level)
    function_declaration_line=None
    in_inline_func=False
    inline_func_lines=[]
    for previous_line, current_line, next_line in myiter:
        if previous_line:
            if previous_line[0] is not None:
                previous_indentation=previous_line[0]
            line_previous= previous_line[1]
        else:
            previous_indentation= None
            line_previous= None
        #print '===>',current_line
        current_indentation,line_of_code,comment, other_info=current_line
        if next_line:
            next_indentation= next_line[0]
            line_next=next_line[1]
        else:
            next_indentation= None
            line_next=None
        # now the processing can start
        if current_indentation==0: # state changes can only occur at indent 0
            if line_of_code.lstrip().startswith(('public inline','private inline','static inline','inline')):
                in_inline_func=True
                line_of_code='static inline '+line_of_code.split('inline',1)[1].strip()
                line_of_code=line_of_code.replace('::','_')
                inline_func_lines.append((0,line_of_code,comment,other_info))
                continue
            else:
                if in_inline_func: # end of inline function
                    mylines=[]
                    # add an empty line !!!
                    inline_func_lines.append((0,"","",{}))
                    for line in (inline_func_lines>>add_braces):
                        mylines.append(line)
                    inline_function_code="".join(mylines)
                    #print "===",inline_function_code
                    G.forward_declarations.append(inline_function_code)
                in_inline_func=False
                inline_func_lines=[]
            if within_function: # current function ends
                within_function=False
                within_private_function_declaration=False
            if not within_function: # this could be a new function
                #print "99:", line_of_code,is_function_declaration(line_of_code)
                if is_function_declaration(line_of_code):
                    within_function=True # we are done with the attributes
                    #print "ddddddd ",line_of_code
                    determine_arguments(line_of_code)
                    #print G.symbol_table
                    if '::' in line_of_code and '(self' in line_of_code:
                        classname= line_of_code[:line_of_code.index('::')].split()[-1]
                        line_of_code= line_of_code.replace('(self','('+classname+'* self')
                    if not line_of_code.lstrip().startswith('public '): # no need of fwd decl for public functions
                        within_private_function_declaration=True
        if within_function:
            if within_private_function_declaration:
                line_of_code, default_args= collect_default_arguments(line_of_code)
                fwd_decl= line_of_code
                if current_indentation is not None and not fwd_decl.lstrip().startswith('private'):
                    fwd_decl= 'private '+ fwd_decl
                if " main(" not in fwd_decl: # no need to fwd declare the main()
                    G.forward_declarations.append(fwd_decl.
                                                replace('::','_').
                                                replace(':',';').
                                                replace('___init__','_constructor').
                                                replace('___del__','_destructor').
                                                rstrip().
                                                replace('private','static',1))
                if default_args:
                    prologue, decl=declare_default_arguments(line_of_code,default_args)
                    if prologue not in G.forward_declarations:
                        G.forward_declarations.insert(0,prologue)
                    G.forward_declarations.append(decl)
                if next_indentation is not None:
                    within_private_function_declaration=False
            if current_indentation==1 and line_of_code.lstrip().startswith((SINGLE_TRIPLE_QUOTE,DOUBLE_TRIPLE_QUOTE)):
                within_doc_string= not within_doc_string
                other_info['within_doc_string']=True
            if within_doc_string:
                other_info['within_doc_string']=True
            yield current_indentation,line_of_code,comment,other_info
        else: # not within function
            if in_inline_func:
                inline_func_lines.append(current_line)
            else:
                yield current_indentation,line_of_code,comment,other_info


@Pipe
def process_private_public(level):
    previous_indentation=0
    myiter=windows(level)
    for previous_line, current_line, next_line in myiter:
        #print "==========>",previous_line, current_line, next_line
        if previous_line:
            if previous_line[0] is not None:
                previous_indentation=previous_line[0]
            line_previous= previous_line[1]
        else:
            previous_indentation= None
            line_previous= None
        current_indentation,line,comment, other_info=current_line
        if next_line:
            next_indentation= next_line[0]
            line_next=next_line[1]
        else:
            next_indentation= None
            line_next=None
        # now the processing can start
        if current_indentation==0: # global declaration
            if line.lstrip().startswith('public '):
                # bug in this line !!!
                if G.mode=='c':
                    current_line=0,line.replace('public ',''),comment,other_info
                else:
                    current_line=0,line.replace('public ','',1),comment,other_info
                # we have three choices: public function, public struct, public var
                if '(' not in line[:len(line) if line.find('=')==-1 else line.find('=')]: # either a struct or a var
                    if '=' in line: # public int myvar=10 or htonl(4545)
                        # private part: int myvar=10
                        d=other_info.copy()
                        d.update(dict(mode='PRIVATE'))
                        yield 0,line.replace('public ',''),comment,d
                        # public part: extern int myvar
                        d=other_info.copy()
                        d.update(dict(mode='PUBLIC'))
                        yield 0,'extern '+line.split('=')[0].replace('public ',''),comment,d
                    else:
                        current_line[-1]['mode']='PUBLIC'
                        yield current_line
                elif is_function_declaration(line): # a functiondeclaration
                    #print "555555555555", line
                    mylines=[copy.deepcopy(current_line)] # we shall collect the prototype
                    current_line[-1]['mode']='PUBLIC'
                    while True: # let's collect the lines of the declaration
                        current_line=current_line[0],current_line[1].rstrip().rstrip(':'),current_line[2],current_line[3]
                        #print '#### ',current_line
                        #print 'UUUU ',collect_default_arguments(current_line[1])[0]
                        #yield current_line
                        cur_line,default_args=collect_default_arguments(current_line[1])
                        if default_args:
                            prologue, decl=declare_default_arguments(cur_line,default_args)
                            for prolog in prologue.split("\n"):
                                yield 0,prolog,"",{}
                            for declar in decl.split("\n"):
                                yield 0,declar,"",{}
                        yield current_line[0],cur_line,current_line[2],current_line[3]
                        if next_indentation and next_indentation> current_indentation: # we are done
                            yield 0, '', '', {}
                            break
                        _, current_line, next_line=myiter.next()
                        mylines.append(current_line[:]) # for multiline declarations
                        current_indentation,_,_,_=current_line
                        if next_line:
                            next_indentation= next_line[0]
                        else:
                            next_indentation= None
                    mylines[0][-1]['mode']='PRIVATE'
                    #print '####',mylines zzzzzzzzz
                    mylines=[(line[0],collect_default_arguments(line[1])[0],line[2],line[3]) for line in mylines]
                    for _line_ in mylines:
                        yield _line_
                #elif line.count('(')>1 and line.count('(')==line.count(')'): # function pointer declaration
                else:
                    #print "444444444444", current_line
                    current_line[-1]['mode']='PUBLIC'
                    yield current_line
            else: # private by default
                if line.lstrip().startswith('private '):
                    if line.lstrip().startswith('private enum:'): # no static for anonymous enums!!!
                        current_line=current_line[0],current_line[1].replace('private ',''),current_line[2],current_line[3]
                    else:
                        current_line=current_line[0],current_line[1].replace('private ','static ',1),current_line[2],current_line[3]
                current_line[-1]['mode']='PRIVATE'
                yield current_line
        else:
            yield current_line

@Pipe
def add_braces(level): # this is the last level
    LBRACE="{"
    RBRACE="}"
    previous_indentation=0
    within_initializer=False
    within_struct_or_union=False
    for previous_line, current_line, next_line in windows(level):
        if previous_line:
            if previous_line[0] is not None:
                previous_indentation=previous_line[0]
            line_previous= previous_line[1]
        else:
            previous_indentation= None
            line_previous= None
        current_indentation,line,comment, other_info=current_line
        if next_line:
            next_indentation= next_line[0]
            line_next=next_line[1]
        else:
            next_indentation= None
            line_next=None
        # this treats the case of a cosmetic blank line
        if not line.strip() and not comment.strip(): # we have an empty line
            if next_indentation == previous_indentation: # we have a cosmetic blank line
                yield line+comment+"\n"
                continue
        if line_previous:
            if line_previous.lstrip().startswith(('struct','static struct','union','static union')):
                if line_previous.rstrip().endswith(':'): # AVOID SINGLE-LINE structs!!!
                    within_struct_or_union=True
            if line_previous.replace('static ','').lstrip().startswith(('enum')):
                within_initializer=True
            if line_previous.rstrip().endswith(('=:')):
                within_initializer=True
        if current_indentation is None:
            curr_indent=previous_indentation
            if next_indentation is None:
                yield line+comment+"\n"
            elif next_indentation > curr_indent : # add LBRACE
                yield line.rstrip().rstrip(":") + " "+LBRACE+" "+comment+"\n"
            else:
                if line.strip():
                    yield line+'; '+comment+"\n"
                else:
                    yield line+comment+"\n"
        else:
            if current_indentation < previous_indentation: # add RBRACE
                end_of_line=RBRACE
                if within_initializer:
                    #print "I AM HERE 1", within_struct_or_union
                    within_initializer=False
                    #within_struct_or_union=False  REMOVED THIS FOR NESTED ENUMS!!
                    end_of_line= RBRACE+";"
                elif within_struct_or_union:
                    #print "I AM HERE 2", line
                    within_struct_or_union=False
                    if not line.rstrip().endswith('=:'):
                        end_of_line=RBRACE+";"
                yield "\t"*(current_indentation+1) + end_of_line
                #if not (next_indentation < current_indentation) or next_indentation is None:
                if next_line or next_indentation is None:
                    yield '\n'
                # exceptions case, default, (public,private)
            if within_initializer:
                terminator=","
            else:
                terminator=";"
                if line.rstrip().endswith(':'):
                    terminator=''
                if line.lstrip().startswith('#'):
                    terminator=''
            if 'mode' in other_info:
                yield "MODE CHANGE {}\n".format(other_info['mode'])
            if next_indentation > current_indentation: # add LBRACE
                yield line.rstrip().rstrip(":") + " "+LBRACE+" "+comment+"\n"
                # exceptions case, default, (public,private)
            else: # add ; or ,
                if line.strip():
                    #if line.strip().endswith('='): # for multiline strings
                    #   terminator=''
                    #QUOTE=('"',';','Q')
                    #if line.strip().startswith(QUOTE) and line.strip().endswith(QUOTE):
                    #   terminator=''   # for multiline strings
                    within_braces= other_info.get('within_braces',False)
                    within_doc_string=other_info.get('within_doc_string',False)
                    if within_doc_string:
                        yield 'DOCSTRING {}\n'.format(line.strip().strip('"').strip("'"))
                    elif not within_braces:
                        yield line.rstrip() + terminator +comment+"\n"
                    else:
                        yield line +comment+"\n"
                else: # empty line at lower or equal indentation level
                    if next_indentation==current_indentation or next_indentation is None:
                        yield line + comment+"\n"
                    else:
                        if line:
                            yield line + comment +'\n'
                        else: # virtual dedent, no need for a newline
                            yield line + comment

def process_enum(lines):
    res=[]
    within_enum=False
    for indent,line_of_code,comment,other in lines:
        if within_enum:
            if indent==1:
                line_of_code += ','
            if indent==0:
                within_enum=0
                line_of_code += '};\n'
        if 'enum:' in line_of_code:
            within_enum=True
            line_of_code=line_of_code.replace('enum:','enum {')
        newline= '\t'*indent+line_of_code+comment
        res.append(newline)
    if within_enum:
        res.append('};\n')
    return res


#########################################################################



def process_lines(source_lines,mode='c'):
    #for ann_line in base_processing(source_lines):
        #print ann_line
    if mode=='c':
        cxx_processor= (base_processing *
                    process_MainClass *
                    process_namespaces *
                    process_struct_union_enum *
                    process_classes *
                    entering_scope *
                    build_forward_declarations *
                    leaving_scope *
                    translate_keywords *
                    process_private_public *
                    add_braces)
    else:
        print "USING C++"
        cxx_processor= (base_processing *
                    process_struct_union_enum *
                    process_cpp_classes *
                    entering_scope *
                    #build_forward_declarations *
                    leaving_scope *
                    translate_keywords *
                    process_private_public *
                    add_braces)
    reset_globals(mode)
    private_lines=[]
    public_lines=[]
    output_list=private_lines
    for ann_line in source_lines >> cxx_processor:
        if ann_line.startswith('MODE CHANGE'):
            if ann_line.split()[-1]=='PRIVATE':
                output_list=private_lines
            else:
                output_list=public_lines
            continue
        if ann_line.startswith('DOCSTRING'):
            docstring=ann_line[10:].strip()
            i=1
            while output_list[-i].count('(')!=1: # find the start of func declaration
                i+=1
            if docstring:
                output_list[-i:-i]=["/* "+docstring+' */\n']
        else:
            output_list.append(ann_line)
    # typedefs have to come first in the forward declarations !!
    # inline destructors have to come last in the Forward declarations
    # because they might make use of some types !!!
    ########################## NEW ########################################
    # THIS PLACES THE typedefs first in a header file, to allow compilation !!!
    new_public_lines=[]
    new_typedefs=[]
    for line in public_lines:
        if line.startswith("typedef "):
            new_typedefs.append(line)
        else:
            new_public_lines.append(line)
    public_lines= new_typedefs+new_public_lines
    ########################## END OF NEW CODE #################################
    sorted_forward_declarations=[]
    typedefs=[]
    inline_functions=[]
    for fwd_decl in G.forward_declarations:
        if fwd_decl.startswith("typedef"):
            typedefs.append(fwd_decl)
        elif fwd_decl.startswith('static inline'):
            inline_functions.append(fwd_decl)
        else:
            sorted_forward_declarations.append(fwd_decl)
    global_decls="\n".join(G.global_declarations)
    if __name__=="__main__":
        if DEBUG:
            if G.global_declarations:
                print 'GLOBALS=\n',global_decls
            if public_lines:
                print "PUBLIC=\n","".join(public_lines)
            if private_lines:
                print "PRIVATE=\n","".join(private_lines)
            if typedefs+sorted_forward_declarations:
                print "FORWARD DECLARATIONS=\n", "\n".join(typedefs+sorted_forward_declarations)
            if inline_functions:
                print "INLINE FUNCTIONS=\n", "\n".join(inline_functions)
            if G.imported_modules:
                print "IMPORTED MODULES=\n", "\n".join(G.imported_modules)
            #raise SystemExit
            #for ann_line in source_lines>>base_processing:
            #for ann_line in source_lines>> base_processing>>process_classes>>process_private_public:
            if G.mode=='c':
                class_processor=process_classes
            else:
                class_processor=process_cpp_classes
            for ann_line in (source_lines
                                >>base_processing
                                #>>process_MainClass
                                #>>process_namespaces
                                >> process_struct_union_enum
                                >> class_processor
                                >>entering_scope
                                >>build_forward_declarations
                                >>leaving_scope
                                >>process_private_public
                                #>>add_braces
                                ):
                    print ann_line
    return public_lines, private_lines, typedefs+G.global_declarations+sorted_forward_declarations,inline_functions,G.imported_modules #, G.defines

def main():
    import sys, os
    input_file=sys.argv[1]
    other_args=sys.argv[2:]
    print "input file=",input_file
    if not input_file.endswith((".cxx",".cxxp",)):
        print "WRONG EXTENSION, ONLY .cxx and .cxxp FILES ARE ACCEPTED"
        raise SystemExit
    if input_file.endswith((".cxx")):
        c_output_file=input_file[:-3]+'c'
        G.mode='c'
    else:
        c_output_file=input_file[:-4]+'cpp'
        G.mode='cpp'
        print "=============================="
    h_output_file=input_file[:-3]+'h'
    with open(input_file,"r") as fin:
        contents=fin.read()
    headerfiles=needed_header_files(contents)
    print 'header files',headerfiles
    lines=contents.split("\n")
    publics, privates,forward_declarations,inline_functions,imported_modules=process_lines(lines,mode=G.mode)
    MAIN_APP= False if publics else True
    if not MAIN_APP:
        make_h_file(h_output_file,c_output_file,publics,headerfiles,imported_modules,inline_functions)
    #print "PRIVATES=",privates
    #print "IMPORTED MODULES=", imported_modules
    if G.PUBLIC_MAIN_CONSTRUCTOR:
        forward_declarations.insert(0,"#define _MAIN_C_\n")
    if not MAIN_APP:
        if "G." in contents: # this is not sufficient, some other includes are needed!!!!
            if not G.PUBLIC_MAIN_CONSTRUCTOR:
                if '#include "globals.h"' not in imported_modules:
                    imported_modules.append('#include "globals.h"')
    make_c_file(h_output_file,c_output_file,privates, forward_declarations,headerfiles,imported_modules,inline_functions,main_app=MAIN_APP, global_file=G.global_declarations)
    if not os.path.exists("Makefile"):
        localDir = os.path.dirname(input_file)
        imported_objects=[]
        pure_header_files=[]
        for line in imported_modules:
            path=line.rstrip().replace("#include ","").replace(".h",".c")
            abspath=os.path.abspath(os.path.join(localDir,path[1:-1]))
            if os.path.exists(abspath):
                print "path exists !!!:", path
                imported_objects.append(path.replace(".h",".o"))
            else:
                pure_header_files.append(abspath.replace(".c",".h"))
        #print "------------HEADER FILES=",headerfiles
        #print "------------INPUT FILE=", input_file, MAIN_APP
        make_makefile(input_file,headerfiles,pure_header_files,imported_objects, main_app=MAIN_APP)
    sys.stderr.write("DONE WRITING TO FILE")
    if not MAIN_APP:
        sys.stderr.write("S")
    sys.stderr.write(" {}".format(os.path.basename(c_output_file)))
    if not MAIN_APP:
        sys.stderr.write(" and {}".format(os.path.basename(h_output_file)))
    sys.stderr.write("\n\n")
    if other_args: # TODO use allman iso ansi (ansi not in version 3.02)
        os.system('astyle -n --style=ansi %s' % c_output_file)
        if sys.platform=="win32":
            if other_args[0]=="vscode":
                os.system('code %s' % c_output_file)
            else:
                os.startfile(c_output_file)
        if not MAIN_APP: # we have a .h file
            os.system('astyle -n --style=ansi %s' % h_output_file)
            if sys.platform=="win32":
                if other_args[0]=="pycharm":
                    os.system('pycharm %s' % h_output_file)
                else:
                    os.startfile(h_output_file)

#########################################################################

if __name__=="__main__":

    source_text=r"""
// C++ TEST !!!!!!!!!!!!!
public class CRectangle(Object):
    int x, y
    float z=999
    public static int e=7
    def __init__(self, int z, float y):
        int c=a+b
    private int area(self):
        return x*y
    def __del__(self):
        print "BYE BYE\n"
"""

    TODOsource_text=r"""
switch sss:
    case 1:
        break
    case 2::
        break
"""


    source_textbufffff=r"""
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
"""

    source_textBUG=r"""
if (a>b or (c==0 and d==255)):
    //if (current_slot_time>requested_slot_time or (current_fr_id==0 and fr_id==255)):
    print
    if 5 < d <= 10:
        print "kkk"
    """

    source_text=r"""
namespace G:
    int x
    float y
"""



    source_text=r"""
int* fun():
    return new int[2]={max_length, longest}
int {x,y}= fun()
// volatile int* res_fun= fun(...); int x=res_fun[0],y=res_fun[1]
"""


    source_text=r"""
volatile File* fp= new File()
volatile fp:= new File()
volatile char* fp = strdup("eeeeee")
volatile Object* fp = strdup("eeeeee")
volatile fp:= new double
volatile fp:= new int[10]
volatile myobj := new Obj = {.a=1,.b=5}
volatile myobj := new float = 5.555
volatile bool x=true  // remains untouched because no pointer involved !!!
volatile a :=new int[ROWS][COLS]
"""

    source_text=r"""
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
"""

    source_text=r"""
class Hello(Parent):
    int c
    int d
    def __del__(self):
        print "i am a destructor"
        print "fffffffffff"
"""

    source_text=r"""
class G:
    #define BYTE 1024
    #define MBYTE 1024
    enum:
        BUF_MIN_ALIGNMENT= 64
        BUFSIZE=100
    int x
    int y=8
    def __init__():
        G.ch= new ProducerConsumerChannel(5,BUFSIZE)
    def __del__():
        print "this is the destructor"
    def get_options():
        print "doit"
"""

    source_text=r"""
if d:
    a := new int[5][2]
    b := reshape(a,2,5)
    b := reshape(int,a,2,5)
"""
    source_text=r""" // BUGS here !!!
//volatile Vector* myslice= myvector->get_slice(1,(int32_t)NULL)
//while (m = num_elems * 2) < self.num_elems :
//  pass
if (n1==n2) or (n3==n4):
    if !*G.pattern_file:
        new Memory()
        Memory::head =new Memory(p, size, file, line)

class HELLO:
    def push(self):
        pass
    def pop(self):
        self.push(e->data, e->pri) //COMPILER BUG HERE !!!
        self.push(e.data, e.pri) // THIS WORKS !!!
        printf "%11.6f      yes    %6.3f    ", self.Temperature, self.push() // BUG
"""


    source_text=r"""
collectibles = new Collectible[G.collectibleCount]
for Collectible col in collectibles:
    print
"""

    source_text=r"""
class ZZZ:
    // comment 0
    enum:
        a=7
        b=8
    // comment 1
    #define ff 4
    // comment 2
    #define ff 4
    int x
    float y
    def __init__(self):
        init_application_code
"""



    source_text=r"""
class G: // should become namespace G
    enum:
        a=7
    def __init__():
        pass
"""

    source_text=r"""
def another_function():
    pass

class G: // should become namespace G
    // comment 0
    enum:
        a=7
        b=8
    // comment 1
    #define ff 4
    // comment 2
    #define ff 4
    // comment 3
    int x=8
    // comment 4
    bool y= true
    def __init__(int argc, char **argv): // should become int main(...)
        G::get_options(argc, argv)
        init_application_code
        G::run()
    def get_options(int argc, char **argv):
        pass
    def __del__():
        exit_application_code
    def run():
        G.myMainReactor = new MainReactor(conf)
        Reactor::run(G.myMainReactor)

"""

    source_text=r"""
public uint8_t levelScenery[3][15] =:
    0,0,0,0,1,1,0,0,0,0,0,0,0,0,0
    0,0,0,1,1,1,5,1,1,5,1,1,1,3,0
    0,0,1,1,1,1,0,0,0,0,0,0,0,0,0

class Scenery:
    public static int level=555
    int x
    def __init__(self):
        pass
"""

    source_text=r"""
class Map:
    enum Direction:
        SNAKE_UP = 1
        SNAKE_RIGHT = 2
        SNAKE_DOWN = 3
        SNAKE_LEFT = 4
    int x
    def __init__(self):
        pass
"""

    source_text=r"""
if ggggg.startswith("kk"):
    print
if ggggg.lstrip().startswith("kk"):
    print
"""

    source_text=r"""
if ggggg.startswith("kk"):
    print
if ggggg=="kk":
    print
if ggggg== "kk":
    print
if ggggg.lstrip()->startswith("kk"):
    print
"""

    source_text9=r"""
events := new structepoll_event[MAXEVENTS]
events := new struct epoll_event[MAXEVENTS]
"""

    source_text=r"""
def fff():
    with new char[255] as buf:
        if not buf:
            print "unable to allocate buf\n"
            break
        sprintf buf, "Hello World"

    with new File("dd") as f:
        if not f:
            print "Error opening file\n"
            break
        f->read()
"""

    source_text=r"""
def main():
    TMReq* tmreq= NULL
    delete tmreq
"""
# BUG !
    source_text=r"""
if (strcmp(arg,"-f") == 0) || (strcmp(arg,"-f1") == 0):
"""

    source_text=r"""
void fun():
    with new double as buf:
        print buf
    with new uint8_t[255] as buf:
        print buf
    with new uint8_t=unhexlify("7844aa99") as inv:
        assert inv[3]==0x99
    """
    source_text=r"""
public class EEEE:
    int x
    public def __init__(self):
        self.x=4
    """

    source_text=r"""
class G: // should become namespace G
    int x
    float y
    def __init__(int argc, char **argv): // should become int main(...)
        G::get_options(argc, argv)
        init_application_code
        G::run()
    def get_options(int argc, char **argv):
        pass
    def __del__():
        exit_application_code
    def run():
        G.myMainReactor = new MainReactor(conf)
        Reactor::run(G.myMainReactor)
"""

    #G.mode='cpp'
    # G.ASSERT_MODE=True # set it to true if you want asserts everywhere !!
    if sys.argv[1:]:
        DEBUG=False
        main()
    else:
        DEBUG=True
        process_lines(source_text.split('\n'), G.mode)

"""
ADVOCACY:
Within C++, there is a much smaller and cleaner language struggling to get out.
-- Bjarne Stroustrup
There are two ways of constructing a software design: One way is to make
it so simple that there are obviously no deficiencies, and the other way
is to make it so complicated that there are no obvious deficiencies.
The first method is far more difficult.
-- C.A.R. Hoare
CXX is an experimental programming language I have been working on, on and off
(mostly off), since 2012. It is a statically typed, object-oriented, imperative language,
As safe as ADA, as performant as C, as productive as Python.
I tried hard to keep it c-like at the lowest level, while infusing it with
python-isms at the highest level to make it more palatable to python users.
The most important thing when coding is to keep code from collapsing under the weigth
of its own complexity.
#C++ my favourite example: f(a<b, c>d)
#Does the f function has 2 bool arguments or do we pass (freshly created) object of class a parametrized with template arguments b,c? "Templates". Fun begins there :D
I am a C-graded coder, couldn't convince myself of becoming D-graded
In the same way my friend's car that maxes out at 80 is not fast but is still fast enough for standard driving.
"""
# THERE ARE 3 LEVELS OF VISIBILITY (caveat, must be preceded by NEWLINE ????)
# 'public class' ==> all internals are made public
# 'protected class' ==> only an opaque type is made public, Accessors must be defined
# 'private class' ==> the type is only visible within the module
# Order of Definitions Is Not Significant:No need of forward declarations, you can group definitions logically, not in an order forced by the limitations of the compiler.
# done: arr= new TYPE[ROWS][COLS]
#    TYPE *arr_p= calloc(ROWS*COLS,sizeof(TYPE))
#    TYPE (*arr)[COLS]=(TYPE(*)[COLS])arr_p
# done : turn  myobj := new Obj = {.a=1,.b=5}
#   into: Obj* myobj := new Obj; *myobj= (Obj){.a=1,.b=5}
# DONE: one cosmetic blank line is allowed between lines of same indentation!!
# done: handle default parameters
# done:fileobj := new FileObject ==>FileObject* fileobj = malloc(sizeof(*fileobj))
# done: add static class parameters
#done: if a class is protected, only the opaque type is exported in the .h file !
# done class A:
#     static int counter=0
# done: namespace G: int a=8;... ==> struct {int a,..}  G={.a=8}
# done: anonymous namespaces within namespaces !!! (use anonymous structs!)
# limitation: anonymous namespaces are only allowed within a named namespace
# done: for int x in gen:  ==>
#       while not gen->exhausted:
#           int x= gen->next()
# done, allow blank lines between method definitions!!!
# done replace 1_000_000 with 1000000
# done  empty lines between same levels of indentation should be allowed
# done add doc strings to the functions !!!
# DONE: an __init__ function can fail and must then return a NULL pointer !!!
# DONE a1 = new int[12] ==> int *a1= malloc(12*sizeof(int))
# done designated_new: e.g MyClass* my = new Myclass(.a=10,.b=15)
# done would translate into MyClass* my =DESIGNATE_NEW(Myclass,.a=10,.b=15)
# #define D_NEW(T,...) memcpy(malloc(sizeof(T)),&(T const){__VA_ARGS__},sizeof(T))
# done: RAII volatile fp:= new File(...)
# ==> File* fp __attribute__((cleanup(File_free)))= File_new();
# done: RAII volatile fp:= new double
# ==> double* fp __attribute__((cleanup(free)))= malloc(sizeof(*fp));
# done: delegate pointers
# advice: NEVER USE CONSTANTS IN YOUR CODE
# done: return new int[2] = {max_length, longest}
# ====>return memcpy(calloc(2,sizeof(int)),(int[]) {max_length, longest});
# DONE: improve base_processing to collapse multi-lines into one line!
# SOLVED BUG, the __init__ declaration MUST be on a single line !!!!
# done: allow volatile int* b=  fun()
# done: implement a main class with constructor and destructor
# done: add asserts for all pointer dereferencings!!!
# done: var.startswith("ffff") ==> strncmp(var,"ffff",strlen("ffff"))==0
# done: var=="ffff" ==> strncmp(var,"ffff",strlen("ffff"))==0
#GENERATORS
#   you can do 'yield' within the 'next' method and on the next call
#   * control will resume just after the 'yield' statement.
#   *  Any local variables must be declared as an instance member.
#   *
#   * Ground rules:
#   *  - because of the use of labels, no local vars can be declared!!!
#   *  - never put two 'yield' statements on the same
#   *    source line.
#   *  - if you want the output to be ignored, yield None
#   *
#   * The caller of a static coroutine calls it just as if it were an
#   * ordinary method call:
#done: call destructor of parent class if not __del__ defined in child class
#done :     b := reshape(a,2,5) ==>int (*b)[5]=(int(*)[5])a_p
#done :     b := reshape(int,a,2,5) ==>int (*b)[5]=(int(*)[5])a_p
#done  : when use is made of "for char* p in array:", introduce
#   #define append(sp, n) (*((sp)+1+(*(int*)(sp))++) = (n))
#   #define pop(sp) ((sp)[--*(int*)(sp)+1])
#  for char* p in array: do ...==> for int i=1;i<=array[0];i++: char*p=array[i]
#  for char* p in array.reversed: do ...==> for int i=array[0];i>0;i--: char*p=array[i]
#done: put G struct at the beginning of the file (with enums and #define declarations)
#done: implement a "globals.h" to be able to split the main file into several files
#      i call it "splitted main functionality"!
#done: implement nested enums for ordinary classed (translates as nested !)
#done: use '=>' for polymorphic calls
#done: create a unitest file for the libraries (in a test directory)!!!
#done: SOLVE THE BUG WITH THE PARENTHESES !!!!
#done: with new char[255] as buf: ==> for char* buf=malloc(255),enter=1;enter;free(buf),enter=0:
#      with new File(..) as f: ==> for f:=new File(..), enter=1;enter;delete f,enter=0:

