"""
============================================================
FUTURE INTERNS — Data Science & Analytics Internship
Task 3: Marketing Funnel & Conversion Performance Analysis
Intern  : Shiv Kumar  |  CIN: FIT/MAY26/DS17882
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ── 1. GENERATE DATASET ──────────────────────────────────────────────────────
# Replace this block with: df = pd.read_csv('your_data.csv') for real data

np.random.seed(77)
from datetime import datetime, timedelta

n = 2000
channels  = ['Organic Search', 'Paid Ads', 'Social Media', 'Email Campaign', 'Referral']
campaigns = ['Summer Sale', 'Product Launch', 'Brand Awareness', 'Retargeting', 'Newsletter']
devices   = ['Desktop', 'Mobile', 'Tablet']

channel_conv = {
    'Organic Search':  {'lead': 0.32, 'qualified': 0.55, 'proposal': 0.50, 'customer': 0.45},
    'Paid Ads':        {'lead': 0.28, 'qualified': 0.40, 'proposal': 0.42, 'customer': 0.38},
    'Social Media':    {'lead': 0.18, 'qualified': 0.35, 'proposal': 0.38, 'customer': 0.30},
    'Email Campaign':  {'lead': 0.42, 'qualified': 0.60, 'proposal': 0.55, 'customer': 0.52},
    'Referral':        {'lead': 0.50, 'qualified': 0.70, 'proposal': 0.65, 'customer': 0.60},
}

rows = []
start = datetime(2024, 1, 1)
for i in range(n):
    channel  = np.random.choice(channels, p=[0.30, 0.25, 0.20, 0.15, 0.10])
    campaign = np.random.choice(campaigns)
    device   = np.random.choice(devices, p=[0.45, 0.45, 0.10])
    date     = start + timedelta(days=np.random.randint(0, 365))
    month    = date.strftime('%Y-%m')
    cr       = channel_conv[channel]

    visitors  = np.random.randint(80, 500)
    leads     = min(int(visitors  * cr['lead']      * np.random.uniform(0.85, 1.15)), visitors)
    qualified = min(int(leads     * cr['qualified']  * np.random.uniform(0.85, 1.15)), leads)
    proposals = min(int(qualified * cr['proposal']   * np.random.uniform(0.85, 1.15)), qualified)
    customers = min(int(proposals * cr['customer']   * np.random.uniform(0.85, 1.15)), proposals)

    avg_deal  = np.random.randint(200, 2000)
    revenue   = customers * avg_deal
    ad_spend  = round(leads * np.random.uniform(5, 40), 2)
    roi       = round((revenue - ad_spend) / ad_spend * 100, 1) if ad_spend > 0 else 0

    rows.append({
        'Date': date.date(), 'Month': month, 'Channel': channel,
        'Campaign': campaign, 'Device': device,
        'Visitors': visitors, 'Leads': leads, 'Qualified_Leads': qualified,
        'Proposals': proposals, 'Customers': customers,
        'Avg_Deal_Value': avg_deal, 'Revenue': revenue,
        'Ad_Spend': ad_spend, 'ROI_%': roi,
    })

df = pd.DataFrame(rows)
df.to_csv('funnel_data.csv', index=False)
print("Dataset ready — 2,000 funnel records across 5 channels and 3 devices.\n")

# ── 2. DATA CLEANING ─────────────────────────────────────────────────────────
print("── Data Cleaning ──")
print(f"  Null values : {df.isnull().sum().sum()}")
print(f"  Duplicates  : {df.duplicated().sum()}")
print(f"  Date range  : {df['Date'].min()} → {df['Date'].max()}\n")

# ── 3. FUNNEL METRICS ────────────────────────────────────────────────────────
total_v = df['Visitors'].sum()
total_l = df['Leads'].sum()
total_q = df['Qualified_Leads'].sum()
total_p = df['Proposals'].sum()
total_c = df['Customers'].sum()
total_rev = df['Revenue'].sum()
overall_conv = total_c / total_v * 100

print("── Funnel Summary ──")
print(f"  Visitors         : {total_v:,}")
print(f"  Leads            : {total_l:,}  ({total_l/total_v*100:.1f}% of visitors)")
print(f"  Qualified Leads  : {total_q:,}  ({total_q/total_l*100:.1f}% of leads)")
print(f"  Proposals        : {total_p:,}  ({total_p/total_q*100:.1f}% of qualified)")
print(f"  Customers        : {total_c:,}  ({total_c/total_p*100:.1f}% of proposals)")
print(f"  Overall Conv Rate: {overall_conv:.2f}%")
print(f"  Total Revenue    : ₹{total_rev:,}\n")

# ── 4. CHANNEL ANALYSIS ──────────────────────────────────────────────────────
print("── Channel Performance ──")
ch_perf = df.groupby('Channel').agg(
    Visitors=('Visitors','sum'), Leads=('Leads','sum'),
    Customers=('Customers','sum'), Revenue=('Revenue','sum')
).assign(
    LeadRate=lambda x: (x['Leads']/x['Visitors']*100).round(2),
    ConvRate=lambda x: (x['Customers']/x['Visitors']*100).round(2)
)
print(ch_perf.sort_values('ConvRate', ascending=False).to_string(), "\n")

# ── 5. STAGE DROP-OFF ────────────────────────────────────────────────────────
print("── Stage-to-Stage Conversion ──")
stages = ['Visitor→Lead', 'Lead→Qualified', 'Qualified→Proposal', 'Proposal→Customer']
rates  = [total_l/total_v, total_q/total_l, total_p/total_q, total_c/total_p]
for s, r in zip(stages, rates):
    print(f"  {s:<25}: {r*100:.1f}%")

# ── 6. DEVICE ANALYSIS ───────────────────────────────────────────────────────
print("\n── Conversion by Device ──")
dev = df.groupby('Device').agg(
    Visitors=('Visitors','sum'), Customers=('Customers','sum')
).assign(ConvRate=lambda x: (x['Customers']/x['Visitors']*100).round(2))
print(dev.sort_values('ConvRate', ascending=False).to_string(), "\n")

# ── 7. DASHBOARD ─────────────────────────────────────────────────────────────
BG, CARD = '#0C0F1D', '#131726'
A1,A2,A3,A4,A5 = '#38BDF8','#FB923C','#4ADE80','#F87171','#C084FC'
TEXT, SUB = '#F0F4FF', '#8892AA'
CH_C = {'Organic Search': A1, 'Paid Ads': A2, 'Social Media': A5,
        'Email Campaign': A3, 'Referral': '#FBBF24'}

plt.rcParams.update({
    'figure.facecolor':BG,'axes.facecolor':CARD,'text.color':TEXT,
    'axes.labelcolor':TEXT,'xtick.color':SUB,'ytick.color':SUB,
    'axes.edgecolor':'#1E2640','grid.color':'#1E2640',
    'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,
})

fig = plt.figure(figsize=(20, 15), facecolor=BG)
gs  = gridspec.GridSpec(4, 4, figure=fig, hspace=0.58, wspace=0.38,
                         top=0.91, bottom=0.06, left=0.05, right=0.97)

# Title
tax = fig.add_axes([0, 0.93, 1, 0.07], facecolor='#0A0D1A')
tax.axis('off')
tax.text(0.5, 0.65, 'MARKETING FUNNEL & CONVERSION PERFORMANCE ANALYSIS',
         ha='center', va='center', fontsize=19, fontweight='bold', color=TEXT, transform=tax.transAxes)
tax.text(0.5, 0.18, 'Digital Marketing · FY 2024  ·  Future Interns  ·  Data Science & Analytics — Shiv Kumar',
         ha='center', va='center', fontsize=9, color=SUB, transform=tax.transAxes)
tax.axhline(0, color=A1, linewidth=2, xmin=0.05, xmax=0.95)

# KPI Cards
kpis = [('Total Visitors', f'{total_v/1e3:.0f}K', A1),
        ('Total Customers', f'{total_c/1e3:.1f}K', A3),
        ('Overall Conv. Rate', f'{overall_conv:.2f}%', A2),
        ('Total Revenue', f'₹{total_rev/1e6:.1f}M', A5)]
for i,(label,val,color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor(CARD); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    rect = FancyBboxPatch((0.04,0.08),0.92,0.84,boxstyle='round,pad=0.02',
                          linewidth=2,edgecolor=color,facecolor='#161D35',
                          transform=ax.transAxes,clip_on=False)
    ax.add_patch(rect)
    ax.text(0.5,0.72,label,ha='center',va='center',fontsize=9,color=SUB,transform=ax.transAxes)
    ax.text(0.5,0.38,val,ha='center',va='center',fontsize=22,fontweight='bold',color=color,transform=ax.transAxes)
    ax.axhline(0.08,color=color,linewidth=3,xmin=0.1,xmax=0.9,alpha=0.4)

# Funnel Chart
ax1 = fig.add_subplot(gs[1, :2])
stages_f = ['Visitors', 'Leads', 'Qualified\nLeads', 'Proposals', 'Customers']
values_f = [total_v, total_l, total_q, total_p, total_c]
colors_f = [A1, '#60A5FA', A3, A2, '#FBBF24']
y_pos    = list(range(len(stages_f)))[::-1]
for yi,(val,color,stage) in enumerate(zip(values_f, colors_f, stages_f)):
    width = val / max(values_f)
    left  = (1 - width) / 2
    ax1.barh(y_pos[yi], width, left=left, color=color, height=0.55, alpha=0.88)
    ax1.text(0.5, y_pos[yi], f'{val:,}', ha='center', va='center',
             color=BG, fontsize=9, fontweight='bold')
ax1.set_yticks(y_pos); ax1.set_yticklabels(stages_f, fontsize=9)
ax1.set_xlim(0,1); ax1.set_xticks([])
for sp in ax1.spines.values(): sp.set_visible(False)
ax1.set_title('Marketing Funnel — Volume at Each Stage', color=TEXT, fontsize=11, pad=10, loc='left')

# Stage Conversion Rates
ax2 = fig.add_subplot(gs[1, 2:])
conv_labels = ['Visitor\n→Lead', 'Lead\n→Qualified', 'Qualified\n→Proposal', 'Proposal\n→Customer']
conv_rates  = [total_l/total_v*100, total_q/total_l*100, total_p/total_q*100, total_c/total_p*100]
bar_colors  = [A3 if v>=40 else A2 if v>=25 else A4 for v in conv_rates]
bars = ax2.bar(conv_labels, conv_rates, color=bar_colors, width=0.5, alpha=0.9)
ax2.axhline(np.mean(conv_rates), color=A1, linestyle='--', linewidth=1.3,
            label=f'Avg {np.mean(conv_rates):.1f}%')
ax2.set_title('Stage-to-Stage Conversion Rates (%)', color=TEXT, fontsize=11, pad=10, loc='left')
ax2.legend(facecolor=CARD, edgecolor='none', labelcolor=TEXT, fontsize=8)
ax2.grid(axis='y', alpha=0.3)
for bar,val in zip(bars,conv_rates):
    ax2.text(bar.get_x()+bar.get_width()/2, val+0.5, f'{val:.1f}%',
             ha='center', color=TEXT, fontsize=9, fontweight='bold')

# Channel Conversion
ax3 = fig.add_subplot(gs[2, :2])
ch_s = df.groupby('Channel').agg(Visitors=('Visitors','sum'),Customers=('Customers','sum'))\
        .assign(ConvRate=lambda x: x['Customers']/x['Visitors']*100).sort_values('ConvRate')
ch_colors3 = [CH_C[c] for c in ch_s.index]
bars3 = ax3.barh(ch_s.index, ch_s['ConvRate'], color=ch_colors3, height=0.5, alpha=0.9)
ax3.set_title('Visitor-to-Customer Conversion by Channel (%)', color=TEXT, fontsize=11, pad=10, loc='left')
for bar,val in zip(bars3, ch_s['ConvRate']):
    ax3.text(val+0.05, bar.get_y()+bar.get_height()/2, f'{val:.2f}%', va='center', color=TEXT, fontsize=8.5)
ax3.grid(axis='x', alpha=0.3)

# Revenue by Channel (donut)
ax4 = fig.add_subplot(gs[2, 2:])
ch_rev = df.groupby('Channel')['Revenue'].sum().sort_values(ascending=False)
_,_,autotexts = ax4.pie(ch_rev, autopct='%1.0f%%', startangle=90,
    colors=[CH_C[c] for c in ch_rev.index], pctdistance=0.75,
    wedgeprops=dict(width=0.5,edgecolor=BG,linewidth=2))
for at in autotexts: at.set(color=BG, fontsize=8, fontweight='bold')
ax4.set_title('Revenue Share by Channel', color=TEXT, fontsize=11, pad=10, loc='left')
ax4.legend(ch_rev.index, loc='lower center', fontsize=7, ncol=2,
           facecolor=CARD, edgecolor='none', labelcolor=TEXT, bbox_to_anchor=(0.5,-0.2))

# Monthly Conversion Trend
ax5 = fig.add_subplot(gs[3, :2])
monthly = df.groupby('Month').agg(Visitors=('Visitors','sum'),Customers=('Customers','sum'))\
            .assign(ConvRate=lambda x: x['Customers']/x['Visitors']*100).reset_index().sort_values('Month')
x5 = range(len(monthly))
ax5.fill_between(x5, monthly['ConvRate'], alpha=0.15, color=A1)
ax5.plot(x5, monthly['ConvRate'], color=A1, linewidth=2.5, marker='o',
         markersize=5, markerfacecolor=A2, markeredgecolor=A1)
ax5.set_xticks(x5); ax5.set_xticklabels([m[5:] for m in monthly['Month']], fontsize=7.5, rotation=30)
ax5.axhline(monthly['ConvRate'].mean(), color=A2, linestyle='--', linewidth=1.3,
            label=f"Avg {monthly['ConvRate'].mean():.2f}%")
ax5.set_title('Monthly Conversion Rate Trend (%)', color=TEXT, fontsize=11, pad=10, loc='left')
ax5.legend(facecolor=CARD, edgecolor='none', labelcolor=TEXT, fontsize=8)
ax5.grid(axis='y', alpha=0.3)

# Device Performance
ax6 = fig.add_subplot(gs[3, 2:])
dev = df.groupby('Device').agg(Visitors=('Visitors','sum'),Leads=('Leads','sum'),Customers=('Customers','sum'))\
        .assign(LeadRate=lambda x: x['Leads']/x['Visitors']*100,
                CustRate=lambda x: x['Customers']/x['Visitors']*100).reset_index()
xi6 = np.arange(len(dev)); w6 = 0.3
ax6.bar(xi6-w6/2, dev['LeadRate'], width=w6, color=A1, label='Lead Conv %',     alpha=0.9)
ax6.bar(xi6+w6/2, dev['CustRate'], width=w6, color=A3, label='Customer Conv %', alpha=0.9)
ax6.set_xticks(xi6); ax6.set_xticklabels(dev['Device'], fontsize=10)
ax6.set_title('Conversion Rates by Device', color=TEXT, fontsize=11, pad=10, loc='left')
ax6.legend(facecolor=CARD, edgecolor='none', labelcolor=TEXT, fontsize=8)
ax6.grid(axis='y', alpha=0.3)
for idx, row in dev.iterrows():
    ax6.text(idx-w6/2, row['LeadRate']+0.2, f"{row['LeadRate']:.1f}%", ha='center', color=TEXT, fontsize=8)
    ax6.text(idx+w6/2, row['CustRate']+0.2, f"{row['CustRate']:.1f}%", ha='center', color=A3,   fontsize=8)

plt.savefig('funnel_dashboard.png', dpi=160, bbox_inches='tight', facecolor=BG)
print("Dashboard saved as funnel_dashboard.png")
