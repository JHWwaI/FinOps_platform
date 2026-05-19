<template>
  <v-app :style="{ backgroundColor: '#F4F7FB' }">
    <v-progress-linear v-if="isFetching" indeterminate color="cyan-accent-3" height="4" absolute top z-index="9999"></v-progress-linear>

    <v-container v-if="!isLoggedIn" class="fill-height login-bg" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card class="pa-10 rounded-xl elevation-24 login-card">
            <div class="d-flex justify-center mb-6">
              <v-avatar color="indigo-darken-4" size="80">
                <v-icon size="40" color="white">mdi-finance</v-icon>
              </v-avatar>
            </div>
            <h1 class="text-h4 font-weight-black text-center mb-2" style="letter-spacing: -1px;">NOAH <span class="text-indigo-accent-4">FINOPS</span></h1>
            <p class="text-subtitle-2 text-grey-darken-1 text-center mb-8">IT 인프라 원가 및 SPC 통합 회계 관리 시스템</p>
            
            <v-text-field v-model="loginId" label="User ID" placeholder="admin 또는 viewer" variant="filled" rounded="lg" color="indigo" class="mb-2" @keyup.enter="handleLogin"></v-text-field>
            <v-text-field label="Password" type="password" variant="filled" rounded="lg" color="indigo" class="mb-6"></v-text-field>
            
            <v-btn block color="indigo-darken-4" size="x-large" rounded="xl" elevation="8" class="font-weight-bold" :loading="isFetching" @click="handleLogin">
              시스템 접속
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <template v-else>
      <v-navigation-drawer permanent color="#0A192F" theme="dark" width="280" elevation="10">
        <v-list-item class="pa-8 mb-4">
          <div class="d-flex align-center">
            <v-icon color="cyan-accent-3" class="mr-2" size="32">mdi-shield-check</v-icon>
            <v-list-item-title class="text-h5 font-weight-black text-uppercase">Noah Portal</v-list-item-title>
          </div>
          <v-chip size="x-small" color="cyan-accent-3" variant="outlined" class="mt-2 font-weight-bold">
            {{ userRole.toUpperCase() }} AUTHENTICATED
          </v-chip>
        </v-list-item>

        <v-divider class="mx-4 opacity-20"></v-divider>

        <v-list nav class="pa-4 mt-4 sidebar-list">
          <v-list-item prepend-icon="mdi-chart-bell-curve-cumulative" title="실시간 모니터링" @click="currentMenu = 'monitor'" :active="currentMenu === 'monitor'" active-color="cyan-accent-3" rounded="lg" class="mb-2"></v-list-item>
          <v-list-item prepend-icon="mdi-layers-triple" title="IT 자산 원가 분석" @click="currentMenu = 'cost'" :active="currentMenu === 'cost'" active-color="cyan-accent-3" rounded="lg" class="mb-2"></v-list-item>
          <v-list-item prepend-icon="mdi-file-chart-outline" title="SPC 회계/재무 관리" @click="currentMenu = 'spc'" :active="currentMenu === 'spc'" active-color="cyan-accent-3" rounded="lg" class="mb-2"></v-list-item>
          <v-list-item v-if="userRole === 'admin'" prepend-icon="mdi-cog-sync" title="보안 관리" @click="currentMenu = 'admin'" :active="currentMenu === 'admin'" active-color="orange" rounded="lg"></v-list-item>
        </v-list>

        <template v-slot:append>
          <div class="pa-6">
            <v-btn block variant="tonal" color="grey-lighten-1" size="small" prepend-icon="mdi-logout" class="rounded-lg" @click="handleLogout">SIGN OUT</v-btn>
          </div>
        </template>
      </v-navigation-drawer>

      <v-main>
        <v-container fluid class="pa-10">
          
          <v-row v-if="currentMenu !== 'admin'" class="mb-8">
            <v-col cols="12" md="3">
              <v-card class="pa-6 rounded-xl border-none shadow-sm" elevation="0">
                <div class="text-overline text-grey-darken-1">인프라 안정성</div>
                <div class="d-flex align-end">
                  <div class="text-h4 font-weight-black text-indigo-darken-4">{{ (100 - parseFloat(errorRate)).toFixed(2) }}%</div>
                  <v-icon color="success" size="24" class="ml-2 mb-1">mdi-arrow-up-bold</v-icon>
                </div>
                <v-progress-linear :model-value="100 - parseFloat(errorRate)" color="indigo" height="6" rounded class="mt-4"></v-progress-linear>
              </v-card>
            </v-col>
            <v-col cols="12" md="3">
              <v-card class="pa-6 rounded-xl border-none shadow-sm" elevation="0">
                <div class="text-overline text-grey-darken-1">평균 응답 속도</div>
                <div class="text-h4 font-weight-black text-cyan-darken-3">{{ avgResponseTime }} <span class="text-body-1">ms</span></div>
                <div class="text-caption text-success font-weight-bold mt-2">상태: 최적화됨</div>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <v-card class="pa-1 rounded-xl bg-indigo-darken-4 d-flex align-center overflow-hidden" theme="dark">
                <v-card-text class="d-flex align-center justify-space-between">
                  <div>
                    <div class="text-subtitle-2 font-weight-bold opacity-70">AI FINOPS INSIGHT</div>
                    <div class="text-body-2 mt-1">현재 트래픽 패턴 기반 비용 절감 기회 1건 탐지</div>
                  </div>
                  <v-btn color="cyan-accent-3" variant="flat" size="large" rounded="lg" prepend-icon="mdi-robot-vacuum-variant" class="text-black font-weight-bold ml-4" :loading="aiLoading" @click="runSmartAnalysis">분석 시작</v-btn>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-window v-model="currentMenu">
            <v-window-item value="monitor">
              <div class="d-flex justify-space-between align-center mb-4">
                <h2 class="text-h5 font-weight-black"><v-icon class="mr-2">mdi-pulse</v-icon> 실시간 인터페이스 관제</h2>
                <v-chip color="indigo" variant="flat" size="small">LIVE UPDATE</v-chip>
              </div>
              <MonitorTable :logs="logs" :userRole="userRole" />
            </v-window-item>
            
            <v-window-item value="cost">
              <div class="d-flex justify-space-between align-center mb-4">
                <h2 class="text-h5 font-weight-black"><v-icon class="mr-2">mdi-currency-usd</v-icon> IT 자산 원가 배분 현황</h2>
                <v-btn color="indigo" variant="outlined" rounded="lg" prepend-icon="mdi-file-excel" @click="downloadExcel">데이터 추출</v-btn>
              </div>
              <CostBoard :costs="costs" :chartData="chartData" :chartOptions="chartOptions" />
            </v-window-item>

            <v-window-item value="spc">
              <div class="d-flex justify-space-between align-center mb-4">
                <h2 class="text-h5 font-weight-black"><v-icon class="mr-2">mdi-bank-transfer</v-icon> SPC 펀드 회계 터미널</h2>
                <v-chip color="success" size="small" prepend-icon="mdi-check-decagram">대차 일치 검증 완료</v-chip>
              </div>
              <SpcBoard />
            </v-window-item>

            <v-window-item value="admin">
              <v-card class="pa-15 rounded-xl text-center border-none shadow-sm" elevation="0">
                <v-icon size="80" color="orange-lighten-2" class="mb-4 pulse-icon">mdi-shield-account</v-icon>
                <h2 class="text-h4 font-weight-black">시스템 관리자 모드</h2>
                <p class="text-subtitle-1 text-grey-darken-1 mt-2">보안 설정 및 권한 제어 엔진이 활성화되었습니다.</p>
              </v-card>
            </v-window-item>
          </v-window>
        </v-container>

        <v-dialog v-model="aiDialog" max-width="650">
          <v-card class="rounded-xl overflow-hidden shadow-24">
            <v-toolbar color="#0A192F" theme="dark" class="px-6">
              <v-icon color="cyan-accent-3" class="mr-2">mdi-brain</v-icon>
              <v-toolbar-title class="font-weight-black">AI FinOps Strategy Report</v-toolbar-title>
            </v-toolbar>
            <v-card-text class="pa-8">
              <div v-if="aiAnalysis">
                <div class="text-h5 font-weight-bold text-indigo-darken-4 mb-3">{{ aiAnalysis.title }}</div>
                <p class="text-body-1 text-grey-darken-3 mb-6 line-height-lg">{{ aiAnalysis.cause }}</p>
                <v-alert type="warning" border="start" variant="tonal" class="rounded-lg">
                  <div class="text-subtitle-1 font-weight-bold">권장 최적화 액션</div>
                  <div class="mt-1">{{ aiAnalysis.action }}</div>
                </v-alert>
              </div>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions class="pa-6 bg-grey-lighten-4">
              <v-spacer></v-spacer>
              <v-btn color="indigo-darken-4" variant="flat" width="120" rounded="lg" @click="aiDialog = false">확인</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-snackbar v-model="showError" color="error" timeout="3000" location="bottom right">
          <v-icon class="mr-2">mdi-alert-circle</v-icon> {{ errorMessage }}
        </v-snackbar>
      </v-main>
    </template>
  </v-app>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue';
import axios from 'axios';
import MonitorTable from './components/dashboard/MonitorTable.vue';
import CostBoard from './components/dashboard/CostBoard.vue';
import SpcBoard from './components/dashboard/SpcBoard.vue';

// ⭐️ 1. 환경변수 API Base URL
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

// ⭐️ 2. 타입 정의 (Interface)
interface TrafficLog {
  trace_id: string;
  timestamp: string;
  service_endpoint: string;
  project_code: string;
  status_code: number;
  latency_ms: number;
  payload_bytes: number;
}

interface CostAllocation {
  project_code: string;
  department: string;
  traffic_share_pct: number;
  breakdown: { direct_infra_cost: number; amortized_cost: number; allocated_shared_cost: number; };
  total_allocated_cost: number;
}

const isLoggedIn = ref(false);
const loginId = ref('');
const userRole = ref('');
const currentMenu = ref('monitor');

const logs = ref<TrafficLog[]>([]);
const costs = ref<CostAllocation[]>([]);

// ⭐️ 3. 에러 & 로딩 상태
const isFetching = ref(false);
const showError = ref(false);
const errorMessage = ref('');
const aiLoading = ref(false);
const aiDialog = ref(false);
const aiAnalysis = ref<any>(null);

let pollingInterval: ReturnType<typeof setInterval> | null = null;

const handleLogin = async () => {
  if (loginId.value === 'admin' || loginId.value === 'viewer') {
    userRole.value = loginId.value;
    isFetching.value = true;
    await fetchData();
    isFetching.value = false;
    
    if (!showError.value) {
      isLoggedIn.value = true;
      startPolling();
    }
  } else {
    alert("존재하지 않는 사용자입니다. (테스트용: admin 또는 viewer)");
  }
};

const handleLogout = () => {
  isLoggedIn.value = false;
  loginId.value = '';
  userRole.value = '';
  stopPolling();
};

const fetchData = async () => {
  try {
    const [l, c] = await Promise.all([
      axios.get<TrafficLog[]>(`${API_BASE}/interface-logs`),
      axios.get<CostAllocation[]>(`${API_BASE}/cost-allocation`)
    ]);
    logs.value = l.data;
    costs.value = c.data;
    showError.value = false; 
  } catch (e) {
    showError.value = true;
    errorMessage.value = "서버와의 통신이 끊어졌습니다. 관리자에게 문의하세요.";
    console.error("API Error", e);
  }
};

const startPolling = () => {
  stopPolling();
  pollingInterval = setInterval(fetchData, 3000);
};

const stopPolling = () => { if (pollingInterval) clearInterval(pollingInterval); };
onUnmounted(stopPolling);

const errorRate = computed(() => {
  if (logs.value.length === 0) return "0";
  return ((logs.value.filter(l => l.status_code >= 400).length / logs.value.length) * 100).toFixed(1);
});
const avgResponseTime = computed(() => {
  if (logs.value.length === 0) return 0;
  return Math.round(logs.value.reduce((acc, cur) => acc + (cur.latency_ms || 0), 0) / logs.value.length);
});

const chartOptions = { responsive: true, maintainAspectRatio: false };
const chartData = computed(() => {
  const deptMap: Record<string, number> = {};
  costs.value.forEach(c => { deptMap[c.department] = (deptMap[c.department] || 0) + c.total_allocated_cost; });
  return {
    labels: Object.keys(deptMap),
    datasets: [{ backgroundColor: ['#1A237E', '#0097A7', '#388E3C', '#FBC02D', '#C2185B'], data: Object.values(deptMap) }]
  };
});

const runSmartAnalysis = () => {
  aiLoading.value = true;
  setTimeout(() => {
    aiAnalysis.value = {
      title: "인프라 부하 및 원가 누수 경고",
      cause: "디지털혁신본부(PRD-102)의 API 호출량이 지난 시간 대비 45% 급증하여 전사 공통망 배분 비용이 예산을 초과할 것으로 예상됩니다.",
      action: "관리자 권한으로 해당 프로젝트의 실패 로그를 점검하고, 리소스 자동 스케일링 규칙을 적용하십시오."
    };
    aiLoading.value = false;
    aiDialog.value = true;
  }, 1200);
};

const downloadExcel = () => { window.location.href = `${API_BASE}/download/costs`; };
</script>

<style scoped>
.login-bg { background: linear-gradient(135deg, #0D47A1 0%, #1A237E 100%); }
.login-card { backdrop-filter: blur(10px); background-color: rgba(255, 255, 255, 0.95) !important; }
.sidebar-list :deep(.v-list-item--active) { background-color: rgba(0, 184, 212, 0.1) !important; border-left: 4px solid #00B8D4; }
.pulse-icon { animation: pulse 2s infinite; }
@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
}
.shadow-sm { box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important; }
.line-height-lg { line-height: 1.6; }
</style>