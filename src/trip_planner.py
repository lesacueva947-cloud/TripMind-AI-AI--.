from __future__ import annotations

from typing import Any, Dict, List

INTEREST_LIBRARY = {
    'culture': {
        'default': 'Old town walk and local history route',
        'rainy': 'Museum circuit and covered heritage quarter'
    },
    'food': {
        'default': 'Street-food tastings and market lunch',
        'rainy': 'Covered market tasting and chef-led workshop'
    },
    'nature': {
        'default': 'Scenic walk and viewpoint stop',
        'rainy': 'Botanical garden and indoor lookout terrace'
    },
    'adventure': {
        'default': 'Bike route and active sightseeing',
        'rainy': 'Indoor climbing and craft workshop'
    },
    'beach': {
        'default': 'Seafront walk and beach club',
        'rainy': 'Spa afternoon and seaside café'
    },
    'nightlife': {
        'default': 'Sunset rooftop and live music',
        'rainy': 'Jazz bar and cocktail lounge'
    },
    'family': {
        'default': 'Park and interactive city loop',
        'rainy': 'Science museum and family game café'
    },
}

SCENARIOS = {
    'econom': {
        'title': 'Econom Scenario',
        'description': 'Smart-value route with local stays and free walking highlights.',
        'multiplier': 0.72,
        'stay': 'guesthouse or local hostel',
    },
    'comfort': {
        'title': 'Comfort Scenario',
        'description': 'Balanced mix of quality stays, flexible stops and extra comfort.',
        'multiplier': 1.0,
        'stay': 'mid-range boutique hotel',
    },
    'premium': {
        'title': 'Premium Scenario',
        'description': 'Top-tier experiences, curated dining and premium transfers.',
        'multiplier': 1.45,
        'stay': '4-star or luxury hotel',
    },
}


def _normalize_interests(interests: List[str] | None) -> List[str]:
    if not interests:
        return ['culture', 'food']

    normalized = []
    for interest in interests:
        value = str(interest).strip().lower()
        if value:
            normalized.append(value)

    if not normalized:
        return ['culture', 'food']

    return normalized[:4]


def _weather_note(weather: str | None) -> str:
    weather_value = (weather or 'sunny').lower()
    if weather_value in {'rainy', 'stormy', 'windy', 'cloudy'}:
        return 'Rain-aware route: keep the plan indoor-first and swap open-air stops for museums, food halls and covered attractions.'
    return 'Weather-friendly route: keep outdoor walks, viewpoints and city promenade moments in the plan.'


def _resolve_activity(interest: str, weather: str | None) -> str:
    weather_key = 'rainy' if (weather or 'sunny').lower() in {'rainy', 'stormy', 'windy', 'cloudy'} else 'default'
    return INTEREST_LIBRARY.get(interest, INTEREST_LIBRARY['culture']).get(weather_key, 'Old town walk and local history route')


def _route_points(destination: str, interests: List[str]) -> List[str]:
    primary = interests[0] if interests else 'culture'
    area_map = {
        'culture': ['Historic center', 'Art district', 'Old town'],
        'food': ['Market quarter', 'Local dining lane', 'Street-food route'],
        'nature': ['Riverside trail', 'Nature reserve', 'Viewpoint park'],
        'adventure': ['Active district', 'Outdoor loop', 'Rooftop viewpoint'],
        'beach': ['Coastal promenade', 'Harbor line', 'Beach club'],
        'nightlife': ['Rooftop zone', 'Live music district', 'Late-night lane'],
        'family': ['Park zone', 'Interactive museum', 'Kid-friendly square'],
    }
    base = area_map.get(primary, ['Historic center', 'Market quarter', 'Viewpoint route'])
    return [f"{destination}: {point}" for point in base]


def _travel_score(destination: str, days: int, budget: float, travellers: int, interests: List[str], pace: str, weather: str, scenario: str) -> int:
    weather_value = (weather or 'sunny').lower()
    pace_value = (pace or 'balanced').lower()
    scenario_value = (scenario or 'comfort').lower()

    score = 55
    score += min(20, len(interests) * 7)
    score += {'relaxed': 12, 'balanced': 8, 'fast': 4}.get(pace_value, 8)
    score += {'econom': 6, 'comfort': 10, 'premium': 12}.get(scenario_value, 10)

    daily_budget = (float(budget or 1800) / max(1, int(days or 3)))
    score += min(12, int(daily_budget / 150))

    if travellers > 3:
        score -= 8
    if weather_value in {'rainy', 'stormy', 'windy', 'cloudy'}:
        score -= 10
    if destination and len(destination) > 10:
        score += 2

    return max(0, min(100, round(score)))


def _build_insights(destination: str, days: int, budget: float, travellers: int, interests: List[str], pace: str, weather: str, scenario: str) -> List[str]:
    interest_text = ', '.join(interests)
    daily_budget = round((float(budget or 1800) / max(1, int(days or 3))), 2)
    weather_value = (weather or 'sunny').lower()
    scenario_key = (scenario or 'comfort').lower()
    suggestion = 'Keep one flexible block each day for spontaneous stops.'

    if weather_value in {'rainy', 'stormy', 'windy', 'cloudy'}:
        suggestion = 'Prioritize indoor culture and food stops, and shift outdoor walks to the clearest hours.'

    return [
        f"{destination} fits a {pace} pace well for {travellers} traveller(s) with a {days}-day structure.",
        f"Daily spend is about €{daily_budget:.2f}, which keeps the {SCENARIOS.get(scenario_key, SCENARIOS['comfort'])['title']} style realistic.",
        f"Best focus: {interest_text}. {suggestion}",
    ]


def _packing_list(destination: str, weather: str, interests: List[str], pace: str, travellers: int) -> List[str]:
    weather_value = (weather or 'sunny').lower()
    interest_set = {item.lower() for item in interests}
    items = ['passport', 'phone charger', 'wallet', 'comfortable walking shoes']

    if weather_value in {'rainy', 'stormy', 'windy', 'cloudy'}:
        items.extend(['compact umbrella', 'light rain jacket', 'waterproof shoes'])
    else:
        items.extend(['sunscreen', 'sunglasses', 'water bottle'])

    if 'beach' in interest_set:
        items.extend(['swimwear', 'beach towel'])
    if 'nature' in interest_set or 'adventure' in interest_set:
        items.extend(['daypack', 'light snack pouch'])
    if 'culture' in interest_set:
        items.append('camera or phone tripod')
    if 'food' in interest_set:
        items.append('small reusable tote bag')
    if travellers > 2:
        items.append('portable power bank for shared charging')
    if (pace or 'balanced').lower() == 'fast':
        items.append('quick-dry outfit')
    else:
        items.append('light layer for evening strolls')

    deduped = []
    seen = set()
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped


def _best_time_to_visit(destination: str, interests: List[str], weather: str) -> Dict[str, str]:
    interest_set = {item.lower() for item in interests}
    weather_value = (weather or 'sunny').lower()

    if 'beach' in interest_set:
        return {
            'month': 'May to September',
            'reason': 'Warm sea and long daylight hours are ideal for beach routes and outdoor evenings.'
        }
    if 'nature' in interest_set or 'adventure' in interest_set:
        return {
            'month': 'May to October',
            'reason': 'The best conditions for walking, hikes and scenic stops are mild and dry.'
        }
    if 'culture' in interest_set or 'food' in interest_set:
        return {
            'month': 'April to June or September to October',
            'reason': 'Comfortable temperatures and lighter crowds make city walks and food discovery more enjoyable.'
        }
    if weather_value in {'rainy', 'stormy', 'windy', 'cloudy'}:
        return {
            'month': 'Late spring to early autumn',
            'reason': 'The weather is typically more stable, which reduces disruption to outdoor plans.'
        }
    return {
        'month': 'May to June or September to October',
        'reason': f'{destination} is most enjoyable in shoulder season when daytime comfort and pricing are balanced.'
    }


def _budget_breakdown(total_budget: float, days: int, scenario: str) -> Dict[str, Any]:
    multiplier = SCENARIOS.get((scenario or 'comfort').lower(), SCENARIOS['comfort'])['multiplier']
    actual_total = round(float(total_budget or 1800) * multiplier, 2)
    per_day = round(actual_total / max(1, int(days or 3)), 2)
    categories = {
        'accommodation': round(actual_total * 0.4, 2),
        'food': round(actual_total * 0.25, 2),
        'activities': round(actual_total * 0.22, 2),
        'transport': round(actual_total * 0.13, 2),
    }
    return {
        'total': actual_total,
        'per_day': per_day,
        'categories': categories,
    }


def build_trip_plan(destination: str, days: int = 3, budget: float = 1800, travellers: int = 2, interests: List[str] | None = None, pace: str = 'balanced', weather: str = 'sunny', scenario: str = 'comfort') -> Dict[str, Any]:
    destination = destination or 'Roma'
    days_value = max(1, int(days or 3))
    interest_list = _normalize_interests(interests)
    selected_scenario = SCENARIOS.get(scenario.lower(), SCENARIOS['comfort'])
    trip_total = float(budget or 1800)
    daily_budget = round(trip_total / days_value, 2)
    travel_score = _travel_score(destination, days_value, trip_total, travellers, interest_list, pace, weather, scenario)
    insights = _build_insights(destination, days_value, trip_total, travellers, interest_list, pace, weather, scenario)
    best_time = _best_time_to_visit(destination, interest_list, weather)
    budget_breakdown = _budget_breakdown(trip_total, days_value, scenario)

    itinerary: List[Dict[str, Any]] = []
    for day in range(1, days_value + 1):
        activities = []
        for slot in ('Morning', 'Afternoon', 'Evening'):
            interest = interest_list[(day + len(slot)) % len(interest_list)]
            activity = _resolve_activity(interest, weather)
            activities.append(
                {
                    'slot': slot,
                    'interest': interest.title(),
                    'title': activity,
                    'budget_estimate': round(daily_budget * (0.28 if slot == 'Morning' else 0.42 if slot == 'Afternoon' else 0.3), 2),
                }
            )
        itinerary.append(
            {
                'day': day,
                'theme': f"{destination} day {day}",
                'activities': activities,
                'daily_budget': daily_budget,
            }
        )

    summary = (
        f"TripMind AI suggests a {days_value}-day plan in {destination} for {travellers} traveler(s) "
        f"with a {pace} pace, {', '.join(interest_list)} focus and a {selected_scenario['title']} budget."
    )

    return {
        'destination': destination,
        'summary': summary,
        'weather_note': _weather_note(weather),
        'travel_score': travel_score,
        'insights': insights,
        'packing_list': _packing_list(destination, weather, interest_list, pace, travellers),
        'best_time_to_visit': best_time,
        'budget_breakdown': budget_breakdown,
        'scenario': {
            'id': scenario.lower(),
            'title': selected_scenario['title'],
            'description': selected_scenario['description'],
            'stay': selected_scenario['stay'],
            'total_budget': round(trip_total * selected_scenario['multiplier'], 2),
        },
        'itinerary': itinerary,
        'map_points': _route_points(destination, interest_list),
        'ai_chat': {
            'prompt': f"I want a relaxing {pace} trip in {destination} with {', '.join(interest_list)} and a total budget around {trip_total}.",
            'answer': f"{destination} works well for a {pace} trip. I would structure the route around {', '.join(_route_points(destination, interest_list)[:2])} and keep the morning flexible for local experiences before a lighter evening plan. Overall route quality score: {travel_score}/100.",
        },
    }


def compare_scenarios(destination: str, budget: float, days: int, travellers: int, interests: List[str] | None = None, pace: str = 'balanced', weather: str = 'sunny') -> List[Dict[str, Any]]:
    interest_list = _normalize_interests(interests)
    base_budget = float(budget or 1800)
    rows = []
    for scenario_id, config in SCENARIOS.items():
        total_budget = round(base_budget * config['multiplier'], 2)
        rows.append(
            {
                'id': scenario_id,
                'title': config['title'],
                'description': config['description'],
                'stay': config['stay'],
                'total_budget': total_budget,
                'highlights': [
                    f"{days}-day route in {destination}",
                    f"{travellers} traveler(s)",
                    f"{pace} pace with {', '.join(interest_list)} focus",
                ],
            }
        )
    return rows
