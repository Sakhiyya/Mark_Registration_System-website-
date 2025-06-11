from django import forms

class MarksForm(forms.Form):
    module_code = forms.CharField(max_length=10)
    module_name = forms.CharField(max_length=100)
    coursework1_mark = forms.IntegerField(min_value=0, max_value=200)
    coursework2_mark = forms.IntegerField(min_value=0, max_value=200)
    coursework3_mark = forms.IntegerField(min_value=0, max_value=200)
    student_id = forms.CharField(max_length=10)
    student_name = forms.CharField(max_length=100)
    date_of_entry = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])

    def clean(self):
        cleaned_data = super().clean()
        coursework1_mark = cleaned_data.get('coursework1_mark')
        coursework2_mark = cleaned_data.get('coursework2_mark')
        coursework3_mark = cleaned_data.get('coursework3_mark')
        if not (0 <= coursework1_mark <= 200):
            self.add_error('coursework1_mark', 'Mark must be between 0 and 200.')
        if not (0 <= coursework2_mark <= 200):
            self.add_error('coursework2_mark', 'Mark must be between 0 and 200.')
        if not (0 <= coursework3_mark <= 200):
            self.add_error('coursework3_mark', 'Mark must be between 0 and 200.')   
        return cleaned_data