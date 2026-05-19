"""인터페이스 통합관리 관련 API 엔드포인트"""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/interfaces", tags=["interfaces"])

DB_PATH = Path(__file__).parent.parent / "data" / "mock_db.json"


@lru_cache(maxsize=1)
def _load_db() -> dict:
    with open(DB_PATH, encoding="utf-8") as f:
        return json.load(f)


@router.get("")
def list_interfaces():
    return _load_db()["interfaces"]


@router.get("/summary")
def interface_summary(month: Optional[str] = Query(default=None, example="2026-04")):
    db = _load_db()
    logs = db["traffic_logs"]
    if month:
        logs = [l for l in logs if l["date"].startswith(month)]

    summary: dict[str, dict] = {}
    for log in logs:
        iid = log["interface_id"]
        if iid not in summary:
            summary[iid] = {"interface_id": iid, "total_calls": 0, "total_errors": 0}
        summary[iid]["total_calls"] += log["call_count"]
        summary[iid]["total_errors"] += log["error_count"]

    iface_map = {i["id"]: i for i in db["interfaces"]}
    result = []
    for iid, stats in summary.items():
        info = iface_map.get(iid, {})
        total = stats["total_calls"] or 1
        result.append({
            **stats,
            "name": info.get("name", ""),
            "source": info.get("source", ""),
            "target": info.get("target", ""),
            "protocol": info.get("protocol", ""),
            "error_rate": round(stats["total_errors"] / total * 100, 2),
        })

    result.sort(key=lambda x: -x["total_calls"])
    return result


@router.get("/{interface_id}/traffic")
def interface_traffic(
    interface_id: str,
    month: Optional[str] = Query(default=None, example="2026-04"),
):
    db = _load_db()
    iface_ids = {i["id"] for i in db["interfaces"]}
    if interface_id not in iface_ids:
        raise HTTPException(status_code=404, detail="Interface not found")

    logs = [l for l in db["traffic_logs"] if l["interface_id"] == interface_id]
    if month:
        logs = [l for l in logs if l["date"].startswith(month)]

    logs.sort(key=lambda x: x["date"])
    return {"interface_id": interface_id, "records": logs}
