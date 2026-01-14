from django import forms
from .models import Resource

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'link', 'resource_type', 'file']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Title'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Description'
            }),
            'link': forms.URLInput(attrs={
                'placeholder': 'Paste resource link (optional)'
            }),
            'resource_type': forms.Select(attrs={
                'placeholder': 'Select Source Tag'
            }),
            'file': forms.ClearableFileInput(attrs={
                'placeholder': 'Upload file (optional)'
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        link = cleaned_data.get('link')
        file = cleaned_data.get('file')

        if link and file:
            raise forms.ValidationError("Provide either link or file, not both.")
        if not link and not file:
            raise forms.ValidationError("Link or file is required.")

        return cleaned_data
