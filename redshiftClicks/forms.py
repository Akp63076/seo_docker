from django import forms

class Myform(forms.Form):
    Link = forms.URLField(label='Query Link',
                    widget=forms.TextInput(attrs={'placeholder': 'https://collegedunia.com/university/25598-christ-university-bangalore',
                    'class':"form-control"  ,    
                    'id':"form-linkID"                } 
                             ))
    email = forms.EmailField(label='Enter your email', max_length=100,
    widget=forms.TextInput(attrs={'placeholder': 'youremail@company.com',
                    'class':"form-control" 
                                   } 
                             ))

    OPTIONS = (
        ('1 week','Weekly'),
        ('1 month','Monthly'),
        ('3 month','3 Months'),
        ('6 month','6 Months'),

        )
    Range = forms.ChoiceField(label='Time Range',required=True, choices=OPTIONS,
    widget=forms.Select(attrs={"class":"form-control btn-primary dropdown-toggle"}))

