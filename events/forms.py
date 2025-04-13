from django import forms
from .models import Event, Participant

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'location', 'status']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        print(start_date)
        print(end_date)
        print(end_date < start_date)

        if start_date and end_date and end_date < start_date:
            self.add_error(
                'end_date',
                'Дата окончания не может быть раньше даты начала.'
            )

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'event']
        widgets = {
            'event': forms.HiddenInput()  # Скрываем поле события, если оно передается через URL
        }