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
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global ── */
.stApp { background: radial-gradient(circle at 50% -20%, #1a0204 0%, #0d0000 50%, #000 100%) !important; color: #f5f5f5 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header, .stDeployButton { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Typography ── */
h1, h2, h3 { color: #fff !important; font-family: 'Inter', sans-serif !important; font-weight: 800 !important; letter-spacing: -0.5px; }

/* ── Metrics Glassmorphism ── */
[data-testid="stMetric"] {
    background: rgba(20, 20, 20, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important; padding: 20px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(229,9,20,0.5) !important;
}
[data-testid="stMetricValue"] {
    font-size: 2.2rem !important; font-weight: 800 !important;
    background: linear-gradient(90deg, #fff, #aaa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
[data-testid="stMetricLabel"] { color: #888 !important; font-weight: 600 !important; letter-spacing: 1px !important; }

/* ── Cards & Tiles ── */
.tile-card {
    background: rgba(20, 20, 20, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 10px; overflow: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    cursor: pointer; position: relative;
    box-shadow: 0 10px 20px rgba(0,0,0,0.4);
}
.tile-card:hover {
    transform: scale(1.05) translateY(-5px);
    border-color: rgba(255,255,255,0.2);
    box-shadow: 0 20px 40px rgba(0,0,0,0.8), 0 0 20px rgba(229,9,20,0.2);
    z-index: 10;
}
.tile-gradient {
    height: 140px; display: flex; align-items: center; justify-content: center;
    font-size: 2.8rem; position: relative;
}
.tile-badge {
    position: absolute; top: 8px; left: 8px;
    background: rgba(229,9,20,0.9); color: #fff; padding: 3px 10px;
    border-radius: 4px; font-size: 0.65rem; font-weight: 800;
    letter-spacing: 1px; text-transform: uppercase;
    box-shadow: 0 4px 10px rgba(229,9,20,0.5);
}
.tile-body { padding: 16px; }
.tile-title { color: #fff; font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; }
.tile-desc { color: #999; font-size: 0.8rem; line-height: 1.5; }

/* ── Buttons ── */
div.stButton > button {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(10px); color: #fff !important; 
    border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 8px !important; 
    font-weight: 600 !important; transition: all 0.3s ease !important;
}
div.stButton > button:hover {
    background: rgba(229,9,20,0.8) !important; border-color: #E50914 !important;
    box-shadow: 0 0 20px rgba(229,9,20,0.4) !important; transform: translateY(-2px) !important;
}
div.stButton > button[kind="primary"] {
    background: #fff !important; color: #000 !important; border: none !important; font-weight: 800 !important;
}
div.stButton > button[kind="primary"]:hover { 
    background: #e5e5e5 !important; box-shadow: 0 0 20px rgba(255,255,255,0.4) !important; 
}
.play-button > button {
    background: #fff !important; color: #000 !important; font-weight: 800 !important; 
    font-size: 1.1rem !important; padding: 12px 35px !important; border-radius: 8px !important;
}
.play-button > button:hover { background: #ccc !important; transform: scale(1.02) !important; }

/* ── Input elements ── */
.stSelectbox > div > div, .stNumberInput > div > div > input, .stSlider > div > div {
    background: rgba(25,25,25,0.8) !important; border: 1px solid rgba(255,255,255,0.15) !important; 
    color: #fff !important; border-radius: 8px !important;
}
.stSelectbox > div > div:hover {
    border-color: #E50914 !important; box-shadow: 0 0 10px rgba(229,9,20,0.2) !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] { background: rgba(20,20,20,0.6) !important; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 12px !important; }

/* ── Intro ── */
@keyframes introFadeOut { 0% { opacity: 1; } 70% { opacity: 1; } 100% { opacity: 0; pointer-events: none; } }
@keyframes introN { 0% { transform: scale(0.3); opacity: 0; } 30% { transform: scale(1.15); opacity: 1; } 50% { transform: scale(1); } 70% { transform: scale(1); opacity: 1; } 100% { transform: scale(1); opacity: 0; } }
@keyframes introText { 0% { opacity: 0; transform: translateY(20px); } 60% { opacity: 1; transform: translateY(0); } 80% { opacity: 1; } 100% { opacity: 0; } }
.intro-overlay { position: fixed; inset: 0; z-index: 99999; background: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; animation: introFadeOut 4s ease-in-out forwards; pointer-events: none; }
.intro-n { font-family: 'Bebas Neue', sans-serif; font-size: 14rem; color: #E50914; line-height: 1; text-shadow: 0 0 80px rgba(229,9,20,0.6), 0 0 200px rgba(229,9,20,0.2); animation: introN 3.8s ease-out forwards; }
.intro-sub { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; color: #E50914; letter-spacing: 12px; animation: introText 3.8s ease-out forwards; }

.np-bar { background: linear-gradient(180deg, rgba(229,9,20,0.15) 0%, rgba(20,20,20,0.8) 100%); padding: 30px; border-radius: 12px; margin-bottom: 24px; border: 1px solid rgba(255,255,255,0.05); }
.np-badge { display: inline-block; background: #E50914; color: #fff; padding: 4px 12px; border-radius: 4px; font-size: 0.75rem; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; box-shadow: 0 2px 8px rgba(229,9,20,0.5); }
.np-title { font-size: 2.2rem; font-weight: 800; color: #fff; margin: 12px 0 6px 0; letter-spacing: -0.5px; }
.np-desc { color: #aaa; font-size: 1rem; line-height: 1.5;}
.tag { display: inline-block; background: rgba(255,255,255,0.1); backdrop-filter: blur(5px); color: #ddd; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; margin-right: 8px; font-weight: 500; border: 1px solid rgba(255,255,255,0.05); }
.nf-footer { text-align: center; color: #555; font-size: 0.8rem; padding: 40px 0 20px 0; font-weight: 500;}
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
        if st.button("▶  Play", key="hero_play", width='stretch'):
            st.session_state.exp = "exp1"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        if st.button("ℹ  More Info", key="hero_info", width='stretch'):
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
            if st.button(f"▶  Play", key=f"tile_{e['key']}", width='stretch'):
                st.session_state.exp = e['key']
                st.rerun()

    # ── Quick stats ──
    st.markdown("<div style='font-size:1.15rem;font-weight:600;color:#e5e5e5;margin:35px 0 12px 0;'>Dataset at a Glance</div>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Titles", f"{len(df):,}")
    m2.metric("Movies", f"{len(df[df['type']=='Movie']):,}")
    m3.metric("Avg Movie Length", f"{df[df['type']=='Movie']['duration_num'].mean():.0f} mins")
    m4.metric("TV Shows", f"{len(df[df['type']=='TV Show']):,}")
    m5.metric("Avg TV Seasons", f"{df[df['type']=='TV Show']['duration_num'].mean():.1f}")

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
    col1, col2 = st.columns(2)
    with col1: target_col = st.selectbox("Select Feature", ['duration_num', 'release_year'], key="e1_feat")
    with col2: content_type = st.selectbox("Content Type", ["Movie", "TV Show"], key="e1_type")
    
    data = df[df['type'] == content_type]
    unit_label = ("Minutes" if content_type == "Movie" else "Seasons") if target_col == 'duration_num' else "Year"
    
    c1, c2 = st.columns([2, 1])
    with c1:
        fig, ax = plt.subplots()
        sns.boxplot(x=data[target_col], ax=ax, color=NRED,
                    flierprops=dict(markerfacecolor=NRED, markersize=4),
                    boxprops=dict(facecolor=NRED, alpha=0.7),
                    medianprops=dict(color='#fff', linewidth=2))
        ax.set_title(f"Box Plot — {content_type} {target_col}", fontweight='bold', pad=12)
        ax.set_xlabel(unit_label)
        plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown(f"#### Summary Statistics ({content_type}s)")
        stats = data[target_col].describe()
        for name, val in stats.items():
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.1);'>"
                        f"<span style='color:#808080;text-transform:capitalize;'>{name}</span>"
                        f"<span style='color:#fff;font-weight:600;'>{val:.2f}</span></div>", unsafe_allow_html=True)
    with st.expander("🔍 Outlier Details"):
        Q1, Q3 = data[target_col].quantile(0.25), data[target_col].quantile(0.75)
        IQR = Q3 - Q1
        out = data[(data[target_col] < Q1 - 1.5*IQR) | (data[target_col] > Q3 + 1.5*IQR)]
        st.write(f"**IQR:** {IQR:.2f} · **Fences:** [{Q1-1.5*IQR:.2f}, {Q3+1.5*IQR:.2f}] · **Outliers:** {len(out)}")


def render_exp2():
    content_type = st.selectbox("Content Type", ["Movie", "TV Show"], key="e2_type")
    data = df[df['type'] == content_type]
    unit_label = "Minutes" if content_type == "Movie" else "Seasons"
    
    X = data[['release_year']].values; y = data['duration_num'].values
    model = LinearRegression().fit(X, y); y_pred = model.predict(X)
    c1, c2 = st.columns([2, 1])
    with c1:
        fig, ax = plt.subplots()
        ax.scatter(X, y, color='#555', alpha=0.5, s=15, edgecolors='none')
        ax.plot(X, y_pred, color=NRED, linewidth=3, zorder=5)
        ax.fill_between(X.flatten(), y_pred - np.std(y-y_pred), y_pred + np.std(y-y_pred), alpha=0.15, color=NRED)
        ax.set_xlabel("Release Year"); ax.set_ylabel(f"Duration ({unit_label})")
        ax.set_title(f"Linear Regression — Year vs Duration ({content_type}s)", fontweight='bold', pad=12)
        plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown(f"#### Model Metrics ({content_type}s)")
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
        sample = df.groupby('type', group_keys=False).sample(frac=n/len(df), random_state=42)
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
        st.dataframe(sample[['type','title','release_year','duration']].reset_index(drop=True), width='stretch', height=380)
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
                ax.set_ylabel('Proportion', fontsize=8)
            else:
                ax.hist(df[col], bins=20, alpha=0.4, color='#444', density=True, label='Pop')
                ax.hist(sample[col], bins=20, alpha=0.7, color=NRED, density=True, label='Sample')
                ax.set_ylabel('Density', fontsize=8)
            ax.set_title(title, fontsize=10, fontweight='bold')
            ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white', fontsize=7)
        plt.tight_layout(); st.pyplot(fig)


def render_exp4():
    col1, col2 = st.columns(2)
    with col1: K = st.slider("Number of Clusters (K)", 2, 10, 5, key="e4_k")
    with col2: content_type = st.selectbox("Content Type", ["Movie", "TV Show"], key="e4_type")
    
    data = df[df['type'] == content_type]
    unit = "Minutes" if content_type == "Movie" else "Seasons"
    
    X_c = data[['release_year','duration_num']].copy()
    scaler = StandardScaler(); X_s = scaler.fit_transform(X_c)
    km = KMeans(n_clusters=K, random_state=42, n_init=10); labels = km.fit_predict(X_s)
    df_p = data.copy(); df_p['cluster'] = labels

    palette = [NRED, NGREEN, '#4facfe', '#f5576c', '#fee140', '#a18cd1', '#43e97b', '#fa709a', '#667eea', '#38f9d7']

    c1, c2 = st.columns([2, 1])
    with c1:
        fig, ax = plt.subplots()
        ax.scatter(df_p['release_year'], df_p['duration_num'], c=labels,
                   cmap=plt.cm.colors.ListedColormap(palette[:K]), alpha=0.7, s=20, edgecolors='none')
        centers = scaler.inverse_transform(km.cluster_centers_)
        ax.scatter(centers[:,0], centers[:,1], c='#fff', marker='X', s=200, edgecolors=NRED, linewidths=2, zorder=5, label='Centroids')
        ax.set_xlabel("Release Year"); ax.set_ylabel(f"Duration ({unit})")
        ax.set_title(f"K-Means Clustering ({content_type}s, K={K})", fontweight='bold', pad=12)
        ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white'); plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown(f"#### Cluster Summary ({content_type}s)")
        for i in range(K):
            cd = df_p[df_p['cluster']==i]
            st.markdown(f"""<div style="background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);border-left:4px solid {palette[i]};padding:12px;border-radius:6px;margin-bottom:8px;">
                <span style="color:{palette[i]};font-weight:800;font-size:0.9rem;">Cluster {i}</span>
                <div style="color:#aaa;font-size:0.8rem;margin-top:4px;">{len(cd)} items · Year ~{cd['release_year'].mean():.0f} · Dur ~{cd['duration_num'].mean():.0f} {unit}</div>
            </div>""", unsafe_allow_html=True)
        with st.expander("📈 Elbow Method"):
            inertias = [KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_s).inertia_ for k in range(2,11)]
            fig2, ax2 = plt.subplots(figsize=(5,3))
            ax2.plot(range(2,11), inertias, 'o-', color=NRED, linewidth=2, markersize=5)
            ax2.axvline(x=K, color=NGREEN, linestyle='--', alpha=0.7)
            ax2.set_xlabel("K"); ax2.set_ylabel("Inertia"); ax2.set_title("Elbow Method", fontsize=10, fontweight='bold')
            plt.tight_layout(); st.pyplot(fig2)


def render_exp5():
    content_type = st.selectbox("Select Content Type to Analyze", ["Movie", "TV Show"], key="e5_type")
    data = df[df['type'] == content_type]['duration_num']
    unit = "Minutes" if content_type == "Movie" else "Seasons"

    c1, c2 = st.columns([2, 1])
    with c1:
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
        sns.histplot(data, kde=True, color=NRED, stat="density", ax=axes[0], alpha=0.4, edgecolor='none')
        axes[0].set_title(f"Probability Density (PDF) - {content_type}s", fontweight='bold')
        axes[0].set_xlabel(f"Duration ({unit})")
        
        sorted_d = np.sort(data); cdf = np.arange(1, len(sorted_d)+1)/len(sorted_d)
        axes[1].plot(sorted_d, cdf, color=NGREEN, linewidth=2)
        axes[1].fill_between(sorted_d, cdf, alpha=0.08, color=NGREEN)
        axes[1].set_title(f"Cumulative Distribution (CDF) - {content_type}s", fontweight='bold')
        axes[1].set_xlabel(f"Duration ({unit})")
        axes[1].set_ylabel("Probability")
        plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown(f"#### Distribution Insights ({content_type}s)")
        st.metric("Mean", f"{data.mean():.2f} {unit}")
        st.metric("Median", f"{data.median():.2f} {unit}")
        st.metric("Mode", f"{data.mode().iloc[0]:.0f} {unit}")
        
        st.markdown(f"#### Normal Fit Overlay ({content_type}s)")
        fig2, ax2 = plt.subplots(figsize=(5,3))
        sns.histplot(data, kde=False, stat='density', color=NRED, alpha=0.3, ax=ax2, edgecolor='none')
        xr = np.linspace(data.min(), data.max(), 200)
        ax2.plot(xr, norm.pdf(xr, data.mean(), data.std()), color=NGREEN, linewidth=2)
        ax2.set_xlabel(f"Duration ({unit})")
        ax2.set_title("Normal Overlay", fontsize=10, fontweight='bold')
        plt.tight_layout(); st.pyplot(fig2)


def render_exp6():
    content_type = st.selectbox("Content Type to Analyze", ["Movie", "TV Show"], key="e6_type")
    data = df[df['type'] == content_type]['duration_num']
    unit = "Mins" if content_type == "Movie" else "Seasons"
    
    sk, ku = skew(data), kurtosis(data)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric(f"Mean ({unit})", f"{data.mean():.2f}")
    m2.metric(f"Variance", f"{data.var():.2f}")
    m3.metric(f"Std Dev", f"{data.std():.2f}")
    m4.metric("Skewness", f"{sk:.2f}")
    m5.metric("Kurtosis", f"{ku:.2f}")

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots()
        sns.histplot(data, kde=True, color=NRED, alpha=0.5, ax=ax, edgecolor='none', bins=40)
        ax.axvline(data.mean(), color=NGREEN, linewidth=2, linestyle='--', label=f'Mean {data.mean():.0f}')
        ax.axvline(data.median(), color='#4facfe', linewidth=2, linestyle='--', label=f'Median {data.median():.0f}')
        ax.set_title(f"Distribution with Central Tendency ({content_type}s)", fontweight='bold', pad=12)
        ax.set_xlabel(f"Duration ({unit})")
        ax.legend(facecolor='#1a1a1a', edgecolor='#333', labelcolor='white')
        plt.tight_layout(); st.pyplot(fig)
    with c2:
        st.markdown(f"#### Interpretation ({content_type}s)")
        sk_text = 'Right-skewed — tail extends right' if sk > 0.5 else ('Left-skewed — tail extends left' if sk < -0.5 else 'Approximately symmetric')
        ku_text = 'Leptokurtic — heavy tails' if ku > 0 else 'Platykurtic — light tails'
        cv = data.std()/data.mean()*100
        st.markdown(f"""<div style="background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);padding:22px;border-radius:12px;border:1px solid rgba(255,255,255,0.1);box-shadow:0 10px 30px rgba(0,0,0,0.5);">
            <div style="margin-bottom:18px;"><span style="color:{NRED};font-weight:800;font-size:1.1rem;">Skewness = {sk:.2f}</span><br><span style="color:#aaa;font-size:0.9rem;">{sk_text}</span></div>
            <div style="margin-bottom:18px;"><span style="color:{NGREEN};font-weight:800;font-size:1.1rem;">Kurtosis = {ku:.2f}</span><br><span style="color:#aaa;font-size:0.9rem;">{ku_text}</span></div>
            <div><span style="color:#4facfe;font-weight:800;font-size:1.1rem;">CV = {cv:.1f}%</span><br><span style="color:#aaa;font-size:0.9rem;">Coefficient of Variation</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"#### Violin vs Box Plot ({content_type}s)")
    fig2, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    sns.violinplot(x=data, ax=axes[0], color=NRED, inner='quartile')
    axes[0].set_title("Violin Plot", fontweight='bold')
    axes[0].set_xlabel(f"Duration ({unit})")
    
    sns.boxplot(x=data, ax=axes[1], color=NRED,
                flierprops=dict(markerfacecolor=NRED, markersize=3, alpha=0.5),
                boxprops=dict(facecolor=NRED, alpha=0.7),
                medianprops=dict(color='#fff', linewidth=2))
    axes[1].set_title("Box Plot", fontweight='bold')
    axes[1].set_xlabel(f"Duration ({unit})")
    plt.tight_layout(); st.pyplot(fig2)


# ═══════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════
if st.session_state.exp is None:
    browse()
else:
    play(st.session_state.exp)