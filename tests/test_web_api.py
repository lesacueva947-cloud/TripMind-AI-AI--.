import unittest

from src.trip_planner import build_trip_plan, compare_scenarios
from src.web_api import scenarios_from_query, trip_plan_from_query


class WebApiTest(unittest.TestCase):
    def test_trip_plan_from_query_parses_form_values(self):
        plan = trip_plan_from_query(
            'destination=Barcelona&days=4&budget=2400&travellers=3'
            '&pace=fast&weather=sunny&scenario=premium&interests=beach%2C+food'
        )

        expected = build_trip_plan(
            destination='Barcelona',
            days=4,
            budget=2400.0,
            travellers=3,
            interests=['beach', 'food'],
            pace='fast',
            weather='sunny',
            scenario='premium',
        )
        self.assertEqual(plan, expected)

    def test_trip_plan_from_empty_query_uses_defaults(self):
        plan = trip_plan_from_query('')

        self.assertEqual(plan['destination'], 'Rome')
        self.assertEqual(len(plan['itinerary']), 3)
        self.assertEqual(plan['scenario']['id'], 'comfort')

    def test_scenarios_from_query_returns_three_tiers(self):
        scenarios = scenarios_from_query('destination=Lisbon&budget=2000&days=4&travellers=2&interests=food')

        self.assertEqual(scenarios, compare_scenarios(
            destination='Lisbon',
            budget=2000.0,
            days=4,
            travellers=2,
            interests=['food'],
        ))


if __name__ == '__main__':
    unittest.main()
