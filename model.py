from click import DateTime
from traitlets import Integer


class Event:
    id = Integer
    date = DateTime
    title = str
    text = str