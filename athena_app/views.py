# from django.shortcuts import render
import os
from django.shortcuts import render_to_response, redirect
# from django.template import RequestContext

from django.http import HttpResponse
from athena_app.harvest_manager import get_harvests, delete_harvest

from django.views.generic.edit import FormView, DeleteView
from athena_app.forms import HarvestForm

def index(request):
    return render_to_response('base.html')


class HarvestView(FormView):
    template_name = 'index.html'
    form_class = HarvestForm
    success_url = '/app/harvest/'

    def get_context_data(self, **kwargs):
        context = super(HarvestView, self).get_context_data(**kwargs)
        context['harvests'] = get_harvests()
        return context

    def form_valid(self, form):
        form.create_harvest()
        return super(HarvestView, self).form_valid(form)


def harvest_delete(request, uuid):
    delete_harvest(uuid)
    return redirect('/app/harvest/')
