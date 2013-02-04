from django.shortcuts import *
from django.core.urlresolvers import reverse

from document.models import Document, Section, Content
from document.generator import generate_document
from document.forms import DocumentForm, SectionForm, ContentForm

def all_documents(request):
    documents = Document.objects.all()

    return render_to_response('index.html',
    {
        'documents':documents,
        'title':"All Documents",
    },RequestContext(request))


def document(request, document_id):
    document = Document.objects.get(pk=document_id)
    doc_html = generate_document(document)

    return render_to_response('document.html',
    {
        'document':document,
        'doc_html':doc_html,
    })


def create_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            try:
                doc = form.save()
                return redirect(reverse('document.views.edit_document', args=(doc.id,)))
            except Exception as ex:
                print ex
        else:
            print form.errors
    else:
        form = DocumentForm()
    return render_to_response('new.html',
    {
        'title':'Create New Document',
        'form':form,
    },RequestContext(request))


def edit_document(request, document_id):
    document = Document.objects.get(pk=document_id)
    post = request.POST
    if post['type'] == 'new_section':
        if post['parent']:
            parent = Section.objects.get(pk=post['parent_id'])
            new_index = parent.get_next_child()
            new_section = Section.objects.create(
                index = new_index,
                title = post['title']
            )
            new_section.save()
            parent.subsections.add(new_section)
            parent.save()
        else: #parent is document
            new_index = document.get_next_section_index()
            new_section = Section.objects.create(
                index=new_index,
                title = post['title']
            )
            new_section.save()
            document.sections.add(new_section)
            document.save()
    elif post['type'] == 'new_content':
        if post['parent'] == 'content':
            parent = Content.objects.get(pk=post['parent_id'])
            new_content = Content.objects.create(
                content_type = post['content_type'],
                content = post['content'],
            )
            new_content.save()
            parent.children.add(new_content)
            parent.save()
        elif post['parent'] == 'section':
            parent = Section.objects.get(pk=post['parent_id'])
            new_content = Content.objects.create(
                content_type = post['content_type'],
                content = post['content'],
            )
            new_content.save()
            parent.children.add(new_content)
            parent.save()
    else:
        pass

