from cxx_utils import windows, get_indentation, get_sanitized_line, Pipe
@Pipe
def process_cpp_classes(level):
    within_class=False;within_methods=False;classname=""
    within_constructor=False
    for indent,line_of_code,comment,other_info in level:
        if indent==0:# state changes can only occur at indent 0
            if within_class: # current class ends
                within_class=False
                for line in static_members:
                    if line[1].startswith("public"):
                        cur_line=line[1]
                    else: #bug in process_classes!!!!
                        cur_line=line[1].replace('private','static',1)
                    yield line[0],cur_line, line[2],line[3]
                for line in methods_lines:
                    yield line
                within_methods=False;classname='';within_constructor=False
            if not within_class:
                if line_of_code.lstrip().startswith(("class ","public class ","private class ","protected class ")):
                    within_class=True;methods_lines=[]; instance_members=[]
                    static_members=[]; initialized_members=[]
                    classname=line_of_code.strip().partition('class ')[2].partition('(')[0].lstrip().split()[0].rstrip('):')
                    if "(" in line_of_code and ")" in line_of_code:
                        parent_classname=line_of_code.strip().partition('(')[2].lstrip().split()[0].rstrip('):')
                        line_of_code=line_of_code.partition('(')[0].rstrip()+': public '+parent_classname+':'
                    is_private= line_of_code.lstrip().startswith(('private','class'))
                    is_protected= line_of_code.lstrip().startswith('protected')
                    if is_private or is_protected:
                        opaque_comment= '// opaque type'
                        opaque_declaration=line_of_code.strip().rstrip(': ')
                        if is_private:
                            pass #G.forward_declarations.append(opaque_declaration.replace('private ','')+'; '+opaque_comment)
                        else:
                            if not opaque_declaration.startswith('public'):
                                opaque_declaration = 'public '+opaque_declaration
                            yield 0,opaque_declaration, opaque_comment,{}
                        line_of_code= line_of_code.replace("protected ","",1).replace("private ","",1)
                    else:
                        typedef_decl=line_of_code.rstrip(' :')
                        [typedef_decl]=typedef_decl.split(':')[0:1]
                        if not typedef_decl.startswith('public'):
                            typedef_decl = 'public '+typedef_decl
                        yield 0,typedef_decl, "",{}
                    ###############
                    yield indent,line_of_code,comment,other_info
                    continue
        if indent==1:# state changes (for within_methods) can only occur at 1
            if within_class and 'self' in line_of_code and '(' in line_of_code:
                within_methods=True # we are done with the attributes
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
                    newline=newline[:vidx]+classname+'::'+static_var_name+newline[vidx+len(static_var_name):]
                    static_members.append((0,newline,comment,other_info))
                elif '=' in line_of_code and indent==1:
                    idx=line_of_code.find('=')
                    splitted_line=line_of_code[:idx].split()
                    identifier=splitted_line[-1]
                    type=" ".join(splitted_line[:-1])
                    initialiser=line_of_code[idx+1:]
                    if type=="char*":
                        newline='\tstrcpy(self.%s,%s)'% (identifier,initialiser)
                    else:
                        newline='\tself.'+identifier+'='+initialiser
                    yield (indent,line_of_code[:idx],comment,other_info)
                    initialized_members.append((1,newline,comment,other_info))
                else:
                    yield indent,line_of_code,comment,other_info
            else: # we are within a method
                if line_of_code.lstrip().startswith(("def ","public def")) and "__del__" in line_of_code:
                    line_of_code= line_of_code.replace('self','',1).replace('def','')
                    line_of_code= line_of_code.replace('__del__','~'+classname,1).strip(':')
                if line_of_code.lstrip().startswith(("def ","public def")) and "__init__" in line_of_code:
                    yield 1,"public:","",{}
                    within_constructor=True
                    line_of_code= line_of_code.replace('__init__',classname.strip(),1).strip(':')
                elif indent==1:
                    if within_constructor==True:
                        for line in initialized_members:
                            methods_lines.append(line)
                        initialized_members=[]; within_constructor=False
                if indent==1: # method declaration
                    line_of_code= line_of_code.replace('self, ','',1)
                    line_of_code= line_of_code.replace('self,','',1)
                    line_of_code= line_of_code.replace('self','',1)
                    line_of_code= line_of_code.replace('def','')
                    yield 1,line_of_code.strip(':'),"",{}
                if indent==1 and line_of_code[1:]:
                    if line_of_code.lstrip().startswith('private '):
                        line_of_code= line_of_code.replace('private ','private '+classname+'::')[1:].lstrip()
                    else:
                        line_of_code= classname+'::'+line_of_code[1:].lstrip()
                else:
                    line_of_code=line_of_code[1:]
                methods_lines.append((indent-1,line_of_code,comment,other_info))
