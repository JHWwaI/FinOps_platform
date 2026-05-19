"""
더미 데이터 생성 스크립트
실행: python mock_generator.py
결과: mock_db.json 파일 생성
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

INTERFACES = [
    {"id": "IF-001", "name": "ERP→SCM 발주연동", "source": "ERP", "target": "SCM", "protocol": "REST"},
    {"id": "IF-002", "name": "ERP→HR 인사연동", "source": "ERP", "target": "HR", "protocol": "SOAP"},
    {"id": "IF-003", "name": "SCM→WMS 입출고연동", "source": "SCM", "target": "WMS", "protocol": "REST"},
    {"id": "IF-004", "name": "HR→ERP 급여연동", "source": "HR", "target": "ERP", "protocol": "REST"},
    {"id": "IF-005", "name": "WMS→ERP 재고연동", "source": "WMS", "target": "ERP", "protocol": "MQ"},
    {"id": "IF-006", "name": "ERP→외부결제 결제연동", "source": "ERP", "target": "PG", "protocol": "REST"},
    {"id": "IF-007", "name": "CRM→ERP 수주연동", "source": "CRM", "target": "ERP", "protocol": "REST"},
    {"id": "IF-008", "name": "ERP→BIS 경영정보연동", "source": "ERP", "target": "BIS", "protocol": "DB"},
]

PROJECTS = [
    {"id": "PRJ-001", "name": "ERP 고도화", "department": "IT기획팀"},
    {"id": "PRJ-002", "name": "SCM 최적화", "department": "공급망팀"},
    {"id": "PRJ-003", "name": "HR 디지털전환", "department": "인사팀"},
    {"id": "PRJ-004", "name": "WMS 구축", "department": "물류팀"},
    {"id": "PRJ-005", "name": "CRM 고도화", "department": "영업팀"},
]

PROJECT_INTERFACE_MAP = {
    "PRJ-001": ["IF-001", "IF-002", "IF-004", "IF-005", "IF-006", "IF-007", "IF-008"],
    "PRJ-002": ["IF-001", "IF-003"],
    "PRJ-003": ["IF-002", "IF-004"],
    "PRJ-004": ["IF-003", "IF-005"],
    "PRJ-005": ["IF-007"],
}

MONTHLY_COSTS = {
    "2026-01": 12_500_000,
    "2026-02": 11_800_000,
    "2026-03": 13_200_000,
    "2026-04": 12_900_000,
}


def generate_daily_traffic(interface_id: str, year_month: str) -> list[dict]:
    random.seed(hash(interface_id + year_month))
    year, month = map(int, year_month.split("-"))
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

    base_traffic = random.randint(500, 8000)
    records = []
    current = start
    while current < end:
        is_weekend = current.weekday() >= 5
        multiplier = random.uniform(0.1, 0.4) if is_weekend else random.uniform(0.7, 1.4)
        count = max(0, int(base_traffic * multiplier + random.gauss(0, base_traffic * 0.05)))
        error_count = int(count * random.uniform(0, 0.02))
        records.append({
            "date": current.isoformat(),
            "interface_id": interface_id,
            "call_count": count,
            "error_count": error_count,
            "avg_response_ms": int(random.uniform(50, 800)),
        })
        current += timedelta(days=1)
    return records


def generate_mock_db() -> dict:
    traffic_logs: list[dict] = []
    months = list(MONTHLY_COSTS.keys())

    for iface in INTERFACES:
        for month in months:
            traffic_logs.extend(generate_daily_traffic(iface["id"], month))

    monthly_traffic_totals: dict[str, dict[str, int]] = {}
    for log in traffic_logs:
        ym = log["date"][:7]
        iid = log["interface_id"]
        monthly_traffic_totals.setdefault(ym, {}).setdefault(iid, 0)
        monthly_traffic_totals[ym][iid] += log["call_count"]

    cost_allocations = []
    for month, total_cost in MONTHLY_COSTS.items():
        traffic_by_if = monthly_traffic_totals.get(month, {})

        for prj in PROJECTS:
            prj_interfaces = PROJECT_INTERFACE_MAP.get(prj["id"], [])
            prj_traffic = sum(traffic_by_if.get(iid, 0) for iid in prj_interfaces)

            all_traffic = sum(traffic_by_if.values()) or 1
            ratio = round(prj_traffic / all_traffic, 6)
            allocated_cost = int(total_cost * ratio)

            cost_allocations.append({
                "month": month,
                "project_id": prj["id"],
                "project_name": prj["name"],
                "department": prj["department"],
                "traffic_count": prj_traffic,
                "traffic_ratio": ratio,
                "allocated_cost": allocated_cost,
                "total_cost_pool": total_cost,
            })

    return {
        "interfaces": INTERFACES,
        "projects": PROJECTS,
        "traffic_logs": traffic_logs,
        "cost_allocations": cost_allocations,
        "monthly_costs": [{"month": k, "total": v} for k, v in MONTHLY_COSTS.items()],
    }


if __name__ == "__main__":
    db = generate_mock_db()
    out_path = Path(__file__).parent / "mock_db.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"mock_db.json generated: {len(db['traffic_logs'])} traffic records")
