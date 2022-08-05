"""
Injects Quantity-Value in to the doctest namespace for pytest and uses
`sybil <https://pypi.org/project/sybil/>`_ to test ".. code-block:: python"
examples in the documentation.
"""
from __future__ import division
import sys
from doctest import NORMALIZE_WHITESPACE, ELLIPSIS

import pytest

from sybil import Sybil
from sybil.parsers.doctest import DocTestParser
try:
    # in sybil 3.0.0, CodeBlockParser was renamed to PythonCodeBlockParser
    from sybil.parsers.codeblock import PythonCodeBlockParser
except ImportError:
    from sybil.parsers.codeblock import CodeBlockParser as PythonCodeBlockParser

from QV import *


@pytest.fixture(autouse=True)
def add_quantity_value(doctest_namespace):
    for key, val in globals().items():
        if key.startswith('_'):
            continue
        doctest_namespace[key] = val

    if sys.version_info.major > 2:
        doctest_namespace['xrange'] = range


pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=NORMALIZE_WHITESPACE | ELLIPSIS),
        PythonCodeBlockParser(future_imports=['division']),
    ],
    pattern='*.rst',
    fixtures=['add_quantity_value']
).pytest()

