from __future__ import with_statement
from nose.tools import assert_raises
import sys

from tests.util import fail_msg
from expecter import expect


class describe_expecter:
    def it_expects_equals(self):
        expect(2) == 1 + 1
        def _fails(): expect(1) == 2
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == 'Expected 2 but got 1'

    def it_shows_diff_when_strings_differ(self):
        def _fails(): expect('foo\nbar') == 'foo\nbaz'
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == ("Expected 'foo\\nbaz' but got 'foo\\nbar'\n"
               "Diff:\n"
               "@@ -1,2 +1,2 @@\n"
               " foo\n"
               "-baz\n"
               "+bar"
               ), fail_msg(_fails)

    def it_shows_diff_for_large_reprs(self):
        sequence = list(range(1000, 1050))
        big_list = sequence[:20] + [1019] + sequence[20:]
        def _fails(): expect(big_list) == sequence
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == ("Expected {0} but got {1}\n"
               "Diff:\n"
               "@@ -17,6 +17,7 @@\n"
               "  1016,\n"
               "  1017,\n"
               "  1018,\n"
               "+ 1019,\n"
               "  1019,\n"
               "  1020,\n"
               "  1021,"
               ).format(repr(sequence), repr(big_list)), fail_msg(_fails)

    def it_can_compare_bytes(self):
        null = bytes((0,))
        expect(null) == null
        data = bytes(range(9, 32))
        def _fails():
            expect(data) == data + null
        assert_raises(AssertionError, _fails)

    def it_expects_not_equals(self):
        expect(1) != 2
        def _fails(): expect(1) != 1
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == 'Expected anything except 1 but got it'

    def it_expects_less_than(self):
        expect(1) < 2
        def _fails(): expect(1) < 0
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == 'Expected something less than 0 but got 1'

    def it_expects_greater_than(self):
        expect(2) > 1
        def _fails(): expect(0) > 1
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected something greater than 1 but got 0')

    def it_expects_less_than_or_equal(self):
        expect(1) <= 1
        expect(1) <= 2
        def _fails(): expect(2) <= 1
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected something less than or equal to 1 but got 2')

    def it_expects_greater_than_or_equal(self):
        expect(1) >= 1
        expect(2) >= 1
        def _fails(): expect(1) >= 2
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected something greater than or equal to 2 but got 1')

    def it_can_chain_comparison_expectations(self):
        # In each of these chains, the first expectation passes and the second
        # fails. This forces the first expectation to return self.
        failing_chains = [lambda: 1 == expect(1) != 1,
                          lambda: 1 != expect(2) != 2,
                          lambda: 1 < expect(2) != 2,
                          lambda: 1 > expect(0) != 0,
                          lambda: 1 <= expect(1) != 1,
                          lambda: 1 >= expect(1) != 1]
        for chain in failing_chains:
            assert_raises(AssertionError, chain)

        # Mote bug: if we leave the lambda in a local variable, it will try to
        # run it as a spec.
        del chain

    def it_expects_isinstance(self):
        expect(1).isinstance(int)
        def _fails():
            expect(1).isinstance(str)
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected an instance of str but got an instance of int')

    def it_expects_isinstance_for_multiple_types(self):
        expect('str').isinstance((str, bytes))
        def _fails():
            expect('str').isinstance((int, tuple))
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            'Expected an instance of int or tuple but got an instance of str')

    def it_expects_containment(self):
        expect([1]).contains(1)
        def _fails():
            expect([2]).contains(1)
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Expected [2] to contain 1 but it didn't")

    def it_expects_non_containment(self):
        expect([1]).does_not_contain(0)
        def _fails():
            expect([1]).does_not_contain(1)
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Expected [1] not to contain 1 but it did")

    def it_expects_exclusion(self):
        expect([1]).excludes(0)
        def _fails():
            expect([1]).excludes(1)
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Expected [1] to exclude 1 but it didn't")

    def it_optimizes_containment_message_for_multiline_strings(self):
        expect("<p>\nHello, world!\n</p>\n").contains("Hello, world!")
        def _fails():
            expect("<p>\nHello, world!\n</p>\n").contains("Foobar")
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Given text:\n\n"
            "<p>\nHello, world!\n</p>\n\n"
            "Expected to contain 'Foobar' but didn't")

    def it_optimizes_non_containment_message_for_multiline_strings(self):
        expect("<p>\nHello, world!\n</p>\n").does_not_contain("Foobar")
        def _fails():
            expect("<p>\nHello, world!\n</p>\n").does_not_contain("Hello")
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Given text:\n\n"
            "<p>\nHello, world!\n</p>\n\n"
            "Expected not to contain 'Hello' but did")

    def it_optimizes_exclusion_message_for_multiline_strings(self):
        expect("<p>\nHello, world!\n</p>\n").excludes("Foobar")
        def _fails():
            expect("<p>\nHello, world!\n</p>\n").excludes("Hello")
        assert_raises(AssertionError, _fails)
        assert fail_msg(_fails) == (
            "Given text:\n\n"
            "<p>\nHello, world!\n</p>\n\n"
            "Expected to exclude 'Hello' but didn't")
