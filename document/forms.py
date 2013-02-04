from django.forms import ModelForm

from document.models import Content, Section, Document


class DocumentForm(ModelForm):

     class Meta:
         model = Document
         fields = (
             'title',
             'description',
         )


class SectionForm(ModelForm):

    class Meta:
        model = Section


class ContentForm(ModelForm):

    class Meta:
        model = Content