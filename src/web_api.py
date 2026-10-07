from __future__ import annotations

from typing import Any, Dict, List
from urllib.parse import parse_qs

from src.trip_planner import build_trip_plan, compare_scenarios


def _interests(params: Dict[str, List[str]]) -> List[str]:
    interests = params.get('interests', ['culture,food'])
    return [item.strip() for item in interests[0].split(',') if item.strip()]


def trip_plan_from_query(query: str) -> Dict[str, Any]:
    params = parse_qs(query)
    return build_trip_plan(
        destination=params.get('destination', ['Rome'])[0],
        days=int(params.get('days', ['3'])[0]),
        budget=float(params.get('budget', ['1800'])[0]),
        travellers=int(params.get('travellers', ['2'])[0]),
        interests=_interests(params),
        pace=params.get('pace', ['balanced'])[0],
        weather=params.get('weather', ['sunny'])[0],
        scenario=params.get('scenario', ['comfort'])[0],
    )


def scenarios_from_query(query: str) -> List[Dict[str, Any]]:
    params = parse_qs(query)
    return compare_scenarios(
        destination=params.get('destination', ['Rome'])[0],
        budget=float(params.get('budget', ['1800'])[0]),
        days=int(params.get('days', ['3'])[0]),
        travellers=int(params.get('travellers', ['2'])[0]),
        interests=_interests(params),
        pace=params.get('pace', ['balanced'])[0],
        weather=params.get('weather', ['sunny'])[0],
    )
