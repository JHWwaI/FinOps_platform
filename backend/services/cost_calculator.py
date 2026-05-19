"""트래픽 기반 원가 배분 핵심 계산 로직"""
from __future__ import annotations
from typing import Any


def calculate_allocation(
    total_cost: int,
    project_traffic: dict[str, int],
) -> dict[str, dict[str, Any]]:
    """
    트래픽 비율에 따라 총 원가를 프로젝트별로 배분한다.
    부동소수점 오차는 가장 큰 프로젝트에 흡수시킨다.
    """
    total_traffic = sum(project_traffic.values()) or 1
    result: dict[str, dict[str, Any]] = {}
    allocated_sum = 0

    sorted_projects = sorted(project_traffic.items(), key=lambda x: -x[1])

    for i, (prj_id, traffic) in enumerate(sorted_projects):
        ratio = traffic / total_traffic
        if i < len(sorted_projects) - 1:
            cost = int(total_cost * ratio)
        else:
            cost = total_cost - allocated_sum

        allocated_sum += cost
        result[prj_id] = {
            "traffic_count": traffic,
            "traffic_ratio": round(ratio, 6),
            "allocated_cost": cost,
        }

    return result


def summarize_monthly(cost_allocations: list[dict]) -> list[dict]:
    """월별 원가 배분 데이터를 집계하여 월별 요약 리스트로 반환한다."""
    monthly: dict[str, dict] = {}
    for row in cost_allocations:
        m = row["month"]
        if m not in monthly:
            monthly[m] = {
                "month": m,
                "total_cost_pool": row["total_cost_pool"],
                "projects": [],
            }
        monthly[m]["projects"].append({
            "project_id": row["project_id"],
            "project_name": row["project_name"],
            "department": row["department"],
            "traffic_count": row["traffic_count"],
            "traffic_ratio": row["traffic_ratio"],
            "allocated_cost": row["allocated_cost"],
        })
    return sorted(monthly.values(), key=lambda x: x["month"])
