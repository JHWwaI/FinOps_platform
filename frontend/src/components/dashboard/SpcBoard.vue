<template>
  <v-row>
    <v-col cols="12" md="4">
      <v-card elevation="24" class="pa-6 rounded-xl h-100 bloomberg-card" theme="dark">
        <div class="d-flex align-center mb-6">
          <v-icon size="x-large" color="#00E676" class="mr-3">mdi-ferry</v-icon>
          <div>
            <div class="text-h6 font-weight-black text-white">Noah SPC Fund 1호</div>
            <div class="text-caption text-grey-lighten-1 font-mono">LIVE FINANCIAL STATEMENTS</div>
          </div>
        </div>
        <v-divider class="mb-5 border-opacity-25" color="grey"></v-divider>

        <div v-if="statements">
          <div class="text-overline text-grey-lighten-1 mb-2 tracking-wide">Balance Sheet (BS)</div>
          <div class="d-flex justify-space-between mb-2 font-mono"><span class="text-grey-lighten-2">Total Assets</span><span class="font-weight-bold text-green-accent-3">₩ {{ statements.balance_sheet.assets.toLocaleString() }}</span></div>
          <div class="d-flex justify-space-between mb-2 font-mono"><span class="text-grey-lighten-2">Total Liabilities</span><span class="font-weight-bold text-red-accent-2">₩ {{ statements.balance_sheet.liabilities.toLocaleString() }}</span></div>
          <div class="d-flex justify-space-between mb-6 font-mono"><span class="text-white font-weight-bold">Total Equity</span><span class="font-weight-bold text-white">₩ {{ (statements.balance_sheet.equity + statements.balance_sheet.retained_earnings).toLocaleString() }}</span></div>

          <div class="text-overline text-grey-lighten-1 mb-2 tracking-wide">Income Statement (IS)</div>
          <div class="d-flex justify-space-between mb-2 font-mono"><span class="text-grey-lighten-2">Revenue</span><span class="font-weight-bold text-green-accent-3">+ ₩ {{ statements.income_statement.revenue.toLocaleString() }}</span></div>
          <div class="d-flex justify-space-between mb-3 font-mono"><span class="text-grey-lighten-2">Expenses</span><span class="font-weight-bold text-red-accent-2">- ₩ {{ statements.income_statement.expenses.toLocaleString() }}</span></div>
          
          <v-card color="#161B22" elevation="0" class="pa-4 rounded-lg border-solid border-cyan">
            <div class="d-flex justify-space-between font-mono">
              <span class="font-weight-black text-cyan-accent-2">NET INCOME</span>
              <span class="font-weight-black text-cyan-accent-2" style="font-size: 1.2rem;">₩ {{ statements.income_statement.net_income.toLocaleString() }}</span>
            </div>
          </v-card>
        </div>
      </v-card>
    </v-col>

    <v-col cols="12" md="8">
      <v-card elevation="24" class="rounded-xl h-100 overflow-hidden bloomberg-card" theme="dark">
        <v-toolbar color="#0D1117" class="px-4" elevation="0" border="bottom">
          <v-icon color="#00E676" class="mr-2 pulse">mdi-circle-medium</v-icon>
          <span class="font-weight-bold text-white font-mono" style="font-size: 0.9rem;">GENERAL_LEDGER_STREAM</span>
        </v-toolbar>
        
        <v-data-table 
          :headers="headers" 
          :items="journals" 
          hover 
          density="compact"
          theme="dark"
          class="terminal-table bg-transparent"
        >
          <template v-slot:item.type="{ item }">
            <span :class="['font-weight-bold font-mono text-caption', getTypeColor(item.type)]">{{ item.type }}</span>
          </template>
          
          <template v-slot:item.debit="{ item }">
            <span v-if="item.debit > 0" class="text-green-accent-3 font-weight-bold font-mono">{{ item.debit.toLocaleString() }}</span>
            <span v-else class="text-grey-darken-2">-</span>
          </template>
          <template v-slot:item.credit="{ item }">
            <span v-if="item.credit > 0" class="text-red-accent-2 font-weight-bold font-mono">{{ item.credit.toLocaleString() }}</span>
            <span v-else class="text-grey-darken-2">-</span>
          </template>
        </v-data-table>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
interface JournalEntry { id: number; date: string; desc: string; account: string; type: string; debit: number; credit: number; }
interface SpcStatements { balance_sheet: any; income_statement: any; }

const journals = ref<JournalEntry[]>([]);
const statements = ref<SpcStatements | null>(null);

const headers = [
  { title: 'DATETIME', key: 'date', sortable: false },
  { title: 'DESCRIPTION', key: 'desc', sortable: false },
  { title: 'ACCOUNT', key: 'account', sortable: false },
  { title: 'TYPE', key: 'type', sortable: false },
  { title: 'DEBIT (차변)', key: 'debit', align: 'end' as const, sortable: false },
  { title: 'CREDIT (대변)', key: 'credit', align: 'end' as const, sortable: false }
];

const getTypeColor = (type: string) => {
  const map: Record<string, string> = { '자산': 'text-cyan-accent-2', '부채': 'text-pink-accent-2', '자본': 'text-purple-accent-2', '수익': 'text-green-accent-3', '비용': 'text-orange-accent-2' };
  return map[type] || 'text-grey';
};

const fetchSpcData = async () => {
  try {
    const [j, s] = await Promise.all([ axios.get<JournalEntry[]>(`${API_BASE}/spc/journal`), axios.get<SpcStatements>(`${API_BASE}/spc/statements`) ]);
    journals.value = j.data;
    statements.value = s.data;
  } catch (e) { console.error("SPC 데이터 조회 실패", e); }
};
onMounted(fetchSpcData);
</script>

<style scoped>
.bloomberg-card { background-color: #0D1117 !important; border: 1px solid #30363D; }
.terminal-table :deep(th) { background-color: #0D1117 !important; color: #8B949E !important; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; border-bottom: 1px solid #21262D !important; }
.terminal-table :deep(td) { border-bottom: 1px solid #21262D !important; color: #C9D1D9; }
.font-mono { font-family: 'JetBrains Mono', 'Roboto Mono', 'Courier New', monospace !important; }
.tracking-wide { letter-spacing: 0.1em; }
.border-solid { border: 1px solid rgba(0, 229, 255, 0.3); }
.pulse { animation: pulse 1.5s infinite; }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
</style>