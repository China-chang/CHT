from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TEMP1 = """
<div class='content' style='margin-left:%s;'>
    <span>%s</span>
"""


def generate_comment_html(sub_comment_dic, margin_left_val):
    html = '<div class="comment">'
    #遍历子元素
    for k, v_dic in sub_comment_dic.items():
        html += TEMP1 % (margin_left_val, k[1])
        #假如子元素的值为真,说明有子评论
        if v_dic:
            #递归处理,直到全部处理完
            html += generate_comment_html(v_dic, margin_left_val)
        html += "</div>"
    html += "</div>"
    return html


@register.simple_tag
def tree(comment_dic):
    html = '<div class="comment">'
    for k, v in comment_dic.items():
        html += TEMP1 % (0, k[1])
        #设置向右偏移30个像素
        html += generate_comment_html(v, 30)
        html += "</div>"
    html += '</div>'

    return mark_safe(html)
