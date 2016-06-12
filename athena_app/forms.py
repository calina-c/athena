from django import forms
from athena_app.tasks import harvest_task
from athena_app.harvest_manager import get_harvests
from athena_app.normalise_manager import normalise
from datetime import datetime


class HarvestForm(forms.Form):
    hashtag = forms.CharField(label='hashtag or content')
    start_date = forms.DateField(
        label='Tweet from start date',
        widget=forms.TextInput(
            attrs={'class':'datepicker'}
        )
    )
    end_date = forms.DateField(
        label='Tweets through date',
        widget=forms.TextInput(
            attrs={'class':'datepicker'}
        )
    )

    def create_harvest(self):
        harvest_task.delay(
            self.cleaned_data['hashtag'],
            unicode(self.cleaned_data['start_date']),
            unicode(self.cleaned_data['end_date']),
        )

def get_normalisable_harvests():
    all_harvests = list(get_harvests())
    return [
        (
            x.uuid,
            x.hashtag + ' from ' +
            datetime.strftime(x.start_date, '%Y-%m-%d') + 'to ' +
            datetime.strftime(x.end_date, '%Y-%m-%d')
        )
        for x in all_harvests if x.done
    ]

class NormaliseForm(forms.Form):
    harvest = forms.ChoiceField(choices=get_normalisable_harvests())

    def normalise_harvest(self):
        normalise(self.cleaned_data['harvest'])
