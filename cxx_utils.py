class Pipe:
    def __init__(self, function):
        self.function = function
    def __ror__(self, left):
        return self.function(left)
    def __call__(self, *args, **kwargs):
        return Pipe(lambda x: self.function(x, *args, **kwargs))
    __rrshift__=__ror__ # >>
    def __mul__(self,other):
        return Pipe(lambda x: x >> self | other)

TAB='\t'
SINGLE_QUOTE="'"
DOUBLE_QUOTE='"'
def get_indentation(line,tab=TAB,i=0): # line.rstrip().count('\t')
    while line[i:] and line[i:i+len(tab)]==tab:
        i+= len(tab)
    return i
def get_sanitized_line(line, REPLACER="$"): # replace anythin within quotes with REPLACER
    output_string,within_single_quote, within_double_quote="",False, False
    for char in line:
        if within_single_quote:
            if char == SINGLE_QUOTE:
                within_single_quote=False
            output_string+= REPLACER
            continue
        if within_double_quote:
            if char == DOUBLE_QUOTE:
                within_double_quote=False
            output_string+= REPLACER
            continue
        if char == SINGLE_QUOTE:
            within_single_quote=True
            output_string+= REPLACER
            continue
        if char == DOUBLE_QUOTE:
            within_double_quote=True
            output_string+= REPLACER
            continue
        output_string+= char
    return output_string

import itertools

def windows(seq,n=3):
    """Returns a sliding window (of width 3 by default)
    """
    it = itertools.chain(iter([None]),iter(seq), iter([None]))
    result = tuple(itertools.islice(it, n))
    if len(result) == n: yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result # TO DO: replace None by NullObject !!!
    for _ in range(n-3):# dont lose the n-3 tokens at the end of the stream !
        result = result[1:]+ (elem,)
        yield result
