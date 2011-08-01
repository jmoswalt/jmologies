from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

VERB_CHOICES = (
    ('am','am'),
    ('is','is'),
    ('are','are'),
    ('was','was'),
    ('were','were',),
)

class Item(models.Model):
    name = models.CharField(_('name'), max_length=80, unique=True)
    slug = models.CharField(_('slug'), max_length=100, default="", unique=True, editable=False)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __unicode__(self):
        return self.name

    def save(self):
        self.slug = slugify(self)
        super(Item, self).save()


class Analogy(models.Model):
    first = models.ForeignKey(Item, related_name='first')
    verb = models.CharField(_('verb'), max_length=5, choices=VERB_CHOICES, default="is")
    second = models.ForeignKey(Item, related_name='second')
    content = models.TextField(_('content'))
    slug = models.CharField(_('slug'), max_length=180, default="")
    private = models.BooleanField(_('private'), default=False)
    create_dt = models.DateTimeField(_('create date'), auto_now_add=True)

    class Meta:
        verbose_name = _('Analogy')
        verbose_name_plural = _('Analogies')

    def __unicode__(self):
        return "%s %s like %s" % (self.first, self.verb, self.second)

    @models.permalink
    def get_absolute_url(self):
        return ('analogies.detail', [self.slug])

    def save(self):
        self.slug = "%s-%s-like-%s" % (self.first.slug, self.verb, self.second.slug)
        super(Analogy, self).save()
