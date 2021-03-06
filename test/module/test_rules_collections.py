"""
  Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from cfnlint import RulesCollection, Template, DEFAULT_RULESDIR  # pylint: disable=E0401
import cfnlint.parser  # pylint: disable=E0401
from testlib.testcase import BaseTestCase


class TestTemplate(BaseTestCase):
    """Test Template RulesCollection in cfnlint """
    def setUp(self):
        """ SetUp template object"""
        self.rules = RulesCollection()
        rulesdirs = [DEFAULT_RULESDIR]
        for rulesdir in rulesdirs:
            self.rules.extend(
                RulesCollection.create_from_directory(rulesdir))

    def test_rule_ids_unique(self):
        """Test Rule IDs are Unique"""
        existing_rules = []
        for rule in self.rules:
            self.assertFalse(rule.id in existing_rules)
            existing_rules.append(rule.id)

    def test_success_run(self):
        """ Test Run Logic"""
        filename = 'templates/good/generic.yaml'
        fp = open(filename)
        loader = cfnlint.parser.MarkedLoader(fp.read())
        loader.add_multi_constructor("!", cfnlint.parser.multi_constructor)
        template = loader.get_single_data()
        cfn = Template(template, ['us-east-1'])

        matches = list()
        matches.extend(self.rules.run(filename, cfn, []))
        assert(matches == [])

    def test_fail_run(self):
        """Test failure run"""
        filename = 'templates/bad/generic.yaml'
        fp = open(filename)
        loader = cfnlint.parser.MarkedLoader(fp.read())
        loader.add_multi_constructor("!", cfnlint.parser.multi_constructor)
        template = loader.get_single_data()
        cfn = Template(template, ['us-east-1'])

        matches = list()
        matches.extend(self.rules.run(filename, cfn, []))
        assert(len(matches) == 24)

    def test_fail_sub_properties_run(self):
        """Test failure run"""
        filename = 'templates/bad/properties_onlyone.yaml'
        fp = open(filename)
        loader = cfnlint.parser.MarkedLoader(fp.read())
        loader.add_multi_constructor("!", cfnlint.parser.multi_constructor)
        template = loader.get_single_data()
        cfn = Template(template, ['us-east-1'])

        matches = list()
        matches.extend(self.rules.run(filename, cfn, []))
        assert(len(matches) == 2)
