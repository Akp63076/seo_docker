from django import forms

class Myform(forms.Form):
    Link = forms.URLField(label='Query Link',
                    widget=forms.TextInput(attrs={'placeholder': 'https://collegedunia.com/university/25598-christ-university-bangalore',
                    'class':"form-control"  ,    
                    'id':"form-linkID"                } 
                             ))

    OPTIONS = (
        ('1 week','last 7 days'),
        ('1 month','Last 30 days'),
        ('3 month','Last 3 Months'),
        ('6 month','Last 6 Months'),
        ('1 year','Last 1 year'),   

        )
    Range = forms.ChoiceField(label='Time Range',required=True, choices=OPTIONS,
    widget=forms.Select(attrs={"class":"form-control btn-primary dropdown-toggle"}))


class AdForm(forms.Form):
    keyword = forms.CharField(
        label='keyword',
                    widget=forms.Textarea(attrs={'placeholder': '10 keywords at a time \njee main\njee advanced\njee main 2021',
                    # 'class':"form-control"  ,    
                    'id':"form-linkID" ,
                    'rows':10, 'cols':100 } 
                             )
    )



