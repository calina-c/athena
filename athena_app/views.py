# from django.shortcuts import render
import os
from django.shortcuts import render_to_response
# from django.template import RequestContext

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from django.http import HttpResponse

from django.views.generic.edit import FormView
from athena_app.forms import HarvestForm

consumer_key="tARl2kr5TrsirivWX2VDv5SZo"
consumer_secret="6h4MgUKAPKZpGqHOPVAr6QIofmqkAEh3udBsEVvagBav8OydKd"

access_token="728982451-bgabGFyiqh4uMp85b5y3IicPjqifWDcgf9T1gvvg"
access_token_secret= "t4D3lnP1cjmqYJLMsE08s8sw0zFn15WUUyjRuXk18MRiY"


def index(request):
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth)
    # tweets = tweepy.Cursor(api.search, q='cricket').items(10)
    #
    # for tweet in tweets:
    #     print tweet.created_at, tweet.text, tweet.lang

    return render_to_response('base.html')


class HarvestView(FormView):
    template_name = 'index.html'
    form_class = HarvestForm
    success_url = '/app/'

    def form_valid(self, form):
        form.create_harvest()
        return super(HarvestView, self).form_valid(form)
