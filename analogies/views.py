from itertools import chain

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q

from analogies.models import Analogy, Item


def index(request, template_name='analogies/index.html'):
    analogies = Analogy.objects.all()

    if request.user.is_anonymous():
        analogies = analogies.filter(private=False)

    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))


def short_url(request, id=None):
    analogy = get_object_or_404(Analogy, pk=id)
    return HttpResponseRedirect(reverse('analogies.detail', args=[analogy.slug, analogy.pk]))


def detail(request, slug=None, id=None, template_name='analogies/detail.html'):
    analogy = get_object_or_404(Analogy, slug=slug, pk=id)

    if request.user.is_anonymous() and analogy.private:
        raise Http404

    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))


def item(request, slug=None, template_name='analogies/item.html'):
    item = get_object_or_404(Item, slug=slug)

    analogies_first = Analogy.objects.filter(first=item)
    analogies_second = Analogy.objects.filter(second=item)

    analogies = analogies_first | analogies_second

    if request.user.is_anonymous():
        analogies = analogies.filter(private=False)

    analogies = analogies.order_by('-create_dt')

    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))
