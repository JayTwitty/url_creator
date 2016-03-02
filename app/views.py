from django.core.urlresolvers import reverse
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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_index_view")

    def get(self, request):
        url_form = URLForm()
        return render(request, "app/url_form.html", {"form": url_form})

    def post(self, request):
        form_instance = URLForm(self.request.POST)
        hashids = Hashids()
        if form_instance.is_valid():
            url_object = form_instance.save()
            hashid = hashids.encode(url_object.id)
            url_object.output_url=hashid
            url_object.user=self.request.user
            url_object.save()
            bookmarks = URL.objects.all()
        return render(request, 'user_list_template.html', {"bookmarks":bookmarks,
                                                'url': url_object})

class UserListView(ListView):
    model = URL
    fields = ('input_url', 'output_url', 'timestamp')
    template_name = "user_list_template.html"

    def get_queryset(self):
        user=self.request.user
        return URL.objects.filter(user=user)