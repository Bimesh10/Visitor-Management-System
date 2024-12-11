from django import forms
from .models import Visitor, Contact

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'email', 'phone', 'date_of_visit', 'purpose']  # Match fields with the Visitor model
    
    # Adjust this line if you want to display contact names with their statuses
    # Assuming 'contact' is a foreign key to the Contact model
    contact = forms.ModelChoiceField(queryset=Contact.objects.all(), label="Contact Person")

    # Add a date picker for 'date_of_visit' using the DateInput widget
    date_of_visit = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # This will render a date picker
        label="Date of Visit"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'contact' in self.fields:
            self.fields['contact'].label_from_instance = lambda obj: f"{obj.name} ({obj.get_status_display()})"
