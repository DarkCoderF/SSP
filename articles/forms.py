from django import forms
from . import models

class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'slug', 'subheading', 'body', 'image', 'tags']
        def __init__(self, *args, **kwargs):
            super(models.Article, self).__init__(*args, **kwargs)
            for name, field in self.fields.items():
                field.widget.attrs.update({'class' : 'input'})