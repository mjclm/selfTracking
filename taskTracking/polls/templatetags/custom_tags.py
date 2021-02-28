import random
from django import template

register = template.Library()


@register.simple_tag
def champion_welcome(name, level):
    if level > 42:
        welcome = f"Hello great champion {name}!"
    elif level > 20:
        welcome = f"Greetings noble warrior {name}!"
    elif level > 5:
        welcome = f"Hello {name}."
    else:
        welcome = "Oh, it's you."
    return welcome
