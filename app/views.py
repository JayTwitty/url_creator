from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView
from hashids import Hashids

from app.forms import URLForm
from app.models import URL


class URLListView(ListView):
    model = URL
    fields = ('input_url',)


class URLCreateView(CreateView):
    model = URL
    fields = ('input_url', 'title', 'description')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        hashids = Hashids(min_length=5)
        hashid = hashids.encode(object.id)
        object.output_url=hashid
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_index_view")


def redirect_view(request, captured_id):
    redirect_object = URL.objects.get(output_url=captured_id)
    redirect = redirect_object.input_url
    return HttpResponseRedirect(redirect)


class UserListView(ListView):
    model = URL
    fields = ('input_url', 'output_url', 'timestamp')
    template_name = "user_list_template.html"

    def get_queryset(self):
        user=self.request.user
        return URL.objects.filter(user=user)

