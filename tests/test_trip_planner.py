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

    def test_build_trip_plan_includes_travel_score_and_insights(self):
        plan = build_trip_plan(
            destination='Prague',
            days=3,
            budget=1500,
            travellers=2,
            interests=['culture', 'food'],
            pace='balanced',
            weather='sunny',
            scenario='comfort',
        )

        self.assertIn('travel_score', plan)
        self.assertIn('insights', plan)
        self.assertGreaterEqual(plan['travel_score'], 0)
        self.assertLessEqual(plan['travel_score'], 100)
        self.assertGreater(len(plan['insights']), 0)

    def test_build_trip_plan_includes_packing_list(self):
        plan = build_trip_plan(
            destination='Barcelona',
            days=4,
            budget=2400,
            travellers=2,
            interests=['beach', 'food'],
            pace='relaxed',
            weather='sunny',
            scenario='premium',
        )

        self.assertIn('packing_list', plan)
        self.assertGreater(len(plan['packing_list']), 0)
        self.assertTrue(any('sunscreen' in item.lower() or 'water' in item.lower() for item in plan['packing_list']))

    def test_build_trip_plan_includes_best_time_to_visit(self):
        plan = build_trip_plan(
            destination='Rome',
            days=3,
            budget=1800,
            travellers=2,
            interests=['culture', 'food'],
            pace='balanced',
            weather='sunny',
            scenario='comfort',
        )

        self.assertIn('best_time_to_visit', plan)
        self.assertIn('month', plan['best_time_to_visit'])
        self.assertIn('reason', plan['best_time_to_visit'])

    def test_build_trip_plan_includes_budget_breakdown(self):
        plan = build_trip_plan(
            destination='Kyiv',
            days=4,
            budget=2200,
            travellers=2,
            interests=['culture', 'food'],
            pace='balanced',
            weather='rainy',
            scenario='comfort',
        )

        self.assertIn('budget_breakdown', plan)
        self.assertIn('total', plan['budget_breakdown'])
        self.assertIn('per_day', plan['budget_breakdown'])
        self.assertIn('categories', plan['budget_breakdown'])
        self.assertGreater(plan['budget_breakdown']['total'], 0)


if __name__ == '__main__':
    unittest.main()
