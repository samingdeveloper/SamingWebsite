from RestrictedPython.Guards import safe_builtins
import builtins

def mgb(libs=[]):
    tb = globals()['__builtins__'].copy()
    tb_del = ('__import__', '__loader__', '__spec__', '__package__', '__name__')
    for i in tb_del:
        del tb[i]
    tb.update(safe_builtins)

    if len(libs) != 0:
        for lib in libs:
            if ' ' not in lib:
                tb[lib] = getattr(builtins, lib)

    return tb
