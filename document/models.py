from django.db import models
from django.contrib.auth.models import User


class Content(models.Model):
    '''Content of a section'''
    content_type = models.CharField(choices=(
        ('ul','List(unordered)'),
        ('ol','List(ordered)'),
        ('li','List item'),
        ('div','Divider'),
        ('p','Paragraph'),
        ('pre','Code Block'),
        ('h5','Header'),
        ('dl','description list'),
        ('dt','description title'),
        ('dd','description description'),
        ('txt','text'),
    ),default='p',max_length=10)
    content = models.TextField(blank=True, null=True)
    children = models.ManyToManyField("self", symmetrical=False, blank=True, null=True, related_name='child')

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'content'
        verbose_name_plural = 'content'


class Section(models.Model):
    '''Section of document'''
    section_type = models.CharField(choices=(
        ('abs','Abstract'),
        ('prf','Preface'),
        ('toc','Table of Content'),
        ('cpt','Chapter'),
        ('sub','SubChapter'),
        ('rev','Revision History'),
        ('bib','Bibliography'),
    ),max_length=5, blank=True, null=True)
    index = models.IntegerField(default=1)
    subsections = models.ManyToManyField("self", symmetrical=False, blank=True, null=True)
    content = models.ManyToManyField(Content, blank=True, null=True)
    title = models.CharField(max_length=32)

    def get_parent(self):
        '''Gets section Parent'''
        parents = self.section_set.all()
        if parents.count() == 1:
            return parents[0]
        else:
            return False

    def get_next_index(self):
        parent = self.get_parent()
        index = parent.subsections.all().count()
        return index + 1

    def get_next_child(self):
        return  self.subsections.all().count() + 1

    def get_number(self):
        '''Gets Section Number'''
        section_tree = [self.index]
        def climb_tree(section):
            parent = section.get_parent()
            if parent:
                section_tree.append(parent.index)
                climb_tree(parent)
            else:
                return True
        climb_tree(self)
        return ".".join([str(s) for s in reversed(section_tree)])

    def get_full_title(self):
        '''gets section title'''
        return self.get_number() + " " + self.title.title()

    def get_html_title(self):
        header_size = self.get_number().count('.') + 2
        return "<h{0} id={2}>{1}</h{0}>".format(header_size, self.get_full_title(),self.get_number())

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'section'
        verbose_name_plural = 'sections'


class DocumentType(models.Model):
    '''Defines type of document'''
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ['name']
        verbose_name = 'type'
        verbose_name_plural = 'types'

class Audit(models.Model):
    '''change history for everything'''
    changed_by = models.ForeignKey(User)
    changed_date = models.DateTimeField(auto_now=True)
    reason_changed = models.TextField(blank=True, null=True)



class DocumentTags(models.Model):
    '''Create Tags for Docueents'''
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ['name']
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class Document(models.Model):
    '''Document Model'''
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    type = models.ForeignKey(DocumentType, blank=True, null=True)
    tags = models.ManyToManyField(DocumentTags, blank=True, null=True)
    creator = models.ForeignKey(User)
    sections = models.ManyToManyField(Section, blank=True, null=True)
    
    def get_section_list(self):
        sections = []
        def list_children(section):
            children = []
            if section.subsections.all().count() > 0:
                children.append(section.get_full_title)
            else:
                children.append(section.get_full_title)
                for subsection in section.subsections.all():
                    children += list_children(subsection)
            return children
        for section in self.sections:
            sections.append(section.get_full_title)
            sections += list_children(section)
        return sections
                

    def __unicode__(self):
        return self.title

    def get_next_section_index(self):
        return self.sections.all().count() + 1

    class Meta:
        verbose_name = 'document'
        verbose_name_plural = 'documents'


class DocumentHistory(models.Model):
    '''Revision History of Document'''
    audit = models.ForeignKey(Audit)
    document = models.ManyToManyField(Document, blank=True, null=True)

class SectionHistory(models.Model):
    '''Revision History of Document'''
    audit = models.ForeignKey(Audit)
    section = models.ManyToManyField(Section, blank=True, null=True)

class ContentHistory(models.Model):
    '''Revision History of Document'''
    audit = models.ForeignKey(Audit)
    content = models.ManyToManyField(Content, blank=True, null=True)