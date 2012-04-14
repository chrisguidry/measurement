from __future__ import division, unicode_literals

from measurement import *

from decimal import Decimal

def should_represent_orthogonally(incoming):
    assert eval(repr(incoming)) == incoming, "%s != %s" % (repr(incoming), repr(eval(repr(incoming))))

    assert incoming.__class__.parse(unicode(incoming)) == incoming, "%s != %s" % (incoming.__class__.parse(unicode(incoming)), incoming)
