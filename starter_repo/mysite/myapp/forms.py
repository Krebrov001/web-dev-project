# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def validate_new_response(value):
    error_message = """Your post appears to contain code that is not properly
    formatted as code. Please surround all code snippets with
    ``` characters, before and after."""
    code_delimiter = "```"
    # The number of characters in the value string.
    num_chars = len(value)
    # The number of code_delimiters in the response text.
    num_delimiters = 0
    # The index into the code_delimiter string.
    index1 = 0
    j = 0
    # This loop counts the number of code_delimiters "```".
    # Why in the world are hter no "normal" for-loops in Python?
    while j < num_chars:
        if code_delimiter[index1] == value[j]:
            # The current character matches.
            index1 += 1
        else:
            # No match.
            index1 = 0
        # All 3 characters of "```'" matched.
        # We found a code delimiter!
        if index1 == 3:
            num_delimiters += 1
            index1 = 0
        j += 1
    # We need to have an even number of code delimiters,
    # which means that for every opening code delimiter there is also a closing
    # code delimiter
    if num_delimiters % 2 != 0:
        raise forms.ValidationError(error_message)
    else:
        return value


# This is an anonymous response.
class ResponseForm(forms.Form):
    # The name of the author.
    author_name = forms.CharField(label='Your name', max_length=32)
    # The author's email address.
    author_email = forms.EmailField(validators=[validate_email],
    label='Your email address', max_length=254)
    # The date and time when this response was made.
    # response_date = models.DateTimeField(auto_now_add=True)
    # The text content of the response.
    response_content = forms.CharField(validators=[validate_new_response],
    label="""Write your response here.\n Add ``` characters before and after
    code snippets to enable syntax formatting.""",
     widget=forms.Textarea, max_length=4000)


# This is a user response.
class UserResponseForm(forms.Form):
    # The date and time when this response was made.
    # response_date = models.DateTimeField(auto_now_add=True)
    # The text content of the response.
    response_content = forms.CharField(validators=[validate_new_response],
    label="""Write your response here.\n Add ``` characters before and after
    code snippets to enable syntax formatting.""",
     widget=forms.Textarea, max_length=4000)


# This is an anonymous comment.
class AnonCommentForm(forms.Form):
    # The name of the author.
    author_name = forms.CharField(label='Your name', max_length=32)
    # The author's email address.
    author_email = forms.EmailField(validators=[validate_email],
    label='Your email address', max_length=254)
    # The date and time when this comment was made.
    # comment_date = models.DateTimeField(auto_now_add=True)
    # The text content of the comment.
    comment_content = forms.CharField(validators=[validate_new_response],
    label="""Write your comment here.\n Add ``` characters before and after
    code snippets to enable syntax formatting.""",
     widget=forms.Textarea, max_length=4000)
    parent_response_id = forms.IntegerField(widget=forms.HiddenInput(),
    required=False, initial=0)
    parent_response_type = forms.CharField(widget=forms.HiddenInput(),
    max_length=4, required=False)


# This is a user comment.
class UserCommentForm(forms.Form):
    # The date and time when this comment was made.
    # comment_date = models.DateTimeField(auto_now_add=True)
    # The text content of the comment.
    comment_content = forms.CharField(validators=[validate_new_response],
    label="""Write your comment here.\n Add ``` characters before and after
    code snippets to enable syntax formatting.""",
     widget=forms.Textarea, max_length=10000)
    parent_response_id = forms.IntegerField(widget=forms.HiddenInput(),
    required=False, initial=0)
    parent_response_type = forms.CharField(widget=forms.HiddenInput(),
    max_length=4, required=False)


class EmailForm(forms.Form):
    # The name of the sender.
    sender_name = forms.CharField(label='Your name', max_length=32)
    # The sender's email address.
    sender_email = forms.EmailField(validators=[validate_email],
    label='Your email address', max_length=254)
    # The text content of the email.
    email_text = forms.CharField(label="Write the body of your email here.",
    widget=forms.Textarea, max_length=80000)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email], label="Email", required=True)
    first_name = forms.CharField(label='Your first name', max_length=30)
    last_name = forms.CharField(label='Your last name', max_length=150)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name",
                  "last_name")

    # Default argument for the commit variable.
    # Unless told otherwise, it always commits.
    def save(self, commit=True):
        # The superclass instance tales care of the inherited fields.
        # commit=False makes sure that the superclass instance does not save
        # the data into the database because it is not complete yet.
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


# my
