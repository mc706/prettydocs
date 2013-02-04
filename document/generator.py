from document.models import Content, Section, Document


def wrap(string, element):
    return "<" + element+ ">\n" + string + "\n</" + element + ">\n"

def generate_content(content):
    '''reverses self referential model to dom structure'''
    if content.content_type == 'txt' or content.children.all().count()==0:
        return str(content.content)
    else:
        dom = ""
        for child in content.children.all():
            dom += generate_content(child)
        return wrap(dom,content.content_type)

def generate_section(section):
    dom = ''
    dom += section.get_html_title() + '\n'
    for content in section.content.all():
        dom += generate_content(content)
    for subsection in section.subsections.all():
        dom += generate_section(subsection)
    return dom

def generate_document(document):
    dom = '<h1>%s</h1>'%document.title
    for section in document.sections.all():
        dom += generate_section(section)
    return dom

if __name__ == '__main__':
    #TESTS
    c1 = Content.objects.create(
        content_type='div'
    )
    c2 = Content.objects.create(
        content_type='ul'
    )
    c3 = Content.objects.create(
        content_type='li'
    )
    c4 = Content.objects.create(
        content_type='txt',
        content = 'test1'
    )
    c5 = Content.objects.create(
        content_type='li',
    )
    c6 = Content.objects.create(
        content_type='text',
        content = 'test2'
    )
    c7 = Content.objects.create(
        content_type='text',
        content = 'test3'
    )
    c5.children.add(c6)
    c3.children.add(c4)
    c2.children.add(c3)
    c2.children.add(c5)
    c1.children.add(c2)
    c1.children.add(c7)
    g = generate_content(c1)
    print g
