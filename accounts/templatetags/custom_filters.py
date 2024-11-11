from django import template

register = template.Library()

@register.filter
def attr(obj, field_name):
    """
    自定义过滤器：动态获取对象的属性值
    :param obj: 模板中传入的对象
    :param field_name: 模板中指定的属性名
    :return: 对象的属性值或 None
    """
    return getattr(obj, field_name, None)