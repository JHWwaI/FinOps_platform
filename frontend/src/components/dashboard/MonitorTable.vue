<template>
  <v-card elevation="0" class="border-none bg-transparent">
    <v-data-table 
      :headers="headers" 
      :items="logs" 
      hover 
      density="comfortable"
      class="datadog-table rounded-lg shadow-sm"
    >
      <template v-slot:item.status_code="{ item }">
        <v-chip 
          :color="item.status_code === 200 ? '#10B981' : '#EF4444'" 
          size="small" 
          variant="elevated"
          class="font-weight-black font-mono text-white px-3"
        >
          {{ item.status_code === 200 ? '200 OK' : '500 ERR' }}
        </v-chip>
        <v-btn 
          v-if="item.status_code !== 200 && userRole === 'admin'" 
          size="x-small" color="red-darken-4" variant="flat" class="ml-3 font-weight-bold" rounded="sm"
          @click="handleRetry(item)"
        >
          RETRY
        </v-btn>
      </template>

      <template v-slot:item.latency_ms="{ item }">
        <span :class="['font-mono font-weight-black', item.latency_ms >= 1000 ? 'text-red-darken-1' : 'text-blue-grey-darken-2']">
          {{ item.latency_ms.toLocaleString() }} ms
        </span>
      </template>
      
      <template v-slot:item.trace_id="{ item }"><span class="font-mono text-grey-darken-1">{{ item.trace_id }}</span></template>
      <template v-slot:item.timestamp="{ item }"><span class="font-mono text-grey-darken-1">{{ item.timestamp }}</span></template>
    </v-data-table>
  </v-card>
</template>

<script setup lang="ts">
interface TrafficLog { trace_id: string; timestamp: string; service_endpoint: string; status_code: number; latency_ms: number; }
defineProps<{ logs: TrafficLog[], userRole: string }>();

const headers = [
  { title: 'TIMESTAMP', key: 'timestamp', sortable: false },
  { title: 'TRACE ID', key: 'trace_id', sortable: false },
  { title: 'ENDPOINT', key: 'service_endpoint', sortable: false },
  { title: 'STATUS', key: 'status_code', sortable: false },
  { title: 'LATENCY', key: 'latency_ms', align: 'end' as const }
];
const handleRetry = (item: TrafficLog) => { alert(`Trace ID: ${item.trace_id} 재처리 요청 전송 완료`); };
</script>

<style scoped>
.datadog-table { border: 1px solid #E2E8F0 !important; background-color: white; }
.datadog-table :deep(th) { background-color: #F8FAFC !important; font-weight: 800 !important; color: #64748B !important; font-size: 0.75rem; letter-spacing: 0.5px; }
.datadog-table :deep(td) { border-bottom: 1px solid #F1F5F9 !important; }
.shadow-sm { box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important; }
.font-mono { font-family: 'JetBrains Mono', 'Roboto Mono', monospace !important; }
</style>