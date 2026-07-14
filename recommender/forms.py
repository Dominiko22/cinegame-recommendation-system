from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Adres e-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "auth-input",
                "placeholder": "np. dominik@email.com",
                "autocomplete": "email",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Nazwa użytkownika",
            "password1": "Hasło",
            "password2": "Powtórz hasło",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "auth-input",
                    "placeholder": "Wpisz nazwę użytkownika",
                    "autocomplete": "username",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        self.fields["password1"].widget.attrs.update(
            {
                "class": "auth-input",
                "placeholder": "Minimum 8 znaków",
                "autocomplete": "new-password",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "auth-input",
                "placeholder": "Wpisz hasło ponownie",
                "autocomplete": "new-password",
            }
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Konto z tym adresem e-mail już istnieje."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Wpisz nazwę użytkownika",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(
            attrs={
                "class": "auth-input",
                "placeholder": "Wpisz hasło",
                "autocomplete": "current-password",
            }
        ),
    )
