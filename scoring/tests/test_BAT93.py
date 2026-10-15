import unittest

from scoring.BAT93 import BAT93
import scoring.dictionary.BAT93 as dictionary


class BAT93AnswerTests(unittest.TestCase):
    def test_valid_options_keep_their_value(self):
        for option in range(1, 6):
            for value in (option, float(option), str(option)):
                with self.subTest(value=value):
                    answer = BAT93._answer({'user_answered': value}, 7)
                    self.assertEqual(answer, option)
                    self.assertIs(type(answer), int)

    def test_malformed_answers_are_rejected(self):
        invalid = (1.9, 5.9, 0.9, -1.9, '1.9', '5.9', True, False,
                   None, '', 'abc', [], {}, float('nan'),
                   float('inf'), float('-inf'), 0, 6, '0', '6')
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, 'BAT93 item 7'):
                    BAT93._answer({'user_answered': value}, 7)
        with self.assertRaises(ValueError):
            BAT93._answer({}, 7)

    def test_valid_questionnaire_scores_are_unchanged(self):
        expected_levels = dict(zip(dictionary.factors_names,
                                   (2, 1, 2, 2, 3, 2, 0, 0)))
        for value in (3, 3.0, '3'):
            data = BAT93({'items': [{'user_answered': value} for _ in range(33)]},
                         'object')
            result = data.scoring().toDict()
            self.assertEqual(result, {
                factor: {'raw': dictionary.counts[factor] * 3,
                         'score': 3.0, 'level': expected_levels[factor]}
                for factor in dictionary.factors_names
            })

    def test_fractional_answer_aborts_scoring_at_each_item(self):
        for index in range(33):
            with self.subTest(item=index + 1):
                items = [{'user_answered': '3'} for _ in range(33)]
                items[index]['user_answered'] = 1.9
                data = BAT93({'items': items}, 'object')
                with self.assertRaisesRegex(ValueError,
                                            'BAT93 item {} '.format(index + 1)):
                    data.scoring()
                self.assertEqual(data.score.toDict(), {})

    def test_rounding_and_classification_still_use_two_decimals(self):
        self.assertEqual(BAT93._mean(25, 8), 3.13)
        for factor, (green, orange) in dictionary.cutoffs.items():
            for value, level in ((round(green - 0.01, 2), 1), (green, 1),
                                 (round(green + 0.01, 2), 2),
                                 (round(orange - 0.01, 2), 2), (orange, 2),
                                 (round(orange + 0.01, 2), 3)):
                with self.subTest(factor=factor, mean=value):
                    self.assertEqual(BAT93._level(value, (green, orange)), level)


if __name__ == '__main__':
    unittest.main()
