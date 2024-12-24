from django import forms
from weblogapp.models import Comments,Subscribe
from django.utils.translation import gettext_lazy as _

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = {'content','name','email','website'}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Please type your comments .....'

        self.fields['email'].widget.attrs['placeholder'] = 'Email'

        self.fields['name'].widget.attrs['placeholder'] = 'Name'

        self.fields['website'].widget.attrs['placeholder'] = 'Website'


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields ='__all__'
        labels ={'email': _('')}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Please Write your eamil address'


        