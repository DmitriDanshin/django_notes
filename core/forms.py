from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CharField, Textarea
from .models import Note


class NoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = {
            "class": "form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white "
                     "bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 "
                     "focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
        }
        self.fields['text'].widget.attrs.update(attrs)

    text = CharField(widget=Textarea)

    class Meta:
        model = Note
        fields = ['text']


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = {'class': 'shadow appearance-none border'
                          'rounded w-full py-2 px-3 text-gray-700 mb-3 '
                          'leading-tight '
                          ' focus:outline-none focus:shadow-outline', }
        self.fields['username'].widget.attrs.update(attrs)
        self.fields['password1'].widget.attrs.update(attrs)
        self.fields['password2'].widget.attrs.update(attrs)
