from django import forms
 
class StringListField(forms.CharField):
    def prepare_value(self, value):
        #return ', '.join(value)
        return ','.join(str(v) for v in value)

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]
