# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.core.exceptions import ValidationError
from django.test import TestCase

# Local application / specific library imports
from precise_bbcode.models import BBCodeTag
from precise_bbcode.parser import get_parser


class CustomTagsTestCase(TestCase):
    ERRONEOUS_TAGS_TESTS = (
        {'tag_definition': '[tag]', 'html_replacement': ''},
        {'tag_definition': 'it\s not a tag', 'html_replacement': ''},
        {'tag_definition': '[first]{TEXT1}[/end]', 'html_replacement': '<p>{TEXT1}</p>'},
        {'tag_definition': '[tag2]{TEXT1}[/tag2]', 'html_replacement': '<p>{TEXT1}</p>', 'standalone': True},
        {'tag_definition': '[start]{TEXT1}[/end]', 'html_replacement': '<p>{TEXT1}</p>'},
        {'tag_definition': '[start]{TEXT1}[/end]', 'html_replacement': '<p>{TEXT1}</p>'},
        {'tag_definition': '[b]{TEXT1}[/b]', 'html_replacement': '<b>{TEXT1}</b>'},
        {'tag_definition': '[justify]{TEXT1}[/justify]', 'html_replacement': '<div style="text-align:justify;"></div>'},
        {'tag_definition': '[center][/center]', 'html_replacement': '<div style="text-align:center;">{TEXT1}</div>'},
        {'tag_definition': '[spe={COLOR}]{TEXT}[/spe]', 'html_replacement': '<div class="spe">{TEXT}</div>'},
        {'tag_definition': '[spe]{TEXT}[/spe]', 'html_replacement': '<div class="spe" style="color:{COLOR};">{TEXT}</div>'},
        {'tag_definition': '[spe]{UNKNOWN}[/spe]', 'html_replacement': '<div>{UNKNOWN}</div>'},
        {'tag_definition': '[io]{TEXT#1}[/io]', 'html_replacement': '<span>{TEXT#1}</span>'},
        {'tag_definition': '[io]{TEXTa}[/io]', 'html_replacement': '<span>{TEXTb}</span>'},
        {'tag_definition': '[ test]{TEXT1}[/test]', 'html_replacement': '<span>{TEXT}</span>'},
        {'tag_definition': '[test ]{TEXT1}[/test]', 'html_replacement': '<span>{TEXT}</span>'},
        {'tag_definition': '[test]{TEXT1}[/ test ]', 'html_replacement': '<span>{TEXT}</span>'},
        {'tag_definition': '[test]{TEXT1}[/test ]', 'html_replacement': '<span>{TEXT}</span>'},
    )

    VALID_TAG_TESTS = (
        {'tag_definition': '[pre]{TEXT}[/pre]', 'html_replacement': '<pre>{TEXT}</pre>'},
        {'tag_definition': '[pre2={COLOR}]{TEXT1}[/pre2]', 'html_replacement': '<pre style="color:{COLOR};">{TEXT1}</pre>'},
        {'tag_definition': '[hr]', 'html_replacement': '<hr />', 'standalone': True},
        {'tag_definition': '[h]{TEXT}[/h]', 'html_replacement': '<strong>{TEXT}</strong>', 'helpline': u'Display your text in bold'},
        {'tag_definition': '[h]{TEXT}[/h]', 'html_replacement': '<strong>{TEXT}</strong>', 'display_on_editor': False},
        {'tag_definition': '[pre]{TEXT}[/pre]', 'html_replacement': '<pre>{TEXT}</pre>', 'newline_closes': True},
        {'tag_definition': '[pre]{TEXT}[/pre]', 'html_replacement': '<pre>{TEXT}</pre>', 'same_tag_closes': True},
        {'tag_definition': '[troll]{TEXT}[/troll]', 'html_replacement': '<div class="troll">{TEXT}</div>', 'end_tag_closes': True},
        {'tag_definition': '[troll]{TEXT}[/troll]', 'html_replacement': '<div class="troll">{TEXT}</div>', 'transform_newlines': True},
        {'tag_definition': '[idea]{TEXT1}[/idea]', 'html_replacement': '<div class="idea">{TEXT1}</div>', 'render_embedded': False},
        {'tag_definition': '[idea]{TEXT1}[/idea]', 'html_replacement': '<div class="idea">{TEXT1}</div>', 'escape_html': False},
        {'tag_definition': '[link]{URL}[/link]', 'html_replacement': '<div class="idea">{URL}</div>', 'replace_links': False},
        {'tag_definition': '[link]{URL}[/link]', 'html_replacement': '<div class="idea">{URL}</div>', 'strip': True},
        {'tag_definition': '[mailto]{EMAIL}[/mailto]', 'html_replacement': '<a href="mailto!{EMAIL}">{EMAIL}</div>', 'swallow_trailing_newline': True},
    )

    def setUp(self):
        self.parser = get_parser()

    def test_erroneous_tags_cleaning(self):
        # Run & check
        for tag_dict in self.ERRONEOUS_TAGS_TESTS:
            with self.assertRaises(ValidationError):
                tag = BBCodeTag(**tag_dict)
                tag.clean()

    def test_valid_tags_cleaning(self):
        # Run & check
        for tag_dict in self.VALID_TAG_TESTS:
            tag = BBCodeTag(**tag_dict)
            try:
                tag.clean()
            except ValidationError:
                self.fail("The following BBCode failed to validate: {}".format(tag_dict))
