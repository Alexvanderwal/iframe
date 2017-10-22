from djchoices import DjangoChoices, ChoiceItem


class PinStatus(DjangoChoices):
    none = ChoiceItem('Not pinned')
    locally = ChoiceItem('Locally pinned for category')
    globally = ChoiceItem('Globally pinned for category')