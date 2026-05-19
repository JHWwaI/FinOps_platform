"""원가/관리회계 관련 API 엔드포인트"""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Query

from services.cost_calculator import summarize_monthly

router = APIRouter(prefix="/api/costs", tags=["costs"])

DB_PATH = Path(__file__).parent.parent / "data" / "mock_db.json"


@lru_cache(maxsize=1)
def _load_db() -> dict:
    with open(DB_PATH, encoding="utf-8") as f:
        return json.load(f)


@router.get("")
def list_cost_allocations(month: Optional[str] = Query(default=None, example="2026-04")):
    allocations = _load_db()["cost_allocations"]
    if month:
        allocations = [a for a in allocations if a["month"] == month]
    return allocations


@router.get("/summary")
def cost_summary():
    return summarize_monthly(_load_db()["cost_allocations"])


@router.get("/monthly")
def monthly_cost_pools():
    return _load_db()["monthly_costs"]


@router.get("/projects")
def projects_cost(month: Optional[str] = Query(default=None, example="2026-04")):
    db = _load_db()
    allocations = db["cost_allocations"]
    if month:
        allocations = [a for a in allocations if a["month"] == month]

    aggregated: dict[str, dict] = {}
    for row in allocations:
        pid = row["project_id"]
        if pid not in aggregated:
            aggregated[pid] = {
                "project_id": pid,
                "project_name": row["project_name"],
                "department": row["department"],
                "total_allocated_cost": 0,
                "total_traffic": 0,
                "months": [],
            }
        aggregated[pid]["total_allocated_cost"] += row["allocated_cost"]
        aggregated[pid]["total_traffic"] += row["traffic_count"]
        aggregated[pid]["months"].append({
            "month": row["month"],
            "allocated_cost": row["allocated_cost"],
            "traffic_count": row["traffic_count"],
            "traffic_ratio": row["traffic_ratio"],
        })

    return sorted(aggregated.values(), key=lambda x: -x["total_allocated_cost"])
