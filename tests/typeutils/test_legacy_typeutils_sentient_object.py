import unittest

from ccptools.legacyapi.typeutils import sentience


class SentientObjectTest(unittest.TestCase):
    def testComparisons(self):
        class SentientClass(sentience.SentientObject):
            def foo(self):
                pass

            @sentience.SentientObject.sentient()
            def footoo(self):
                pass

            @sentience.SentientObject.sentient(bar=42, bartoo=[2,4])
            def foothree(self):
                pass


        class SentientSubClass(SentientClass):
            def bar(self):
                pass

            @sentience.SentientObject.sentient(e='mc2')
            def bar2(self):
                pass

        class SentientOtherSubClass(SentientClass):
            @sentience.SentientObject.sentient()
            def bar(self):
                pass

            @sentience.SentientObject.sentient(e='magic pill')
            def bar2(self):
                pass

        sentient_object = SentientClass()
        sentient_methods = sentient_object.sentient_methods()
        self.assertIsInstance(sentient_methods, dict)
        self.assertEqual(len(sentient_methods), 2)

        self.assertIn('footoo', sentient_methods)
        self.assertEqual(len(sentient_methods['footoo']), 0)

        self.assertIn('foothree', sentient_methods)
        self.assertEqual(len(sentient_methods['foothree']), 2)

        self.assertIn('bar', sentient_methods['foothree'])
        self.assertIn('bartoo', sentient_methods['foothree'])
        self.assertEqual(len(sentient_methods['foothree']['bartoo']), 2)
        self.assertIn(2, sentient_methods['foothree']['bartoo'])
        self.assertIn(4, sentient_methods['foothree']['bartoo'])

        sentient_sub_object = SentientSubClass()
        sentient_methods = sentient_sub_object.sentient_methods()
        self.assertIsInstance(sentient_methods, dict)
        self.assertEqual(len(sentient_methods), 3)

        self.assertIn('footoo', sentient_methods)
        self.assertEqual(len(sentient_methods['footoo']), 0)

        self.assertIn('foothree', sentient_methods)
        self.assertEqual(len(sentient_methods['foothree']), 2)

        self.assertIn('bar', sentient_methods['foothree'])
        self.assertIn('bartoo', sentient_methods['foothree'])
        self.assertEqual(len(sentient_methods['foothree']['bartoo']), 2)
        self.assertIn(2, sentient_methods['foothree']['bartoo'])
        self.assertIn(4, sentient_methods['foothree']['bartoo'])

        self.assertIn('bar2', sentient_methods)
        self.assertEqual(len(sentient_methods['bar2']), 1)
        self.assertIn('e', sentient_methods['bar2'])
        self.assertEqual(sentient_methods['bar2']['e'], 'mc2')
