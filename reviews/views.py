from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

from .forms import ReviewForm
from .models import Review

# Create your views here.

class ReviewView(FormView):
    form_class = ReviewForm
    template_name = 'reviews/review.html'
    success_url = '/thank-you'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ThankYouView(TemplateView):
   template_name='reviews/thank_you.html'

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['message'] = 'This Works!'
       return context
   
class ReviewListView(ListView):
    template_name='reviews/reviews_list.html'
    model = Review
    context_object_name = 'reviews'

    
class SingleReviewView(DetailView):
    template_name = 'reviews/single_review.html'
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        favorite_id = self.request.get('favorite_review')
        context['is_favorite'] = favorite_id == str(loaded_review.id)
        return context

class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST['review_id']
        request.session['favorite_review'] = review_id
        return HttpResponseRedirect('/reviews/'+review_id)