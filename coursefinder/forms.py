from django import forms


class Myform(forms.Form):
    # OPTIONS = (
    #     ('1 week','last 7 days'),
    #     ('1 month','Last 30 days'),
    #     ('3 month','Last 3 Months'),
    #     ('6 month','Last 6 Months'),
    #     ('1 year','Last 1 year'),

    #     )

    # Range = forms.ChoiceField(label='Time Range',required=True, choices=OPTIONS,
    # widget=forms.Select(attrs={"class":"form-control btn-primary dropdown-toggle",'id':"form-linkID"}))

    Level = forms.ChoiceField(
        label="Level",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control btn-primary dropdown-toggle",
                "id": "level-dropdown",
                "multiple": "multiple",
            }
        ),
    )
    Stream = forms.ChoiceField(
        label="Stream",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control btn-primary dropdown-toggle",
                "id": "stream-dropdown",
                "multiple": "multiple",
            }
        ),
    )

    substream = forms.ChoiceField(
        label="Substream",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control btn-primary dropdown-toggle",
                "id": "sub-stream-dropdown",
                "multiple": "multiple",
            }
        ),
    )

    Country = forms.ChoiceField(
        label="Country",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-control btn-primary dropdown-toggle",
                "id": "country-dropdown",
            }
        ),
    )
