from django import forms
from django.forms import formset_factory
from .models import guest

class Quiz(forms.ModelForm):

    # Основная форма для гостей

    alcohol = forms.MultipleChoiceField(
        choices=guest.ALCOHOL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Предпочитаемый алкоголь (можно несколько вариантов)"
    )

    consent = forms.TypedChoiceField(
        choices=((True, "Да, с радостью приду"), (False, "К сожалению, не смогу")),
        coerce=lambda x: x == "True",
        widget=forms.RadioSelect,
        required=True,
        label="Подтвердите свое присутствие",
    )

    class Meta:
        model = guest
        fields = ('first_name', 'last_name', 'consent', 'alcohol')
        

    def clean_alcohol(self):
        # приводим список к виду для ArrayField
        return self.cleaned_data['alcohol']
    
class Quiz_dop(forms.Form):

    # Форма для добавления доп гостей

    first_name = forms.CharField(max_length=15, label='Имя')
    last_name = forms.CharField(max_length=15, label='Фамилия')

Quiz_dop = formset_factory(Quiz_dop, extra=0, can_delete=True)