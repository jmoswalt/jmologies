from django.contrib import admin
from django.utils.encoding import iri_to_uri
from django.core.urlresolvers import reverse

from analogies.models import Analogy, Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ["name"]

class AnalogyAdmin(admin.ModelAdmin):
    list_display = ['view_on_site', 'edit_link', 'first', 'verb', 'second', 'private']
    list_filter = ["first", "second"]

    fieldsets = (
        (None, {'fields': (
            'first',
            'verb',
            'second',
            'content',
            'private',
        )}),
    )

    def view_on_site(self, obj):
        link = '<a href="%s" title="%s">View</a>' % (
            reverse('analogies.detail', args=[obj.slug, obj.pk]),
            obj,
        )
        return link
    view_on_site.allow_tags = True
    view_on_site.short_description = 'view'

    def edit_link(self, obj):
        link = '<a href="%s" title="edit">Edit</a>' % reverse('admin:analogies_analogy_change', args=[obj.pk])
        return link
    edit_link.allow_tags = True
    edit_link.short_description = 'edit'


    def change_view(self, request, object_id, extra_context=None):
        result = super(AnalogyAdmin, self).change_view(request, object_id, extra_context)

        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and request.GET.has_key('next'):
            result['Location'] = iri_to_uri("%s") % request.GET.get('next')
        return result

admin.site.register(Analogy, AnalogyAdmin)
admin.site.register(Item, ItemAdmin)
