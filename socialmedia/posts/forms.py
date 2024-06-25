from django import forms
from posts.models import Post, Comment


class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    delete_image = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Post
        fields = ['content', 'locked', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = kwargs.get('instance', self.instance)

    def save(self, commit=True):
        post = super().save(commit=False)
        if self.cleaned_data['delete_image']:
            post.image = None
        elif self.cleaned_data['image']:
            post.image = self.cleaned_data['image']
        elif self.instance:
            post.image = self.instance.image
        if commit:
            post.save()
            self.save_m2m()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
