from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

#{% with test|index:forloop.counter0 as anothertest %}{{anothertest.name}} {% endwith %}