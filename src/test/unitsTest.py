from diethack._units import makeConverter
import unittest

converter = makeConverter()
convert = converter.convert
convertDict = converter.convertDict

class TestConvert(unittest.TestCase):
    def testNoUnit(self):
        self.assertEqual(convert(123, None, None), 123)
        self.assertEqual(convert(123, 'foo', None), 123)
        self.assertEqual(convert(123, None, 'foo'), 123)
    def testSameUnit(self):
        self.assertEqual(convert(123, 'foo', 'foo'), 123)
    def testUnknownUnit(self):
        self.assertRaises(Exception, convert, 123, 'foo', 'bar')
    def testRatio(self):
        self.assertAlmostEqual(convert(123, 'g', 'mg'), 123000)
        self.assertAlmostEqual(convert(123, 'mg', 'g'), 0.123)
        self.assertAlmostEqual(convert(123, 'g', 'mcg'), 123000000)
        self.assertAlmostEqual(convert(123, 'mcg', 'g'), 0.000123)
        self.assertAlmostEqual(convert(123, 'ng', 'mg'), 0.000123)

class TestConvertDict(unittest.TestCase):
    def testArbitraryType(self):
        self.assertEqual(convertDict(
            {'foo': 'bar'},
            {'foo': 'bar'}),
            {'foo': 'bar'})
    def testConvert(self):
        self.assertEqual(convertDict(
            {'x': (1000, 'mg')},
            {'x': 'g'}),
            {'x': 1})
        self.assertEqual(convertDict(
            {'x': ([1000, 2000, 3000], 'mg')},
            {'x': 'g'}),
            {'x': [1, 2, 3]})
    def testRecurse(self):
        self.assertEqual(convertDict(
            {'x': {'y': (1000, 'mg')}},
            {'x': {'y': 'g'}}),
            {'x': {'y': 1}})
