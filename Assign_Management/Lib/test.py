def assert_equal(actual, expected, points=0, level=0):
    # rand_string = get_random_string(length=7)
    MyTestCase.num += 1
    # print(locals())
    # print(MyTestCase.num)
    eval(compile(my_globals.string(MyTestCase.num, actual, expected, points, level), 'defstr', 'exec'))
    # print(str(actual)+str(expected)+str(points)+str(hidden))
    # print(string)
    # print(globals())
    # print(globals()[name]['params'])
    # print(str_to_class('test_{0}'.format(rand_string)))
    setattr(MyTestCase, "test_{0}".format(MyTestCase.num), locals()['test_{0}'.format(MyTestCase.num)])
    # setattr(MyTestCase, "test_{0}".format(rand_string), str_to_class('test_{0}'.format(rand_string)))
    # method_list = [func for func in dir(MyTestCase) if callable(getattr(MyTestCase, func)) and not func.startswith("__")]
    # print(method_list)