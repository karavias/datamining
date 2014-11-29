
import unittest

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from dm_lib import * 
import youflask

class UnitTesting(unittest.TestCase):

    def test_tokenizeComm(self):
        self.assertEqual(tokenize_comment("I want to sleep"), ["i","want","to","sleep"])

    def test_lemm(self):
        self.assertEqual(lemmatize([["cars"],["loves","child"]]), [["car"],["lov","child"]])  

    def test_cleanStopWords(self):
        self.assertEqual(clean_stop_words([['the','car','is','under', 'the', 'water']]), [['car','water']]) 

    def test_calculateScore(self):
        rate=read_sentiment_dictionary()
        self.assertEqual(calculate_score([['happiness','sad','day']],rate),(3.0462962962962963, [3.0462962962962963]))


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = youflask.APP_.test_client()

    def tearDown(self):
        pass
    
    def test_search_form(self):
        rv=self.app.get('/')
        assert '<form method="post" action="/search">' in rv.data
        assert '<input name="videoUrl" type="text"/>' in rv.data
        assert '<form method="post" action="/channel">' in rv.data
        assert '<input name="channelName" type="text"/>' in rv.data
    
    def test_channel_results(self):
        channelName = "nigahiga"
        rv=self.app.post('/channel',data=dict(
            channelName=channelName))
        assert ('<h1>' + channelName.upper() + ' Analytics</h1>') in rv.data
        assert '<table border="1" class="dataframe">' in rv.data


#integrational Tests

#functional Tests
