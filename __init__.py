# coding=utf-8

"""
The Measurement Library is a set of classes offering full support for
math using Dimensions, Metrics, and Quantities.
"""

from __future__ import division, unicode_literals
import six

import decimal
import math
import re

ExponentTypographicalSymbols = ["⁰", "", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]

class MeasurementParsingException(Exception):
    """
    An exception that occurs while parsing a Dimension, Metric, or Quantity
    from a string.

    >>> assert "Python 2 and Python 3 doctests are incompatible."
    >>> try:
    ...     Quantity.parse("ThisIsn'tAQuantity!")
    ...     assert False, "MeasurementParsingException was not raised!"
    ... except MeasurementParsingException as e:
    ...     assert str(e) == "Could not parse 'ThisIsn'tAQuantity!' to a Quantity."
    """
class MetricConversionError(Exception):
    """
    An exception raised when a conversion between Metrics is required and
    there is no defined conversion.

    >>> assert "Python 2 and Python 3 doctests are incompatible."
    >>> try:
    ...     (5 * Ampere).to(Meter)
    ...     assert False, "MetricConversionError was not raised!"
    ... except MetricConversionError as e:
    ...     assert str(e) == "There is no conversion between 'A' and 'm', because they measure different Dimensions."
    """

def isnumber(object):
    """
    Determines if the given object should be considered a number from
    measurement's perspective.  This may eventually be replaced when the
    Python 2.6 number classes are reorganized
    """
    return isinstance(object, (int, float, complex, decimal.Decimal))

class Immutable(object):
    """
    A base class for all of the measurement classes.  This class allows
    objects to freeze themselves from further changes.

    >>> class Frigid(Immutable):
    ...   def __init__(self, value):
    ...     self.value = value
    ...     super(Immutable, self).__init__()
    ...     self.frozen = True
    ...
    >>> f = Frigid("my value")
    >>> f.value = "new value"
    Traceback (most recent call last):
      ...
    AttributeError: Frigid is immutable.
    >>> del(f.value)
    Traceback (most recent call last):
      ...
    AttributeError: Frigid is immutable.
    """

    __slots__ = ()

    def __setattr__(self, *args):
        "Overridden to implement object freezing."
        if hasattr(self, "frozen"):
            raise AttributeError(self.__class__.__name__ + " is immutable.")
        super(Immutable, self).__setattr__(*args)

    def __delattr__(self, *args):
        "Overridden to implement object freezing."
        if hasattr(self, "frozen"):
            raise AttributeError(self.__class__.__name__ + " is immutable.")
        super(Immutable, self).__delattr__(*args)

    def _internal__setattr__(self, *args):
        super(Immutable, self).__setattr__(*args)

class Dimension(Immutable):
    """
    A Dimension is a degree of freedom along which something may be measured.
    Dimensions are very abstract objects, representing fundamental
    measurements like Length, Time, Charge, and so forth.  A Dimenion may be
    either a fundamental defined Dimension; or a derived Dimension, expressed
    in Terms of other Dimensions through multiplication or division.
    """

    class Term(Immutable):
        """
        A Dimension.Term is a component of a derived Dimension.  It is a
        Dimension raised to a power (either positive, negative, or zero) and
        define how a Dimension is expressed in terms of the fundamental
        Dimensions.  All Dimensions have terms, and the fundamental Dimensions
        have themselves to the first power as their only term.
        """

        __slots__ = "frozen", "dimension", "power", "scalar", "power_as_typographical_symbol"

        def __init__(self, dimension, power):
            "Creates a Dimension.Term, from a Dimension and an integral power."

            self.dimension = dimension
            self.power = power

            self.scalar = (self.power == 0 or self.dimension.name == "number")
            if isinstance(self.power, int) and abs(self.power) in range(0, 9 + 1):
                self.power_as_typographical_symbol = ExponentTypographicalSymbols[abs(self.power)]
            else:
                self.power_as_typographical_symbol = "^" + six.text_type(abs(self.power))

            super(Dimension.Term, self).__init__()

            self.frozen = True

        def __hash__(self):
            "Computes a hash value for this Dimension.Term."
            return hash(self.dimension.name) ^ hash(self.power)

        def __eq__(self, other):
            "Tests whether this Dimension.Term is equivalent to another Dimension.Term."
            if other == None:         return False
            if id(self) == id(other): return True

            return (self.dimension.name == other.dimension.name and
                    self.power == other.power)
        def __ne__(self, other):
            "Tests whether this Dimension.Term is different from another Dimension.Term."
            return not self.__eq__(other)

        def __repr__(self):
            "Produces a representation of this Dimension.Term, that when eval()ed, produces a Dimension.Term "
            "equivalent to this one."
            return "Dimension.Term(" + repr(self.dimension) + ", " + six.text_type(self.power) + ")"
        def __unicode__(self):
            "Produces a string representation of this Dimension.Term, in typographical symbols"
            return self.typographical_symbol + self.power_as_typographical_symbol
        __str__ = __unicode__

    def __new__(cls, *args, **kwargs):
        """
        measurement treats Dimension objects as flyweights and will try to reuse
        instances base on the canonicalized terms.
        """

        if "derivation" in kwargs:
            cls.__last_canonicalized_terms = Dimension.canonicalize(kwargs["derivation"].terms)
        elif "terms" in kwargs:
            cls.__last_canonicalized_terms = Dimension.canonicalize(kwargs["terms"])
            if cls.__last_canonicalized_terms:
                if cls.__last_canonicalized_terms in Dimension.defined_dimensions_by_terms:
                    return Dimension.defined_dimensions_by_terms[cls.__last_canonicalized_terms]
        else:
            cls.__last_canonicalized_terms = None

        return super(Dimension, cls).__new__(cls)

    __slots__ = "frozen", "defined", "name", "typographical_symbol", "terms"

    def __init__(self, name = None, typographical_symbol = None, terms = None, derivation = None):
        """
        Creates a Dimension.  There are two ways in which Dimensions may be
        created:
        * through definition, by passing a name and a
          typographical_symbol, and optional documentation
        * through derivation, by multiplying/dividing two Dimensions, or by passing a constructed
          list of Dimension.Terms The __new__ method attempts to resolve a novel
          Dimension to a pre-defined Dimension.
        """
        if hasattr(self, "frozen"):
            return

        if not Dimension.__last_canonicalized_terms:
            # defined dimension
            self.defined = True
            self.name = name
            self.typographical_symbol = typographical_symbol
            if not self.typographical_symbol:
                self.typographical_symbol = name
            self.terms = frozenset([Dimension.Term(self, 1)])

            Dimension.define(self)
        else:
            # derived dimension
            self.defined = False

            self.terms = Dimension.__last_canonicalized_terms
            Dimension.__last_canonicalized_terms = None

            if name:
                self.name = name
                if typographical_symbol:
                    self.typographical_symbol = typographical_symbol
                else:
                    self.typographical_symbol = Dimension.identify(self.terms)[1]

                Dimension.define(self)
            else:
                self.name, self.typographical_symbol = Dimension.identify(self.terms)

        super(Dimension, self).__init__()

        self.frozen = True

    defined_dimensions_by_terms = {}
    defined_dimensions_by_symbol = {}

    @classmethod
    def all(cls):
        dimensions = []
        for item in list(globals().values()):
            if isinstance(item, Dimension):
                dimensions.append(item)
        return dimensions
    @classmethod
    def get_by_name(cls, name):
        for dimension in list(Dimension.defined_dimensions_by_symbol.values()):
            if dimension.name == name:
                return dimension
        return None

    @classmethod
    def define(cls, dimension):
        """
        Registers a dimension with the global registry of dimensions.  This
        method is called by the constructor and should NOT be called from your
        code.
        """
        Dimension.defined_dimensions_by_terms[dimension.terms] = dimension
        Dimension.defined_dimensions_by_symbol[dimension.typographical_symbol] = dimension
        Dimension.parsing_pattern_string = None
        Dimension.parsing_pattern = None

    @classmethod
    def canonicalize(cls, terms):
        """
        Canonicalizes a list of Dimension.Terms to a set of terms.  The
        primary purpose of canonicalizing terms when creating a Dimension is
        to flatten the terms into a single set, aggregating duplicates into
        single terms with the combined powers, and to remove extraneous Number
        terms.
        """

        dimension_powers = {}

        # flatten/collect all of the dimensions and their powers
        for term in terms:
            if term.scalar:
                continue

            for inner_term in term.dimension.terms:
                if not inner_term.dimension in dimension_powers:
                    dimension_powers[inner_term.dimension] = 0

                dimension_powers[inner_term.dimension] += term.power * inner_term.power

        # normalize and reduce down terms whose powers have become 0
        normalized_terms = []
        for dimension in dimension_powers:
            power = dimension_powers[dimension]
            if power:
                normalized_terms.append(Dimension.Term(dimension, power))

        # if everything has been normalized down to Number, inject Number as the dimension
        if not normalized_terms:
            normalized_terms.append(Dimension.Term(Number, 1))
        else:
            normalized_terms.sort(key = lambda term: term.dimension.name)

        return frozenset(normalized_terms)

    @classmethod
    def identify(cls, terms):
        """
        Assigns a name and typographical symbol (returned as a tuple) to the
        Dimension that would be defined by the provided terms.  This method
        assists when deriving complex Dimensions by giving a name and
        typographical symbol expressed in terms of the fundamental Dimensions.
        """

        name = ""
        name_numerator = ""
        name_denominator = ""

        symbol = ""
        symbol_numerator = ""
        symbol_denominator = ""

        for term in terms:
            if term.power > 0:
                name_numerator     += term.dimension.name + term.power_as_typographical_symbol
                symbol_numerator   += term.dimension.typographical_symbol + term.power_as_typographical_symbol
            elif term.power < 0:
                name_denominator   += term.dimension.name + term.power_as_typographical_symbol
                symbol_denominator += term.dimension.typographical_symbol + term.power_as_typographical_symbol

        if name_numerator == "" and terms:
            name_numerator = "1"
        if symbol_numerator == "" and terms:
            symbol_numerator = "1"

        name = name_numerator
        symbol = symbol_numerator

        if name_denominator != "":
            name += "/" + name_denominator
        if symbol_denominator != "":
            symbol += "/" + symbol_denominator

        if name == "1" and symbol == "1":
            name = Number.name
            symbol = Number.typographical_symbol

        return (name, symbol)


    @classmethod
    def parse(cls, typographical_symbol):
        "Parses a typographical symbol representing a Dimension into a Dimension."
        parts = typographical_symbol.split("/")

        numerator_terms = Dimension.symbol_string_to_terms(parts[0])

        if len(parts) == 2:
            denominator_terms = Dimension.symbol_string_to_terms(parts[1])
            denominator_terms = [Dimension.Term(term.dimension, 0 - term.power) for term in denominator_terms]
        else:
            denominator_terms = []

        terms = numerator_terms + denominator_terms

        if not terms:
            raise MeasurementParsingException("'%s' doesn't seem to correspond to any defined Dimension" % typographical_symbol)

        return Dimension(terms = terms)

    @classmethod
    def rebuild_parsing_pattern(cls):
        """
        Builds a regular expression that can parse Metrics from a string.
        """
        # the scan pattern should be
        # /(A|B|C|...)(²|³|...|\^\d+)?/
        # where A, B, and C are the typographical_symbols of fundamental dimensions
        # and the superscripts are powers, and for those that aren't typographical superscripts, the ^10, ^11, ^12... notation

        # the typographical symbols should be sorted by length, with the longest strings first, so that
        # matches for longer strings will occur before short strings, as in 'mol' and 'm'
        dimension_tokens = [re.escape(typographical_symbol) for typographical_symbol in list(Dimension.defined_dimensions_by_symbol.keys())]
        dimension_tokens.sort(key = len, reverse = True)
        dimension_tokens = "(" + "|".join(dimension_tokens) + ")"

        power_tokens = "(⁰|⁻¹|⁻²|²|⁻³|³|⁻⁴|⁴|⁻⁵|⁵|⁻⁶|⁶|⁻⁷|⁷|⁻⁸|⁸|⁻⁹|⁹|\\^[\\-\\.\\d]+){0,1}"
        Dimension.parsing_pattern_string = dimension_tokens + power_tokens
        Dimension.parsing_pattern = re.compile(Dimension.parsing_pattern_string)

    @classmethod
    def symbol_string_to_terms(cls, symbol_string):
        """
        Parses a string of positive-powered Dimension symbols (as would be
        found in either a numerator or denominator of a complete Dimension
        symbol) into a list of Dimension.Terms
        """
        if not symbol_string:
            return []

        if not Dimension.parsing_pattern:
            Dimension.rebuild_parsing_pattern()

        terms = []
        for match in Dimension.parsing_pattern.findall(symbol_string):
            matched_symbol = match[0]
            matched_power = match[1]

            if matched_symbol not in Dimension.defined_dimensions_by_symbol:
                raise MeasurementParsingException("Unrecognized symbol '%s' when parsing dimension string '%s'" % (matched_symbol, symbol_string))
            dimension = Dimension.defined_dimensions_by_symbol[matched_symbol]

            powers = {"⁰": 0,
                      "":  1,
                      "²": 2,
                      "³": 3,
                      "⁴": 4,
                      "⁵": 5,
                      "⁶": 6,
                      "⁷": 7,
                      "⁸": 8,
                      "⁹": 9}
            if matched_power in powers:
                power = powers[matched_power]
            else:
                power = int(matched_power.replace("^", ""))

            terms.append(Dimension.Term(dimension, power))

        return terms


    def metrics(self):
        metrics = []
        for metric in list(Metric.defined_metrics_by_symbol.values()):
            if metric.dimension == self:
                metrics.append(metric)
        return metrics


    def __hash__(self):
        "Computes a hash value for this Dimension."
        hash_to_return = 0
        for term in self.terms:
            hash_to_return = hash_to_return ^ hash(term)
        return hash_to_return

    def __eq__(self, other):
        "Tests whether a Dimension is equivalent to this Dimension."
        if other == None:         return False
        if id(self) == id(other): return True

        return self.terms == other.terms
    def __ne__(self, other):
        "Tests whether a Dimension is different from this Dimension."
        return not self.__eq__(other)

    def __mul__(self, other):
        "Derives a new Dimension through multiplication."
        return Dimension(terms = [Dimension.Term(self, 1), Dimension.Term(other, 1)])

    def __pow__(self, power):
        "Derives a new Dimension by raising this dimension to the given power."
        return Dimension(terms = [Dimension.Term(self, power)])

    def __truediv__(self, other):
        "Derives a new Dimension through division."
        return Dimension(terms = [Dimension.Term(self, 1), Dimension.Term(other, -1)])
    __div__ = __truediv__

    def __repr__(self):
        """
        Produces a representation of this Dimension that, when eval()ed, will
        produce a Dimension equivalent to this one.
        """
        if self.defined:
            return "Dimension(" + repr(self.name) + ", " + repr(self.typographical_symbol) + ")"
        else:
            to_return = "Dimension(terms = ["
            to_return += ", ".join([repr(t) for t in self.terms])
            to_return += "])"

            return to_return

    def __unicode__(self):
        "Returns the typographical string representation of this Dimension."
        return self.typographical_symbol
    __str__ = __unicode__

class Metric(Immutable):
    "A Metric is a unit of measurement in some Dimension."

    class Term(Immutable):
        """
        A Metric.Term is a component of a derived Metric.  It is a Metric
        raised to a power (either positive, negative, or zero) and is used to
        define how a Metric is expressed in terms of other base Metrics.  All
        Metrics have terms, and the various base Metrics have themselves to
        the first power as their only term.
        """

        __slots__ = "frozen", "prefix", "metric", "power", "one", "power_as_typographical_symbol"

        def __init__(self, prefix, metric, power):
            self.prefix = prefix
            if not self.prefix:
                self.prefix = Metric.Prefix.find(10, 0)
                if not self.prefix:
                    self.prefix = Metric.Prefix("one", "1", 10, 0)
            self.metric = metric
            self.power = power

            # take floating-point powers to integers, if possible
            if isinstance(self.power, float):
                if self.power == 0.0:
                    self.power = 0
                elif self.power >= 1.0 or self.power <= -1.0:
                    if self.power % round(self.power) == 0.0:
                        self.power = int(self.power)

            self.one = (self.power == 0 or self.metric.name == "one")
            if isinstance(self.power, int) and abs(self.power) in range(0, 9 + 1):
                self.power_as_typographical_symbol = ExponentTypographicalSymbols[abs(self.power)]
            else:
                self.power_as_typographical_symbol = "^" + six.text_type(abs(self.power))

            super(Metric.Term, self).__init__()

            self.frozen = True

        def __hash__(self):
            "Computes a hash value for this Metric.Term."
            return hash(self.prefix) ^ hash(self.metric.name) ^ hash(self.power)

        def __eq__(self, other):
            "Tests whether a Metric.Term is equivalent to this Metric.Term."
            if other == None:         return False
            if id(self) == id(other): return True

            return (self.prefix == other.prefix and
                    self.metric.name == other.metric.name and
                    self.power == other.power)
        def __ne__(self, other):
            "Tests whether a Metric.Term is different from this Metric.Term."
            return not self.__eq__(other)

        def __repr__(self):
            """
            Produces a representation of this Metric.Term that, when eval()ed,
            will produce a Metric.Term equivalent to this one.
            """
            return "Metric.Term(" + repr(self.prefix) + ", " + repr(self.metric) + ", " + six.text_type(self.power) + ")"
        def __unicode__(self):
            "Produces a typographical string representing this Metric.Term."
            return self.prefix.typographical_symbol + self.typographical_symbol + self.power_as_typographical_symbol
        __str__ = __unicode__

    class Prefix(Immutable):
        """
        A modifier which, when prefixed to a metric, multiplies or divides
        that metric by some amount.  The most familiar example of these are
        the SI prefixes (e.g. kilo-, nano-, etc.), which are defined at
        various powers of 10.
        """

        __slots__ = "frozen", "name", "typographical_symbol", "base", "power"

        def __new__(cls, name, typographical_symbol, base, power):
            "Attempts to resolve a pre-defined Prefix."
            existing_prefix = Metric.Prefix.find(base, power)
            if existing_prefix:
                return existing_prefix

            return super(Metric.Prefix, cls).__new__(cls)

        def __init__(self, name, typographical_symbol, base, power):
            """
            Creates a new Metric.Prefix, with it's name and
            typographical_symbol, and it's definition as an integral base and
            an integral power.  For example, 'kilo-' is defined as 10^3 and
            'nano-' is defined as 10^-9.
            """

            if hasattr(self, "frozen"):
                return

            self.name = name
            self.typographical_symbol = typographical_symbol
            self.base = base
            self.power = power

            Metric.Prefix.define(self)

            self.frozen = True

        defined_prefixes_by_value = {}
        defined_prefixes_by_symbol = {}

        @classmethod
        def define(cls, prefix):
            """
            Defines a new Metric.Prefix.  This method is called internally to
            the constructor and should not be called from your code.
            """

            if (prefix.base, prefix.power) in Metric.Prefix.defined_prefixes_by_value:
                raise KeyError("Multiple definitions of Metric.Prefix with base %s and power %s" % (prefix.base, prefix.power))

            Metric.Prefix.defined_prefixes_by_value[(prefix.base, prefix.power)] = prefix
            Metric.Prefix.defined_prefixes_by_symbol[prefix.typographical_symbol] = prefix

        @classmethod
        def find(cls, base, power):
            """
            Finds a Metric.Prefix that has been previously registered.  Handy
            when parsing or otherwise needing to find a prefix when all you
            have are a base and a power.
            """
            if (base, power) in Metric.Prefix.defined_prefixes_by_value:
                return Metric.Prefix.defined_prefixes_by_value[(base, power)]
            return None

        def __mul__(self, other):
            """
            When multiplying a Prefix by a Metric, produces a derived Metric.
            Example: Kilo * Meter produces the unit kilometer
            """
            if isinstance(other, Metric):
                return Metric(terms = [Metric.Term(self, other, 1)])
            else:
                return NotImplemented

        def __add__(self, other):
            """
            When adding two prefixes, produces a new Metric.Prefix with a
            power equal to the sum of the prefixes.  Example: Kilo + Mega ==
            Giga
            """
            if isinstance(other, Metric.Prefix):
                if self.base != other.base and (self.power != 0) and (other.power != 0):
                    return NotImplemented

                collected_power = self.power + other.power
                if not collected_power:
                    return None

                collected_prefix = Metric.Prefix.find(self.base, collected_power)
                if not collected_prefix:
                    collected_prefix = Metric.Prefix("%s^%s" % (self.base, collected_power), "%s^%s" % (self.base, collected_power),
                                                     self.base, collected_power)

                return collected_prefix
            else:
                return NotImplemented

        def __sub__(self, other):
            """
            When subtracting one prefix from another, produces a new
            Metric.Prefix with a power equal to the difference of the
            prefixes.  Example: Kilo - Mega == Milli
            """
            if isinstance(other, Metric.Prefix):
                if self.base != other.base:
                    return NotImplemented

                collected_power = self.power - other.power
                if not collected_power:
                    return None

                collected_prefix = Metric.Prefix.find(self.base, collected_power)
                if not collected_prefix:
                    collected_prefix = Metric.Prefix("%s^%s" % (self.base, collected_power), "%s^%s" % (self.base, collected_power),
                                                     self.base, collected_power)

                return collected_prefix
            else:
                return NotImplemented

        def __hash__(self):
            "Computes a hash value for this Metric.Prefix."
            return hash(self.base) ^ hash(self.power)

        def __eq__(self, other):
            "Tests whether a Metric.Prefix is equivalent to this one"
            if other == None:         return False
            if id(self) == id(other): return True

            return (self.base == other.base and
                    self.power == other.power)
        def __ne__(self, other):
            "Tests whether a Metric.Prefix is different from this one."
            return not self.__eq__(other)

        def __repr__(self):
            """
            Produces a representation of this Metric.Prefix that, when
            eval()ed, will produce an equivalent Metric.Prefix.
            """
            return "Metric.Prefix(" + repr(self.name) + ", " + repr(self.typographical_symbol) + ", " + six.text_type(self.base) + ", " + six.text_type(self.power) + ")"
        def __unicode__(self):
            "Represents this Metric.Prefix as a typographical symbol."
            return self.typographical_symbol
        __str__ = __unicode__

    def __new__(cls, *args, **kwargs):
        """
        measurement treats Metric objects as flyweights and will attempt to reuse
        Metrics when they have the same canonical terms.
        """

        if "derivation" in kwargs:
            cls.__last_canonicalized_terms, cls.__last_canonicalized_dimension = Metric.canonicalize(kwargs["derivation"].terms)
        elif "terms" in kwargs:
            cls.__last_canonicalized_terms, cls.__last_canonicalized_dimension = Metric.canonicalize(kwargs["terms"])
            if cls.__last_canonicalized_terms:
                if cls.__last_canonicalized_terms in Metric.defined_metrics_by_terms:
                    return Metric.defined_metrics_by_terms[cls.__last_canonicalized_terms]
        else:
            cls.__last_canonicalized_terms = cls.__last_canonicalized_dimension = None

        return super(Metric, cls).__new__(cls)

    __slots__ = "frozen", "defined", "name", "plural_name", "typographical_symbol", "dimension", "terms", "_reduced"

    def __init__(self, name = None, typographical_symbol = None, dimension = None, terms = None, derivation = None):
        """
        Creates a Metric.  There are two ways in which Dimensions may be created:
        * through definition, by passing a name and a typographical_symbol, and optional documentation
        * through derived definition, by passing a name, a typographical_symbol, (optional) documentation, and a
          model Metric to copy the Terms of (i.e. a derivation)
        * through derivation, by multiplying/dividing two Dimensions, or by
          passing a constructed list of Dimension.Terms
        """

        if hasattr(self, "frozen"):
            return

        if not Metric.__last_canonicalized_terms:
            # defined metric
            self.defined = True
            self.name = name
            self.typographical_symbol = typographical_symbol
            if not self.typographical_symbol:
                self.typographical_symbol = name
            self.dimension = dimension
            self.terms = frozenset([Metric.Term(None, self, 1)])

            Metric.define(self)
        else:
            # derived metric
            self.defined = False

            self.terms = Metric.__last_canonicalized_terms
            self.dimension = Metric.__last_canonicalized_dimension
            Metric.__last_canonicalized_terms = None
            Metric.__last_canonicalized_dimension = None

            if name:
                self.name = name
                if typographical_symbol:
                    self.typographical_symbol = typographical_symbol
                else:
                    self.typographical_symbol = name

                Metric.define(self)
            else:
                self.name, self.typographical_symbol = Metric.identify(self.terms)

        if self.name.endswith(("ch", "sh", "x", "z")):
            self.plural_name = self.name + "es"
        elif self.name.endswith("y") and self.name[-2] in ("a", "e", "i", "o", "u"):
            self.plural_name = self.name[0:-1] + "ies"
        else:
            self.plural_name = self.name + "s"

        super(Metric, self).__init__()

        self.frozen = True

    defined_metrics_by_terms = {}
    """
    A dictionary of frozenset => Metric, where the frozenset is a set of
    canonicalized Metric.Terms.  This is used to look up defined Metrics for
    reuse as flyweights.
    """
    defined_metrics_by_symbol = {}
    """
    A dictionary of string => Metric, where the string is the typographical
    symbol of a Metric.  This is used to help build the parsing pattern for
    parsing Metric strings.
    """
    base_metric_of = {}
    """
    A dictionary of Dimension => Metric, indicating which Metrics are
    "favored" as the standard base Metric for that Dimension.  These will be
    the SI metrics to begin with.
    """

    @classmethod
    def all(cls):
        return list(Metric.defined_metrics_by_symbol.values())
    @classmethod
    def get_by_name(cls, name):
        for metric in list(Metric.defined_metrics_by_symbol.values()):
            if metric.name == name:
                return metric
        return None

    @classmethod
    def define(cls, metric):
        """
        Registers a metric with the global registry of Metrics, making it
        available for parsing and reuse.  This method should not be called by
        your code.
        """
        Metric.defined_metrics_by_terms[metric.terms] = metric
        Metric.defined_metrics_by_symbol[metric.typographical_symbol] = metric

        # if this is the first Metric defined in this Dimension, consider it
        # the base metric of that Dimension
        if metric.dimension not in Metric.base_metric_of:
            Metric.base_metric_of[metric.dimension] = metric

        Metric.parsing_pattern_string = None
        Metric.parsing_pattern = None

    @classmethod
    def canonicalize(cls, terms):
        """
        Canonicalizes a list of Metric.Terms to a set of terms.  The primary
        purpose of canonicalizing terms when creating a Metric is to flatten
        the terms into a single set, aggregating duplicates into single terms
        with the combined powers, and to remove extraneous 1s terms.
        """

        flattened_terms = []
        dimension_terms = []

        # flatten the powers of each term down to individual terms raised to the power of the outer term
        # for example, take (A^2 * B^3)^4 and make it A4 * A4 * B4 * B4 * B4
        for term in terms:
            dimension_terms.append(Dimension.Term(term.metric.dimension, term.power))

            applied_outer_prefix = False
            for inner_term in term.metric.terms:
                if (inner_term.power > 0):  sign = 1
                else:                       sign = -1

                fractional = inner_term.power % 1
                if (inner_term.power < 0):
                    fractional = 0 - fractional
                whole = int(inner_term.power - (fractional))

                for i in range(abs(whole)):
                    if not applied_outer_prefix:
                        # only apply outer prefixes to the first metric in the numerator
                        applied_outer_prefix = True
                        flattened_terms.append(Metric.Term(term.prefix + inner_term.prefix, inner_term.metric, sign * term.power))
                    else:
                        flattened_terms.append(Metric.Term(inner_term.prefix, inner_term.metric, sign * term.power))

                if fractional != 0:
                    if not applied_outer_prefix:
                        # only apply outer prefixes to the first metric in the numerator
                        applied_outer_prefix = True
                        flattened_terms.append(Metric.Term(term.prefix + inner_term.prefix, inner_term.metric, fractional * term.power))
                    else:
                        flattened_terms.append(Metric.Term(inner_term.prefix, inner_term.metric, fractional * term.power))

        # collect and normalize the powers
        metric_powers = {}
        for term in flattened_terms:
            base_metric = (term.prefix, term.metric)
            if base_metric not in metric_powers:
                metric_powers[base_metric] = Metric.Term(term.prefix, term.metric, 0)

            metric_powers[base_metric] = Metric.Term(term.prefix, term.metric,
                                                     metric_powers[base_metric].power + term.power)

        # normalize and reduce down terms whose powers have become 0
        normalized_terms = []
        for metric in metric_powers:
            term = metric_powers[metric]
            if term.power:
                normalized_terms.append(term)

        # if everything has been normalized down to Number, inject Number as the dimension
        if not normalized_terms:
            normalized_terms.append(Metric.Term(None, Ten, 0))
        else:
            normalized_terms.sort(key = lambda term: term.metric.name)

        return (frozenset(normalized_terms), Dimension(terms = dimension_terms))

    @classmethod
    def identify(cls, terms):
        """
        Assigns a name and typographical symbol (returned as a tuple) to the
        Metric that would be defined by the provided terms.  This method
        assists when deriving complex Metrics by giving a name and
        typographical symbol expressed in terms of the available base Metrics.
        """
        name = ""
        name_numerator = ""
        name_denominator = ""

        symbol = ""
        symbol_numerator = ""
        symbol_denominator = ""

        for term in terms:
            if term.power >= 0:
                if term.prefix.power != 0:
                    name_numerator += term.prefix.name
                    symbol_numerator += term.prefix.typographical_symbol

                name_numerator     += term.metric.name + term.power_as_typographical_symbol
                symbol_numerator   += term.metric.typographical_symbol + term.power_as_typographical_symbol
            else:
                if term.prefix.power != 0:
                    name_denominator += term.prefix.name
                    symbol_denominator += term.prefix.typographical_symbol

                name_denominator   += term.metric.name + term.power_as_typographical_symbol
                symbol_denominator += term.metric.typographical_symbol + term.power_as_typographical_symbol

        if name_numerator == "" and terms:
            name_numerator = "1"
        if symbol_numerator == "" and terms:
            symbol_numerator = "1"

        name = name_numerator
        symbol = symbol_numerator

        if name_denominator:
            name += "/" + name_denominator
        if symbol_denominator:
            symbol += "/" + symbol_denominator

        if name == "1" and symbol == "1":
            name = Number.name
            symbol = Number.typographical_symbol

        return (name, symbol)

    @classmethod
    def parse(cls, typographical_symbol):
        "Parses a typographical symbol representing a Metric into a Metric."
        if typographical_symbol == "1":
            return One
        if typographical_symbol == "10":
            return Ten

        parts = typographical_symbol.split("/")

        numerator_terms = Metric.symbol_string_to_terms(parts[0])

        if len(parts) == 2:
            denominator_terms = Metric.symbol_string_to_terms(parts[1])
            denominator_terms = [Metric.Term(term.prefix, term.metric, 0 - term.power) for term in denominator_terms]
        else:
            denominator_terms = []

        terms = numerator_terms + denominator_terms

        if not terms:
          raise MeasurementParsingException("'%s' doesn't seem to correspond to any defined Metrics" % typographical_symbol)

        return Metric(terms = terms)

    @classmethod
    def rebuild_parsing_pattern(cls):
        """
        Rebuilds the Metric parsing pattern, a cached regular expression that
        is used to parse Metrics from strings.  You should not need to call
        this method directly.

        More information:

        The scan pattern should be:

        ``(Y|Z|...)?(A|B|C|...)+(²|³|...|\\^\\d+)?``

        Where:

        * ``A``, ``B``, and ``C`` are the ``typographical_symbol``s of the defined Metrics (those with names and typographical symbols)
        * ``Y``, ``Z`` are the ``typographical_symbol``s of Metric.Prefixes
        * the superscripted numbers at the end are powers, and for those that aren't typographical
          superscripts, the ^10, ^11, ^12... notation.

        The typographical symbols should be sorted by length, with the longest
        strings first, so that matches for longer strings will occur before
        short strings, as in 'mol' and 'm'.
        """
        metric_tokens = [re.escape(typographical_symbol) for typographical_symbol in list(Metric.defined_metrics_by_symbol.keys())]
        metric_tokens.sort(key = len, reverse = True)

        def resolve_conflicts_between_prefix_and_metric(prefix):
            conflicting_strings = []
            for metric_token in metric_tokens:
                if len(metric_token) > 1 and metric_token.startswith(prefix):
                    conflicting_strings.append(metric_token[len(prefix):])
            if conflicting_strings:
                return "(?!" + "|".join(conflicting_strings) + ")"
            else:
                return ""

        prefix_tokens = [re.escape(typographical_symbol) + resolve_conflicts_between_prefix_and_metric(typographical_symbol) for typographical_symbol in list(Metric.Prefix.defined_prefixes_by_symbol.keys())]
        prefix_tokens.sort(key = len, reverse = True)

        prefix_tokens = "(" + "|".join(prefix_tokens) + "){0,1}"
        metric_tokens = "(" + "|".join(metric_tokens) + "){1}"
        power_tokens = "(⁰|⁻¹|⁻²|²|⁻³|³|⁻⁴|⁴|⁻⁵|⁵|⁻⁶|⁶|⁻⁷|⁷|⁻⁸|⁸|⁻⁹|⁹|\\^[\\-\\.\\d]+){0,1}"

        Metric.parsing_pattern_string = prefix_tokens + metric_tokens + power_tokens
        Metric.parsing_pattern = re.compile(Metric.parsing_pattern_string, re.UNICODE)

    @classmethod
    def symbol_string_to_terms(cls, symbol_string):
        """
        Parses a string of positive-powered Metric symbols (as would be found
        in either a numerator or denominator of a complete Metric symbol) into
        a list of Metric.Terms.
        """
        if not symbol_string:
            return []

        if not Metric.parsing_pattern:
            Metric.rebuild_parsing_pattern()

        terms = []
        for match in Metric.parsing_pattern.findall(symbol_string):
            matched_prefix = match[0]
            matched_symbol = match[1]
            matched_power = match[2]

            if matched_prefix:
                if not matched_prefix in Metric.Prefix.defined_prefixes_by_symbol:
                    raise MeasurementParsingException("Unrecognized prefix symbol '%s' when parsing metric string '%s'" % (matched_prefix, symbol_string))
                prefix = Metric.Prefix.defined_prefixes_by_symbol[matched_prefix]
            else:
                prefix = None

            if matched_symbol:
                if not matched_symbol in Metric.defined_metrics_by_symbol:
                    raise MeasurementParsingException("Unrecognized metric symbol '%s' when parsing metric string '%s'" % (matched_symbol, symbol_string))
                metric = Metric.defined_metrics_by_symbol[matched_symbol]
            else:
                raise MeasurementParsingException("No metric symbol found when parsing metric string '%s'" % symbol_string)

            powers = {
                      "⁰": 0,
                      "":  1,
                      "⁻¹": -1,
                      "²": 2,
                      "⁻²": -2,
                      "³": 3,
                      "⁻³": -3,
                      "⁴": 4,
                      "⁻⁴": -4,
                      "⁵": 5,
                      "⁻⁵": -5,
                      "⁶": 6,
                      "⁻⁶": -6,
                      "⁷": 7,
                      "⁻⁷": -7,
                      "⁸": 8,
                      "⁻⁸": -8,
                      "⁹": 9,
                      "⁻⁹": -9}
            if matched_power in powers:
                power = powers[matched_power]
            else:
                power = int(matched_power.replace("^", ""))

            terms.append(Metric.Term(prefix, metric, power))

        return terms


    def numerator(self):
        return Metric(terms = [t for t in self.terms if t.power > 0])
    def denominator(self):
        return One / Metric(terms = [t for t in self.terms if t.power < 0])


    def __hash__(self):
        "Computes a hash value for this Metric."
        hash_to_return = 0
        for term in self.terms:
            hash_to_return = hash_to_return ^ hash(term)
        return hash_to_return

    def __eq__(self, other):
        """
        Tests whether this Metric is equivalent to another Metric.  Also,
        allows the numbers 1 and 10 to be equivalent to One and Ten.
        """
        if other == None:
            return False
        elif id(self) == id(other):
            return True
        elif isnumber(other):
            if self == One:
                return other == 1
            if self == Ten:
                return other == 10
            else:
                return NotImplemented
        elif isinstance(other, Metric):
            reduced_self = self.reduce()
            reduced_other = other.reduce()
            return (reduced_self.magnitude == reduced_other.magnitude and
                    reduced_self.metric.terms == reduced_other.metric.terms)
        return NotImplemented
    def __ne__(self, other):
        "Tests whether this Metric is different from another Metric."
        equal = self.__eq__(other)
        if equal == NotImplemented:
            return NotImplemented
        else:
            return not equal

    def __mul__(self, other):
        "When multiplying Metrics, derives a new metric through multiplication.  When multiplying by numbers, produces a Quantity in this Metric."
        if isinstance(other, Metric):
            return Metric(terms = [Metric.Term(None, self, 1), Metric.Term(None, other, 1)])
        elif isnumber(other):
            return Quantity(other, self)
        return NotImplemented
    def __rmul__(self, other):
        "When multiplying Metrics, derives a new metric through multiplication.  When multiplying by numbers, produces a Quantity in this Metric."
        if isinstance(other, Metric):
            return Metric(terms = [Metric.Term(None, self, 1), Metric.Term(None, other, 1)])
        elif isnumber(other):
            return Quantity(other, self)
        return NotImplemented

    def __pow__(self, power):
        "Derives a new metric by raising this one to the given power."
        return Metric(terms = [Metric.Term(None, self, power)])

    def __truediv__(self, other):
        "When dividing Metrics, derives a new metric through division.  When dividing by numbers, produces a Quantity in this Metric."
        if isinstance(other, Metric):
            return Metric(terms = [Metric.Term(None, self, 1), Metric.Term(None, other, -1)])
        elif isnumber(other):
            return Quantity(1.0 / other, self)
        return NotImplemented
    def __rtruediv__(self, other):
        "When dividing Metrics, derives a new metric through division.  When dividing by numbers, produces a Quantity in this Metric."
        if isinstance(other, Metric):
            return Metric(terms = [Metric.Term(None, self, 1), Metric.Term(None, other, -1)])
        elif isnumber(other):
            return Quantity(other, One / self)
        return NotImplemented
    __div__ = __truediv__
    __rdiv__ = __rtruediv__


    def reduce(self):
        "Reduces self down to a Quantity expressed without prefixes."

        if not hasattr(self, "_reduced"):
            reduced_magnitude = 1
            reduced_metric_terms = []

            for term in self.terms:
                if term.metric.name == "ten":
                    if term.power != 0:
                        reduced_magnitude *= (10**term.power) * (term.prefix.base**(term.prefix.power * term.power))
                else:
                    reduced_magnitude *= term.prefix.base**(term.prefix.power * term.power)
                    reduced_metric_terms.append(Metric.Term(None, term.metric, term.power))

            # sneak past the Immutable base class for caching this lazy-
            # evaluated property
            self._internal__setattr__("_reduced", Quantity(reduced_magnitude, Metric(terms = reduced_metric_terms)))

        return self._reduced


    def __repr__(self):
        "Produces a representation of this Metric that, when eval()ed, produces a Metric equivalent to this one."
        if self.defined:
            return "Metric(" + repr(self.name) + ", " + repr(self.typographical_symbol) + ", " + repr(self.dimension) + ")"
        else:
            to_return = "Metric(terms = ["
            to_return += ", ".join([repr(m) for m in self.terms])
            to_return += "])"

            return to_return

    def __unicode__(self):
        "Produces the typographical symbol of this metric."
        return self.typographical_symbol
    __str__ = __unicode__




    conversions = {}
    class Conversion(object):
        "A Conversion, which is a callable type that converts a Quantity to a different Metric"

        __slots__ = "metric"
        def __init__(self, metric):
            self.metric = metric
            Metric.conversions[metric] = self

        def applies_to(self, metric):
            "Determines whether this conversion could apply to the metric in question."
            return (self.metric == metric or
                    self.metric == (One / metric))

        def __call__(self, quantity):
            "Performs the conversion of quantity to the desired metric."
            raise NotImplementedError

    class ScalarConversion(Immutable, Conversion):
        "A Conversion which is simply a multiplication or division by a scalar value."

        __slots__ = "frozen", "metric", "scalar_factor"
        def __init__(self, scalar_factor):
            self.scalar_factor = scalar_factor

            super(Metric.ScalarConversion, self).__init__(scalar_factor.metric)
            self.frozen = True

        def __call__(self, quantity):
            "Performs the conversion of quantity."

            reduced_quantity = quantity.reduce()
            reduced_factor = self.scalar_factor.reduce()

            if Metric.Term(None, reduced_quantity.metric, 1) in reduced_factor.metric.terms:
                return reduced_quantity / reduced_factor
            elif Metric.Term(None, reduced_quantity.metric, -1) in reduced_factor.metric.terms:
                return reduced_quantity * reduced_factor
            else:
                # when factor-label conversions are used, it is possible to get
                # Quantities here with derived metrics, for example:
                # mi/h => m/h ... the hours cancel out in the find_conversion method, so
                # simple mi/m is required; however, we need to return the correct metric,
                # as m/h
                if (reduced_quantity.metric.numerator() == reduced_factor.metric.numerator() or
                    reduced_quantity.metric.denominator() == reduced_factor.metric.denominator()):
                    return reduced_quantity / reduced_factor
                elif (reduced_quantity.metric.numerator() == reduced_factor.metric.denominator() or
                      reduced_quantity.metric.denominator() == reduced_factor.metric.numerator()):
                    return reduced_quantity * reduced_factor
                else:
                    raise MetricConversionError("Quantity '%s' is not convertible with scalar conversion '%s'" % (quantity, self.scalar_factor))

    class FunctionConversion(Immutable, Conversion):
        "A Conversion which is a pair of functions (from->to and to->from) to compute on the incoming quantity."

        __slots__ = "frozen", "metric", "from_metric", "to_metric", "from_function", "to_function"
        def __init__(self, from_metric, to_metric, from_function, to_function):
            self.from_metric = from_metric
            self.from_function = from_function

            self.to_metric = to_metric
            self.to_function = to_function

            super(Metric.FunctionConversion, self).__init__(from_metric / to_metric)
            self.frozen = True

        def __call__(self, quantity):
            if quantity.metric == self.to_metric:
                return self.to_function(quantity)
            elif quantity.metric == self.from_metric:
                return self.from_function(quantity)
            else:
                raise MetricConversionError("Quantity '%s' is not convertible with this conversion function between %s and %s" % (quantity, self.from_metric, self.to_metric))

    def is_convertible_to(self, other):
        """
        Returns a boolean indicating whether a Conversion exists that can
        convert self to other.
        """
        if (self == other):
            return True

        if (self.dimension != other.dimension):
            return False

        if Metric.find_conversion(self, other):
            return True

        return False

    def to(self, other):
        """
        Returns a conversion from this Metric to another metric, if one
        exists.  Raises MetricConversionError if no acceptable Conversion is
        found.
        """
        if (self == other):
            return lambda q: (1 * One) * q

        if (self.dimension != other.dimension):
            raise MetricConversionError("There is no conversion between '%s' and '%s', because they measure different Dimensions." % (self, other))

        conversion = Metric.find_conversion(self, other)
        if not conversion:
            raise MetricConversionError("There is no conversion between '%s' and '%s'." % (self, other))

        return conversion

    @classmethod
    def _coerced_multiply(cls, left, right):
        if isinstance(left, decimal.Decimal) and isinstance(right, float):
            return left * decimal.Decimal(six.text_type(right))
        elif isinstance(left, float) and isinstance(right, decimal.Decimal):
            return decimal.Decimal(six.text_type(left)) * right
        else:
            return left * right

    @classmethod
    def find_conversion(cls, from_metric, to_metric):
        """
        Locates or creates a callable conversion between the two metrics.
        find_conversion looks through the global set of defined Conversions,
        and may invert the Conversion if necessary.  It usually won't be
        necessary to call find_conversion directly from your code, and you
        shouldn't rely on the return value from find_conversion begin a
        subclass of Conversion, as it may be a bound function.
        """
        reduced_from = from_metric.reduce()
        reduced_to = to_metric.reduce()
        reduced = reduced_from / reduced_to

        found_conversion = None

        # super simple case: this is just a prefix conversion, as in km -> nm, and thus the metric to find is Metric::One
        if reduced.metric == One:
            return lambda q: Quantity(Metric._coerced_multiply(reduced.magnitude, q.magnitude), to_metric)

        metric_to_find = reduced.metric
        inverse_to_find = One / metric_to_find

        # simple case: find a conversion for the exact metric or it's inverse
        if metric_to_find in Metric.conversions:
            return Metric.conversions[metric_to_find]
        elif inverse_to_find in Metric.conversions:
            return lambda q: Quantity(Metric._coerced_multiply(reduced.magnitude, Metric.conversions[inverse_to_find](q).magnitude), to_metric)

        # more difficult: find a conversion that is expressed in factors of the
        #                 given metrics, as in cubic inches to cubic meters
        #                 note: this can only work with integral powers
        # stepping down from the highest power present, keep factoring the metrics
        # until something turns up
        # for example, m^3 -> ft^3 will first try to take both metrics to the cube-root,
        # which yields m -> ft; if that didn't show up as a conversion, then it would try
        # m^2 -> ft^2
        highest_power = max(metric_to_find.terms, key = lambda t: abs(t.power)).power
        for power in range(highest_power, 1, -1):
            factored_metric = metric_to_find**(1/power)
            inverse_factored_metric = One / factored_metric
            if factored_metric in Metric.conversions:
                return lambda q: Metric.conversions[factored_metric](q**(1/power))**power
            elif inverse_factored_metric in Metric.conversions:
                return lambda q: Metric.conversions[inverse_factored_metric](q**(1/power))**power

        # more difficult: use the factor-label method for finding a set of conversions
        #                 that, chained together, would produce the correct conversion
        #                 as in miles/hour to meters/second
        #
        # simple case, try to take each term down to an SI base metric, so in the example,
        # try to take miles down to meters and then try to take hour down to seconds
        si_conversion = 1 * One
        for term in metric_to_find.terms:
            si_metric = Metric.base_metric_of[term.metric.dimension]
            term_conversion = term.metric.to(si_metric)
            if term.power > 0:
                si_conversion *= term_conversion(1 * term.metric)
            else:
                si_conversion /= term_conversion(1 * term.metric)
        if si_conversion.metric == One:
            return lambda q: Quantity(Metric._coerced_multiply(si_conversion.magnitude, q.magnitude), reduced_to.metric)

        return None

class Quantity(Immutable):
    """
    A Quantity is a magnitude in a Metric, and is the number-like value used
    in measurement-based arithmetic.

    Quantities may be parsed from strings (e.g. ``Quantity.parse('5m')``), constructed by
    multiplying a Python number by a Metric (``5 * Meter``), or by using the
    constructor (``Quantity(5, Meter)``).

    >>> distance = Quantity(10, Meter)
    >>> time = 2 * Second
    >>> speed = distance / time
    >>> assert speed == Quantity.parse("5 m/s")

    Quantities support all of the operators you'd expect of Python numbers,
    including arithmetic (+, -, *, /, and **) and comparison (<, <=, >, >=,
    ==, !=).

    >>> distance = 5 * Meter
    >>> distance = distance + 10 * Meter
    >>> distance == 15 * Meter
    True
    >>> distance = distance - 3 * Meter
    >>> distance == 12 * Meter
    True
    >>> speed = distance / (2 * Second)
    >>> speed == 6 * (Meter / Second)
    True
    >>> acceleration = speed / (3 * Second)
    >>> acceleration == 2 * (Meter / Second**2)
    True

    >>> frequency = 5 / Second
    >>> time = 30 * Second
    >>> time * frequency == 150
    True

    Note: measurement typically uses the new Python 'true' division
    throughout, but it does have an implementation of __div__ for 'floor'
    division.
    """

    @classmethod
    def parse(cls, quantity_string, to = None):
        """
        Converts a string to a Quantity.  The string may be a plain number, in
        which case it will be considered to be a Quantity of Metric ``One``.
        Otherwise, a Metric typographical string is expected to follow the
        number.

        Examples of valid strings:

        >>> Quantity.parse("5") == Quantity(5, One)
        True
        >>> Quantity.parse("-1.0001") == Quantity(-1.0001, One)
        True
        >>> Quantity.parse("20.3 m/s") == Quantity(20.3, Meter / Second)
        True
        >>> Quantity.parse("(-1.4+2.3j) m") == Quantity(complex(-1.4, 2.3), Meter)
        True
        """

        pattern = re.compile(r"(?P<magnitude>((\(?\-?[\d]+\.?[\d]?)[\+\-]([\d]+\.?[\d]?)j\)?)|(\-?[\d]+\.?[\d]*))\s?(?P<metric>.*)")

        match = pattern.match(quantity_string)
        if not match:
            raise MeasurementParsingException("Could not parse '%s' to a Quantity." % quantity_string)

        components = match.groupdict()

        magnitude = components["magnitude"]
        if not to:
            # try to detect the kind of number it is
            if magnitude.startswith("(") and magnitude.endswith(")"):
                magnitude = magnitude[1:len(magnitude)-1]
                to = complex
            else:
                if not magnitude.count("."):
                    if len(magnitude) > 18: # not definitive, but a good guess
                        to = int
                    else:
                        to = int
                else:
                    if len(magnitude) > 18:
                        to = decimal.Decimal
                    else:
                        to = float

        magnitude = to(magnitude)

        if not components["metric"]:
            metric = One
        else:
            metric = Metric.parse(components["metric"])

        return Quantity(magnitude, metric)

    __slots__ = "frozen", "magnitude", "metric"

    def __init__(self, magnitude, metric):
        "Creates a new Quantity with the given magnitude and metric."
        self.magnitude = magnitude

        if isinstance(metric, str):
            self.metric = Metric.parse(metric)
        else:
            self.metric = metric

        self.frozen = True

    def __composite_values__(self):
        "Allows Quantity to be stored as a composite value using SQLAlchemy."
        return self.magnitude, self.metric.typographical_symbol

    def to(self, desired_metric):
        "Converts this quantity to the desired metric."
        return self.metric.to(desired_metric)(self)

    def reduce(self):
        "Reduces this quantity down to a metric with no prefixes."
        reduced_metric = self.metric.reduce()
        return Quantity(self.magnitude * reduced_metric.magnitude, reduced_metric.metric)

    def __hash__(self):
        "Computes the hash value for this Quantity."
        return hash(self.metric) ^ hash(self.magnitude)

    def __bool__(self):
        "Tests whether this Quantity is non-zero."
        return self.magnitude.__nonzero__()

    def _coerce_magnitude(self, other):
        if isinstance(other, Quantity):
            if isinstance(self.magnitude, decimal.Decimal) and isinstance(other.magnitude, float):
                return Quantity(decimal.Decimal(six.text_type(other.magnitude)), other.metric)
            elif isinstance(self.magnitude, float) and isinstance(other.magnitude, decimal.Decimal):
                return Quantity(float(other.magnitude), other.metric)
            else:
                return other
        return other

    def __eq__(self, other):
        """
        Tests whether a Quantity is equivalent to this Quantity.  Also, if
        this Quantity's Metric is One, allows comparing raw numbers, as in
        Quantity(4, One) == 4.0
        """
        if other == None:         return False
        if id(self) == id(other): return True

        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            if self.metric == other.metric:
                return self.magnitude == other.magnitude
            elif other.metric.is_convertible_to(self.metric):
                return self.magnitude == other.to(self.metric).magnitude
            else:
                return False
        elif isnumber(other) and self.metric == One:
            return self.magnitude == other
        else:
            return NotImplemented
    def __ne__(self, other):
        """
        Tests whether a Quantity is different from this Quantity.  Also, if
        this Quantity's Metric is One, allows comparing raw numbers, as in
        Quantity(4, One) == 4.0
        """
        other = self._coerce_magnitude(other)

        equal = self.__eq__(other)
        if equal == NotImplemented:
            return NotImplemented
        else:
            return not equal
    def __lt__(self, other):
        """
        Tests whether this Quantity is less than another Quantity of this
        Metric (allowing comparison with raw numbers if this Quantity's Metric
        is One).
        """
        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            if self.metric == other.metric:
                return self.magnitude < other.magnitude
            elif other.metric.is_convertible_to(self.metric):
                return self.magnitude < other.to(self.metric).magnitude
        elif isnumber(other) and self.metric == One:
                return self.magnitude < other
        return NotImplemented
    def __le__(self, other):
        """
        Tests whether this Quantity is less than or equal to another Quantity
        of this Metric (allowing comparison with raw numbers if this
        Quantity's Metric is One).
        """
        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            if self.metric == other.metric:
                return self.magnitude <= other.magnitude
            elif other.metric.is_convertible_to(self.metric):
                return self.magnitude <= other.to(self.metric).magnitude
        elif isnumber(other) and self.metric == One:
                return self.magnitude <= other
        return NotImplemented
    def __gt__(self, other):
        """
        Tests whether this Quantity is greater than another Quantity of this
        Metric (allowing comparison with raw numbers if this Quantity's Metric
        is One).
        """
        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            if self.metric == other.metric:
                return self.magnitude > other.magnitude
            elif other.metric.is_convertible_to(self.metric):
                return self.magnitude > other.to(self.metric).magnitude
        elif isnumber(other) and self.metric == One:
                return self.magnitude > other
        return NotImplemented
    def __ge__(self, other):
        """
        Tests whether this Quantity is greater than or equal to another
        Quantity of this Metric (allowing comparison with raw numbers if this
        Quantity's Metric is One).
        """
        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            if self.metric == other.metric:
                return self.magnitude >= other.magnitude
            elif other.metric.is_convertible_to(self.metric):
                return self.magnitude >= other.to(self.metric).magnitude
        elif isnumber(other) and self.metric == One:
                return self.magnitude >= other
        return NotImplemented


    def __add__(self, other):
        "Adds two Quantities, if they are in the same Metric."
        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            if other.metric == self.metric:
                return Quantity(self.magnitude + other.magnitude, self.metric)
            elif other.metric.is_convertible_to(self.metric):
                converted = other.to(self.metric)
                return Quantity(self.magnitude + converted.magnitude, self.metric)
        return NotImplemented
    def __sub__(self, other):
        "Subtracts two Quantities, if they are in the same Metric."
        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            if other.metric == self.metric:
                return Quantity(self.magnitude - other.magnitude, self.metric)
            elif other.metric.is_convertible_to(self.metric):
                converted = other.to(self.metric)
                return Quantity(self.magnitude - converted.magnitude, self.metric)
        return NotImplemented

    def __mul__(self, other):
        "Multiplies two Quantities."
        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            return Quantity(self.magnitude * other.magnitude, self.metric * other.metric)
        return NotImplemented
    def __div__(self, other):
        "Divides (using 'floor division') two Quantities."
        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            return Quantity(self.magnitude // other.magnitude, self.metric / other.metric)
        return NotImplemented
    def __truediv__(self, other):
        "Divides two Quantities."
        other = self._coerce_magnitude(other)

        if isinstance(other, Quantity):
            return Quantity(self.magnitude / other.magnitude, self.metric / other.metric)
        return NotImplemented
    def __pow__(self, power):
        "Raises this Quantity (both magnitude and metric) to the given power."
        if isinstance(power, Quantity) and power.metric == One:
            power = power.magnitude

        if isnumber(power):
            return Quantity(self.magnitude**power, self.metric**power)
        return NotImplemented


    def __neg__(self):
        "Returns a Quantity negated from this Quantity."
        return Quantity(self.magnitude.__neg__(), self.metric)
    def __abs__(self):
        "Returns the absolute value of this Quantity."
        return Quantity(self.magnitude.__abs__(), self.metric)


    def __repr__(self):
        """
        Produces a representation of this Quantity that, when eval()ed,
        produces an equivalent Quantity.
        """
        return "Quantity(" + repr(self.magnitude) + ", " + repr(self.metric) + ")"
    def __unicode__(self):
        """
        Produces a string representation of this Quantity in numbers and
        typographical symbols.
        """
        if self.metric == One:
            return six.text_type(self.magnitude)
        elif self.metric == Ten:
            return six.text_type(10 * self.magnitude)
        else:
            return six.text_type(self.magnitude) + " " + six.text_type(self.metric)
    __str__ = __unicode__

class Constant(Quantity):

    def __init__(self, magnitude, metric, name, typographical_symbol = None):

        if hasattr(self, "frozen"):
            return

        self.name = name
        self.typographical_symbol = typographical_symbol
        if not self.typographical_symbol:
            self.typographical_symbol = name

        Constant.define(self)

        super(Constant, self).__init__(magnitude, metric)

    defined_constants_by_name = {}

    @classmethod
    def all(cls):
        return list(Constant.defined_constants_by_name.values())

    @classmethod
    def get_by_name(cls, name):
        if name in Constant.defined_constants_by_name:
            return Constant.defined_constants_by_name[name]
        else:
            return None

    @classmethod
    def define(cls, constant):
        Constant.defined_constants_by_name[constant.name] = constant

## Dimensions ##

# fundamental dimensions
Number = Dimension(name = "number", typographical_symbol = "N")
"""
Number is the dimension of counting.  See http://en.wikipedia.org/wiki/Number
for more information.
"""

# fundamental physical dimensions
Length = Dimension(name = "length", typographical_symbol = "L")
"Length is the dimension of physical extent."

Time = Dimension(name = "time", typographical_symbol = "T")
"Time is the dimension of change."

Mass = Dimension(name = "mass", typographical_symbol = "M")
"Mass is the dimension of matter."

Charge = Dimension(name = "charge", typographical_symbol = "Q")
"Charge is the dimension of the strength of an electric field."

Temperature = Dimension(name = "temperature", typographical_symbol = "Θ")
"Temperature is the dimension of the excitement of a thermodynamic system"

AmountOfSubstance = Dimension(name = "amount of substance")
"""
Amount of Substance is the dimension of counting the fundamental particles of
matter in an object.
"""

LuminousIntensity = Dimension(name = "luminous intensity")
"""
Luminous Intensity is the dimension of the strength and quantity of photons
emitted by a light source.
"""

Information = Dimension(name = "information")
"""
Information is the dimension of measuring the available choices or degrees of
freedom in a system.  See http://en.wikipedia.org/wiki/Information for more
information.
"""

# derived physical dimensions
Frequency = Dimension(name = "frequency", derivation = Number / Time)

Area = Dimension(name = "area", derivation = Length**2)
Volume = Dimension(name = "volume", derivation = Length**3)
Density = Dimension(name = "density", derivation = Mass / Volume)

Speed = Dimension(name = "speed", derivation = Length / Time)
Acceleration = Dimension(name = "acceleration", derivation = Speed / Time)

Momentum = Dimension(name = "momentum", derivation = Mass * Speed)
Energy = Dimension(name = "energy", derivation = Mass * Length * Acceleration)
Action = Dimension(name = "action", derivation = Energy * Time)
Force = Dimension(name = "force", derivation = Mass * Acceleration)
Power = Dimension(name = "power", derivation = Mass * Area / Time**3)
Pressure = Dimension(name = "pressure", derivation = Mass / (Length * (Time**2)))

Current = Dimension(name = "current", derivation = Charge / Time)
Voltage = Dimension(name = "voltage", derivation = (Mass * Area) / ((Time**2) * Charge))
Resistance = Dimension(name = "resistance", derivation = (Mass * Area) / (Time * (Charge**2)))

InformationFlow = Dimension(name = "information flow", derivation = Information / Time)


# fundamental economic dimensions
Exchange = Dimension("exchange")
"The dimension measuring the exchange of value in an economy."


## Metrics ##

# Number units
Ten = Metric("ten", "10", Number)
One = Metric("one", "1", Number, derivation = Ten**0)


# SI decimal prefixes
Yotta = Metric.Prefix("yotta", "Y" , 10, 24)
Zetta = Metric.Prefix("zetta", "Z" , 10, 21)
Exa   = Metric.Prefix("exa"  , "E" , 10, 18)
Peta  = Metric.Prefix("peta" , "P" , 10, 15)
Tera  = Metric.Prefix("tera" , "T" , 10, 12)
Giga  = Metric.Prefix("giga" , "G" , 10, 9)
Mega  = Metric.Prefix("mega" , "M" , 10, 6)
Kilo  = Metric.Prefix("kilo" , "k" , 10, 3)
Hecto = Metric.Prefix("hecto", "h" , 10, 2)
Deca  = Metric.Prefix("deca" , "da", 10, 1)

Deci  = Metric.Prefix("deci" , "d" , 10, -1)
Centi = Metric.Prefix("centi", "c" , 10, -2)
Milli = Metric.Prefix("milli", "m" , 10, -3)
Micro = Metric.Prefix("micro", "µ" , 10, -6)
Nano  = Metric.Prefix("nano" , "n" , 10, -9)
Pico  = Metric.Prefix("pico" , "p" , 10, -12)
Femto = Metric.Prefix("femto", "f" , 10, -15)
Atto  = Metric.Prefix("atto" , "a" , 10, -18)
Zepto = Metric.Prefix("zepto", "z" , 10, -21)
Yocto = Metric.Prefix("yocto", "y" , 10, -24)


# IEC binary prefixes
Yobi = Metric.Prefix("yobi", "Yi", 2, 80)
Zebi = Metric.Prefix("zebi", "Zi", 2, 70)
Exbi = Metric.Prefix("exbi", "Ei", 2, 60)
Pebi = Metric.Prefix("pebi", "Pi", 2, 50)
Tebi = Metric.Prefix("tebi", "Ti", 2, 40)
Gibi = Metric.Prefix("gibi", "Gi", 2, 30)
Mebi = Metric.Prefix("mebi", "Mi", 2, 20)
Kibi = Metric.Prefix("kibi", "Ki", 2, 10)


# SI base units
Meter = Metric("meter", "m", Length)
Gram = Metric("gram", "g", Mass)
Second = Metric("second", "s", Time)
Ampere = Metric("ampere", "A", Current)
Kelvin = Metric("kelvin", "K", Temperature)
Mole = Metric("mole", "mol", AmountOfSubstance)
Candela = Metric("candela", "cd", LuminousIntensity)

# SI derived units
Radian = Metric("radian", "rad", derivation = (Meter / Meter))
Steradian = Metric("steradian", "sr", derivation = (Meter**2 / Meter**2))
Hertz = Metric("hertz", "Hz", derivation = (One / Second))
Coulomb = Metric("coulomb", "C", derivation = (Ampere * Second))
Joule = Metric("joule", "J", derivation = (Kilo*Gram) * ((Meter**2) / (Second**2)))
Ohm = Metric("ohm", "Ω", derivation = ( (Meter**2 * (Kilo * Gram)) / (Second**3 * Ampere**2) ))
Volt = Metric("volt", "V", derivation = ( (Meter**2 * (Kilo * Gram)) / (Second**3 * Ampere) ))
Watt = Metric("watt", "W", derivation = ((Kilo * Gram) * Meter**2) / Second**3)

# SI synonyms
Liter = Metric("liter", "L", derivation = (Deci * Meter)**3)
"The Liter is defined as a cubic decimeter."

Angstrom = Metric("ångström", "Å",
                  terms = [Metric.Term(Metric.Prefix("10^-10", "10^-10", 10, -10),
                                       Meter,
                                       1)])
"The ångström is 0.1 nanometers, or 10e-10 meters."


# Time units
Minute = Metric("minute", "min", dimension = Time)
Metric.ScalarConversion(Quantity(60, Second / Minute))
Hour = Metric("hour", "h", dimension = Time)
Metric.ScalarConversion(Quantity(3600, Second / Hour))
Day = Metric("day", "d", dimension = Time)
Metric.ScalarConversion(Quantity(86400, Second / Day))
Week = Metric("week", "wk", dimension = Time)
Metric.ScalarConversion(Quantity(604800, Second / Week))

Year = Metric("year", "y", dimension = Time)
"The \"common\" year of 365 days.  http://en.wikipedia.org/wiki/Common_year."
Metric.ScalarConversion(Quantity(31536000, Second / Year))



# IEEE 1541/IEC 80000 units of information
Bit = Metric("bit", "bit", Information)
Byte = Metric("byte", "B", Information)
Octet = Metric("octet", "o", Information)

Metric.ScalarConversion(Quantity(8, Bit / Octet))
Metric.ScalarConversion(Quantity(8, Bit / Byte))   # this is NOT completely standard, but COME ON
Metric.ScalarConversion(Quantity(1, Byte / Octet)) # ditto here


# Alternative Temperature Metrics
Celsius = Metric("celsius", "°C", Temperature)
Metric.FunctionConversion(Celsius, Kelvin,
                          lambda c: (c.magnitude + 273.15) * Kelvin,
                          lambda k: (k.magnitude - 273.15) * Celsius)

Fahrenheit = Metric("fahrenheit", "°F", Temperature)
Metric.FunctionConversion(Fahrenheit, Kelvin,
                          lambda f: ((f.magnitude + 459.67) * (5/9)) * Kelvin,
                          lambda k: ((k.magnitude * (9/5)) - 459.67) * Fahrenheit)
Metric.FunctionConversion(Fahrenheit, Celsius,
                          lambda f: ((f.magnitude - 32.0) * (5/9)) * Celsius,
                          lambda c: ((c.magnitude * (9/5)) + 32) * Fahrenheit)

Rankine = Metric("rankine", "°R", Temperature)
Metric.FunctionConversion(Rankine, Kelvin,
                          lambda r: (r.magnitude * (5/9)) * Kelvin,
                          lambda k: (k.magnitude * (9/5)) * Rankine)
Metric.FunctionConversion(Rankine, Celsius,
                          lambda r: ((r.magnitude - 491.67) * (5/9)) * Celsius,
                          lambda c: ((c.magnitude + 273.15) * (9/5)) * Rankine)
Metric.FunctionConversion(Rankine, Fahrenheit,
                          lambda r: (r.magnitude - 459.67) * Fahrenheit,
                          lambda f: (f.magnitude + 459.67) * Rankine)


## Quantities ##

# Mathematical/Numerical Constants
Zero = Constant(0.0, One, "zero", "0")
Unity = Constant(1.0, One, "unity", "1")
ImaginaryUnit = Constant((0 + 1j), One, "imaginary unit", "i")
EulersNumber = Constant(2.7182818284590451, One, "Euler's number", "e")
Pi = Constant(3.14159265359, One, "pi", "π")
Phi = Constant((1 + 5**0.5) / 2, One, "phi", "φ")


# Physical Constants
AbsoluteZero = Constant(0.0, Kelvin, "absolute zero")
PlancksConstant = Constant(6.62606896e-34, Joule * Second, "Planck's constant", "ℎ")
DiracsConstant = Constant(1.054571628e-34, Joule * Second, "Dirac's constant", "ℏ")
ElementaryCharge = Constant(1.602176487e-19, Coulomb, "elementary charge", "e")
GravitationalConstant = Constant(667428000000.0, Meter**3 / ((Kilo*Gram) * Second**2),
                                 "gravitational constant", "G")
SpeedOfLight = Constant(299792458, Meter / Second, "speed of light", "c")





### Calculation Script Support ###
def calculate(script):
    """
    Evaluates a calculation script.  Calculation scripts are a limited subset
    of Python, with the following augmented rules:

    * Quantities may be represented in their string forms, such as '12 V' for
      ``Quantity(12, Volt)``.

      >>> result = calculate("12 V")
      >>> result == 12 * Volt
      True
      >>> result = calculate("12 m/s")
      >>> result == 12 * (Meter / Second)
      True

    * The plural names of Metrics are allowed, so all of the following are
      considered the same: '12 V', '12 volt', '12 volts'.

      >>> calculate("12 volt") == calculate("12 volt") == calculate("12 V")
      True

    * Besides preprocessing Quantities and Metrics, all of the normal Python
      syntax applies, especially variables and the arithmetic and comparison
      operators.

      >>> result = calculate(\"\"\"
      ... v = 12 V
      ... i = 4 A
      ... v / i
      ... \"\"\")
      >>> result == 3 * Ohm
      True
      >>> result = calculate(\"\"\"
      ... v = 12 V
      ... i = 4 A
      ... r = 3 ohm
      ... v == i * r
      ... \"\"\")
      >>> result == True
      True

    * The Python environment in which the calculation script is run has no access
      to Python ``__builtins__``, and may not import modules of any kind.

      >>> assert "PyPy's exec() functionality doesn't quite work the way Python's does."
      >>> import sys
      >>> if "PyPy" not in sys.version:
      ...     result = calculate(\"\"\"
      ... import sys
      ... sys.path
      ...     \"\"\")
      ... else:
      ...     raise ImportError("__import__ not found") # Fake it for doctest completeness
      Traceback (most recent call last):
       ...
      ImportError: __import__ not found

    * The last line of the script is evaluated as the return value of the script,
      and may be any valid Python expression or Quantity expression.  If you need
      to return multiple values, pack them in a ``tuple`` or ``dict``  on the
      last line of your script.

      >>> result = calculate(\"\"\"
      ... v = 12 V
      ... i = 4 A
      ... { "resistance": v / i, "power" : v * i }
      ... \"\"\")
      >>> result["resistance"] == 3 * Ohm
      True
      >>> result["power"] == 48 * Watt
      True

    """

    if not Metric.parsing_pattern_string:
        Metric.rebuild_parsing_pattern()

    scriptlines = script.splitlines()

    if not scriptlines:
        return None

    preparedlines = []


    # step zero.a: make the metric patterns
    metric_tokens = [re.escape(metric.name) for metric in list(Metric.defined_metrics_by_symbol.values())]
    metric_tokens.sort(key = len, reverse = True)

    plural_tokens = [re.escape(metric.plural_name) for metric in list(Metric.defined_metrics_by_symbol.values())]
    plural_tokens.sort(key = len, reverse = True)

    prefix_tokens = [re.escape(prefix.name) for prefix in list(Metric.Prefix.defined_prefixes_by_symbol.values())]
    prefix_tokens.sort(key = len, reverse = True)

    metric_tokens = "(" + "|".join(metric_tokens) + "){1}"
    plural_tokens = "(" + "|".join(plural_tokens) + "){1}"
    prefix_tokens = "(" + "|".join(prefix_tokens) + "){0,1}"

    full_metric_name_pattern = re.compile(prefix_tokens + metric_tokens)
    plural_pattern = re.compile(prefix_tokens + plural_tokens)


    # step zero.b: make the quantity patterns
    magnitude_pattern = r"(\(?\-?[\d]+\.?[\d]?)[\+\-]([\d]+\.?[\d]?)j\)?)|(\-?[\d]+\.?[\d]*)"
    metric_pattern = r"((" + Metric.parsing_pattern_string + ")+?)+(/((" + Metric.parsing_pattern_string + ")+?)+)?"

    quantity_pattern_string = r"(?P<magnitude>(" + magnitude_pattern  + ")\s?(?P<metric>" + metric_pattern  + r")"
    quantity_pattern = re.compile(quantity_pattern_string, re.UNICODE)

    conversion_pattern_string = r"(.*)\sto\s(" + metric_pattern + ")"
    conversion_pattern = re.compile(conversion_pattern_string)

    for number, scriptline in enumerate(scriptlines):
        # pre-processing step one: replace plural metric names with singular
        for match in plural_pattern.finditer(scriptline):
            full_prefix, plural_metric = match.groups()

            found_prefix = None
            if full_prefix:
                for prefix in list(Metric.Prefix.defined_prefixes.values()):
                    if prefix.name == full_prefix:
                        found_prefix = prefix
                        break
                if not found_prefix:
                    raise MeasurementParsingException("Could not find Metric Prefix '%s'." % found_prefix)

            found_metric = None
            for metric in list(Metric.defined_metrics_by_symbol.values()):
                if metric.plural_name == plural_metric:
                    found_metric = metric
                    break

            if not found_metric:
                raise MeasurementParsingException("Could not find Metric '%s'." % plural_metric)

            if found_prefix:
                found_metric = found_prefix * found_metric

            scriptline = scriptline.replace(match.string[match.start():match.end()],
                                            found_metric.name)

        # pre-processing step two: replace full metric names with symbols
        for match in full_metric_name_pattern.finditer(scriptline):
            full_prefix, full_metric = match.groups()

            found_prefix = None
            if full_prefix:
                for prefix in list(Metric.Prefix.defined_prefixes_by_symbol.values()):
                    if prefix.name == full_prefix:
                        found_prefix = prefix
                        break
                if not found_prefix:
                    raise MeasurementParsingException("Could not find Metric Prefix '%s'." % found_prefix)

            found_metric = None
            for metric in list(Metric.defined_metrics_by_symbol.values()):
                if metric.name == full_metric:
                    found_metric = metric
                    break

            if not found_metric:
                raise MeasurementParsingException("Could not find Metric '%s'." % full_metric)

            if found_prefix:
                found_metric = found_prefix * found_metric

            scriptline = scriptline.replace(match.string[match.start():match.end()],
                                            found_metric.typographical_symbol)

        # preprocessing step three: match each occurrence of a Quantity
        for match in quantity_pattern.finditer(scriptline):
            quantity = Quantity.parse(match.string[match.start():match.end()])
            scriptline = scriptline.replace(match.string[match.start():match.end()], repr(quantity))

        # line preprocessing step three.a: convert " to <metric> " statements
        for match in conversion_pattern.finditer(scriptline):
            quantity_repr, to_metric_symbol = match.groups()[0:2]
            to_metric = Metric.parse(to_metric_symbol)
            scriptline = scriptline.replace(match.string[match.start():match.end()],
                                            "(" + quantity_repr + ").to(" + repr(to_metric) + ")")

        preparedlines.append(scriptline)

    # preprocessing step four: make the last line the return value
    preparedlines[-1] = "____return_value____ = (" + preparedlines[-1] + ")"

    # step five: execute as Python code
    safe_globals = {
                    # all builtins are turned off by default
                    "__builtins__" : None,

                    # the Dimension/Metric/Quantity classes, of course
                    "Dimension" : Dimension,
                    "Metric" : Metric,
                    "Quantity" : Quantity,

                    # some useful and safe built-ins
                    "set" : set,
                    "frozenset" : frozenset
                    }
    safe_locals = {}

    python_code = "\n".join(preparedlines)

    exec(python_code, safe_globals, safe_locals)

    # step six: evaluate the return value
    if "____return_value____" in safe_locals:
        return safe_locals["____return_value____"]
    else:
        return None
