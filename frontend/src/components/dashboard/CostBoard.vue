<template>
  <v-row>
    <v-col cols="12" md="4">
      <v-card elevation="0" class="pa-6 rounded-xl h-100 stripe-card">
        <h3 class="text-subtitle-2 font-weight-black mb-6 text-grey-darken-2 text-uppercase tracking-wide">Cost Distribution</h3>
        <div style="height: 280px;"><Pie :data="chartData" :options="chartOptions" /></div>
      </v-card>
    </v-col>
    
    <v-col cols="12" md="8">
      <v-card elevation="0" class="rounded-xl h-100 overflow-hidden stripe-card">
        <v-data-table 
          :headers="headers" 
          :items="costs" 
          item-value="project_code" 
          show-expand 
          density="comfortable"
          class="stripe-table"
        >
          <template v-slot:item.traffic_share_pct="{ item }">
            <v-chip size="small" color="#0F172A" variant="tonal" class="font-weight-bold font-mono">
              {{ item.traffic_share_pct }} %
            </v-chip>
          </template>
          
          <template v-slot:item.total_allocated_cost="{ item }">
            <span class="font-mono font-weight-black text-indigo-darken-4" style="font-size: 1.1rem;">₩ {{ item.total_allocated_cost.toLocaleString() }}</span>
          </template>

          <template v-slot:expanded-row="{ columns, item }">
            <tr>
              <td :colspan="columns.length" class="pa-0">
                <div class="expand-invoice pa-6">
                  <div class="d-flex justify-space-between mb-3 text-body-2">
                    <span class="text-grey-darken-1">전용 리소스 직접비 (Direct Cost)</span>
                    <span class="font-mono font-weight-bold text-grey-darken-3">₩ {{ item.breakdown.direct_infra_cost.toLocaleString() }}</span>
                  </div>
                  <div class="d-flex justify-space-between mb-3 text-body-2">
                    <span class="text-grey-darken-1">H/W 감가상각 배분액 (Amortized)</span>
                    <span class="font-mono font-weight-bold text-grey-darken-3">₩ {{ item.breakdown.amortized_cost.toLocaleString() }}</span>
                  </div>
                  <v-divider class="mb-3 opacity-20"></v-divider>
                  <div class="d-flex justify-space-between">
                    <span class="text-indigo-accent-4 font-weight-bold text-body-2">공통망 트래픽 할당액 (Shared Cost)</span>
                    <span class="font-mono text-indigo-accent-4 font-weight-black">+ ₩ {{ item.breakdown.allocated_shared_cost.toLocaleString() }}</span>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'vue-chartjs';
ChartJS.register(ArcElement, Tooltip, Legend);

interface CostAllocation { project_code: string; department: string; traffic_share_pct: number; total_allocated_cost: number; breakdown: { direct_infra_cost: number; amortized_cost: number; allocated_shared_cost: number; }; }
defineProps<{ costs: CostAllocation[], chartData: any, chartOptions: any }>();

const headers = [
  { title: 'PROJECT CODE', key: 'project_code' },
  { title: 'DEPARTMENT', key: 'department' },
  { title: 'TRAFFIC SHARE', key: 'traffic_share_pct', align: 'center' as const },
  { title: 'TOTAL ALLOCATED COST', key: 'total_allocated_cost', align: 'end' as const }
];
</script>

<style scoped>
.stripe-card { border: 1px solid #F1F5F9; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important; }
.stripe-table :deep(th) { background-color: #FFFFFF !important; font-weight: 700 !important; color: #94A3B8 !important; font-size: 0.75rem; border-bottom: 2px solid #F1F5F9 !important; }
.stripe-table :deep(td) { border-bottom: 1px solid #F8FAFC !important; }
.expand-invoice { background-color: #F8FAFC; border-left: 4px solid #4F46E5; }
.font-mono { font-family: 'JetBrains Mono', 'Roboto Mono', monospace !important; }
.tracking-wide { letter-spacing: 0.05em; }
</style>