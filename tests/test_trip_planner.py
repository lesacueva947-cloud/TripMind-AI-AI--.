import unittest

from src.trip_planner import build_trip_plan, compare_scenarios


class TripPlannerTest(unittest.TestCase):
    def test_build_trip_plan_has_day_by_day_itinerary(self):
        plan = build_trip_plan(
            destination='Rome',
            days=3,
            budget=1800,
            travellers=2,
            interests=['culture', 'food'],
            pace='balanced',
            weather='rainy',
            scenario='comfort',
        )

        self.assertEqual(len(plan['itinerary']), 3)
        self.assertIn('Rome', plan['summary'])
        self.assertRegex(plan['weather_note'], r'indoor|rain')
        self.assertGreaterEqual(len(plan['itinerary'][0]['activities']), 2)
        self.assertIn('Comfort', plan['scenario']['title'])

    def test_compare_scenarios_returns_three_budget_tiers(self):
        scenarios = compare_scenarios(
            destination='Lisbon',
            budget=2000,
            days=4,
            travellers=2,
            interests=['food'],
            pace='relaxed',
        )

        self.assertEqual(len(scenarios), 3)
        self.assertEqual([item['id'] for item in scenarios], ['econom', 'comfort', 'premium'])
        self.assertTrue(all(item['total_budget'] > 0 for item in scenarios))


if __name__ == '__main__':
    unittest.main()
