
def assert_equal(actual,expected,points,hidden=False):
        rand_string = get_random_string(length=5)
        globals()[name]['params'] = [actual,expected,points,hidden]
        string = "def test_{0}(self):\n" \
                 "    self.actual = actual\n" \
                 "    self.expected = expected\n" \
                 "    try:\n" \
                 "        self.assertEquals(self.actual, self.expected)\n" \
                 "        if hidden not True:\n" \
                 "            case_result.append('PASS')\n" \
                 "        score += points\n" \
                 "    except:\n" \
                 "        if hidden not True:\n" \
                 "            case_result.append('FAIL')\n" \
                 "        score += 0\n" \
                 "        raise".format(rand_string,)
        eval(compile(string, '<string>', 'exec'), globals())
        setattr(MyTestCase, "test_{0}".format(rand_string,), str_to_class('test_{0}'.format(rand_string,)))
        # case_result["test_text_{0}".format(i)] = globals()['case_{0}_result'.format(i)]
        # from types import MethodType
        # MyTestCase.test_text_1 = MethodType(test_text_1,MyTestCase)
        # print(eval("'test_text_{0}'.format(i)"))
        # method_list = [func for func in dir(MyTestCase) if
        # callable(getattr(MyTestCase, func)) and not func.startswith("__")]
        # print(method_list)


def assert_equal(actual, expected, points, hidden=False):
    rand_string = get_random_string(length=7)
    globals()[name]['params'][rand_string] = {
        'actual': actual,
        'expected': expected,
        'points': points,
        'hidden': hidden,
    }
    string = "def test_{0}(self):\n" \
             "    self.actual = globals()[name]['params'][rand_string]['actual']\n" \
             "    self.expected = expected\n" \
             "    self.points = points\n" \
             "    self.hidden = hidden\n" \
             "    try:\n" \
             "        self.assertEquals(self.actual, self.expected)\n" \
             "        if self.hidden != True:\n" \
             "            globals()[name]['case'].append('PASS')\n" \
             "        globals()[name]['score'] += self.points\n" \
             "    except:\n" \
             "        if self.hidden != True:\n" \
             "            globals()[name]['case'].append('FAIL')\n" \
             "        globals()[name]['score'] += self.points\n" \
             "        raise".format(rand_string)
    # print(locals())
    eval(compile(string, 'defstr', 'exec'), globals(), locals())
    # print(str(actual)+str(expected)+str(points)+str(hidden))
    # print(string)
    # print(globals())
    # print(globals()[name]['params'])
    # print(str_to_class('test_{0}'.format(rand_string)))
    setattr(MyTestCase, "test_{0}".format(rand_string), locals()['test_{0}'.format(rand_string)])
    # setattr(MyTestCase, "test_{0}".format(rand_string), str_to_class('test_{0}'.format(rand_string)))
    # method_list = [func for func in dir(MyTestCase) if callable(getattr(MyTestCase, func)) and not func.startswith("__")]
    # print(method_list)

