from patron.models import  *
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
        username = forms.CharField(help_text = 'Username')
        password = forms.CharField(widget = forms.PasswordInput(), help_text = 'Password')
        confirm_password = forms.CharField(widget = forms.PasswordInput(), help_text = 'Reenter Password')
	email = forms.CharField(help_text= 'E-Mail')
        class Meta:
                model = User
                fields = ('username', 'email','password',)

class PatronForm(forms.ModelForm):
	picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
        class Meta:
                model = Patron
                fields = ('picture',)

class BidForm(forms.ModelForm):
	title           = forms.CharField(help_text = 'Title')
        startpoint      = forms.CharField(help_text = 'Starting Point')
        #exacttime       = forms.DateTimeField(help_text = 'Time')
        #begin           = forms.DateTimeField(help_text = 'From')
        #end             = forms.DateTimeField(help_text = 'To')

        endpoint        = forms.CharField(help_text = 'End Point')

        description     = models.CharField(help_text = 'Description')
	
	class Meta:
		model = Bid
		exclude  = ['patron','status', 'exacttime','begin', 'end']
