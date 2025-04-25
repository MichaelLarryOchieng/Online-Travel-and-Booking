from django import forms
from .models import Booking, Seat
from flight.models import Flight

class BookingForm(forms.ModelForm):
    selected_seats = forms.ModelMultipleChoiceField(
        queryset=Seat.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Seats"
    )

    class Meta:
        model = Booking
        fields = ['selected_seats']

    def __init__(self, *args, **kwargs):
        flight_instance = kwargs.pop('flight_instance', None)
        super().__init__(*args, **kwargs)
        if flight_instance:
            self.fields['selected_seats'].queryset = Seat.objects.filter(flight=flight_instance, is_available=True)

    def clean(self):
        cleaned_data = super().clean()
        selected_seats = cleaned_data.get('selected_seats')
        seats_booked = self.data.get('seats_booked')

        # Validate seats_booked
        try:
            seats_booked = int(seats_booked)
        except (TypeError, ValueError):
            raise forms.ValidationError("Invalid number of seats booked.")

        if selected_seats:
            if seats_booked != len(selected_seats):
                raise forms.ValidationError(f"Please select exactly {seats_booked} seats.")
        return cleaned_data