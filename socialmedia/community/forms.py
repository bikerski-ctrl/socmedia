from django import forms
from community.models import Community

class CommunityForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Community
        fields = ['name', 'description', 'image', 'only_staff_post']
