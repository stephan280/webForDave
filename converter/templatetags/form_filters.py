from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    existing_attrs = field.field.widget.attrs
    existing_attrs["class"] = css_class
    return field.as_widget(attrs=existing_attrs)

