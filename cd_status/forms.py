from django import forms

class Myform(forms.Form):
        Link = forms.URLField(label='Query Link',
                    widget=forms.TextInput(attrs={'placeholder': 'https://collegedunia.com/university/25598-christ-university-bangalore',
                    'class':"form-control"  ,    
                    'id':"form-linkID"                } 
                             ))