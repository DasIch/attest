from __future__ import with_statement

import sys

from attest import Tests, Assert, assert_hook
import attest

from attest.tests._meta import metatests


suite = Tests()


@suite.test
def get_all_reporters():
    reporters = set(['auto', 'fancy', 'plain', 'xml'])
    assert set(attest.get_all_reporters()) == reporters


@suite.test
def get_reporter_by_name():
    reporters = dict(auto=attest.auto_reporter,
                     fancy=attest.FancyReporter,
                     plain=attest.PlainReporter,
                     xml=attest.XmlReporter,
                    )
    for name, reporter in reporters.iteritems():
        assert attest.get_reporter_by_name(name) == reporter


@suite.test
def auto_reporter():
    # Inside tests, sys.stdout is not a tty
    assert isinstance(attest.auto_reporter(), attest.PlainReporter)

    sys.stdout, orig = sys.__stdout__, sys.stdout
    try:
        assert isinstance(attest.auto_reporter(), attest.FancyReporter)
        with attest.disable_imports('progressbar', 'pygments'):
            assert isinstance(attest.auto_reporter(), attest.PlainReporter)
    finally:
        sys.stdout = orig


@suite.test
def xml_reporter():
    """XmlReporter"""

    with attest.capture_output() as (out, err):
        metatests.run(attest.XmlReporter)

    for line, expected in zip(out[:5] + out[6:], [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<testreport tests="2">',
        '  <pass name="attest.tests._meta.passing"/>',
        '  <fail name="attest.tests._meta.failing" type="AssertionError">',
        '    Traceback (most recent call last):',
        '        assert value == 3',
        '    AssertionError: not (2 == 3)',
        '  </fail>',
        '</testreport>',
    ]):
        assert line == expected


@suite.test
def plain_reporter():
    """PlainReporter"""

    with attest.capture_output() as (out, err):
        with Assert.raises(SystemExit):
            metatests.run(attest.PlainReporter)

    for line, expected in zip(out[:5] + out[6:-1], [
        '.F',
        '',
        'attest.tests._meta.failing',
        '-' * 80,
        'Traceback (most recent call last):',
        '    assert value == 3',
        'AssertionError: not (2 == 3)',
        '',
    ]):
        assert line == expected

    assert out[-1].split(' ')[:2] == ['Failures:', '1/2']
