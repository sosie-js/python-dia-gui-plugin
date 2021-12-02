# recipe-137951-1.py 
# from http://code.activestate.com/recipes/137951-dump-all-the-attributes-of-an-object/
# created by (C) Philip Kromer http://code.activestate.com/recipes/users/552075/
# licence = psf http://code.activestate.com/recipes/tags/meta:license=psf/

#https://code.activestate.com/recipes/137951-dump-all-the-attributes-of-an-object/
#python3 port  import dumpObj;dumpObj.dumpObj(dia)
 
 
import inspect
 
""" 
def classname(obj):
   #Get the fully-qualified class name of a python object 
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = module + "." + name
    return name
"""    
 
def printDict(di, format="%-25s %s"):
    for (key, val) in di.items():
        print(format % (str(key)+':', val))

def dumpObj(obj, maxlen=77, lindent=24, maxspew=600):
    """Print a nicely formatted overview of an object.

    The output lines will be wrapped at maxlen, with lindent of space
    for names of attributes.  A maximum of maxspew characters will be
    printed for each attribute value.

    You can hand dumpObj any data type -- a module, class, instance,
    new class.

    Note that in reformatting for compactness the routine trashes any
    formatting in the docstrings it prints.

    Example:
       >>> class Foo(object):
               a = 30
               def bar(self, b):
                   "A silly method"
                   return a*b
       ... ... ... ... 
       >>> foo = Foo()
       >>> dumpObj(foo)
       Instance of class 'Foo' as defined in module __main__ with id 136863308
       Documentation string:   None
       Built-in Methods:       __delattr__, __getattribute__, __hash__, __init__
                               __new__, __reduce__, __repr__, __setattr__,       
                               __str__
       Methods:
         bar                   "A silly method"
       Attributes:
         __dict__              {}
         __weakref__           None
         a                     30
    """
    
    
    """
    import dill
    d=dill.dumps(obj)
    file_path=__name__+".dump"
      
    with open("dill-dia-"+file_path, "wb") as w:
        w.write(d)
    
    import pickle
    from pprint import pformat as pf
    
    # dump : put the data of the object in a file
  
    #pickle.dump(obj, open(file_path, "wb"))
    def pickle_trick(obj, max_depth=10):
        output = {}

        if max_depth <= 0:
            return output

        try:
            pickle.dumps(obj)
        except (pickle.PicklingError, TypeError) as e:
            failing_children = []

            if hasattr(obj, "__dict__"):
                for k, v in obj.__dict__.items():
                    result = pickle_trick(v, max_depth=max_depth - 1)
                    if result:
                        failing_children.append(result)

            output = {
                "fail": obj, 
                "err": e, 
                "depth": max_depth, 
                "failing_children": failing_children
            }

        return output
    
    
    
        w.write(pf(pickle_trick(obj)))
    """
    
    import types

    # Formatting parameters.
    ltab    = 2    # initial tab in front of level 2 text

    # There seem to be a couple of other types; gather templates of them
    MethodWrapperType = type(object().__hash__)

    #
    # Gather all the attributes of the object
    #
    objclass  = None
    objdoc    = None
    objmodule = '<None defined>'
    
    speclass = None
    objpackage = None
    firstobjmodule = None
    
    methods   = []
    builtins  = []
    classes   = []
    attrs     = []
    
    import sys
    python_ver = sys.version_info[0]
    import dill
    
    # The user home dia python will store  the trace file
    import os
    if 'HOME' not in os.environ:
        os.environ['HOME'] = os.pathsep + 'tmp'
    
    trace_file="trace-dia-"+__name__+str(python_ver)+".txt"
    trace_file=os.path.join(os.environ['HOME'], '.dia', 'python',trace_file)
    
    with open(str(trace_file), "wb") as trc:
        s=0    
        for slot in dir(obj):
            attr = getattr(obj, slot)
            st=slot
            if   slot == '__class__':
                objclass = attr.__name__
            elif slot == '__spec__':
                speclass= attr.name
            elif slot == '__name__':
                objname= attr
            elif slot == '__package__':
                objpackage = attr
                if firstobjmodule is None: #Not sure for python3
                    firstobjmodule = objpackage
            elif slot == '__doc__':
                objdoc = attr
            elif slot == '__file__':
                objfile = attr
            elif slot == '__path__':
                objpath = attr
            elif slot == '__module__':
                objmodule = attr
                if firstobjmodule is None:
                    firstobjmodule = objmodule
            elif (isinstance(attr, types.BuiltinMethodType) or 
                  isinstance(attr, MethodWrapperType)):
                builtins.append( slot )
                st="builtin"
            elif (isinstance(attr, types.MethodType) or
                  isinstance(attr, types.FunctionType)):
                methods.append( (slot, attr) )
                st="method"
            else:
                #from pudb import set_trace; set_trace(paused=True)
                #import web_pdb; web_pdb.set_trace()
                if inspect.ismodule(attr) :
                    objmodule = attr
                else:
                    #isType=isinstance(attr, types.TypeType)  is buggy for classobj
                    #same with from typing import Type; isType=isinstance(attr, Type)
                    #same with isType=isinstance(attr, type)
                    if inspect.isclass(attr):
                        st="class"
                        classes.append( (slot, attr) )
                    else:
                        st="attrs"
                        attrs.append( (slot, attr) )
                    
            tag="\n=======================\n"+str(s)+":"+st+':'+str(attr)+"\n-----------------\n"
            try:
                trc.write(bytes(tag,"utf-8")) #+dill.dumps(attr)) 
            except:
                 trc.write(bytes(tag)) #+dill.dumps(attr))   
            s=s+1

    #
    # Organize them
    #
    methods.sort()
    builtins.sort()
    classes.sort()
    attrs.sort()

    if(speclass == objclass):
        print("Class")
        pass

    #
    # Print a readable summary of those attributes
    #
    normalwidths = [lindent, maxlen - lindent]
    tabbedwidths = [ltab, lindent-ltab, maxlen - lindent - ltab]

    def truncstring(s, maxlen):
        if len(s) > maxlen:
            return s[0:maxlen] + ' ...(%d more chars)...' % (len(s) - maxlen)
        else:
            return s

    # Summary of introspection attributes
    if objclass == '':
        objclass = type(obj).__name__
    intro = "Instance of class '%s' as defined in module %s with id %d" % \
            (speclass, firstobjmodule, id(obj))
    print('\n'.join(prettyPrint(intro, maxlen)))

    # Object's Docstring
    if objdoc is None:
        objdoc = str(objdoc)
    else:
        objdoc = ('"""' + objdoc.strip()  + '"""')
    print()
    print(prettyPrintCols( ('Documentation string:',
                            truncstring(objdoc, maxspew)),
                          normalwidths, ' '))

    # Built-in methods
    if builtins:
        bi_str   = delchars(str(builtins), "[']") or str(None)
        print("")
        print(prettyPrintCols( ('Built-in Methods:',
                                truncstring(bi_str, maxspew)),
                              normalwidths, ', '))
        
    # Classes
    if classes:
        print("")
        print('Classes:')
    for (classname, classtype) in classes:
        classdoc = getattr(classtype, '__doc__', None) or '<No documentation>'
        print(prettyPrintCols( ('',
                                classname,
                                truncstring(classdoc, maxspew)),
                              tabbedwidths, ' '))

    # User methods
    if methods:
        print("")
        print('Methods:')
    for (methodname, method) in methods:
        methoddoc = getattr(method, '__doc__', None) or '<No documentation>'
        print(prettyPrintCols( ('',
                                methodname,
                                truncstring(methoddoc, maxspew)),
                              tabbedwidths, ' '))

    # Attributes
    if attrs:
        print("")
        print('Attributes:')
    for (attr, val) in attrs:
        print(prettyPrintCols( ('',
                                attr,
                                truncstring(str(val), maxspew)),
                              tabbedwidths, ' '))

def prettyPrintCols(strings, widths, split=' '):
    """Pretty prints text in colums, with each string breaking at
    split according to prettyPrint.  margins gives the corresponding
    right breaking point."""

    import sys
    python_ver = sys.version_info[0]
    
    if  python_ver == 2:
        
        
       return  _prettyPrintCols(strings, widths, split)
        
    else:
        #_prettyPrintCols is not fully python3 compatible
        #The parts that seems to work for python3
        #without washing the strings
        assert len(strings) == len(widths)

        strings = map(nukenewlines, strings)
        
        return  '\n'.join(strings)

def _prettyPrintCols(strings, widths, split=' '):
    """Pretty prints text in colums, with each string breaking at
    split according to prettyPrint.  margins gives the corresponding
    right breaking point."""

    assert len(strings) == len(widths)

    strings = map(nukenewlines, strings)

    # pretty print each column
    cols = [''] * len(list(strings))
    for i in range(len(list(strings))):
        cols[i] = prettyPrint(strings[i], widths[i], split)

    # prepare a format line
    format = ''.join(["%%-%ds" % width for width in widths[0:-1]]) + "%s"

    def formatline(*cols):
        return format % tuple(map(lambda s: (s or ''), cols))

    # generate the formatted text
    return '\n'.join(map(formatline, *cols))


    

def prettyPrint(str, maxlen=75, split=' '):
    """Pretty prints the given string to break at an occurrence of
    split where necessary to avoid lines longer than maxlen.

    This will overflow the line if no convenient occurrence of split
    is found"""

    # Tack on the splitting character to guarantee a final match
    str += split
    
    lines   = []
    oldeol  = 0
    eol     = 0
    while not (eol == -1 or eol == len(str)-1):
        eol = str.rfind(split, oldeol, oldeol+maxlen+len(split))
        lines.append(str[oldeol:eol])
        oldeol = eol + len(split)

    return lines

def nukenewlines(string):
    """Strip newlines and any trailing/following whitespace; rejoin
    with a single space where the newlines were.
    
    Bug: This routine will completely butcher any whitespace-formatted
    text."""
    
    if not string: return ''
    lines = string.splitlines()
    return ' '.join( [line.strip() for line in lines] )
    
def delchars(stri, chars):
    """Returns a string for which all occurrences of characters in
    chars have been removed."""

    # Translate demands a mapping string of 256 characters;
    # whip up a string that will leave all characters unmolested.
    identity = ''.join([chr(x) for x in range(256)])

    try:
        stro = stri.translate(identity, chars)
    except:
        stro = stri.translate(dict(zip(identity, chars)))

    return stro
    
    
