from django import template

register = template.Library()


def negative_value(value):
    return -value


def multi(value, arg):
    return value * arg


def dived(value, arg):
    return value // arg


def expression(value, *args):
    for idx, arg in enumerate(args, 1):
        value = value.replace(f'%{idx}', str(arg))
    return eval(value)


register.filter('negative',negative_value)
register.filter('multi',multi)
register.filter('dived',dived)
register.simple_tag(name='expression', func=expression)
