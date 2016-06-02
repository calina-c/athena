# from django.shortcuts import render
import os
from django.shortcuts import render_to_response, render, redirect
# from django.template import RequestContext

from django.http import HttpResponse
from athena_app.harvest_manager import get_harvests, delete_harvest
from athena_app.enhancement_manager import enhance_h

from django.views.generic.edit import FormView, DeleteView
from django.views.generic.base import View
from athena_app.forms import HarvestForm


def index(request):
    return render_to_response('base.html')


def enhance_harvest(request, uuid):
    results = enhance_h(uuid)
    return render_to_response('enhance_result.html', results)

class EnhanceView(View):
    def get(self, request, *args, **kwargs):
        return render_to_response('enhance.html', {
            'harvests': get_harvests()
        })


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
