// Stratify AI Enterprise Mock Data Suite

export const EXECUTIVE_KPIS = [
  {
    id: 'arr',
    label: 'Annual Recurring Revenue',
    value: '$4.85M',
    rawNumeric: 4850000,
    change: '+14.2%',
    isPositive: true,
    timeframe: 'vs last quarter',
    sparkline: [3.8, 4.0, 4.2, 4.35, 4.6, 4.85],
    iconName: 'DollarSign',
    accentColor: 'blue',
  },
  {
    id: 'ndr',
    label: 'Net Dollar Retention',
    value: '118.4%',
    rawNumeric: 118.4,
    change: '+3.1%',
    isPositive: true,
    timeframe: 'vs baseline',
    sparkline: [112, 114, 115, 116.5, 117, 118.4],
    iconName: 'TrendingUp',
    accentColor: 'purple',
  },
  {
    id: 'customers',
    label: 'Enterprise Accounts',
    value: '1,428',
    rawNumeric: 1428,
    change: '+8.7%',
    isPositive: true,
    timeframe: '124 new this month',
    sparkline: [1200, 1260, 1310, 1360, 1390, 1428],
    iconName: 'Users',
    accentColor: 'cyan',
  },
  {
    id: 'efficiency',
    label: 'Operational Health Index',
    value: '94.2/100',
    rawNumeric: 94.2,
    change: '+2.4 pts',
    isPositive: true,
    timeframe: 'Optimal performance',
    sparkline: [88, 89.5, 91, 92.4, 93.5, 94.2],
    iconName: 'Activity',
    accentColor: 'emerald',
  },
];

export const REVENUE_TREND_DATA = [
  { month: 'Jan', revenue: 380000, target: 360000, margin: 72 },
  { month: 'Feb', revenue: 410000, target: 390000, margin: 74 },
  { month: 'Mar', revenue: 450000, target: 420000, margin: 75 },
  { month: 'Apr', revenue: 490000, target: 460000, margin: 73 },
  { month: 'May', revenue: 530000, target: 500000, margin: 77 },
  { month: 'Jun', revenue: 590000, target: 550000, margin: 78 },
  { month: 'Jul', revenue: 640000, target: 600000, margin: 79 },
  { month: 'Aug', revenue: 680000, target: 640000, margin: 81 },
  { month: 'Sep', revenue: 730000, target: 690000, margin: 80 },
  { month: 'Oct', revenue: 790000, target: 740000, margin: 82 },
  { month: 'Nov', revenue: 840000, target: 790000, margin: 83 },
  { month: 'Dec', revenue: 920000, target: 850000, margin: 85 },
];

export const MONTHLY_SALES_DATA = [
  { month: 'Q1 Jan', enterprise: 220, midMarket: 110, smb: 50 },
  { month: 'Q1 Feb', enterprise: 240, midMarket: 120, smb: 50 },
  { month: 'Q1 Mar', enterprise: 270, midMarket: 130, smb: 50 },
  { month: 'Q2 Apr', enterprise: 290, midMarket: 140, smb: 60 },
  { month: 'Q2 May', enterprise: 310, midMarket: 160, smb: 60 },
  { month: 'Q2 Jun', enterprise: 350, midMarket: 180, smb: 60 },
  { month: 'Q3 Jul', enterprise: 380, midMarket: 200, smb: 60 },
  { month: 'Q3 Aug', enterprise: 410, midMarket: 210, smb: 60 },
];

export const REGIONAL_SALES_DATA = [
  { region: 'North America', revenue: '$2.42M', percentage: 50, growth: '+16.8%', activeClients: 714, latency: '12ms', status: 'Optimal' },
  { region: 'Europe (EMEA)', revenue: '$1.35M', percentage: 28, growth: '+11.4%', activeClients: 399, latency: '24ms', status: 'Optimal' },
  { region: 'Asia Pacific', revenue: '$776K', percentage: 16, growth: '+22.5%', activeClients: 228, latency: '38ms', status: 'Expanding' },
  { region: 'Latin America', revenue: '$291K', percentage: 6, growth: '+19.1%', activeClients: 87, latency: '45ms', status: 'Optimal' },
];

export const INVENTORY_STATUS_DATA = [
  { sku: 'Stratify Engine Pro', category: 'SaaS Platform', stockLevel: 98, status: 'In Stock', reorderPoint: 'Auto-scaled' },
  { sku: 'Snowflake Connector v4', category: 'Data Pipeline', stockLevel: 85, status: 'In Stock', reorderPoint: 'Auto-scaled' },
  { sku: 'Predictive GPU Nodes', category: 'Compute Cluster', stockLevel: 32, status: 'Warning', reorderPoint: 'Capacity Limit: 80%' },
  { sku: 'Real-time Stream Relay', category: 'Infrastructure', stockLevel: 94, status: 'In Stock', reorderPoint: 'Auto-scaled' },
  { sku: 'Vector DB Instance X', category: 'AI Store', stockLevel: 68, status: 'In Stock', reorderPoint: 'Normal' },
];

export const CUSTOMER_GROWTH_DATA = [
  { month: 'Jan', activeUsers: 14200, churnRate: 1.2, netPromoter: 68 },
  { month: 'Feb', activeUsers: 15800, churnRate: 1.1, netPromoter: 70 },
  { month: 'Mar', activeUsers: 17400, churnRate: 0.9, netPromoter: 72 },
  { month: 'Apr', activeUsers: 19100, churnRate: 0.8, netPromoter: 73 },
  { month: 'May', activeUsers: 21500, churnRate: 0.7, netPromoter: 75 },
  { month: 'Jun', activeUsers: 24200, churnRate: 0.6, netPromoter: 78 },
];

export const TOP_PRODUCTS_DATA = [
  { id: 1, name: 'Stratify Enterprise AI Suite', category: 'AI Analytics', salesCount: '1,240', revenue: '$1,860,000', margin: '84%', growth: '+24%', status: 'Best Seller' },
  { id: 2, name: 'Fabric Data Connector', category: 'Integration', salesCount: '980', revenue: '$980,000', margin: '79%', growth: '+18%', status: 'High Growth' },
  { id: 3, name: 'Real-Time Anomaly Detector', category: 'Security & Ops', salesCount: '840', revenue: '$756,000', margin: '88%', growth: '+31%', status: 'Trending' },
  { id: 4, name: 'Predictive Churn Engine', category: 'ML Models', salesCount: '620', revenue: '$620,000', margin: '91%', growth: '+15%', status: 'Stable' },
  { id: 5, name: 'Executive BI Copilot', category: 'Generative AI', salesCount: '510', revenue: '$637,500', margin: '82%', growth: '+42%', status: 'Breakout' },
];

export const RECENT_ALERTS = [
  { id: 'alt-1', title: 'Q3 Enterprise Deal Closed', category: 'Revenue', time: '12 min ago', severity: 'success', description: 'Acme Corp signed $350K multi-year expansion.' },
  { id: 'alt-2', title: 'EMEA Latency Spike Resolved', category: 'Infrastructure', time: '45 min ago', severity: 'info', description: 'Automatic failover to Frankfurt region completed.' },
  { id: 'alt-3', title: 'Model Variance Exceeds Threshold', category: 'AI Audit', time: '2 hours ago', severity: 'warning', description: 'Sales forecast confidence band adjusted by +1.4%.' },
  { id: 'alt-4', title: 'Automated Backup Completed', category: 'System', time: '4 hours ago', severity: 'info', description: 'Snowflake data lake snapshot created successfully.' },
];

export const BUSINESS_HEALTH_SCORE = {
  overallScore: 92,
  rating: 'Exceptional',
  categories: [
    { name: 'Financial Momentum', score: 95, detail: 'ARR growth & net margins in top 5th percentile' },
    { name: 'Customer Satisfaction', score: 91, detail: 'NPS score of 78 with 0.6% monthly churn' },
    { name: 'Operational Speed', score: 89, detail: 'Data pipeline latency under 45ms global average' },
    { name: 'Predictive Accuracy', score: 94, detail: 'AI forecast error rate reduced to 1.8%' },
  ]
};

export const AI_RECOMMENDATIONS = [
  {
    id: 'rec-1',
    title: 'Cross-Sell Opportunity Detected',
    impact: 'High Impact (+ $180K ARR)',
    confidence: '96% AI Confidence',
    summary: '14 Mid-Market accounts in EMEA have reached 92% feature utilization. Recommending targeted upgrade campaign to Enterprise tier.',
    actionLabel: 'Launch Campaign',
    category: 'Revenue Optimization'
  },
  {
    id: 'rec-2',
    title: 'Compute Cluster Spend Optimization',
    impact: 'Cost Reduction ($24K / mo)',
    confidence: '92% AI Confidence',
    summary: 'GPU cluster load drops to 14% between 01:00 UTC and 05:00 UTC. Auto-scaling policy adjustment will reduce infrastructure overhead.',
    actionLabel: 'Optimize Policy',
    category: 'Cost Control'
  }
];

export const DATA_SOURCES = [
  { id: 'snow', name: 'Snowflake Data Cloud', type: 'Data Warehouse', status: 'Connected', sync: 'Live (2m ago)', records: '1.4B rows', logo: '❄️' },
  { id: 'aws', name: 'Amazon Redshift', type: 'Data Warehouse', status: 'Connected', sync: 'Scheduled (1h ago)', records: '850M rows', logo: '☁️' },
  { id: 'postgres', name: 'PostgreSQL Production DB', type: 'Transactional DB', status: 'Connected', sync: 'Real-time', records: '240M rows', logo: '🐘' },
  { id: 'salesforce', name: 'Salesforce CRM', type: 'SaaS App', status: 'Connected', sync: '15m ago', records: '42K accounts', logo: '☁️' },
  { id: 'bigquery', name: 'Google BigQuery', type: 'Analytics Warehouse', status: 'Available', sync: 'Not connected', records: '0', logo: '📊' },
];

export const MOCK_REPORTS = [
  { id: 'rep-1', title: 'Q3 Executive Financial Briefing', category: 'Executive', format: 'PDF & Deck', schedule: 'Weekly (Mondays)', lastGenerated: 'Aug 1, 2026', owner: 'Rithvik (CEO Office)' },
  { id: 'rep-2', title: 'Enterprise Customer Retention Audit', category: 'Customer Success', format: 'Interactive CSV', schedule: 'Monthly (1st)', lastGenerated: 'Aug 1, 2026', owner: 'Analytics Team' },
  { id: 'rep-3', title: 'Infrastructure & Latency SLA Report', category: 'Engineering', format: 'PDF', schedule: 'Daily 06:00 UTC', lastGenerated: 'Today 06:00', owner: 'DevOps Engine' },
  { id: 'rep-4', title: 'Global Product Margin Breakdown', category: 'Finance', format: 'Excel Workbench', schedule: 'On Demand', lastGenerated: 'Jul 28, 2026', owner: 'CFO Office' },
];

export const SAMPLE_AI_CONVERSATION = [
  {
    id: 1,
    sender: 'user',
    text: 'What drove our 14.2% ARR growth this quarter?',
    timestamp: '10:14 AM'
  },
  {
    id: 2,
    sender: 'ai',
    text: 'ARR expansion was predominantly driven by EMEA Enterprise tier upsells (+24.5% QoQ) and strong adoption of the new Executive BI Copilot add-on (contributing $637.5K in net new ARR). Net Dollar Retention also expanded to 118.4%.',
    timestamp: '10:14 AM',
    chartType: 'breakdown'
  }
];
