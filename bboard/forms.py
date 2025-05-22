from django import forms

from .models import Rubric, Bb, BbImage


class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = ['rubric', 'title', 'content', 'price', 'youtube_link']

class BbImageForm(forms.ModelForm):
    image = forms.ImageField(label='Фото', required=False)

    class Meta:
        model = BbImage
        fields = ['image']


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label="Поиск")
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Категория')


