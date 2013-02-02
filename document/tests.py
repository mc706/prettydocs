"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from document.models import *
from document.generator import *


class SimpleTest(TestCase):
    def setUp(self):
        self.c1 = Content.objects.create(
            content_type='div'
        )
        self.c2 = Content.objects.create(
            content_type='ul'
        )
        self.c3 = Content.objects.create(
            content_type='li'
        )
        self.c4 = Content.objects.create(
            content_type='txt',
            content = 'test1'
        )
        self.c5 = Content.objects.create(
            content_type='li',
        )
        self.c6 = Content.objects.create(
            content_type='text',
            content = 'test2'
        )
        self.c5.children.add(self.c6)
        self.c3.children.add(self.c4)
        self.c2.children.add(self.c3)
        self.c2.children.add(self.c6)
        self.c1.children.add(self.c2)

    def test_generator(self):
        print generate_content(self.c1)