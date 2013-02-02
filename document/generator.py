from document.models import Content

def wrap(element):
    def wrapper(f):
        def wrapped(*args):
            return "<" + element+ ">" + f() + "</" + element + ">"
        return wrapped
    return wrapper

def enclose(f,element):
    return "<" + element+ ">" + f() + "</" + element + ">"


def generate_content(content,dom=""):
    if content.content_type == 'txt':
        return content.content
    else:
        for child in content.children.all():
            enclose(generate_content(child),content.content_type)



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
    c5.children.add(c6)
    c3.children.add(c4)
    c2.children.add(c3)
    c2.children.add(c6)
    c1.children.add(c2)
    print generate_content(c1)