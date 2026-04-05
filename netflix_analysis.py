import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.stats import skew, kurtosis, norm

# ── Page Config ──
st.set_page_config(page_title="NETFLIX | Streaming Data Analytics", page_icon="🎬", layout="wide", initial_sidebar_state="collapsed")

# ═══════════════════════════════════════════════════════
# NETFLIX CSS — faithful to the real thing
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
.stApp { background: #141414 !important; color: #fff !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header, .stDeployButton { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #141414; }
::-webkit-scrollbar-thumb { background: #E50914; border-radius: 3px; }

/* ── Typography ── */
h1, h2, h3 { color: #fff !important; font-family: 'Inter', sans-serif !important; }
p, span, label, .stMarkdown { color: #e5e5e5 !important; }

/* ── Netflix Intro Overlay (CSS-only, no sleep) ── */
@keyframes introFadeOut {
    0%   { opacity: 1; }
    70%  { opacity: 1; }
    100% { opacity: 0; pointer-events: none; }
}
@keyframes introN {
    0%   { transform: scale(0.3); opacity: 0; }
    30%  { transform: scale(1.15); opacity: 1; }
    50%  { transform: scale(1); }
    70%  { transform: scale(1); opacity: 1; }
    100% { transform: scale(1); opacity: 0; }
}
@keyframes introText {
    0%   { opacity: 0; transform: translateY(20px); }
    40%  { opacity: 0; transform: translateY(20px); }
    60%  { opacity: 1; transform: translateY(0); }
    80%  { opacity: 1; }
    100% { opacity: 0; }
}
.intro-overlay {
    position: fixed; inset: 0; z-index: 99999;
    background: #000; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    animation: introFadeOut 4s ease-in-out forwards;
    pointer-events: none;
}
.intro-n {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 14rem; color: #E50914; line-height: 1;
    text-shadow: 0 0 80px rgba(229,9,20,0.6), 0 0 200px rgba(229,9,20,0.2);
    animation: introN 3.8s ease-out forwards;
}
.intro-sub {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem; color: #E50914; letter-spacing: 12px;
    animation: introText 3.8s ease-out forwards;
}

/* ── Buttons (Netflix-style) ── */
div.stButton > button {
    background: rgba(255,255,255,0.1) !important;
    color: #fff !important; border: none !important;
    border-radius: 4px !important; font-weight: 600 !important;
    font-size: 0.85rem !important; padding: 8px 22px !important;
    transition: background 0.2s !important;
}
div.stButton > button:hover {
    background: #E50914 !important;
    transform: none !important; box-shadow: none !important;
}

/* Primary play buttons */
div.stButton > button[kind="primary"],
.play-button > button {
    background: #fff !important; color: #000 !important;
    font-weight: 700 !important; font-size: 1rem !important;
    padding: 10px 30px !important;
}
.play-button > button:hover { background: #e0e0e0 !important; color: #000 !important; }

/* Back button */
.back-button > button {
    background: transparent !important; color: #999 !important;
    border: 1px solid #555 !important; font-size: 0.85rem !important;
}
.back-button > button:hover { color: #fff !important; border-color: #fff !important; background: transparent !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #1a1a1a !important; border: 1px solid #2a2a2a !important;
    border-radius: 8px !important; padding: 16px !important;
}
[data-testid="stMetricLabel"] { color: #999 !important; font-size: 0.8rem !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
[data-testid="stMetricValue"] { color: #fff !important; }

/* ── Selectbox / Slider / Number Input ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #2a2a2a !important; color: #fff !important; border: 1px solid #444 !important; border-radius: 4px !important;
}
.stSelectbox label, .stNumberInput label, .stSlider label { color: #999 !important; }

/* ── Expander ── */
[data-testid="stExpander"] { background: #1a1a1a !important; border: 1px solid #2a2a2a !important; border-radius: 8px !important; }

/* ── Dataframe ── */
.stDataFrame { border: 1px solid #2a2a2a !important; border-radius: 6px !important; }

/* ── Alert boxes ── */
.stAlert { background: #1a1a1a !important; border-left-color: #E50914 !important; color: #e5e5e5 !important; }

/* ── Divider ── */
hr { border-color: #2a2a2a !important; }

/* ── Tile card hover effect ── */
.tile-card {
    background: #1a1a1a; border-radius: 4px; overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer; position: relative;
}
.tile-card:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 30px rgba(0,0,0,0.7);
    z-index: 10;
}
.tile-gradient {
    height: 140px; display: flex; align-items: center; justify-content: center;
    font-size: 2.8rem; position: relative;
}
.tile-badge {
    position: absolute; top: 8px; left: 8px;
    background: #E50914; color: #fff; padding: 2px 8px;
    border-radius: 2px; font-size: 0.65rem; font-weight: 700;
    letter-spacing: 1px; text-transform: uppercase;
}
.tile-body { padding: 12px; }
.tile-title { color: #fff; font-weight: 600; font-size: 0.95rem; margin-bottom: 4px; }
.tile-desc { color: #808080; font-size: 0.72rem; line-height: 1.4; }

/* ── Now-playing header ── */
.np-bar {
    background: linear-gradient(180deg, rgba(0,0,0,0.8) 0%, #141414 100%);
    padding: 24px 0; margin-bottom: 20px;
}
.np-badge {
    display: inline-block; background: #E50914; color: #fff;
    padding: 3px 10px; border-radius: 3px; font-size: 0.7rem;
    font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
}
.np-title {
    font-size: 2rem; font-weight: 700; color: #fff; margin: 8px 0 4px 0;
}
.np-desc { color: #999; font-size: 0.9rem; }

/* ── Tags ── */
.tag { display: inline-block; background: #2a2a2a; color: #999; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; margin-right: 6px; }

/* ── Footer ── */
.nf-footer { text-align: center; color: #444; font-size: 0.75rem; padding: 30px 0 10px 0; }
</style>
""", unsafe_allow_html=True)

# ── Intro overlay (pure CSS, no sleep/rerun) ──
st.markdown("""
<div class="intro-overlay">
    <div class="intro-n">N</div>
    <div class="intro-sub">DATA ANALYTICS LAB</div>
</div>
<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3" type="audio/mpeg"></audio>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# DARK MATPLOTLIB
# ═══════════════════════════════════════════════════════
plt.rcParams.update({
    'figure.facecolor': '#141414', 'axes.facecolor': '#1a1a1a',
    'axes.edgecolor': '#333', 'axes.labelcolor': '#ccc',
    'text.color': '#fff', 'xtick.color': '#888', 'ytick.color': '#888',
    'grid.color': '#252525', 'grid.alpha': 0.4, 'axes.grid': True,
    'grid.linestyle': '--', 'figure.figsize': (10, 5),
})
NRED = '#E50914'
NGREY = '#808080'
NGREEN = '#46d369'


# ═══════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2021/2021-04-20/netflix_titles.csv"
    df = pd.read_csv(url)
    def parse_duration(dur):
        if pd.isna(dur): return np.nan
        if 'min' in dur: return float(dur.replace(' min', ''))
        if 'Season' in dur: return float(dur.replace(' Season', '').replace('s', ''))
        return np.nan
    df['duration_num'] = df['duration'].apply(parse_duration)
    df['type_code'] = df['type'].map({'Movie': 0, 'TV Show': 1})
    df = df.dropna(subset=['duration_num', 'release_year'])
    return df

df = load_data()


# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════
if 'exp' not in st.session_state:
    st.session_state.exp = None


# ═══════════════════════════════════════════════════════
# EXPERIMENT METADATA
# ═══════════════════════════════════════════════════════
EXPS = [
    {"key": "exp1", "num": "01", "icon": "📊", "title": "Box Plot Analysis",
     "desc": "Detect outliers and visualize data spread across Netflix content features.",
     "tags": ["Visualization", "Outliers", "Descriptive Stats"],
     "bg": "linear-gradient(135deg, #1a1a2e, #16213e)"},
    {"key": "exp2", "num": "02", "icon": "📈", "title": "Linear Regression",
     "desc": "Model the relationship between release year and content duration.",
     "tags": ["Machine Learning", "Prediction", "Supervised"],
     "bg": "linear-gradient(135deg, #2d1b36, #1a1128)"},
    {"key": "exp3", "num": "03", "icon": "🎯", "title": "Sampling Techniques",
     "desc": "Compare Simple Random, Stratified, and Systematic sampling on Netflix data.",
     "tags": ["Statistics", "Sampling", "Data Collection"],
     "bg": "linear-gradient(135deg, #0d2137, #0a1628)"},
    {"key": "exp4", "num": "04", "icon": "🔮", "title": "K-Means Clustering",
     "desc": "Cluster Netflix content based on release year and duration using unsupervised ML.",
     "tags": ["Unsupervised ML", "Clustering", "Patterns"],
     "bg": "linear-gradient(135deg, #1a2e1a, #0f1f0f)"},
    {"key": "exp5", "num": "05", "icon": "🎲", "title": "Probability Distributions",
     "desc": "Analyze continuous probability density and cumulative distribution functions.",
     "tags": ["Probability", "PDF", "CDF"],
     "bg": "linear-gradient(135deg, #2e1a1a, #1f0f0f)"},
    {"key": "exp6", "num": "06", "icon": "📐", "title": "Statistical Properties",
     "desc": "Compute mean, variance, skewness and kurtosis to understand data shape.",
     "tags": ["Central Tendency", "Moments", "Dispersion"],
     "bg": "linear-gradient(135deg, #1a1a2e, #1a0f2e)"},
]


# ═══════════════════════════════════════════════════════
# TOPBAR
# ═══════════════════════════════════════════════════════
def topbar(subtitle=""):
    right = f"<span style='color:#808080;font-size:0.8rem;'>{subtitle}</span>" if subtitle else ""
    st.markdown(f"""<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 0 20px 0;">
        <span style="color:#E50914;font-family:'Bebas Neue',sans-serif;font-size:2.2rem;letter-spacing:3px;">NETFLIX</span>
        {right}
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# BROWSE VIEW
# ═══════════════════════════════════════════════════════
def browse():
    topbar("🔬 TY AI-DS B3 Data Analytics Lab  ·  Sohom Mallick 16014223083")

    # ── Hero ──
    st.markdown(f"""
    <div style="background:linear-gradient(to right,#000 20%,transparent),
                linear-gradient(to top,#141414 5%,transparent),
                linear-gradient(135deg,#1a0000 0%,#0d0d0d 50%,#000 100%);
                padding:50px 35px;border-radius:6px;margin-bottom:30px;min-height:280px;
                display:flex;flex-direction:column;justify-content:flex-end;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
            <span style="color:#46d369;font-weight:700;font-size:0.85rem;">98% Match</span>
            <span style="color:#888;font-size:0.85rem;">2025</span>
            <span style="border:1px solid #666;color:#888;padding:0 5px;font-size:0.75rem;">DAL</span>
            <span style="color:#888;font-size:0.85rem;">6 Experiments</span>
        </div>
        <div style="font-size:3rem;font-weight:900;color:#fff;line-height:1.1;margin-bottom:8px;
                    font-family:'Bebas Neue',sans-serif;letter-spacing:3px;">NETFLIX STREAMING DATA ANALYTICS</div>
        <div style="color:#b3b3b3;font-size:0.95rem;max-width:550px;line-height:1.6;">
            Six data science experiments exploring Netflix content — from statistical 
            distributions and regression models to clustering and sampling techniques.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero buttons ──
    c1, c2, _ = st.columns([1, 1, 5])
    with c1:
        st.markdown('<div class="play-button">', unsafe_allow_html=True)
        if st.button("▶  Play", key="hero_play", use_container_width=True):
            st.session_state.exp = "exp1"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.button("ℹ  More Info", key="hero_info", use_container_width=True):
            st.session_state.exp = "exp1"
            st.rerun()

    # ── Experiment row ──
    st.markdown("<div style='font-size:1.15rem;font-weight:600;color:#e5e5e5;margin:30px 0 12px 0;'>All Experiments</div>", unsafe_allow_html=True)
    cols = st.columns(6, gap="small")
    for i, e in enumerate(EXPS):
        with cols[i]:
            st.markdown(f"""
            <div class="tile-card">
                <div class="tile-gradient" style="background:{e['bg']};">
                    <span class="tile-badge">EXP {e['num']}</span>
                    {e['icon']}
                </div>
                <div class="tile-body">
                    <div class="tile-title">{e['title']}</div>
                    <div class="tile-desc">{e['desc'][:70]}…</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"▶  Play", key=f"tile_{e['key']}", use_container_width=True):
                st.session_state.exp = e['key']
                st.rerun()

    # ── Quick stats ──
    st.markdown("<div style='font-size:1.15rem;font-weight:600;color:#e5e5e5;margin:35px 0 12px 0;'>Dataset at a Glance</div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Titles", f"{len(df):,}")
    m2.metric("Movies", f"{len(df[df['type']=='Movie']):,}")
    m3.metric("TV Shows", f"{len(df[df['type']=='TV Show']):,}")
    m4.metric("Avg Duration", f"{df['duration_num'].mean():.0f} min")

    st.markdown('<div class="nf-footer">Somaiya Vidyavihar University · Netflix Dataset Analysis · Data Analytics Lab</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# EXPERIMENT PLAYER VIEW
# ═══════════════════════════════════════════════════════
def play(exp_key):
    e = next(x for x in EXPS if x['key'] == exp_key)
    topbar(f"Now Playing · {e['title']}")

    # Back button
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("← Back to Browse", key="back"):
        st.session_state.exp = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Now-playing bar
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in e['tags'])
    st.markdown(f"""
    <div class="np-bar">
        <span class="np-badge">● NOW PLAYING</span>
        <div class="np-title">{e['icon']}  Exp {e['num']}: {e['title']}</div>
        <div class="np-desc">{e['desc']}</div>
        <div style="margin-top:10px;">{tags_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # Render experiment
    {"exp1": render_exp1, "exp2": render_exp2, "exp3": render_exp3,
     "exp4": render_exp4, "exp5": render_exp5, "exp6": render_exp6}[exp_key]()

    # ── Up Next ──
    st.markdown("---")
    keys = [x['key'] for x in EXPS]
    nxt = EXPS[(keys.index(exp_key) + 1) % len(EXPS)]
    st.markdown(f"""
    <div style="color:#808080;font-size:0.75rem;text-transform:uppercase;letter-spacing:2px;margin-bottom:6px;">Up Next</div>
    <div style="background:{nxt['bg']};padding:18px 22px;border-radius:6px;display:flex;align-items:center;gap:14px;max-width:400px;">
        <span style="font-size:2rem;">{nxt['icon']}</span>
        <div>
            <div style="color:#fff;font-weight:600;font-size:0.95rem;">Exp {nxt['num']}: {nxt['title']}</div>
            <div style="color:#999;font-size:0.75rem;">{nxt['desc'][:60]}…</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"▶  Play Next", key="next"):
        st.session_state.exp = nxt['key']
        st.rerun()

    st.markdown('<div class="nf-footer">Somaiya Vidyavihar University · Netflix Dataset Analysis · Data Analytics Lab</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# EXPERIMENT RENDERERS
# ═══════════════════════════════════════════════════════

def render_exp1():
    target_col = st.selectbox("Select Feature", ['duration_num', 'release_year'], key="e1_feat")
    c1, c2 = st.columns([2, 1])
    with c1:
        fig, ax = plt.subplots()
        sns.boxplot(x=df[target_col], ax=ax, color=NRED,
                    flierprops=dict(markerfacecolor=NRED, markersize=4),
                    boxprops=dict(facecolor=NRED, alpha=0.7),
                    medianprops=dict(color='#fff', linewidth=2))
        ax.set_title(f"Box Plot — {target_col}", fontweight='bold', pad=12)
        plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown("#### Summary Statistics")
        stats = df[target_col].describe()
        for name, val in stats.items():
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #222;'>"
                        f"<span style='color:#808080;text-transform:capitalize;'>{name}</span>"
                        f"<span style='color:#fff;font-weight:600;'>{val:.2f}</span></div>", unsafe_allow_html=True)
    with st.expander("🔍 Outlier Details"):
        Q1, Q3 = df[target_col].quantile(0.25), df[target_col].quantile(0.75)
        IQR = Q3 - Q1
        out = df[(df[target_col] < Q1 - 1.5*IQR) | (df[target_col] > Q3 + 1.5*IQR)]
        st.write(f"**IQR:** {IQR:.2f} · **Fences:** [{Q1-1.5*IQR:.2f}, {Q3+1.5*IQR:.2f}] · **Outliers:** {len(out)}")


def render_exp2():
    X = df[['release_year']].values; y = df['duration_num'].values
    model = LinearRegression().fit(X, y); y_pred = model.predict(X)
    c1, c2 = st.columns([2, 1])
    with c1:
        fig, ax = plt.subplots()
        ax.scatter(X, y, color='#444', alpha=0.3, s=8)
        ax.plot(X, y_pred, color=NRED, linewidth=3, zorder=5)
        ax.fill_between(X.flatten(), y_pred - np.std(y-y_pred), y_pred + np.std(y-y_pred), alpha=0.08, color=NRED)
        ax.set_xlabel("Release Year"); ax.set_ylabel("Duration")
        ax.set_title("Linear Regression — Year vs Duration", fontweight='bold', pad=12)
        plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown("#### Model Metrics")
        st.metric("R² Score", f"{model.score(X, y):.4f}")
        st.metric("Slope", f"{model.coef_[0]:.4f}")
        st.metric("Intercept", f"{model.intercept_:.2f}")
        st.latex(f"y = {model.coef_[0]:.4f}x + {model.intercept_:.2f}")


def render_exp3():
    c1, c2 = st.columns(2)
    with c1:
        method = st.selectbox("Sampling Method", ["Simple Random", "Stratified (by Type)", "Systematic"], key="e3_m")
    with c2:
        n = st.number_input("Sample Size", 5, len(df), 50, key="e3_n")

    if method == "Simple Random":
        sample = df.sample(n=n, random_state=42); info = "Equal probability selection."
    elif method == "Stratified (by Type)":
        sample = df.groupby('type', group_keys=False).apply(lambda x: x.sample(frac=n/len(df), random_state=42))
        info = "Proportional samples from each stratum."
    else:
        step = max(1, len(df) // n); sample = df.iloc[::step].head(n)
        info = f"Every {step}th element selected."

    st.markdown(f"""<div style="background:#1a1a1a;border-left:3px solid {NRED};padding:12px 18px;border-radius:4px;margin:12px 0;">
        <span style="color:{NRED};font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;">{method}</span>
        <span style="color:#808080;font-size:0.85rem;margin-left:10px;">{info}</span>
        <span style="color:{NGREEN};font-weight:600;float:right;">✓ {len(sample)} / {len(df)}</span>
    </div>""", unsafe_allow_html=True)

    l, r = st.columns([2, 1])
    with l:
        st.dataframe(sample[['type','title','release_year','duration']].reset_index(drop=True), use_container_width=True, height=380)
    with r:
        st.markdown("#### Sample vs Population")
        fig, axes = plt.subplots(2, 1, figsize=(5, 5))
        for ax_i, (col, title) in enumerate([('type', 'Type Split'), ('release_year', 'Year Spread')]):
            ax = axes[ax_i]
            if col == 'type':
                pop = df[col].value_counts(normalize=True); samp_v = sample[col].value_counts(normalize=True)
                x = range(len(pop)); w = 0.35
                ax.bar([i-w/2 for i in x], pop.values, w, color='#444', label='Pop')
                ax.bar([i+w/2 for i in x], [samp_v.get(t,0) for t in pop.index], w, color=NRED, label='Sample')
                ax.set_xticks(x); ax.set_xticklabels(pop.index)
            else:
                ax.hist(df[col], bins=20, alpha=0.4, color='#444', density=True, label='Pop')
                ax.hist(sample[col], bins=20, alpha=0.7, color=NRED, density=True, label='Sample')
            ax.set_title(title, fontsize=10, fontweight='bold')
            ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white', fontsize=7)
        plt.tight_layout(); st.pyplot(fig)


def render_exp4():
    K = st.slider("Number of Clusters (K)", 2, 10, 5, key="e4_k")
    X_c = df[['release_year','duration_num']].copy()
    scaler = StandardScaler(); X_s = scaler.fit_transform(X_c)
    km = KMeans(n_clusters=K, random_state=42, n_init=10); labels = km.fit_predict(X_s)
    df_p = df.copy(); df_p['cluster'] = labels

    palette = [NRED, NGREEN, '#4facfe', '#f5576c', '#fee140', '#a18cd1', '#43e97b', '#fa709a', '#667eea', '#38f9d7']

    c1, c2 = st.columns([2, 1])
    with c1:
        fig, ax = plt.subplots()
        ax.scatter(df_p['release_year'], df_p['duration_num'], c=labels,
                   cmap=plt.cm.colors.ListedColormap(palette[:K]), alpha=0.5, s=12)
        centers = scaler.inverse_transform(km.cluster_centers_)
        ax.scatter(centers[:,0], centers[:,1], c='#fff', marker='X', s=180, edgecolors=NRED, linewidths=2, zorder=5, label='Centroids')
        ax.set_xlabel("Release Year"); ax.set_ylabel("Duration")
        ax.set_title(f"K-Means Clustering (K={K})", fontweight='bold', pad=12)
        ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white'); plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown("#### Cluster Summary")
        for i in range(K):
            cd = df_p[df_p['cluster']==i]
            st.markdown(f"""<div style="background:#1a1a1a;border-left:3px solid {palette[i]};padding:8px 12px;border-radius:4px;margin-bottom:6px;">
                <span style="color:{palette[i]};font-weight:700;font-size:0.8rem;">Cluster {i}</span>
                <span style="color:#808080;font-size:0.72rem;margin-left:8px;">{len(cd)} items · Year ~{cd['release_year'].mean():.0f} · Dur ~{cd['duration_num'].mean():.0f}</span>
            </div>""", unsafe_allow_html=True)
        with st.expander("📈 Elbow Method"):
            inertias = [KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_s).inertia_ for k in range(2,11)]
            fig2, ax2 = plt.subplots(figsize=(5,3))
            ax2.plot(range(2,11), inertias, 'o-', color=NRED, linewidth=2, markersize=5)
            ax2.axvline(x=K, color=NGREEN, linestyle='--', alpha=0.7)
            ax2.set_xlabel("K"); ax2.set_ylabel("Inertia"); ax2.set_title("Elbow Method", fontsize=10, fontweight='bold')
            plt.tight_layout(); st.pyplot(fig2)


def render_exp5():
    data = df['duration_num']
    c1, c2 = st.columns([2, 1])
    with c1:
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
        sns.histplot(data, kde=True, color=NRED, stat="density", ax=axes[0], alpha=0.4, edgecolor='none')
        axes[0].set_title("Probability Density (PDF)", fontweight='bold')
        sorted_d = np.sort(data); cdf = np.arange(1, len(sorted_d)+1)/len(sorted_d)
        axes[1].plot(sorted_d, cdf, color=NGREEN, linewidth=2)
        axes[1].fill_between(sorted_d, cdf, alpha=0.08, color=NGREEN)
        axes[1].set_title("Cumulative Distribution (CDF)", fontweight='bold')
        axes[1].set_ylabel("Probability")
        plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown("#### Distribution Insights")
        st.metric("Mean", f"{data.mean():.2f}")
        st.metric("Median", f"{data.median():.2f}")
        st.metric("Mode", f"{data.mode().iloc[0]:.0f}")
        st.markdown("#### Normal Fit Overlay")
        fig2, ax2 = plt.subplots(figsize=(5,3))
        sns.histplot(data, kde=False, stat='density', color=NRED, alpha=0.3, ax=ax2, edgecolor='none')
        xr = np.linspace(data.min(), data.max(), 200)
        ax2.plot(xr, norm.pdf(xr, data.mean(), data.std()), color=NGREEN, linewidth=2)
        ax2.set_title("Normal Overlay", fontsize=10, fontweight='bold')
        plt.tight_layout(); st.pyplot(fig2)


def render_exp6():
    data = df['duration_num']
    sk, ku = skew(data), kurtosis(data)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Mean", f"{data.mean():.2f}")
    m2.metric("Variance", f"{data.var():.2f}")
    m3.metric("Std Dev", f"{data.std():.2f}")
    m4.metric("Skewness", f"{sk:.2f}")
    m5.metric("Kurtosis", f"{ku:.2f}")

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        sns.histplot(data, kde=True, color=NRED, alpha=0.35, ax=ax, edgecolor='none', bins=40)
        ax.axvline(data.mean(), color=NGREEN, linewidth=2, linestyle='--', label=f'Mean {data.mean():.0f}')
        ax.axvline(data.median(), color='#4facfe', linewidth=2, linestyle='--', label=f'Median {data.median():.0f}')
        ax.set_title("Distribution with Central Tendency", fontweight='bold', pad=12)
        ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white')
        plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown("#### Interpretation")
        sk_text = 'Right-skewed — tail extends right' if sk > 0.5 else ('Left-skewed — tail extends left' if sk < -0.5 else 'Approximately symmetric')
        ku_text = 'Leptokurtic — heavy tails' if ku > 0 else 'Platykurtic — light tails'
        cv = data.std()/data.mean()*100
        st.markdown(f"""<div style="background:#1a1a1a;padding:18px;border-radius:6px;border:1px solid #222;">
            <div style="margin-bottom:14px;"><span style="color:{NRED};font-weight:700;">Skewness = {sk:.2f}</span><br><span style="color:#808080;font-size:0.85rem;">{sk_text}</span></div>
            <div style="margin-bottom:14px;"><span style="color:{NGREEN};font-weight:700;">Kurtosis = {ku:.2f}</span><br><span style="color:#808080;font-size:0.85rem;">{ku_text}</span></div>
            <div><span style="color:#4facfe;font-weight:700;">CV = {cv:.1f}%</span><br><span style="color:#808080;font-size:0.85rem;">Coefficient of Variation</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Violin vs Box Plot")
    fig2, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    sns.violinplot(x=data, ax=axes[0], color=NRED, inner='quartile')
    axes[0].set_title("Violin Plot", fontweight='bold')
    sns.boxplot(x=data, ax=axes[1], color=NRED,
                flierprops=dict(markerfacecolor=NRED, markersize=3),
                boxprops=dict(facecolor=NRED, alpha=0.7),
                medianprops=dict(color='#fff', linewidth=2))
    axes[1].set_title("Box Plot", fontweight='bold')
    plt.tight_layout(); st.pyplot(fig2)


# ═══════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════
if st.session_state.exp is None:
    browse()
else:
    play(st.session_state.exp)