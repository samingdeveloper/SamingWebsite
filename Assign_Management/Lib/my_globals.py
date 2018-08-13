from RestrictedPython.Limits import limited_builtins
from RestrictedPython.Utilities import utility_builtins
from RestrictedPython.Guards import safe_builtins

import importlib
from . import test
#import builtins
#import resource
#import time
############################## uploadgrading ##############################

def string(*args): #execute string and setattr.
    string = "def test_{0}(self):\n" \
             "    self.actual = {1}\n" \
             "    self.expected = {2}\n" \
             "    self.points = {3}\n" \
             "    self.level = {4}\n" \
             "    self.result['max_score'] += self.points\n" \
             "    try:\n" \
             "        self.assertEquals(self.actual, self.expected)\n" \
             "        if self.level == 0:\n" \
             "            self.result['case'][{0}] = str({1})+' == '+str({2})\n" \
             "        elif self.level == 1:\n" \
             "            self.result['case'][{0}] = 'PASS'\n" \
             "        self.result['score'] += self.points\n" \
             "    except Exception as e:\n" \
             "        if self.level == 0:\n" \
             "            self.result['case'][{0}] = str(e)\n" \
             "        elif self.level == 1:\n" \
             "            self.result['case'][{0}] = 'FAIL'\n" \
             "        raise AssertionError\n".format(repr(args[0]), repr(args[1]), repr(args[2]), args[3], abs(args[4]))
    return string

def mgb(globe=globals(), libs=None): #return globals()['__builtins__'] without __import__
    import copy
    tb = copy.deepcopy(globe['__builtins__'])
    tb_del = ('__import__', '__loader__', '__spec__', '__package__', '__name__', 'open', 'quit', 'exit', 'compile', 'exec', 'eval')
    try:
        for lib in libs:
            try:
                #print(importlib.import_module(lib))
                tb[lib] = importlib.import_module(lib) #getattr(builtins, lib)
            except Exception as e:
                print(e)
                continue
    except:
        pass
    for i in tb_del:
        try:
            del tb[i]
        except:
            continue
    #tb['assert_equal'] = test.assert_equal
    tb.update(safe_builtins)
    tb.update(utility_builtins)
    tb.update(limited_builtins)
    return tb

def scr(case_dict): #import libs #not ready
    for i in case_dict.values():
        if i == "PASS" or i.count('=') == 2:
            return True
    else:
        return False

############################## limit_uploadgrading ##############################

'''def limit_memory():
    #soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (150*1024*1024, get_memory() * 1024 / 2.5)) #(get_memory() * 1024 / 3, hard))

def limit_cpu(): # The maximum amount of processor time (in seconds) that a process can use.
    #soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU, (5,5))

def limit_stack():
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    resource.setrlimit(resource.RLIMIT_STACK, (soft,soft))

def limit_heap():
    #soft, hard = resource.getrlimit(resource.RLIMIT_DATA)
    resource.setrlimit(resource.RLIMIT_DATA, (soft,soft))

def limit_nproc():
    # soft, hard = resource.getrlimit(resource.RLIMIT_NPROC)
    resource.setrlimit(resource.RLIMIT_NPROC, (1,1))

def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        #print(mem)
        for i in mem:
            #print(i)
            sline = i.split()
            #print(i,sline)
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
        #print(free_memory)
    return free_memory

def limit_info():
    for name, desc in [
        ('RLIMIT_CORE', 'core file size'),
        ('RLIMIT_CPU', 'CPU time'),
        ('RLIMIT_AS', ' maximum as area (bytes)'),
        ('RLIMIT_FSIZE', 'file size'),
        ('RLIMIT_DATA', 'heap size'),
        ('RLIMIT_STACK', 'stack size'),
        ('RLIMIT_RSS', 'resident set size'),
        ('RLIMIT_NPROC', 'number of processes'),
        ('RLIMIT_NOFILE', 'number of open files'),
        ('RLIMIT_MEMLOCK', 'lockable memory address'),
    ]:
        limit_num = getattr(resource, name)
        soft, hard = resource.getrlimit(limit_num)
        print('Maximum %-25s (%-15s) : %20s %20s' % (desc, name, soft, hard))

def limit_selfusage():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    for name, desc in [
        ('ru_utime', 'User time'),
        ('ru_stime', 'System time'),
        ('ru_maxrss', 'Max. Resident Set Size'),
        ('ru_ixrss', 'Shared Memory Size'),
        ('ru_idrss', 'Unshared Memory Size'),
        ('ru_isrss', 'Stack Size'),
        ('ru_inblock', 'Block inputs'),
        ('ru_oublock', 'Block outputs'),
        ]:
        print ('%-25s (%-10s) = %s' % (desc, name, getattr(usage, name)))

def limit_childrenusage():
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    for name, desc in [
        ('ru_utime', 'User time'),
        ('ru_stime', 'System time'),
        ('ru_maxrss', 'Max. Resident Set Size'),
        ('ru_ixrss', 'Shared Memory Size'),
        ('ru_idrss', 'Unshared Memory Size'),
        ('ru_isrss', 'Stack Size'),
        ('ru_inblock', 'Block inputs'),
        ('ru_oublock', 'Block outputs'),
        ]:
        print ('%-25s (%-10s) = %s' % (desc, name, getattr(usage, name)))

def limit_grader():
    limit_memory()
    limit_cpu()
    limit_stack()
    limit_info()
    limit_selfusage()
    limit_childrenusage()'''