from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        # Указываем, что надо отобразить все поля.
        fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


# class UserUpdateForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and (User.objects.filter(email=email)
                      .exclude(username=username).exists()):
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email
