# =============================================================================
# CodeAlpha Data Analytics Internship
# TASK 3 — Data Visualization
# Dataset : IPL 2025 Batting Statistics
# Tools   : Python, Pandas, Matplotlib, Seaborn
# Author  : [Your Name]
# =============================================================================

# pip install pandas matplotlib seaborn numpy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')
os.makedirs('charts', exist_ok=True)

# ── Global style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.dpi'       : 150,
    'font.family'      : 'DejaVu Sans',
    'axes.titlesize'   : 14,
    'axes.titleweight' : 'bold',
    'axes.labelsize'   : 11,
    'xtick.labelsize'  : 9,
    'ytick.labelsize'  : 9,
})

TEAM_COLORS = {
    'GT'  : '#1D4ED8', 'MI'  : '#1E3A8A', 'RCB' : '#DC2626',
    'LSG' : '#7C3AED', 'PBKS': '#DB2777', 'RR'  : '#EA580C',
    'DC'  : '#0891B2', 'SRH' : '#D97706', 'KKR' : '#6D28D9',
    'CSK' : '#CA8A04',
}

print("=" * 60)
print("  CodeAlpha — Task 3 : Data Visualization")
print("  IPL 2025 Batting Statistics")
print("=" * 60)

# ── Load & Clean ──────────────────────────────────────────────────────────────
df = pd.read_csv('IPL2025Batters.csv')
df['AVG_num'] = pd.to_numeric(df['AVG'], errors='coerce')
df['HS_num']  = df['HS'].str.replace('*', '', regex=False).astype(int)

print(f"\n✅ Dataset loaded: {df.shape[0]} players, {df.shape[1]} columns\n")

# =============================================================================
# CHART 1 — Horizontal Bar: Top 10 Run Scorers
# =============================================================================
print("[1/8] Chart 1: Top 10 Run Scorers...")

top10 = df.nlargest(10, 'Runs').sort_values('Runs')
colors = [TEAM_COLORS[t] for t in top10['Team']]

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(top10['Player Name'], top10['Runs'], color=colors, edgecolor='white', linewidth=0.6, height=0.65)

for bar, val in zip(bars, top10['Runs']):
    ax.text(bar.get_width() + 8, bar.get_y() + bar.get_height()/2,
            f'{val}', va='center', fontsize=9, fontweight='bold')

legend_patches = [mpatches.Patch(color=TEAM_COLORS[t], label=t) for t in top10['Team'].unique()]
ax.legend(handles=legend_patches, loc='lower right', fontsize=8, ncol=2, title='Team')

ax.set_xlabel('Total Runs', fontsize=11)
ax.set_title('🏏 Top 10 Run Scorers — IPL 2025', fontsize=15, fontweight='bold', pad=15)
ax.set_xlim(0, top10['Runs'].max() + 100)
ax.spines[['top','right']].set_visible(False)
ax.axvline(x=top10['Runs'].mean(), color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.text(top10['Runs'].mean() + 5, 0.2, 'Avg', color='gray', fontsize=8)

plt.tight_layout()
plt.savefig('charts/chart1_top10_run_scorers.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart1_top10_run_scorers.png")

# =============================================================================
# CHART 2 — Bar Chart: Total Runs Per Team
# =============================================================================
print("[2/8] Chart 2: Total Runs Per Team...")

team_runs = df.groupby('Team')['Runs'].sum().sort_values(ascending=False).reset_index()
clrs = [TEAM_COLORS[t] for t in team_runs['Team']]

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(team_runs['Team'], team_runs['Runs'], color=clrs, edgecolor='white', linewidth=0.8, width=0.65)

for bar, val in zip(bars, team_runs['Runs']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'{val:,}', ha='center', fontsize=9, fontweight='bold')

ax.axhline(y=team_runs['Runs'].mean(), color='crimson', linestyle='--', linewidth=1.5, label=f"Avg: {team_runs['Runs'].mean():.0f}")
ax.legend(fontsize=9)
ax.set_ylabel('Total Runs', fontsize=11)
ax.set_title('🏆 Total Runs Scored by Each Team — IPL 2025', fontsize=15, fontweight='bold', pad=15)
ax.set_ylim(0, team_runs['Runs'].max() + 350)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('charts/chart2_team_total_runs.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart2_team_total_runs.png")

# =============================================================================
# CHART 3 — Scatter Plot: Strike Rate vs Average
# =============================================================================
print("[3/8] Chart 3: Strike Rate vs Average...")

scatter_df = df[(df['BF'] >= 50) & df['AVG_num'].notna()].copy()
scatter_df['color'] = scatter_df['Team'].map(TEAM_COLORS)

fig, ax = plt.subplots(figsize=(11, 7))

for team, grp in scatter_df.groupby('Team'):
    ax.scatter(grp['AVG_num'], grp['SR'], color=TEAM_COLORS[team],
               s=grp['Runs']/4, alpha=0.75, edgecolors='white', linewidth=0.5, label=team)

# Label top players
top_players = scatter_df.nlargest(8, 'Runs')
for _, row in top_players.iterrows():
    ax.annotate(row['Player Name'].split()[-1],
                xy=(row['AVG_num'], row['SR']),
                xytext=(5, 4), textcoords='offset points',
                fontsize=7.5, color='#1f2937')

ax.axhline(y=scatter_df['SR'].mean(), color='gray', linestyle='--', alpha=0.4, linewidth=1)
ax.axvline(x=scatter_df['AVG_num'].mean(), color='gray', linestyle='--', alpha=0.4, linewidth=1)
ax.text(scatter_df['AVG_num'].mean()+0.5, scatter_df['SR'].min()+5, 'Avg AVG', fontsize=7.5, color='gray')

ax.set_xlabel('Batting Average', fontsize=11)
ax.set_ylabel('Strike Rate', fontsize=11)
ax.set_title('⚡ Strike Rate vs Batting Average — IPL 2025\n(bubble size = total runs)', fontsize=13, fontweight='bold', pad=12)
ax.legend(loc='upper left', fontsize=7.5, ncol=2, title='Team', title_fontsize=8)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('charts/chart3_sr_vs_avg_scatter.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart3_sr_vs_avg_scatter.png")

# =============================================================================
# CHART 4 — Box Plot: Run Distribution Per Team
# =============================================================================
print("[4/8] Chart 4: Run Distribution Per Team...")

team_order = df.groupby('Team')['Runs'].median().sort_values(ascending=False).index.tolist()

fig, ax = plt.subplots(figsize=(13, 7))
bp = ax.boxplot(
    [df[df['Team'] == t]['Runs'].values for t in team_order],
    labels=team_order,
    patch_artist=True,
    medianprops=dict(color='white', linewidth=2),
    whiskerprops=dict(linewidth=1.2),
    capprops=dict(linewidth=1.5),
    flierprops=dict(marker='o', markersize=4, alpha=0.5)
)

for patch, team in zip(bp['boxes'], team_order):
    patch.set_facecolor(TEAM_COLORS[team])
    patch.set_alpha(0.85)

ax.set_ylabel('Runs Scored', fontsize=11)
ax.set_xlabel('Team', fontsize=11)
ax.set_title('📦 Run Distribution per Team — IPL 2025\n(Median line shown in white)', fontsize=14, fontweight='bold', pad=12)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('charts/chart4_run_distribution_boxplot.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart4_run_distribution_boxplot.png")

# =============================================================================
# CHART 5 — Heatmap: Correlation Matrix
# =============================================================================
print("[5/8] Chart 5: Correlation Heatmap...")

corr_cols = ['Runs', 'Matches', 'Inn', 'BF', 'SR', '100s', '50s', '4s', '6s', 'AVG_num']
corr_labels = ['Runs', 'Matches', 'Innings', 'Balls\nFaced', 'Strike\nRate',
               'Centuries', 'Fifties', 'Fours', 'Sixes', 'Average']
corr_matrix = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(11, 9))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

sns.heatmap(corr_matrix,
            annot=True, fmt='.2f',
            cmap='RdYlGn', center=0,
            vmin=-1, vmax=1,
            linewidths=0.5, linecolor='white',
            ax=ax,
            xticklabels=corr_labels,
            yticklabels=corr_labels,
            annot_kws={'size': 9})

ax.set_title('🔥 Correlation Heatmap — IPL 2025 Batting Stats', fontsize=14, fontweight='bold', pad=15)
plt.xticks(rotation=0, ha='center')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('charts/chart5_correlation_heatmap.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart5_correlation_heatmap.png")

# =============================================================================
# CHART 6 — Stacked Bar: Team 4s vs 6s
# =============================================================================
print("[6/8] Chart 6: Team Boundaries (4s vs 6s)...")

b_stats = df.groupby('Team').agg(Fours=('4s','sum'), Sixes=('6s','sum')).reset_index()
b_stats = b_stats.sort_values('Fours', ascending=False)
x = np.arange(len(b_stats))
w = 0.55

fig, ax = plt.subplots(figsize=(12, 6))
p1 = ax.bar(x, b_stats['Fours'], w, label='Fours (4s)', color='#3B82F6', edgecolor='white')
p2 = ax.bar(x, b_stats['Sixes'], w, bottom=b_stats['Fours'], label='Sixes (6s)', color='#F97316', edgecolor='white')

for i, (fours, sixes) in enumerate(zip(b_stats['Fours'], b_stats['Sixes'])):
    ax.text(i, fours/2,            f'{fours}', ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
    ax.text(i, fours + sixes/2,    f'{sixes}', ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
    ax.text(i, fours + sixes + 8,  f'{fours+sixes}', ha='center', fontsize=8, color='#1f2937', fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(b_stats['Team'], fontsize=10)
ax.set_ylabel('Number of Boundaries', fontsize=11)
ax.set_title('🏏 Team-wise Fours (4s) & Sixes (6s) — IPL 2025', fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=10, loc='upper right')
ax.spines[['top','right']].set_visible(False)
ax.set_ylim(0, b_stats[['Fours','Sixes']].sum(axis=1).max() + 60)

plt.tight_layout()
plt.savefig('charts/chart6_team_boundaries_stacked.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart6_team_boundaries_stacked.png")

# =============================================================================
# CHART 7 — Pie Chart: Team Share of Total Runs
# =============================================================================
print("[7/8] Chart 7: Team Share of Total Runs...")

team_total = df.groupby('Team')['Runs'].sum().sort_values(ascending=False)
pie_colors = [TEAM_COLORS[t] for t in team_total.index]
explode    = [0.04] * len(team_total)

fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(
    team_total.values,
    labels=team_total.index,
    autopct='%1.1f%%',
    colors=pie_colors,
    explode=explode,
    startangle=140,
    pctdistance=0.78,
    wedgeprops=dict(edgecolor='white', linewidth=1.5)
)
for at in autotexts:
    at.set_fontsize(8.5)
    at.set_fontweight('bold')
    at.set_color('white')
for t in texts:
    t.set_fontsize(10)
    t.set_fontweight('bold')

ax.set_title('🥧 Team Share of Total Runs — IPL 2025', fontsize=14, fontweight='bold', pad=20)

# Add total in center
total_runs = team_total.sum()
ax.text(0, 0, f'Total\n{total_runs:,}\nruns', ha='center', va='center', fontsize=11,
        fontweight='bold', color='#1f2937')

plt.tight_layout()
plt.savefig('charts/chart7_team_runs_pie.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart7_team_runs_pie.png")

# =============================================================================
# CHART 8 — Histogram: Run Distribution (All Players)
# =============================================================================
print("[8/8] Chart 8: Run Distribution Histogram...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Histogram
ax1 = axes[0]
n, bins, patches = ax1.hist(df['Runs'], bins=20, edgecolor='white', linewidth=0.6, color='#3B82F6')

# Color bars by run range
for patch, left_edge in zip(patches, bins[:-1]):
    if   left_edge < 100:  patch.set_facecolor('#EF4444')
    elif left_edge < 300:  patch.set_facecolor('#F97316')
    elif left_edge < 500:  patch.set_facecolor('#22C55E')
    else:                  patch.set_facecolor('#3B82F6')

ax1.axvline(df['Runs'].mean(),   color='black',  linestyle='--', linewidth=1.5, label=f"Mean: {df['Runs'].mean():.0f}")
ax1.axvline(df['Runs'].median(), color='purple', linestyle=':',  linewidth=1.5, label=f"Median: {df['Runs'].median():.0f}")
ax1.set_xlabel('Runs Scored', fontsize=11)
ax1.set_ylabel('Number of Players', fontsize=11)
ax1.set_title('Run Distribution — All 156 Players', fontsize=12, fontweight='bold')
ax1.legend(fontsize=9)
ax1.spines[['top','right']].set_visible(False)

legend_patches = [
    mpatches.Patch(color='#EF4444', label='0–100 (lower order)'),
    mpatches.Patch(color='#F97316', label='100–300 (middle order)'),
    mpatches.Patch(color='#22C55E', label='300–500 (top order)'),
    mpatches.Patch(color='#3B82F6', label='500+ (elite)'),
]
ax1.legend(handles=legend_patches, fontsize=8, loc='upper right')

# Right: Strike Rate Distribution
ax2 = axes[1]
sr_data = df[df['BF'] >= 20]['SR']
ax2.hist(sr_data, bins=18, color='#6366F1', edgecolor='white', linewidth=0.6)
ax2.axvline(sr_data.mean(),   color='black',  linestyle='--', linewidth=1.5, label=f"Mean SR: {sr_data.mean():.1f}")
ax2.axvline(sr_data.median(), color='crimson',linestyle=':',  linewidth=1.5, label=f"Median SR: {sr_data.median():.1f}")
ax2.set_xlabel('Strike Rate', fontsize=11)
ax2.set_ylabel('Number of Players', fontsize=11)
ax2.set_title('Strike Rate Distribution (min 20 balls)', fontsize=12, fontweight='bold')
ax2.legend(fontsize=9)
ax2.spines[['top','right']].set_visible(False)

fig.suptitle('📊 Player Performance Distribution — IPL 2025', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('charts/chart8_distribution_histograms.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart8_distribution_histograms.png")

# =============================================================================
# BONUS CHART 9 — Top Scorer Per Team (Grouped Bar)
# =============================================================================
print("[Bonus] Chart 9: Top Scorer Per Team...")

top_team = df.loc[df.groupby('Team')['Runs'].idxmax()].sort_values('Runs', ascending=False)
clrs9 = [TEAM_COLORS[t] for t in top_team['Team']]

fig, ax = plt.subplots(figsize=(13, 6))
bars = ax.bar(range(len(top_team)), top_team['Runs'], color=clrs9, edgecolor='white', linewidth=0.6, width=0.65)

for i, (bar, (_, row)) in enumerate(zip(bars, top_team.iterrows())):
    name_short = row['Player Name'].split()[-1]
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
            f'{row["Runs"]}', ha='center', fontsize=9, fontweight='bold')
    ax.text(bar.get_x() + bar.get_width()/2, -45,
            name_short, ha='center', fontsize=8.5, rotation=0, color='#374151')

ax.set_xticks(range(len(top_team)))
ax.set_xticklabels(top_team['Team'], fontsize=10, fontweight='bold')
ax.set_ylabel('Runs', fontsize=11)
ax.set_title('🌟 Top Scorer for Each IPL 2025 Team', fontsize=14, fontweight='bold', pad=15)
ax.spines[['top','right']].set_visible(False)
ax.set_ylim(-70, top_team['Runs'].max() + 100)
ax.axhline(y=top_team['Runs'].mean(), color='gray', linestyle='--', alpha=0.5, linewidth=1)

plt.tight_layout()
plt.savefig('charts/chart9_top_scorer_per_team.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart9_top_scorer_per_team.png")

# =============================================================================
# BONUS CHART 10 — Avg Strike Rate Per Team (Horizontal Bar)
# =============================================================================
print("[Bonus] Chart 10: Avg Strike Rate Per Team...")

avg_sr = df[df['BF'] >= 20].groupby('Team')['SR'].mean().round(2).sort_values()
clrs10 = [TEAM_COLORS[t] for t in avg_sr.index]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(avg_sr.index, avg_sr.values, color=clrs10, edgecolor='white', linewidth=0.6, height=0.6)

for bar, val in zip(bars, avg_sr.values):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val}', va='center', fontsize=9, fontweight='bold')

ax.axvline(x=avg_sr.mean(), color='crimson', linestyle='--', linewidth=1.5, label=f'Overall Avg: {avg_sr.mean():.1f}')
ax.set_xlabel('Average Strike Rate', fontsize=11)
ax.set_title('⚡ Average Team Strike Rate — IPL 2025', fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=9)
ax.set_xlim(0, avg_sr.max() + 20)
ax.spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig('charts/chart10_avg_sr_per_team.png', bbox_inches='tight')
plt.close()
print("   ✅ Saved: charts/chart10_avg_sr_per_team.png")

# =============================================================================
# FINAL SUMMARY
# =============================================================================
charts = sorted(os.listdir('charts'))
print("\n" + "=" * 60)
print("  ✅  TASK 3 — DATA VISUALIZATION COMPLETE!")
print("=" * 60)
print(f"\n  Total charts created: {len(charts)}")
print("\n  Charts saved in charts/ folder:")
for i, c in enumerate(charts, 1):
    print(f"    {i:>2}. {c}")
print()
print("  Charts Summary:")
print("   1. Top 10 Run Scorers          → Horizontal Bar")
print("   2. Team Total Runs             → Bar Chart")
print("   3. Strike Rate vs Average      → Bubble Scatter")
print("   4. Run Distribution Per Team   → Box Plot")
print("   5. Correlation Matrix          → Heatmap")
print("   6. Team Boundaries (4s & 6s)   → Stacked Bar")
print("   7. Team Share of Runs          → Pie Chart")
print("   8. Run & SR Distribution       → Histogram")
print("   9. Top Scorer Per Team         → Bar Chart")
print("  10. Avg Strike Rate Per Team    → Horizontal Bar")
print()
print("=" * 60)
