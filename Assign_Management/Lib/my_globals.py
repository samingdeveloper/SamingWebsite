from RestrictedPython.Guards import safe_builtins
import builtins

def string(*args):
    string = "def test_{0}(self):\n" \
             "    self.actual = {1}\n" \
             "    self.expected = {2}\n" \
             "    self.points = {3}\n" \
             "    self.level = {4}\n" \
             "    globals()[name]['max_score'] += self.points\n" \
             "    try:\n" \
             "        self.assertEquals(self.actual, self.expected)\n" \
             "        if self.level == 0:\n" \
             "            globals()[name]['case'][{0}] = str({1})+' == '+str({2})\n" \
             "        elif self.level == 1:\n" \
             "            globals()[name]['case'][{0}] = 'PASS'\n" \
             "        globals()[name]['score'] += self.points\n" \
             "    except Exception as e:\n" \
             "        if self.level == 0:\n" \
             "            globals()[name]['case'][{0}] = str(e)\n" \
             "        elif self.level == 1:\n" \
             "            globals()[name]['case'][{0}] = 'FAIL'\n" \
             "        raise AssertionError\n".format(repr(args[0]), repr(args[1]), repr(args[2]), args[3], abs(args[4]))
    return string

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

def scr(case_dict):
    for i in case_dict.values():
        if i[2] == "PASS":
            return True
    else:
        return False