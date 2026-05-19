from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import random
from datetime import datetime, timedelta
import io
import csv
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# [Phase 1] IT 인프라 활동기준원가(ABC) 모델
# ==========================================
INFRA_ASSETS = {
    "PRJ-101": {"direct_cost": 2500000, "amortized_hw_cost": 450000},
    "PRJ-102": {"direct_cost": 1800000, "amortized_hw_cost": 320000},
    "PRJ-103": {"direct_cost": 3200000, "amortized_hw_cost": 800000},
}
SHARED_OVERHEAD_COST = 5000000 

DEPARTMENT_MAPPING = {
    "PRJ-101": "리테일금융본부",
    "PRJ-102": "디지털혁신본부",
    "PRJ-103": "글로벌사업본부"
}

global_traffic_logs = []

@app.get("/api/interface-logs")
def get_interface_logs():
    global global_traffic_logs
    logs = []
    
    for i in range(20):
        project = random.choice(list(INFRA_ASSETS.keys()))
        is_fail = random.random() < 0.05
        logs.append({
            "trace_id": f"req-{random.randint(100000, 999999)}",
            "timestamp": (datetime.now() - timedelta(seconds=i*2)).strftime("%H:%M:%S"),
            "service_endpoint": f"/api/v1/{project.lower()}/data",
            "project_code": project,
            "status_code": 500 if is_fail else 200,
            "latency_ms": random.randint(800, 3000) if is_fail else random.randint(45, 120),
            "payload_bytes": random.randint(1024, 51200)
        })
    
    global_traffic_logs.extend(logs)
    global_traffic_logs = global_traffic_logs[-200:]
    return logs

def calculate_enterprise_cost():
    global global_traffic_logs
    if not global_traffic_logs:
        return []

    project_traffic_count = {prj: 0 for prj in INFRA_ASSETS.keys()}
    total_traffic = 0
    
    for log in global_traffic_logs:
        if log["status_code"] == 200:
            project_traffic_count[log["project_code"]] += 1
            total_traffic += 1

    allocation_results = []
    # ⭐️ 원가 계산 시 다이내믹한 노이즈(변동성) 추가
    dynamic_shared = SHARED_OVERHEAD_COST + random.randint(-50, 50) * 1000
    
    for project, asset in INFRA_ASSETS.items():
        traffic_share = project_traffic_count[project] / total_traffic if total_traffic > 0 else 0
        allocated_shared_cost = dynamic_shared * traffic_share
        
        dynamic_direct = asset["direct_cost"] + random.randint(-10, 10) * 1000
        dynamic_amort = asset["amortized_hw_cost"] + random.randint(-5, 5) * 1000
        
        total_project_cost = dynamic_direct + dynamic_amort + allocated_shared_cost
        
        allocation_results.append({
            "project_code": project,
            "department": DEPARTMENT_MAPPING[project],
            "traffic_share_pct": round(traffic_share * 100, 2),
            "breakdown": {
                "direct_infra_cost": dynamic_direct,
                "amortized_cost": dynamic_amort,
                "allocated_shared_cost": round(allocated_shared_cost)
            },
            "total_allocated_cost": round(total_project_cost)
        })
    return allocation_results

@app.get("/api/cost-allocation")
def get_cost_allocation():
    return calculate_enterprise_cost()

@app.get("/api/download/costs")
def download_costs_csv():
    data = calculate_enterprise_cost()
    stream = io.StringIO()
    # 엑셀에서 한글이 깨지지 않도록 유니코드 시그니처(BOM)를 수동으로 삽입하는 대신
    # 응답 시 인코딩을 utf-8-sig로 처리하도록 변경합니다.
    writer = csv.writer(stream)
    
    # 헤더 작성 (한글 필드명으로 변경하면 더 직관적입니다)
    writer.writerow(["프로젝트 코드", "담당 부서", "트래픽 점유율(%)", "직접비", "감가상각비", "공통비 배분액", "최종 할당 원가"])
    
    for item in data:
        writer.writerow([
            item["project_code"],
            item["department"],
            item["traffic_share_pct"],
            item["breakdown"]["direct_infra_cost"],
            item["breakdown"]["amortized_cost"],
            item["breakdown"]["allocated_shared_cost"],
            item["total_allocated_cost"]
        ])
    
    # ⭐️ 핵심: 인코딩을 utf-8-sig로 변환하여 엑셀이 한글을 인식하게 함
    content = stream.getvalue().encode("utf-8-sig") 
    
    return StreamingResponse(
        io.BytesIO(content), 
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=cost_allocation_report.csv"}
    )

# ==========================================
# [Phase 2] SPC 회계 및 재무제표 파이프라인
# ==========================================
SPC_JOURNAL_ENTRIES = [
    {"id": 1, "date": "2026-04-01 09:00:00", "desc": "펀드 설정 및 출자금 납입", "account": "현금", "type": "자산", "debit": 10000, "credit": 0},
    {"id": 2, "date": "2026-04-01 09:00:00", "desc": "펀드 설정 및 출자금 납입", "account": "자본금", "type": "자본", "debit": 0, "credit": 10000},
    {"id": 3, "date": "2026-04-05 10:30:00", "desc": "선박 매입용 은행 차입", "account": "현금", "type": "자산", "debit": 50000, "credit": 0},
    {"id": 4, "date": "2026-04-05 10:30:00", "desc": "선박 매입용 은행 차입", "account": "장기차입금", "type": "부채", "debit": 0, "credit": 50000},
    {"id": 5, "date": "2026-04-10 14:00:00", "desc": "초대형 유조선(VLCC) 매입", "account": "선박자산", "type": "자산", "debit": 60000, "credit": 0},
    {"id": 6, "date": "2026-04-10 14:00:00", "desc": "초대형 유조선(VLCC) 매입", "account": "현금", "type": "자산", "debit": 0, "credit": 60000},
]

last_spc_update = time.time()

def update_spc_dynamics():
    """시간이 지남에 따라 실시간으로 선박 용선료(수익)가 분개장에 누적되는 함수"""
    global last_spc_update
    now = time.time()
    
    # 3초마다 수익금 분개 생성 (역동적인 화면 연출)
    if now - last_spc_update > 3:
        new_id = len(SPC_JOURNAL_ENTRIES) + 1
        daily_revenue = random.randint(15, 60)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 차변(자산 증가), 대변(수익 발생) 분개 동시 입력
        SPC_JOURNAL_ENTRIES.append({"id": new_id, "date": now_str, "desc": "실시간 용선료 수익 누적", "account": "현금", "type": "자산", "debit": daily_revenue, "credit": 0})
        SPC_JOURNAL_ENTRIES.append({"id": new_id+1, "date": now_str, "desc": "실시간 용선료 수익 누적", "account": "임대수익", "type": "수익", "debit": 0, "credit": daily_revenue})
        last_spc_update = now

@app.get("/api/spc/journal")
def get_spc_journal():
    update_spc_dynamics() # 호출 시 실시간 분개 업데이트
    # 최신 분개 20건만 리턴 (화면 렌더링용)
    return sorted(SPC_JOURNAL_ENTRIES, key=lambda x: x["id"], reverse=True)[:20]

@app.get("/api/spc/statements")
def get_spc_financial_statements():
    update_spc_dynamics() # 호출 시 실시간 분개 업데이트
    ledger = {"자산": 0, "부채": 0, "자본": 0, "수익": 0, "비용": 0}
    
    # 누적된 모든 분개를 대차 원리에 따라 원장(Ledger) 집계
    for entry in SPC_JOURNAL_ENTRIES:
        if entry["type"] in ["자산", "비용"]:
            ledger[entry["type"]] += (entry["debit"] - entry["credit"])
        elif entry["type"] in ["부채", "자본", "수익"]:
            ledger[entry["type"]] += (entry["credit"] - entry["debit"])

    net_income = ledger["수익"] - ledger["비용"]
    
    return {
        "balance_sheet": {
            "assets": ledger["자산"],
            "liabilities": ledger["부채"],
            "equity": ledger["자본"],
            "retained_earnings": net_income, 
            "total_liabilities_equity": ledger["부채"] + ledger["자본"] + net_income 
        },
        "income_statement": {
            "revenue": ledger["수익"],
            "expenses": ledger["비용"],
            "net_income": net_income
        }
    }