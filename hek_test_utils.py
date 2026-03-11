import sys
import textwrap, inspect

NullObject=type('',(),{'__getattr__':lambda self,n: lambda *x,**y: None})()

def idx_first_mismatch(str1,str2):
    for i in range(min(len(str1),len(str2))):
        if str1[i] != str2[i]:
            return i
    return 9999999

import difflib
def compare_text(left, right):
    if left == right:
        print("Transformation done correctly")
    else:
        print("Transformation done incorrectly")
        d = difflib.Differ()
        diff = d.compare(left.splitlines(),right.splitlines())
        print('\n'.join(diff))

def main(f):
    def runner():
        print((f.__name__.center(80,'-')))
        print(('-'*(80)))
        f()
        print(('-'*(80)))
    if f.__globals__['__name__']=='__main__':
        atexit.register(runner)
    return f


#################################################################
class TEST_CONTEXT(object):
    """ these are the globals """
    tests=[]
    debug=False
    failed_tests=[]
    current_test = None

def unittest2(parse_func):
    def wrapper(f):
        """ This decorator allows to unit test all functions,
        It runs at the end, this means all functions are available !!!
        CAVEAT: this runs the tests in the reverse order"""
        text=inspect.getsource(f) # extract the snippet from the body of the test function
        source_text,sep,target_text=text.partition('EXPECTED:')
        source_lines=source_text.split('\n')[2:]
        source_text="\n".join(source_lines).strip().lstrip("'").lstrip('"')
        if not target_text:
            source_text =source_text.strip().rstrip('"').rstrip("'")
        source_text += "\n"
        source_text= textwrap.dedent(source_text)
        target_lines=target_text.split('\n')[1:]
        target_text= textwrap.dedent("\n".join(target_lines)).strip().rstrip('"').rstrip("'")
        def runner(*args,**kwargs):
            sys.stdout.write( f.__name__.center(80,'-')+'\n')
            sys.stdout.write( '-'*(80)+'\n')
            TEST_CONTEXT.current_test = f.__name__
            TEST_CONTEXT.tests.append(f.__name__)
            try:
                TEST_CONTEXT.verify(source_text,target_text,parse_func,*args,**kwargs)
            except AssertionError:
                sys.stdout.write( 'TEST FAILED '*10+'\n')
                lineno=inspect.getsourcelines(f)[1]
                error_info='File "%s", line %d' %(inspect.getfile(f),lineno)
                TEST_CONTEXT.failed_tests.append(f.__name__+' failed , in '+error_info)
                print(("FAILED SOURCE=", source_text))
            else:
                sys.stdout.write( 'Test succeeded\n')
            sys.stdout.write( '-'*(80)+'\n')

        if f.__globals__['__name__']=='__main__':
            if not sys.argv[1:]: # dont run when argument is given
                atexit.register(runner, **inspect.getcallargs(f))
        return f
    return wrapper

def final_runner():
    print('TEST SUMMARY'.center(80,'-'))
    print("%3d TESTS SUCCESSFUL" % (len(TEST_CONTEXT.tests)-len(TEST_CONTEXT.failed_tests)))
    print("%3d TESTS FAILED" % len(TEST_CONTEXT.failed_tests))
    for i,test in enumerate(TEST_CONTEXT.failed_tests):
        print('\t',i,' ==> ',test)

#################################################
####################################################################
@staticmethod
def verify(sourcetext,targettext,rule,*args,**kwargs):
    DEBUG=kwargs.get("DEBUG",False)
    FAILS=kwargs.get("FAILS",False) #
    print("SOURCE=\n", repr(sourcetext))
    print("EXPECTED=\n", targettext)
    # print 'rule=', rule
    try:
        from .hek_rd_parser import ParsingContext as P
        P.new(sourcetext)
        if 0:
            P.print_tokens()
        # print [x[0] for x in list(P.curr_gen)]
        ast=rule.parse(scope)
        # print "==================", ast
        if not ast:
            P.printSyntaxError()
            print("#"*80)
            raise AssertionError
        # else:
        #     print "no syntax error detected!!!"
    except Exception as e:
        print("==================>",e)
        raise AssertionError
    else:
        # return # TEMPORARY !!!
        translated=ast.to_py()
        print("TRANSLATED:\n",translated)
        #print new_text_snippet
    if not targettext:
        return
        print("GOT=\n", translated.replace('\t','    '))
    else:
        return
        try:
            assert targettext.strip() == translated.strip()
        except AssertionError:
            myidx=idx_first_mismatch(targettext.strip(),translated.strip())
            expected=targettext.strip()[myidx]
            got=translated.strip()[myidx]
            print("expected======",len(targettext.strip()),expected.replace('\t','    '), ord(expected))
            print("got     ======",len(translated.strip()),got.replace('\t','    ') ,ord(got))
            print("first mismatch at index ",myidx)
            print(translated.replace('\t','    ').strip()[:myidx]+'!!!'+translated.replace('\t','    ').strip()[myidx:])
            raise
    if DEBUG: # WE CAN PASS ARGUMENTS TO THE RUNNER                 #
        sys.stdout=NullObject # WE STOP FOR ALL FOLLOWING TESTS     #
    assert not FAILS

TEST_CONTEXT.verify=verify

import atexit; atexit.register(final_runner)
