import unittest

from shingle import canonize, get_shingles, get_texts_similarity, \
    get_shingles_similarity


class TestShingle(unittest.TestCase):

    def test_canonize(self):
        self.assertEqual(canonize('Це як ові@? фшо "!! шцойщ що; цй він.'),
                         ['ові@', 'фшо', 'шцойщ', 'цй'])

        self.assertEqual(canonize('Це ddd як ові@? фш.'),
                         ['ddd', 'ові@', 'фш'])

    def test_get_shingles(self):
        words = ['a' for i in range(0, 12)] + ['b', 'b']
        shingles = get_shingles(words)
        self.assertEqual(len(shingles), 5)
        self.assertEqual(shingles[0], shingles[1])
        self.assertNotEqual(shingles[0], shingles[-1])

    def test_get_shingles_similarity(self):
        words1 = ['a' for i in range(0, 12)] + ['b', 'b']
        words2 = ['b', 'b'] + ['a' for i in range(0, 12)]
        shingles1 = get_shingles(words1)
        shingles2 = get_shingles(words2)

        self.assertGreater(get_shingles_similarity(shingles1, shingles2), 0)
        self.assertEqual(get_shingles_similarity(shingles1, shingles1), 1)

    def test_get_texts_similarity(self):
        str1 = "Десять негритят отправились обедать " \
               "один поперхнулся и их осталось девять"
        str2 = "Девять негритят поев клевали носом" \
               " один не смог пронуться и их осталось восемь"
        str3 = "Восемь негритят в девон ушли потом " \
               "один не возвратился остались всесером"

        self.assertLess(get_texts_similarity(str1, str2),
                        get_texts_similarity(str2, str2))

        self.assertLess(get_texts_similarity('. '.join(
            (str1, str2, str3)), str2),
                        get_texts_similarity(
                            '. '.join((str1, str2, str3, str2)), str2))

if __name__ == "__main__":
    unittest.main()
