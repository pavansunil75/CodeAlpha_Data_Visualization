import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def generate_space_data():
    np.random.seed(42)
    agencies = {
        'NASA':        {'start': 1958, 'peak': 1970, 'color': '#4361ee', 'country': 'USA'},
        'Roscosmos':   {'start': 1957, 'peak': 1975, 'color': '#e63946', 'country': 'Russia'},
        'ESA':         {'start': 1975, 'peak': 2000, 'color': '#ffd700', 'country': 'Europe'},
        'ISRO':        {'start': 1969, 'peak': 2010, 'color': '#f77f00', 'country': 'India'},
        'CNSA':        {'start': 1970, 'peak': 2015, 'color': '#2dc653', 'country': 'China'},
        'SpaceX':      {'start': 2006, 'peak': 2020, 'color': '#adb5bd', 'country': 'USA'},
        'JAXA':        {'start': 1969, 'peak': 2005, 'color': '#bc8cff', 'country': 'Japan'},
        'Arianespace':{'start': 1980, 'peak': 1995, 'color': '#4cc9f0', 'country': 'Europe'},
    }
    mission_types = ['Satellite','Crewed','Probe','Telescope','Lander','Rover','Space Station','Flyby']
    rows = []
    for agency, info in agencies.items():
        years = range(info['start'], 2024)
        for year in years:
            n_missions = max(1, int(np.random.poisson(3 if year >= info['peak'] - 5 else 1.5)))
            for _ in range(n_missions):
                success_prob = 0.95 if year >= 2000 else 0.75 if year >= 1980 else 0.60
                status = np.random.choice(['Success','Failure','Partial Success'],
                                          p=[success_prob, (1-success_prob)*0.7, (1-success_prob)*0.3])
                mtype = np.random.choice(mission_types,
                                         p=[0.35,0.10,0.15,0.08,0.10,0.08,0.05,0.09])
                cost = max(5, np.random.exponential(250 if agency in ['NASA','ESA'] else 150))
                rows.append({
                    'agency':       agency,
                    'country':      info['country'],
                    'year':         year,
                    'mission_type': mtype,
                    'status':       status,
                    'cost_million': round(cost, 1),
                    'duration_days': int(np.random.exponential(180)),
                    'crew_size':    int(np.random.choice([0,0,0,0,2,4,6,7], p=[0.5,0.15,0.1,0.05,0.1,0.05,0.03,0.02])),
                })
    df = pd.DataFrame(rows)
    df['decade'] = (df['year'] // 10 * 10).astype(str) + 's'
    df['is_success'] = (df['status'] == 'Success').astype(int)
    return df

print("=" * 60)
print("DATA VISUALIZATION: SPACE MISSIONS")
print("=" * 60)

df = generate_space_data()
df.to_csv("space_missions.csv", index=False)
print(f"Dataset ready: {len(df)} missions saved as 'space_missions.csv'")
print(f"Agencies : {df['agency'].nunique()}")
print(f"Date range: {df['year'].min()} - {df['year'].max()}")

DARK   = '#0a0a1a'
SPACE  = '#12122a'
GOLD   = '#FFD700'
BLUE   = '#4361ee'
RED    = '#e63946'
GREEN  = '#2dc653'
CYAN   = '#4cc9f0'
WHITE  = '#e0e0f0'

AGENCY_COLORS = {
    'NASA':        '#4361ee',
    'Roscosmos':   '#e63946',
    'ESA':         '#ffd700',
    'ISRO':        '#f77f00',
    'CNSA':        '#2dc653',
    'SpaceX':      '#adb5bd',
    'JAXA':        '#bc8cff',
    'Arianespace': '#4cc9f0',
}

def style_ax(ax, title):
    ax.set_facecolor(SPACE)
    ax.set_title(title, color=WHITE, fontsize=12, fontweight='bold', pad=10)
    ax.tick_params(colors=WHITE)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2a2a4a')

fig = plt.figure(figsize=(22, 20), facecolor=DARK)
fig.suptitle('Space Missions Data Analysis (1957–2023)',
             fontsize=24, fontweight='bold', color=WHITE, y=0.99)

gs = fig.add_gridspec(3, 3, hspace=0.45, wspace=0.35,
                      left=0.06, right=0.97, top=0.95, bottom=0.05)

ax1 = fig.add_subplot(gs[0, 0])
agency_counts = df['agency'].value_counts()
bars = ax1.bar(agency_counts.index,
               agency_counts.values,
               color=[AGENCY_COLORS[a] for a in agency_counts.index],
               edgecolor=DARK, linewidth=0.8)
style_ax(ax1, 'Total Missions by Agency')
ax1.set_ylabel('Number of Missions', color=WHITE)
ax1.tick_params(axis='x', rotation=35)
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 1,
             str(int(bar.get_height())),
             ha='center', color=WHITE, fontsize=8)

ax2 = fig.add_subplot(gs[0, 1])
success_rate = df.groupby('agency')['is_success'].mean().mul(100).sort_values(ascending=False)
colors_sr = [GREEN if r >= 90 else GOLD if r >= 75 else RED for r in success_rate.values]
ax2.barh(success_rate.index[::-1], success_rate.values[::-1],
         color=colors_sr[::-1], edgecolor=DARK)
style_ax(ax2, 'Mission Success Rate by Agency (%)')
ax2.set_xlabel('Success Rate (%)', color=WHITE)
ax2.axvline(success_rate.mean(), color=WHITE, linestyle='--',
            linewidth=1.5, alpha=0.6, label=f"Avg: {success_rate.mean():.1f}%")
ax2.legend(facecolor=SPACE, labelcolor=WHITE, fontsize=8)
for bar in ax2.patches:
    w = bar.get_width()
    ax2.text(w + 0.3, bar.get_y() + bar.get_height()/2,
             f'{w:.1f}%', va='center', color=WHITE, fontsize=8)

ax3 = fig.add_subplot(gs[0, 2])
status_counts = df['status'].value_counts()
wedge_colors  = [GREEN, RED, GOLD]
wedges, texts, autotexts = ax3.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct='%1.1f%%', startangle=90,
    colors=wedge_colors,
    wedgeprops=dict(edgecolor=DARK, linewidth=1.5),
    textprops=dict(color=WHITE, fontsize=10)
)
for at in autotexts:
    at.set_color(WHITE)
    at.set_fontweight('bold')
ax3.set_facecolor(SPACE)
style_ax(ax3, 'Overall Mission Status Distribution')

ax4 = fig.add_subplot(gs[1, :2])
yearly = df.groupby(['year','agency'])['mission_type'].count().reset_index()
yearly.columns = ['year','agency','count']
for agency, color in AGENCY_COLORS.items():
    adf = yearly[yearly['agency'] == agency]
    ax4.plot(adf['year'], adf['count'],
             label=agency, color=color, linewidth=1.8, alpha=0.85)
ax4.axvline(1969, color=GOLD, linestyle='--', linewidth=1.5, alpha=0.7)
ax4.text(1969, ax4.get_ylim()[1] if ax4.get_ylim()[1] > 0 else 10,
         'Moon Landing', color=GOLD, fontsize=7, rotation=90, va='top')
ax4.axvline(2004, color=CYAN, linestyle='--', linewidth=1.5, alpha=0.7)
ax4.text(2004, ax4.get_ylim()[1] if ax4.get_ylim()[1] > 0 else 10,
         'SpaceX Founded', color=CYAN, fontsize=7, rotation=90, va='top')
style_ax(ax4, 'Missions Launched Per Year by Agency (1957–2023)')
ax4.set_xlabel('Year', color=WHITE)
ax4.set_ylabel('Number of Missions', color=WHITE)
ax4.legend(facecolor=SPACE, labelcolor=WHITE, fontsize=7,
           loc='upper left', ncol=2)

ax5 = fig.add_subplot(gs[1, 2])
type_counts = df['mission_type'].value_counts()
wedge_colors2 = sns.color_palette('husl', len(type_counts))
wedges2, texts2, autotexts2 = ax5.pie(
    type_counts.values,
    labels=type_counts.index,
    autopct='%1.0f%%', startangle=140,
    pctdistance=0.8,
    colors=wedge_colors2,
    wedgeprops=dict(edgecolor=DARK, linewidth=1),
    textprops=dict(color=WHITE, fontsize=8)
)
for at in autotexts2:
    at.set_fontweight('bold')
ax5.set_facecolor(SPACE)
style_ax(ax5, 'Mission Type Breakdown')

ax6 = fig.add_subplot(gs[2, 0])
decade_agency = df.groupby(['decade','agency']).size().unstack(fill_value=0)
decade_agency.plot(kind='bar', ax=ax6, stacked=True,
                   color=[AGENCY_COLORS[a] for a in decade_agency.columns],
                   edgecolor=DARK, linewidth=0.5)
style_ax(ax6, 'Missions per Decade by Agency (Stacked)')
ax6.set_xlabel('Decade', color=WHITE)
ax6.set_ylabel('Number of Missions', color=WHITE)
ax6.tick_params(axis='x', rotation=30)
ax6.legend(facecolor=SPACE, labelcolor=WHITE, fontsize=7,
           loc='upper left', ncol=2)

ax7 = fig.add_subplot(gs[2, 1])
success_decade = df.groupby('decade')['is_success'].mean().mul(100)
ax7.plot(success_decade.index, success_decade.values,
         marker='o', color=GREEN, linewidth=2.5, markersize=8)
ax7.fill_between(range(len(success_decade)),
                 success_decade.values, alpha=0.2, color=GREEN)
style_ax(ax7, 'Success Rate Improvement Over Decades (%)')
ax7.set_xlabel('Decade', color=WHITE)
ax7.set_ylabel('Success Rate (%)', color=WHITE)
ax7.tick_params(axis='x', rotation=20)
for i, (dec, val) in enumerate(success_decade.items()):
    ax7.text(i, val + 0.5, f'{val:.0f}%', ha='center', color=WHITE, fontsize=8)

ax8 = fig.add_subplot(gs[2, 2])
top_cost = df.groupby('agency')['cost_million'].mean().sort_values(ascending=False)
ax8.bar(top_cost.index, top_cost.values,
        color=[AGENCY_COLORS[a] for a in top_cost.index],
        edgecolor=DARK)
style_ax(ax8, 'Average Mission Cost by Agency (Million $)')
ax8.set_ylabel('Avg Cost (Million $)', color=WHITE)
ax8.tick_params(axis='x', rotation=35)
for bar in ax8.patches:
    ax8.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 2,
             f'${bar.get_height():.0f}M',
             ha='center', color=WHITE, fontsize=7)

plt.savefig('space_missions_visualization.png', dpi=150,
            bbox_inches='tight', facecolor=DARK)
plt.show()
print("\nPlot saved as 'space_missions_visualization.png'")

print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)
print(f"  Total missions tracked    : {len(df)}")
print(f"  Year range                : {df['year'].min()} – {df['year'].max()}")
print(f"  Most active agency        : {agency_counts.idxmax()} ({agency_counts.max()} missions)")
print(f"  Highest success rate      : {success_rate.idxmax()} ({success_rate.max():.1f}%)")
print(f"  Most common mission type  : {df['mission_type'].value_counts().idxmax()}")
print(f"  Overall success rate      : {df['is_success'].mean()*100:.1f}%")
print(f"  Most expensive agency avg : {top_cost.idxmax()} (${top_cost.max():.0f}M)")
print("=" * 60)
