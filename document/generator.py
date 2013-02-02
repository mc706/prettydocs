from document.models import *

def wrap(element):
    def wrapper(f):
        def wrapped(*args):
            return "<" + element+ ">" + f() + "</" + element + ">"
        return wrapped
    return wrapper


def generate_content(content,dom=""):
    if content.content_type == 'txt':
        return content.content
    else:
        for child in content.children:
            @wrap(child.content_type)
            generate_content(child)



if __name__ == '__main__':
    @wrap('h')
    @wrap('div')
    def hello():
        return "Hello World!"

    print hello()