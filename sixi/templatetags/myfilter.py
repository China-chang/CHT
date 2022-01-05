#coding=utf-8
from django import  template
from django.template import Library

register = Library()

@register.filter
def md(value):
    import markdown
    return markdown.markdown(value)