from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class ussignup(UserCreationForm):
    
    class Meta:
        model=CustomUser

    def save(self, commit=True):
        user = super(ussignup, self).save(commit=False)
        user.email=self.cleaned_data["email"]
        user.first_name=self.cleaned_data["first_name"]
        user.last_name=self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user