import re

with open('c:\\TY\\DAL\\netflix_analysis.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Home Screen Metric Split
old_metrics = '''    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Titles", f"{len(df):,}")
    m2.metric("Movies", f"{len(df[df['type']=='Movie']):,}")
    m3.metric("TV Shows", f"{len(df[df['type']=='TV Show']):,}")
    m4.metric("Avg Duration", f"{df['duration_num'].mean():.0f} min")'''

new_metrics = '''    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Titles", f"{len(df):,}")
    m2.metric("Movies", f"{len(df[df['type']=='Movie']):,}")
    m3.metric("Avg Movie Length", f"{df[df['type']=='Movie']['duration_num'].mean():.0f} mins")
    m4.metric("TV Shows", f"{len(df[df['type']=='TV Show']):,}")
    m5.metric("Avg TV Seasons", f"{df[df['type']=='TV Show']['duration_num'].mean():.1f}")'''

code = code.replace(old_metrics, new_metrics)

# 2. Update CSS completely for aesthetics
css_start = code.find('<style>')
css_end = code.find('</style>')
if css_start != -1 and css_end != -1:
    new_css = '''<style>
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
'''
    code = code[:css_start] + new_css + code[css_end:]

# 3. Replace EXP 1
exp1_old = '''def render_exp1():
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
        st.write(f"**IQR:** {IQR:.2f} · **Fences:** [{Q1-1.5*IQR:.2f}, {Q3+1.5*IQR:.2f}] · **Outliers:** {len(out)}")'''

exp1_new = '''def render_exp1():
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
        st.write(f"**IQR:** {IQR:.2f} · **Fences:** [{Q1-1.5*IQR:.2f}, {Q3+1.5*IQR:.2f}] · **Outliers:** {len(out)}")'''

code = code.replace(exp1_old, exp1_new)

# 4. Replace EXP 2
exp2_old = '''def render_exp2():
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
        st.latex(f"y = {model.coef_[0]:.4f}x + {model.intercept_:.2f}")'''

exp2_new = '''def render_exp2():
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
        st.latex(f"y = {model.coef_[0]:.4f}x + {model.intercept_:.2f}")'''

code = code.replace(exp2_old, exp2_new)

# 5. Replace EXP 3 (Fix apply warning & UI spacing)
exp3_old = '''        sample = df.groupby('type', group_keys=False).apply(lambda x: x.sample(frac=n/len(df), random_state=42))'''
exp3_new = '''        sample = df.groupby('type', group_keys=False).sample(frac=n/len(df), random_state=42)'''
code = code.replace(exp3_old, exp3_new)

# 6. Replace EXP 4
exp4_old = '''def render_exp4():
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
            plt.tight_layout(); st.pyplot(fig2)'''

exp4_new = '''def render_exp4():
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
            plt.tight_layout(); st.pyplot(fig2)'''

code = code.replace(exp4_old, exp4_new)


# 7. Replace EXP 6
exp6_old = '''def render_exp6():
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
    plt.tight_layout(); st.pyplot(fig2)'''

exp6_new = '''def render_exp6():
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
    plt.tight_layout(); st.pyplot(fig2)'''

code = code.replace(exp6_old, exp6_new)

# Deprecation warning rewrite: `use_container_width=True` to `use_container_width=True` is replaced with `use_container_width="stretch"` ?
# wait, actually the API replacement is `.dataframe(..., use_container_width=True)` -> no wait, the log says "replace use_container_width with width='stretch'" or similar.
# Let's just suppress `use_container_width` entirely.
code = code.replace("use_container_width=True", "width='stretch'")
code = code.replace("use_container_width=False", "width='content'")

with open('c:\\TY\\DAL\\netflix_analysis.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("done")
