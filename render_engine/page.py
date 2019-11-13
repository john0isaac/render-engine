import os
import re
import typing
from pathlib import Path

from jinja2 import Markup
from markdown import markdown

from ._type_hint_helpers import PathString


class Page:
    """Base component used to make web pages all components that represent
    content in HTML, XML, or JSON generated by Render Engine should be a Page
    object"""

    engine: str = ""  # The engine that the Site should refer to. If empty, use
    # site's default

    template: str = ""  # The template that the Site should refer to. If empty,
    # use site's default

    match_param: str = r"(^\w+: \b.+$)"  # The regular expression used to
    # identify metadata in a content file

    routes: typing.List = [""]  # all routes that the file should be created at.

    def __init__(self, content_path=None):
        """If a content_path exists, check the associated file, processing the
        vars at the top and restitching the remaining lines
        """

        if content_path:
            if not Path(content_path).exists():
                raise ValueError('The content_path does not exist')

            content = Path(content_path).read_text()
            parsed_content = re.split(self.match_param, content, flags=re.M)
            self._content = parsed_content.pop().strip()
            valid_attrs = (x for x in parsed_content if x.strip("\n"))
            # We want to allow leading spaces and tabs so only strip new-lines

            for attr in valid_attrs:
                name, value = attr.split(": ")
                setattr(self, name.lower(), value.strip())

    def __str__(self):
        if hasattr(self, "slug"):
            string = self.slug

        elif hasattr(self, "title"):
            string = self.title

        else:
            string = self.__class__.__name__

        return string.lower().replace(" ", "_")

    @property
    def html(self):
        """the text from self._content converted to html"""

        if hasattr(self, "_content"):
            return markdown(self._content)

        else:
            return ""

    @property
    def content(self):
        """html = rendered html (not marked up). Is None if content is none"""
        return Markup(self.html)
