from django import forms
from jypprj.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('writer','content')


