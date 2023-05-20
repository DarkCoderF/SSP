from django.forms import ModelForm
from .models import Posts, Comment

class PostsForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'photo', 'description']
    def __init__(self, *args, **kwargs):
        super(PostsForm, self).__init__(*args, **kwargs)
        
        #self.fields['title'].widget.attrs.update({'class' : 'input', 'placeholder': 'Add title'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'input'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'input'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'input', 'rows':'5'}
