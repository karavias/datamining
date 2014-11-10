
import unittest
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises


'''
-lemm removed and 
'''

'''
class Test(object):
    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""

    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""

    def setUp(self):
        """This method is run once before _each_ test method is executed"""

    def teardown(self):
        """This method is run once after _each_ test method is executed"""       

    def test_tokenizeComm(self):
        assert_equal(tokenizeComment("I want to sleep"), ["I","want","to","sleep"])


    @raises(KeyError)
    def test_raise_exc_with_decorator(self):
 '''
import unittest
from pyramid import testing

#unit Tests
class UnitTesting(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

#nadd on unicode stuff
    def test_tokenizeComm(self):
        from youtest import tokenizeComment
        self.assertEqual(tokenizeComment("I want to sleep"), ["i","want","to","sleep"])

    def test_lemm(self):
        from youtest import lemmatize
        # write more examples of words that should be lammatized
        self.assertEqual(lemmatize([["cars"],["loves","child"]]), [["car"],["love","child"]])  

    def test_cleanStopWords(self):
        from youtest import cleanStopWords
        self.assertEqual(cleanStopWords([['the','car','is','under', 'the', 'water']]), [['car','water']]) 

    def test_calculateScore(self):
        from youtest import calculateScore
        from youtest import read_sentiment_dictionary
        rate=read_sentiment_dictionary()
       
        self.assertEqual(calculateScore(['happy','sad','day'],rate), 5.34)




#integrational Tests

#functional Tests