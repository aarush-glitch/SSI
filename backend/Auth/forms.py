from django import forms


class OTPForm(forms.Form):
    action_choices = [
        ('generate', 'Generate OTP'),
        ('verify', 'Verify OTP'),
        ('resend', 'Resend OTP')
    ]
    phone_number = forms.IntegerField(required=True)
    action = forms.ChoiceField(required=True, choices=action_choices)
    otp = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        action = cleaned_data.get('action')
        otp_code = cleaned_data.get('otp')

        if not phone_number or len(str(phone_number)) != 10:
            self.add_error('phone_number', f"Enter a valid 10 digit Mobile Number")
            return

        if action == 'verify' and not otp_code:
            self.add_error('otp', f"OTP is required for verification")
            return

        if action == 'verify' and len(str(otp_code)) != 6:
            self.add_error('otp', f"Enter a valid 6 digit OTP")
            return

        return self.cleaned_data
