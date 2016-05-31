from django import forms
from athena_app.tasks import harvest_task


class HarvestForm(forms.Form):
    hashtag = forms.CharField();
    start_date = forms.DateField(widget=forms.TextInput(
        attrs={'class':'datepicker'})
    )
    end_date = forms.DateField(widget=forms.TextInput(
        attrs={'class':'datepicker'})
    )

    def create_harvest(self):
        harvest_task.delay(
            self.cleaned_data['hashtag'],
            unicode(self.cleaned_data['start_date']),
            unicode(self.cleaned_data['end_date']),
        )
