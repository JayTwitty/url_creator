from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.views.generic import CreateView, ListView, DetailView, UpdateView
from hashids import Hashids

from app.models import URL, Click


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
        object.output_url = hashid
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_index_view")


def redirect_view(request, captured_id):
    redirect_object = URL.objects.get(output_url=captured_id)
    redirect = redirect_object.input_url
    Click.objects.create(url=redirect_object)
    return HttpResponseRedirect(redirect)


class UserListView(ListView):
    model = URL
    fields = ('input_url', 'output_url', 'timestamp')
    template_name = "user_list_template.html"

    def get_queryset(self):
        user = self.request.user
        return URL.objects.filter(user=user)


class URLDetailView(DetailView):
    model = URL



class URLUpdateView(UpdateView):
    model = URL
    fields = ('input_url', )

    def get_success_url(self):
        return reverse("user_index_view")
