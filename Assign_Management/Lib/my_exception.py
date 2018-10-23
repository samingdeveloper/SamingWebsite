import sys
#import string
import traceback

class my_traceback:

    @staticmethod
    def error_msg(error,escape=0):
        limit = None
        error_type, value, tb = error
        list = traceback.format_exception_only(error_type, value)
        #list = traceback.format_tb(tb, limit) + traceback.format_exception_only(error_type, value)
        body = f'Traceback (most recent call): {error_type.__name__}\n{"".join(list[:-1])}'
        #body = "Traceback (innermost last):\n" + "%-20s %s" % ("".join(list[:-1]), list[-1])
        if escape:
            import html
            body = '\n<PRE>'+html.escape(body)+'</PRE>\n'
        return body

    @staticmethod
    def get_limit(error,file_name='gradingstr'):
        extracts = traceback.extract_tb(sys.exc_info()[2])
        count = len(extracts)
        # find the first occurrence of the module file name
        for i, extract in enumerate(extracts):
            if extract[0] == file_name and "<module>" not in str(extract):
                break
            count -= 1
        return -count