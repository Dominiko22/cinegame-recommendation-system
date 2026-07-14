from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Adres e-mail",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()\
        
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Konto z tym adresem e-mail już istnieje."
            )
        
        return email
    
    def save(self, commit=True):
        user = super().save(commit=True)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user