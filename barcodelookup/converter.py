
class BarcodeConverter:
    regex = '[0-9]{13}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%013d' % value