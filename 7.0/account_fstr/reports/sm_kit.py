import re

def groupe_digits(digite, separator=','):
    digite = str(digite)
    if '.' in digite:
        re_obj = re.compile(r'(?<=\d)(?=(?:\d\d\d)+\.)')
    else:
        re_obj = re.compile(r'(?<=\d)(?=(?:\d\d\d)+$)')
    result = re_obj.sub(separator, digite)
    return result
