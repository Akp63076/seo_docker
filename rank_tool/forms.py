from django import forms
from rank_tool.models import upload


class EmailModelForm(forms.ModelForm):    
    email = forms.EmailField(max_length=200,widget=forms.TextInput(attrs={'class': "form-control",'id': "clientemail"}))
    class Meta:
        model = upload
        fields =('email','file',)