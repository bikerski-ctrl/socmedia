from django import forms
from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    image = forms.FileField()

    class Meta:
        model = Post
        fields = ['content', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
