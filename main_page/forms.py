from django import forms

CHOICES = (
    ("1", "Today"),
    ("2", "Yesterday"),
    ("3", "Week"),
    ("4", "Month"),
    ("5", "Year")
)


class DateSelectionForm(forms.Form):
    date = forms.ChoiceField(choices=CHOICES)
