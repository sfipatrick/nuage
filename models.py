# -*- coding: utf-8 -*-


from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User, Group

from datetime import datetime, date


class Page(MPTTModel):

    title = models.CharField(_("Title"), max_length=100, help_text=_("100 caract max"))
    subhead = models.CharField(_("Subhead"), max_length=300, blank=True,help_text=_("300 caract max"))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    num = models.IntegerField(_("Order of the page"), help_text=_("Integer"))
    logo = models.ImageField(_("Logo of the page"),blank=True, upload_to="upload/pages/logo")
    text = models.TextField(_("Text"),blank=True,)

    description = models.TextField(_("Description in meta"),blank=True,)
    url = models.SlugField(_("url"), unique=True, db_index=True, max_length=100, help_text=_("100 caract max"))


    def __unicode__(self):
        return u'%s' %(self.title)

    def json_list(self):
        fields =('id','title','url','level','lft','rght')
        d = dict((field, self.__dict__[field]) for field in fields)
        d["parent_id"] = (self.parent.id if self.parent else 0)

        return d

    def json(self):
        fields =('id','title','url','lft','rght','level','subhead','text')
        d = dict((field, self.__dict__[field]) for field in fields)
        d["parent_id"] = (self.parent.id if self.parent else 0)
        d["childs"] = [p.json_list() for p in Page.objects.filter(parent=self)]
        return d


    class Meta:
        unique_together = ("parent", "num")
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def get_absolute_url(self):
        return u'%s#page%s' %(self.url, self.id)

    class MPTTMeta:
        level_attr = 'level'
        order_insertion_by = ['num']


class PageImage(models.Model):
    image = models.ImageField(_("Image"), blank=True, upload_to="upload/pages/img" )
    page = models.ForeignKey('Page')
    title = models.CharField(_("Title"),max_length=50)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ('num',)


    def __unicode__(self):
        return u'%s ' %(self.title)
