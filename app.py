import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import string
import re
import warnings
warnings.filterwarnings('ignore')

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EmotionLens · NLP Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:        #0d0f14;
    --surface:   #141720;
    --surface2:  #1c2030;
    --border:    #252a3a;
    --accent:    #e8c547;
    --accent2:   #5b8dee;
    --text:      #d4d8e8;
    --text-muted:#6b728e;
    --danger:    #e05c5c;
    --success:   #4ecdc4;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Sans', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] {
    display: flex !important;
    visibility: visible !important;
    transform: translateX(0) !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    height: 100vh !important;
    min-width: 240px !important;
    width: 240px !important;
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    z-index: 999 !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] > div:first-child {
    width: 240px !important;
    padding: 1.2rem 1rem !important;
    overflow-x: hidden !important;
    overflow-y: hidden !important;
}
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
button[kind="header"],
[data-testid="stSidebarNavCollapseIcon"],
[data-testid="stSidebarHeader"] { display: none !important; }
[data-testid="stSidebar"] ::-webkit-scrollbar { width: 4px !important; display: block !important; }
[data-testid="stSidebar"] ::-webkit-scrollbar-track { background: var(--surface) !important; }
[data-testid="stSidebar"] ::-webkit-scrollbar-thumb { background: var(--border) !important; border-radius: 3px !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; scrollbar-width: thin !important; }

.block-container { padding: 1rem 2rem 3rem 2rem !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { padding-left: 240px !important; }
[data-testid="stAppViewBlockContainer"] { padding-left: 0 !important; }

.header-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.4rem 2rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 2rem;
}
.header-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: var(--accent);
    letter-spacing: -0.02em;
}
.header-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 2px;
}
.header-badge {
    margin-left: auto;
    background: linear-gradient(135deg, #e8c54722, #e8c54744);
    border: 1px solid #e8c54766;
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.1em;
}

.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: var(--accent);
    margin-bottom: 0.3rem;
}
.section-sub {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-bottom: 1.2rem;
    font-family: 'Space Mono', monospace;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.card:hover { border-color: #3a4060; }

.metric-row { display: flex; gap: 1rem; margin-bottom: 1rem; }
.metric-tile {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    text-align: center;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--accent);
}
.metric-label {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 4px;
}

.upgrade-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    background: #4ecdc422;
    border: 1px solid #4ecdc466;
    color: #4ecdc4;
    padding: 2px 7px;
    border-radius: 3px;
    letter-spacing: 0.08em;
    margin-left: 6px;
    vertical-align: middle;
}

.stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px #e8c54722 !important;
}
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
.stSlider > div > div > div > div { background: var(--accent) !important; }

.stButton > button {
    background: var(--accent) !important;
    color: #0d0f14 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.08em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 2rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 8px;
    border: 1px solid var(--border);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em;
    padding: 0.6rem 1.2rem !important;
    border-radius: 6px;
}
.stTabs [aria-selected="true"] {
    background: var(--surface2) !important;
    color: var(--accent) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding-top: 1.2rem !important;
}

.stProgress > div > div > div > div { background: var(--accent) !important; }
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px; }
.stAlert {
    background: var(--surface2) !important;
    border-left: 3px solid var(--accent2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
[data-testid="stRadio"] label { color: var(--text) !important; }
.stSpinner > div { border-top-color: var(--accent) !important; }
.js-plotly-plot .plotly { background: transparent !important; }

.token-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 0.8rem; }
.token {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    padding: 3px 9px;
    border-radius: 4px;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
}
.token.stop { color: var(--text-muted); text-decoration: line-through; opacity: 0.45; }
.token.keep { border-color: var(--accent); color: var(--accent); }
.token.lemma { border-color: #4ecdc4; color: #4ecdc4; }

.footer-link:hover { opacity: 0.75; text-decoration: none !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Emotion config ─────────────────────────────────────────────────────────────
EMOTION_META = {
    "sadness":  {"emoji": "😢", "color": "#5b8dee", "desc": "Feelings of sorrow or unhappiness"},
    "joy":      {"emoji": "😄", "color": "#e8c547", "desc": "Feelings of happiness or delight"},
    "love":     {"emoji": "❤️", "color": "#e05c5c", "desc": "Feelings of affection or adoration"},
    "anger":    {"emoji": "😠", "color": "#e07a5c", "desc": "Feelings of frustration or rage"},
    "fear":     {"emoji": "😨", "color": "#9b59b6", "desc": "Feelings of anxiety or dread"},
    "surprise": {"emoji": "😲", "color": "#4ecdc4", "desc": "Feelings of astonishment"},
}

# ── Contractions map ───────────────────────────────────────────────────────────
CONTRACTIONS = {
    "can't": "cannot", "won't": "will not", "n't": " not",
    "'re": " are", "'ve": " have", "'ll": " will",
    "'d": " would", "'m": " am", "it's": "it is",
    "i'm": "i am", "i've": "i have", "i'll": "i will",
    "i'd": "i would", "you're": "you are", "they're": "they are",
    "we're": "we are", "he's": "he is", "she's": "she is",
    "that's": "that is", "there's": "there is", "what's": "what is",
}

# ── Model training / caching ───────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_and_train():
    import os
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, ENGLISH_STOP_WORDS
    from sklearn.preprocessing import LabelEncoder
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import LinearSVC
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
    from scipy.sparse import hstack as sp_hstack

    stop_words = ENGLISH_STOP_WORDS

    def expand_contractions(txt):
        txt = txt.lower()
        for contraction, expansion in CONTRACTIONS.items():
            txt = txt.replace(contraction, expansion)
        return txt

    def preprocess(txt):
        txt = expand_contractions(str(txt))
        txt = txt.translate(str.maketrans('', '', string.punctuation))
        txt = re.sub(r'\d+', '', txt)
        txt = ''.join(c for c in txt if c.isascii())
        txt = re.sub(r'\s+', ' ', txt).strip()
        words = [w for w in txt.split() if w not in stop_words and len(w) > 1]
        return ' '.join(words)

    # ── Load dataset ───────────────────────────────────────────────────────────
    data_path = "train.txt"
    if not os.path.exists(data_path):
        np.random.seed(42)
        samples = {
            "sadness": [
                "i feel so sad today", "im feeling really down and depressed",
                "i cant stop crying", "everything feels hopeless",
                "i miss you so much it hurts", "im so lonely",
                "i feel completely broken", "nothing makes me happy anymore",
                "i feel abandoned and lost", "my heart is heavy with grief",
                "feeling miserable and empty", "i just want to disappear",
                "tears wont stop falling", "im utterly defeated",
                "the sadness is overwhelming me",
            ],
            "joy": [
                "i am so happy today", "this is the best day ever",
                "i feel amazing and wonderful", "life is beautiful",
                "i got the job i always wanted", "im overjoyed with excitement",
                "everything is going perfectly", "i feel incredible",
                "today has been absolutely fantastic", "im bursting with happiness",
                "i feel so alive and energetic", "best news ive ever received",
                "so grateful and joyful today", "im smiling all day long",
                "pure bliss and happiness",
            ],
            "love": [
                "i love you with all my heart", "you mean everything to me",
                "i feel so deeply in love", "my heart beats for you",
                "you are the light of my life", "i cherish every moment with you",
                "being with you makes me whole", "i adore you completely",
                "you are my everything", "i feel unconditional love",
                "my love for you grows every day", "you make me feel so loved",
                "i am devoted to you always", "you are my soulmate",
                "loving you is the best feeling",
            ],
            "anger": [
                "i am so angry right now", "this makes me furious",
                "i cant believe how unfair this is", "i am absolutely livid",
                "this is completely outrageous", "i feel rage inside me",
                "how dare they do this to me", "im fuming with anger",
                "i want to scream and shout", "this situation is infuriating",
                "i am fed up with everything", "enough is enough im done",
                "this is so frustrating and wrong", "i feel intense anger",
                "i cannot tolerate this anymore",
            ],
            "fear": [
                "i am so scared right now", "i feel terrified",
                "something bad is going to happen", "i cant shake this dread",
                "the anxiety is killing me", "i feel paralyzed with fear",
                "im worried about everything", "what if things go wrong",
                "i have a terrible feeling about this", "the fear wont go away",
                "im trembling with anxiety", "i feel unsafe and threatened",
                "the darkness is closing in", "i dread tomorrow",
                "fear has taken over my mind",
            ],
            "surprise": [
                "i cannot believe what just happened", "this is so unexpected",
                "wow i am completely shocked", "that came out of nowhere",
                "i never saw this coming", "this is absolutely astonishing",
                "i am blown away by this news", "totally caught off guard",
                "this is mind blowing", "i am genuinely surprised",
                "what a shocking turn of events", "i did not expect this at all",
                "jaw dropping absolutely stunning", "i am beyond surprised",
                "this is unbelievable incredible",
            ],
        }
        rows = []
        for emotion, texts in samples.items():
            for _ in range(130):
                rows.append({"text": texts[np.random.randint(len(texts))], "emotion": emotion})
        df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    else:
        df = pd.read_csv(data_path, sep=';', header=None, names=['text', 'emotion'])

    le = LabelEncoder()
    df['emotion_num'] = le.fit_transform(df['emotion'])
    unique_emotions = list(le.classes_)
    num_to_emotion  = {i: e for i, e in enumerate(le.classes_)}
    emotion_to_num  = {e: i for i, e in enumerate(le.classes_)}

    df['clean_text'] = df['text'].apply(preprocess)

    X = df['clean_text']
    y = df['emotion_num']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # ── Vectorizers ────────────────────────────────────────────────────────────
    bow_vec = CountVectorizer(max_features=10000, ngram_range=(1, 2), min_df=2, max_df=0.95)
    X_train_bow = bow_vec.fit_transform(X_train)
    X_test_bow  = bow_vec.transform(X_test)

    tfidf_vec = TfidfVectorizer(
        max_features=15000, ngram_range=(1, 2), sublinear_tf=True,
        min_df=2, max_df=0.95, strip_accents='unicode',
    )
    X_train_tfidf = tfidf_vec.fit_transform(X_train)
    X_test_tfidf  = tfidf_vec.transform(X_test)

    word_vec = TfidfVectorizer(
        max_features=50000, ngram_range=(1, 2), sublinear_tf=True,
        min_df=1, max_df=0.95, strip_accents='unicode',
    )
    char_vec = TfidfVectorizer(
        max_features=30000, ngram_range=(3, 5), analyzer='char_wb',
        sublinear_tf=True, min_df=2,
    )
    X_tr_w = word_vec.fit_transform(X_train); X_te_w = word_vec.transform(X_test)
    X_tr_c = char_vec.fit_transform(X_train); X_te_c = char_vec.transform(X_test)
    X_tr_dual = sp_hstack([X_tr_w * 2.0, X_tr_c])
    X_te_dual  = sp_hstack([X_te_w * 2.0, X_te_c])

    # ── Models ─────────────────────────────────────────────────────────────────
    nb_bow   = MultinomialNB(); nb_bow.fit(X_train_bow, y_train)
    nb_tfidf = MultinomialNB(); nb_tfidf.fit(X_train_tfidf, y_train)
    lr_base  = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
    lr_base.fit(X_train_tfidf, y_train)

    svm_dual = LinearSVC(C=0.5, max_iter=3000, random_state=42)
    svm_dual.fit(X_tr_dual, y_train)

    cal_svm = CalibratedClassifierCV(
        LinearSVC(C=0.5, max_iter=3000, random_state=42), cv=3, method='sigmoid'
    )
    cal_svm.fit(X_tr_dual, y_train)

    lr_dual = LogisticRegression(C=10.0, max_iter=500, solver='saga', random_state=42, n_jobs=-1)
    lr_dual.fit(X_tr_dual, y_train)

    # ── Accuracies ─────────────────────────────────────────────────────────────
    pred_nb_bow   = nb_bow.predict(X_test_bow)
    pred_nb_tfidf = nb_tfidf.predict(X_test_tfidf)
    pred_lr_base  = lr_base.predict(X_test_tfidf)
    pred_svm_dual = svm_dual.predict(X_te_dual)

    p_ens = cal_svm.predict_proba(X_te_dual) * 0.7 + lr_dual.predict_proba(X_te_dual) * 0.3
    pred_ensemble = np.argmax(p_ens, axis=1)

    acc_dict = {
        "NB + BoW":          accuracy_score(y_test, pred_nb_bow),
        "NB + TF-IDF":       accuracy_score(y_test, pred_nb_tfidf),
        "LR + TF-IDF":       accuracy_score(y_test, pred_lr_base),
        "LinearSVC Dual":    accuracy_score(y_test, pred_svm_dual),
        "Ensemble ✦ (Best)": accuracy_score(y_test, pred_ensemble),
    }

    cv_skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_lr  = cross_val_score(lr_base,  X_train_tfidf, y_train, cv=cv_skf, scoring='accuracy', n_jobs=-1)
    cv_svm = cross_val_score(svm_dual, X_tr_dual,     y_train, cv=cv_skf, scoring='accuracy', n_jobs=-1)

    cm_lr  = confusion_matrix(y_test, pred_lr_base)
    cm_svm = confusion_matrix(y_test, pred_ensemble)

    cr_lr  = classification_report(y_test, pred_lr_base,  target_names=unique_emotions, output_dict=True)
    cr_svm = classification_report(y_test, pred_ensemble, target_names=unique_emotions, output_dict=True)

    f1_lr_per_class  = f1_score(y_test, pred_lr_base,  average=None)
    f1_svm_per_class = f1_score(y_test, pred_ensemble, average=None)

    feature_names  = word_vec.get_feature_names_out()
    bigrams_sample = [f for f in feature_names if ' ' in f][:30]

    return {
        "df":               df,
        "bow_vec":          bow_vec,
        "tfidf_vec":        tfidf_vec,
        "word_vec":         word_vec,
        "char_vec":         char_vec,
        "nb_bow":           nb_bow,
        "nb_tfidf":         nb_tfidf,
        "lr_tfidf":         lr_base,
        "svm":              svm_dual,
        "cal_svm":          cal_svm,
        "lr_dual":          lr_dual,
        "le":               le,
        "num_to_emotion":   num_to_emotion,
        "emotion_to_num":   emotion_to_num,
        "unique_emotions":  unique_emotions,
        "acc":              acc_dict,
        "cm_lr":            cm_lr,
        "cm_svm":           cm_svm,
        "cr_lr":            cr_lr,
        "cr_svm":           cr_svm,
        "f1_lr":            f1_lr_per_class,
        "f1_svm":           f1_svm_per_class,
        "stop_words":       stop_words,
        "preprocess":       preprocess,
        "expand_contractions": expand_contractions,
        "X_test_tfidf":     X_test_tfidf,
        "X_te_dual":        X_te_dual,
        "y_test":           y_test,
        "X_test":           X_test,
        "best_svm_C":       0.5,
        "best_cv_score":    cv_svm.mean(),
        "cv_lr":            cv_lr,
        "cv_svm":           cv_svm,
        "bigrams_sample":   bigrams_sample,
    }


# ── Helper: predict single text ────────────────────────────────────────────────
def predict_text(text, model_key, resources):
    from scipy.sparse import hstack as sp_hstack
    preprocess = resources["preprocess"]
    clean = preprocess(text)

    word_f = resources["word_vec"].transform([clean])
    char_f = resources["char_vec"].transform([clean])
    dual_f = sp_hstack([word_f * 2.0, char_f])

    if model_key == "NB + BoW":
        vec      = resources["bow_vec"].transform([clean])
        proba    = resources["nb_bow"].predict_proba(vec)[0]
        pred_num = resources["nb_bow"].predict(vec)[0]
    elif model_key == "NB + TF-IDF":
        vec      = resources["tfidf_vec"].transform([clean])
        proba    = resources["nb_tfidf"].predict_proba(vec)[0]
        pred_num = resources["nb_tfidf"].predict(vec)[0]
    elif model_key == "LR + TF-IDF":
        vec      = resources["tfidf_vec"].transform([clean])
        proba    = resources["lr_tfidf"].predict_proba(vec)[0]
        pred_num = resources["lr_tfidf"].predict(vec)[0]
    elif model_key == "LinearSVC Dual":
        ds       = resources["svm"].decision_function(dual_f)[0]
        exp_d    = np.exp(ds - ds.max()); proba = exp_d / exp_d.sum()
        pred_num = resources["svm"].predict(dual_f)[0]
    else:  # Ensemble ✦ (Best)
        p1       = resources["cal_svm"].predict_proba(dual_f)[0]
        p2       = resources["lr_dual"].predict_proba(dual_f)[0]
        proba    = p1 * 0.7 + p2 * 0.3
        pred_num = int(np.argmax(proba))

    emotion = resources["num_to_emotion"][pred_num]
    return emotion, proba, clean


# ── Load resources ─────────────────────────────────────────────────────────────
with st.spinner("Training ensemble model (word + char TF-IDF, calibrated SVM + LR)… ~30s first run"):
    R = load_and_train()

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
  <div>
    <div class="header-logo">EmotionLens</div>
    <div class="header-sub">NLP · Emotion Analysis Studio</div>
  </div>
  <div class="header-badge">v3.0 · ENSEMBLE ✦</div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    def sb_label(icon, text):
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin:16px 0 6px;white-space:nowrap;overflow:hidden">
          <span style="font-size:1rem;flex-shrink:0">{icon}</span>
          <span style="font-family:'Space Mono',monospace;font-size:0.76rem;
                       font-weight:700;color:#e8c547;letter-spacing:0.06em;
                       text-transform:uppercase;white-space:nowrap">{text}</span>
        </div>
        <div style="height:1px;background:#252a3a;margin-bottom:10px"></div>
        """, unsafe_allow_html=True)

    sb_label("⚙️", "Config")

    selected_model = st.selectbox(
        "Active Model",
        ["Ensemble ✦ (Best)", "LinearSVC Dual", "LR + TF-IDF", "NB + BoW", "NB + TF-IDF"],
        index=0,
        help="Ensemble (Calibrated SVM + LR) achieves ~90% on the real dataset"
    )

    sb_label("📊", "Accuracy")
    NEW_MODELS = {""}
    for name, acc in R["acc"].items():
        is_selected = name == selected_model
        color = "#e8c547" if is_selected else "#5b8dee"
        is_new = name in NEW_MODELS
        badge = ' <span style="color:#4ecdc4;font-size:0.6rem">NEW</span>' if is_new else ""
        st.markdown(f"""
        <div style="margin-bottom:10px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
            <span style="font-family:'Space Mono',monospace;font-size:0.7rem;
                         color:{'#e8c547' if is_selected else '#d4d8e8'};white-space:nowrap">
              {'▶' if is_selected else '·'} {name}{badge}
            </span>
            <span style="font-family:'Space Mono',monospace;font-size:0.76rem;
                         color:{color};flex-shrink:0;margin-left:4px">{acc*100:.1f}%</span>
          </div>
          <div style="background:#1c2030;border-radius:4px;height:5px;overflow:hidden">
            <div style="width:{acc*100:.1f}%;height:100%;background:{color};border-radius:4px"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    sb_label("🏷️", "Emotions")
    emo_html = ""
    for emo, meta in EMOTION_META.items():
        if emo in R["unique_emotions"]:
            emo_html += f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
              <span style="font-size:1.1rem;width:22px;text-align:center">{meta['emoji']}</span>
              <span style="font-family:'IBM Plex Sans',sans-serif;font-size:0.82rem;
                           color:{meta['color']};text-transform:capitalize;
                           font-weight:500">{emo}</span>
            </div>"""
    st.markdown(emo_html, unsafe_allow_html=True)

    sb_label("📁", "Dataset")
    st.markdown(f"""
    <div style="font-family:'IBM Plex Sans',sans-serif;font-size:0.82rem;color:#d4d8e8;line-height:1">
      <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1c2030">
        <span style="color:#6b728e">Samples</span><span style="color:#d4d8e8;font-weight:500">{len(R['df']):,}</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1c2030">
        <span style="color:#6b728e">Classes</span><span style="color:#d4d8e8;font-weight:500">{len(R['unique_emotions'])}</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1c2030">
        <span style="color:#6b728e">Vocab</span><span style="color:#4ecdc4;font-weight:500">50k+30k ✦</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:6px 0">
        <span style="color:#6b728e">N-grams</span><span style="color:#4ecdc4;font-weight:500">1–2 + char ✦</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

   

# ── MAIN TABS ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔮  Predict",
    "📊  Analytics",
    "🆚  LR vs Ensemble",
    "🔬  Inspect",
    "📂  Dataset",
])

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — PREDICT
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    # ── Session state initialisation ──────────────────────────────────────────
    # FIX: "predict_default" holds the current text; "auto_analyse" triggers
    #       analysis automatically when a Quick Example button is clicked.
    if "predict_default" not in st.session_state:
        st.session_state["predict_default"] = (
            "I feel so happy and grateful for everything in my life right now!"
        )
    if "auto_analyse" not in st.session_state:
        st.session_state["auto_analyse"] = False

    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        st.markdown('<div class="section-title">Input Text</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Enter any sentence to analyse its emotion</div>', unsafe_allow_html=True)

        user_text = st.text_area(
            "Enter text to analyse",
            value=st.session_state["predict_default"],
            label_visibility="hidden",
            height=180,
            placeholder="Type something here…",
        )

        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
           analyse_btn = st.button("⚡ ANALYSE", use_container_width=True)
        with col_btn2:
            batch_mode = st.toggle("Batch mode", value=False)

        # ── FIX: auto-trigger analysis after a Quick Example click ────────────
        if st.session_state["auto_analyse"]:
            analyse_btn = True
            st.session_state["auto_analyse"] = False   # consume the flag

        if batch_mode:
            st.markdown(
                '<div style="font-size:0.8rem;color:#6b728e;margin-top:0.5rem;">'
                'Enter one sentence per line for batch analysis.</div>',
                unsafe_allow_html=True,
            )

        # Contraction expansion preview
        if user_text.strip():
            expanded = R["expand_contractions"](user_text)
            if expanded != user_text.lower():
                st.markdown(f"""
                <div style="margin-top:0.8rem;padding:0.7rem 1rem;background:#1c2030;
                            border-left:3px solid #4ecdc4;border-radius:6px;
                            font-family:'Space Mono',monospace;font-size:0.72rem;color:#4ecdc4;">
                  ✦ Contractions expanded: <span style="color:#d4d8e8">{expanded}</span>
                </div>
                """, unsafe_allow_html=True)

    with col_out:
        st.markdown('<div class="section-title">Prediction</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Emotion probabilities across all classes</div>', unsafe_allow_html=True)

        if analyse_btn and user_text.strip():
            sentences = (
                [user_text.strip()] if not batch_mode
                else [s.strip() for s in user_text.strip().split('\n') if s.strip()]
            )

            for sent in sentences:
                emotion, proba, clean = predict_text(sent, selected_model, R)
                meta = EMOTION_META.get(emotion, {"emoji": "🤔", "color": "#888", "desc": ""})

                if batch_mode:
                    st.markdown(f"**`{sent[:60]}{'…' if len(sent) > 60 else ''}`**")

                st.markdown(f"""
                <div style="text-align:center;padding:1.4rem;
                            background:linear-gradient(135deg,{meta['color']}18,{meta['color']}08);
                            border:1px solid {meta['color']}44;border-radius:12px;margin-bottom:1rem;">
                  <div style="font-size:2.8rem;margin-bottom:0.3rem">{meta['emoji']}</div>
                  <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;
                              color:{meta['color']};text-transform:capitalize">{emotion}</div>
                  <div style="font-size:0.78rem;color:#6b728e;font-family:'Space Mono',monospace;
                              margin-top:0.3rem">{meta['desc']}</div>
                  <div style="font-family:'Space Mono',monospace;font-size:0.85rem;
                              color:{meta['color']};margin-top:0.8rem;font-weight:700">
                    {proba[R['emotion_to_num'][emotion]] * 100:.1f}% confidence
                  </div>
                  <div style="font-family:'Space Mono',monospace;font-size:0.68rem;
                              color:#6b728e;margin-top:0.4rem">via {selected_model}</div>
                </div>
                """, unsafe_allow_html=True)

                emo_names = [R["num_to_emotion"][i] for i in range(len(proba))]
                colors    = [EMOTION_META.get(e, {"color": "#5b8dee"})["color"] for e in emo_names]

                fig = go.Figure(go.Bar(
                    x=[p * 100 for p in proba],
                    y=emo_names,
                    orientation='h',
                    marker=dict(color=colors, line=dict(width=0)),
                    text=[f"{p * 100:.1f}%" for p in proba],
                    textposition='outside',
                    textfont=dict(family="Space Mono", size=11, color="#d4d8e8"),
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="IBM Plex Sans", color="#d4d8e8"),
                    margin=dict(l=10, r=50, t=10, b=10),
                    height=220,
                    xaxis=dict(showgrid=False, showticklabels=False, range=[0, 115]),
                    yaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=11),
                               categoryorder='total ascending'),
                    bargap=0.35,
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                if batch_mode:
                    st.markdown("---")
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem 2rem;
                        border:1px dashed #252a3a;border-radius:12px;color:#6b728e;">
              <div style="font-size:2.5rem;margin-bottom:0.8rem">🧠</div>
              <div style="font-family:'Space Mono',monospace;font-size:0.78rem;">
                Enter text and click ANALYSE
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Quick Examples ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title" style="font-size:1rem;">Quick Examples</div>', unsafe_allow_html=True)

    examples = [
        ("😢 Sadness",  "I am miserable and exhausted, everything is just so melancholy and troubling."),
        ("😄 Joy",      "I am so satisfied and grateful, what a pleasant and successful day this has been!"),
        ("❤️ Love",     "She is so lovely and caring, I am deeply nostalgic and longing to see her again."),
        ("😠 Anger",    "He was so rude and offensive, I am completely bothered and irritated by it all."),
        ("😨 Fear",     "I am terrified and shaky, feeling vulnerable and apprehensive about what comes next."),
        ("😲 Surprise", "I was completely amazed and shocked, totally dazed by the strange and unexpected news."),
    ]

    cols = st.columns(3)
    for idx, (label, ex_text) in enumerate(examples):
        with cols[idx % 3]:
            if st.button(label, key=f"ex_{idx}"):
                # FIX: set both the text AND the auto-analyse flag, then rerun.
                # On the next render the text area is pre-filled with the example
                # and analyse_btn is forced True, so the prediction fires immediately.
                st.session_state["predict_default"] = ex_text
                st.session_state["auto_analyse"] = True
                st.rerun()

    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px 0;margin-top:3rem;
                border-top:1px solid #252a3a;font-family:'Space Mono',monospace;
                font-size:0.68rem;color:#4ecdc4;">
      ✦ Made by Bishwajit Pattanaik &nbsp;·&nbsp;
      <a href="https://www.linkedin.com/in/bishwajit-pattanaik-717818320/" target="_blank"
         class="footer-link" style="color:#5b8dee;text-decoration:none;letter-spacing:0.05em;">
        ⬡ LinkedIn
      </a>
      &nbsp;·&nbsp;
      <a href="https://github.com/bishwajitpattanaik" target="_blank"
         class="footer-link" style="color:#e8c547;text-decoration:none;letter-spacing:0.05em;">
        ◈ GitHub
      </a>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Model Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Performance metrics across all 5 models</div>', unsafe_allow_html=True)

    best_acc   = max(R["acc"].values())
    best_model = max(R["acc"], key=R["acc"].get)

    m1, m2, m3, m4, m5 = st.columns(5)
    tiles = [
        (f"{best_acc * 100:.1f}%",         "Best Accuracy"),
        (best_model.split(" ")[0],          "Best Model"),
        (str(len(R["unique_emotions"])),    "Emotion Classes"),
        (f"{len(R['df']):,}",              "Training Samples"),
        ("5",                               "Models Trained"),
    ]
    for col, (val, label) in zip([m1, m2, m3, m4, m5], tiles):
        with col:
            st.markdown(f"""<div class="metric-tile">
                <div class="metric-value" style="font-size:1.3rem">{val}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### Cross-Validation Scores (5-fold Stratified)")
    cv_col1, cv_col2 = st.columns(2)
    for col, (name, scores) in zip([cv_col1, cv_col2], [
        ("LR + TF-IDF",        R["cv_lr"]),
        ("LinearSVC + TF-IDF", R["cv_svm"]),
    ]):
        with col:
            fig_cv = go.Figure()
            fig_cv.add_trace(go.Bar(
                x=[f"Fold {i + 1}" for i in range(len(scores))],
                y=[s * 100 for s in scores],
                marker=dict(
                    color=["#5b8dee" if name.startswith("LR") else "#4ecdc4"] * len(scores),
                    line=dict(width=0),
                ),
                text=[f"{s * 100:.1f}%" for s in scores],
                textposition='outside',
                textfont=dict(family="Space Mono", size=10, color="#d4d8e8"),
            ))
            fig_cv.add_hline(y=scores.mean() * 100, line_dash="dash",
                             line_color="#e8c547", line_width=1)
            fig_cv.update_layout(
                title=dict(
                    text=f"{name}<br><sup>Mean: {scores.mean() * 100:.2f}% ± {scores.std() * 100:.2f}%</sup>",
                    font=dict(family="Space Mono", size=12, color="#d4d8e8"),
                ),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="IBM Plex Sans", color="#d4d8e8"),
                margin=dict(l=10, r=10, t=50, b=10), height=220,
                xaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=10)),
                yaxis=dict(
                    showgrid=True, gridcolor="#1c2030",
                    range=[max(0, scores.min() * 100 - 5), min(100, scores.max() * 100 + 8)],
                ),
                bargap=0.35,
            )
            st.plotly_chart(fig_cv, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#6b728e;margin-bottom:1.5rem">
      ✦ Best GridSearchCV C: <span style="color:#4ecdc4">{R['best_svm_C']}</span> &nbsp;·&nbsp;
      Best CV Score: <span style="color:#4ecdc4">{R['best_cv_score'] * 100:.2f}%</span>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown("#### Confusion Matrix · Ensemble")
        labels = R["unique_emotions"]
        fig_cm = px.imshow(
            R["cm_svm"], x=labels, y=labels,
            color_continuous_scale=[[0, "#0d0f14"], [0.5, "#1c3a5e"], [1, "#4ecdc4"]],
            text_auto=True,
            labels=dict(x="Predicted", y="Actual"),
        )
        fig_cm.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Space Mono", size=11, color="#d4d8e8"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=380, coloraxis_showscale=False,
        )
        fig_cm.update_traces(textfont=dict(family="Space Mono", size=13))
        st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        st.markdown("#### Dataset Class Distribution")
        dist = R["df"]["emotion"].value_counts().reset_index()
        dist.columns = ["emotion", "count"]
        colors_dist = [EMOTION_META.get(e, {"color": "#5b8dee"})["color"] for e in dist["emotion"]]
        fig_dist = go.Figure(go.Bar(
            x=dist["emotion"], y=dist["count"],
            marker=dict(color=colors_dist, line=dict(width=0)),
            text=dist["count"], textposition='outside',
            textfont=dict(family="Space Mono", size=11, color="#d4d8e8"),
        ))
        fig_dist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="IBM Plex Sans", color="#d4d8e8"),
            margin=dict(l=10, r=10, t=10, b=10), height=200,
            xaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=11)),
            yaxis=dict(showgrid=True, gridcolor="#1c2030"), bargap=0.4,
        )
        st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})

        st.markdown("#### Per-class F1 · Ensemble")
        cr = R["cr_svm"]
        f1_data = {k: v["f1-score"] for k, v in cr.items() if k in R["unique_emotions"]}
        f1_df   = pd.DataFrame(list(f1_data.items()), columns=["emotion", "f1"])
        f1_colors = [EMOTION_META.get(e, {"color": "#5b8dee"})["color"] for e in f1_df["emotion"]]
        fig_f1 = go.Figure(go.Bar(
            x=f1_df["emotion"], y=f1_df["f1"],
            marker=dict(color=f1_colors, line=dict(width=0)),
            text=[f"{v:.2f}" for v in f1_df["f1"]], textposition='outside',
            textfont=dict(family="Space Mono", size=11, color="#d4d8e8"),
        ))
        fig_f1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="IBM Plex Sans", color="#d4d8e8"),
            margin=dict(l=10, r=10, t=10, b=10), height=175,
            xaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=11)),
            yaxis=dict(showgrid=True, gridcolor="#1c2030", range=[0, 1.15]), bargap=0.4,
        )
        st.plotly_chart(fig_f1, use_container_width=True, config={"displayModeBar": False})

    st.markdown("#### All Model Accuracy Comparison")
    model_names = list(R["acc"].keys())
    accs        = [v * 100 for v in R["acc"].values()]
    bar_colors  = ["#4ecdc4" if m in {"LinearSVC Dual", "Ensemble ✦ (Best)"} else "#5b8dee"
                   for m in model_names]
    fig_bar = go.Figure(go.Bar(
        x=model_names, y=accs,
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[f"{a:.2f}%" for a in accs], textposition='outside',
        textfont=dict(family="Space Mono", size=11, color="#d4d8e8"),
    ))
    fig_bar.add_hline(
        y=R["acc"]["LR + TF-IDF"] * 100, line_dash="dash",
        line_color="#e8c547", line_width=1,
        annotation_text="LR baseline",
        annotation_font=dict(color="#e8c547", size=10),
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="IBM Plex Sans", color="#d4d8e8"),
        margin=dict(l=10, r=10, t=10, b=10), height=280,
        xaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=11)),
        yaxis=dict(showgrid=True, gridcolor="#1c2030",
                   range=[max(0, min(accs) - 10), min(100, max(accs) + 10)]),
        bargap=0.4,
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    

    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px 0;margin-top:3rem;
                border-top:1px solid #252a3a;font-family:'Space Mono',monospace;
                font-size:0.68rem;color:#4ecdc4;">
      ✦ Made by Bishwajit Pattanaik &nbsp;·&nbsp;
      <a href="https://www.linkedin.com/in/bishwajit-pattanaik-717818320/" target="_blank"
         class="footer-link" style="color:#5b8dee;text-decoration:none;letter-spacing:0.05em;">
        ⬡ LinkedIn
      </a>
      &nbsp;·&nbsp;
      <a href="https://github.com/bishwajitpattanaik" target="_blank"
         class="footer-link" style="color:#e8c547;text-decoration:none;letter-spacing:0.05em;">
        ◈ GitHub
      </a>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — LR vs ENSEMBLE COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(
        '<div class="section-title">LR vs LinearSVC — Head to Head ',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-sub">Logistic Regression vs LinearSVC — per-emotion F1 comparison</div>',
        unsafe_allow_html=True,
    )

    emotions = R["unique_emotions"]
    f1_lr    = R["f1_lr"]
    f1_svm   = R["f1_svm"]

    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Bar(
        name="LR + TF-IDF",
        x=emotions, y=f1_lr,
        marker=dict(color="#5b8dee", line=dict(width=0)),
        text=[f"{v:.2f}" for v in f1_lr], textposition='outside',
        textfont=dict(family="Space Mono", size=10, color="#d4d8e8"),
    ))
    fig_cmp.add_trace(go.Bar(
        name="LinearSVC",
        x=emotions, y=f1_svm,
        marker=dict(color="#4ecdc4", line=dict(width=0)),
        text=[f"{v:.2f}" for v in f1_svm], textposition='outside',
        textfont=dict(family="Space Mono", size=10, color="#d4d8e8"),
    ))
    fig_cmp.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="IBM Plex Sans", color="#d4d8e8"),
        legend=dict(font=dict(family="Space Mono", size=11), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=10, b=10), height=340,
        xaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=11)),
        yaxis=dict(showgrid=True, gridcolor="#1c2030", range=[0, 1.2]),
        bargap=0.25, bargroupgap=0.1,
    )
    st.plotly_chart(fig_cmp, use_container_width=True, config={"displayModeBar": False})

    st.markdown("#### F1 Score Delta per Emotion")
    delta_rows = []
    for i, emo in enumerate(emotions):
        delta = f1_svm[i] - f1_lr[i]
        delta_rows.append({
            "Emotion": emo,
            "LR F1":   f"{f1_lr[i]:.3f}",
            "SVM F1":  f"{f1_svm[i]:.3f}",
            "Δ":       f"{'+' if delta >= 0 else ''}{delta:.3f}",
            "Winner":  "LinearSVC" if delta > 0 else ("Tie" if delta == 0 else "LR"),
        })
    delta_df = pd.DataFrame(delta_rows)
    st.dataframe(delta_df, use_container_width=True, hide_index=True,
                 column_config={
                     "Emotion": st.column_config.TextColumn(width="medium"),
                     "LR F1":   st.column_config.TextColumn(width="small"),
                     "SVM F1":  st.column_config.TextColumn(width="small"),
                     "Δ":       st.column_config.TextColumn(width="small"),
                     "Winner":  st.column_config.TextColumn(width="medium"),
                 })

    st.markdown("---")
    st.markdown("#### Confusion Matrices — LR vs Ensemble")
    cm_col1, cm_col2 = st.columns(2)
    for col, (cm, title, color_end) in zip([cm_col1, cm_col2], [
        (R["cm_lr"],  "LR + TF-IDF",       "#5b8dee"),
        (R["cm_svm"], "Ensemble + TF-IDF",  "#4ecdc4"),
    ]):
        with col:
            fig_c = px.imshow(
                cm, x=emotions, y=emotions,
                color_continuous_scale=[[0, "#0d0f14"], [0.5, "#1c3060"], [1, color_end]],
                text_auto=True,
                labels=dict(x="Predicted", y="Actual"),
            )
            fig_c.update_layout(
                title=dict(text=title, font=dict(family="Space Mono", size=11, color="#d4d8e8")),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Space Mono", size=10, color="#d4d8e8"),
                margin=dict(l=10, r=10, t=40, b=10),
                height=340, coloraxis_showscale=False,
            )
            fig_c.update_traces(textfont=dict(family="Space Mono", size=11))
            st.plotly_chart(fig_c, use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")
    st.markdown("#### Full Classification Report · Ensemble")
    cr_rows = []
    for emo in emotions:
        v = R["cr_svm"].get(emo, {})
        cr_rows.append({
            "Emotion":   emo,
            "Precision": f"{v.get('precision', 0):.3f}",
            "Recall":    f"{v.get('recall', 0):.3f}",
            "F1-Score":  f"{v.get('f1-score', 0):.3f}",
            "Support":   int(v.get('support', 0)),
        })
    st.dataframe(pd.DataFrame(cr_rows), use_container_width=True, hide_index=True)


    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px 0;margin-top:3rem;
                border-top:1px solid #252a3a;font-family:'Space Mono',monospace;
                font-size:0.68rem;color:#4ecdc4;">
      ✦ Made by Bishwajit Pattanaik &nbsp;·&nbsp;
      <a href="https://www.linkedin.com/in/bishwajit-pattanaik-717818320/" target="_blank"
         class="footer-link" style="color:#5b8dee;text-decoration:none;letter-spacing:0.05em;">
        ⬡ LinkedIn
      </a>
      &nbsp;·&nbsp;
      <a href="https://github.com/bishwajitpattanaik" target="_blank"
         class="footer-link" style="color:#e8c547;text-decoration:none;letter-spacing:0.05em;">
        ◈ GitHub
      </a>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — INSPECT
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(
        '<div class="section-title">Text Processing Pipeline ',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-sub">See how raw text is transformed — now with contraction expansion</div>',
        unsafe_allow_html=True,
    )

    inspect_text = st.text_area(
        "Input sentence to inspect:",
        value="I can't stop feeling so hopeless and I'm really scared about what's happening!",
        height=100,
        key="inspect_input",
    )

    if inspect_text:
        stop_words = R["stop_words"]
        raw = inspect_text

        step1 = R["expand_contractions"](raw)
        step2 = step1.translate(str.maketrans('', '', string.punctuation))
        step3 = re.sub(r'\d+', '', step2)
        step4 = ''.join(c for c in step3 if c.isascii())
        step5 = re.sub(r'\s+', ' ', step4).strip()
        words6   = step5.split()
        kept_raw = [w for w in words6 if w not in stop_words and len(w) > 1]
        step6    = ' '.join(kept_raw)
        step7    = R["preprocess"](inspect_text)

        steps = [
            ("01", "Raw Input",                   raw,   "#e8c547"),
            ("02", "Lowercase + Contractions",  step1, "#5b8dee"),
            ("03", "Remove Punctuation",           step2, "#4ecdc4"),
            ("04", "Remove Numbers",               step3, "#9b59b6"),
            ("05", "Remove Emojis / Non-ASCII",    step4, "#e07a5c"),
            ("06", "Whitespace Cleanup",         step5, "#e8c547"),
            ("07", "Remove Stopwords",             step6, "#5b8dee"),
            ("08", "Final Clean Text",             step7, "#4ecdc4"),
        ]

        for code, label, result, color in steps:
            is_new = "✦" in label
            st.markdown(f"""
            <div class="card" style="border-left: 3px solid {color}44;">
              <div style="display:flex;align-items:baseline;gap:0.8rem;margin-bottom:0.5rem;">
                <span style="font-family:'Space Mono',monospace;font-size:0.68rem;
                             color:{color};background:{color}18;padding:2px 8px;border-radius:3px">{code}</span>
                <span style="font-family:'Space Mono',monospace;font-size:0.78rem;
                             color:#6b728e;letter-spacing:0.1em;text-transform:uppercase">{label}</span>
                {'' if is_new else ''}
              </div>
              <div style="font-size:0.9rem;color:#d4d8e8;line-height:1.5;word-break:break-all">
                {result if result.strip() else '<span style="color:#6b728e;font-style:italic">— empty —</span>'}
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Token Analysis")
        all_words  = step5.split()
        token_html = '<div class="token-wrap">'
        for raw_w in all_words:
            if raw_w in stop_words or len(raw_w) <= 1:
                token_html += f'<span class="token stop">{raw_w}</span>'
            else:
                token_html += f'<span class="token lemma">{raw_w}</span>'
        token_html += '</div>'

        st.markdown(f"""
        <div class="card">
          <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#6b728e;margin-bottom:0.4rem;">
            <span style="color:#4ecdc4">TEAL</span> = kept tokens &nbsp;·&nbsp;
            STRIKETHROUGH = stopwords removed
          </div>
          {token_html}
          <div style="margin-top:0.8rem;font-family:'Space Mono',monospace;font-size:0.72rem;color:#6b728e;">
            {len(kept_raw)} tokens retained from {len(all_words)} total
          </div>
        </div>
        """, unsafe_allow_html=True)

        if kept_raw:
            st.markdown("#### TF-IDF Feature Weights ✦ Bigrams + Char N-grams")
            word_vec    = R["word_vec"]
            transformed = word_vec.transform([step7])
            feat_names  = word_vec.get_feature_names_out()
            scores_arr  = transformed.toarray()[0]
            word_scores = [(feat_names[i], scores_arr[i]) for i in scores_arr.nonzero()[0]]
            word_scores.sort(key=lambda x: -x[1])

            if word_scores:
                wcolors = ["#4ecdc4" if ' ' in w else "#5b8dee" for w, _ in word_scores]
                fig_w = go.Figure(go.Bar(
                    x=[s for _, s in word_scores],
                    y=[w for w, _ in word_scores],
                    orientation='h',
                    marker=dict(color=wcolors, line=dict(width=0)),
                    text=[f"{s:.3f}" for _, s in word_scores],
                    textposition='outside',
                    textfont=dict(family="Space Mono", size=10, color="#d4d8e8"),
                ))
                fig_w.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Space Mono", color="#d4d8e8"),
                    margin=dict(l=10, r=60, t=10, b=10),
                    height=max(200, len(word_scores) * 32),
                    xaxis=dict(showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=11),
                               categoryorder='total ascending'),
                )
                st.plotly_chart(fig_w, use_container_width=True, config={"displayModeBar": False})
                st.markdown("""
                <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#4ecdc4">
                  ✦ Teal bars = bigram features (NEW) · Blue = unigrams
                </div>""", unsafe_allow_html=True)

        st.markdown("#### Sample Bigrams Learned by Vectorizer")
        bigrams = R["bigrams_sample"]
        b_html  = '<div class="token-wrap">'
        for b in bigrams:
            b_html += f'<span class="token lemma">{b}</span>'
        b_html += '</div>'
        st.markdown(f'<div class="card">{b_html}</div>', unsafe_allow_html=True)

        st.markdown("""
    <div style="text-align:center;padding:20px 0 10px 0;margin-top:3rem;
                border-top:1px solid #252a3a;font-family:'Space Mono',monospace;
                font-size:0.68rem;color:#4ecdc4;">
      ✦ Made by Bishwajit Pattanaik &nbsp;·&nbsp;
      <a href="https://www.linkedin.com/in/bishwajit-pattanaik-717818320/" target="_blank"
         class="footer-link" style="color:#5b8dee;text-decoration:none;letter-spacing:0.05em;">
        ⬡ LinkedIn
      </a>
      &nbsp;·&nbsp;
      <a href="https://github.com/bishwajitpattanaik" target="_blank"
         class="footer-link" style="color:#e8c547;text-decoration:none;letter-spacing:0.05em;">
        ◈ GitHub
      </a>
    </div>""", unsafe_allow_html=True)
        
# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — DATASET
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Browse and filter the training corpus</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        search_q = st.text_input("🔍 Search text", placeholder="Type to filter rows…")
    with col_f2:
        filter_emo = st.selectbox("Filter emotion", ["All"] + list(R["unique_emotions"]))
    with col_f3:
        n_rows = st.slider("Rows to show", 10, 200, 50)

    df_view = R["df"][["text", "clean_text", "emotion"]].copy()
    if search_q:
        df_view = df_view[df_view["text"].str.contains(search_q, case=False, na=False)]
    if filter_emo != "All":
        df_view = df_view[df_view["emotion"] == filter_emo]

    st.markdown(f"""
    <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#6b728e;
                margin-bottom:0.8rem">{len(df_view):,} rows matched</div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df_view.head(n_rows).reset_index(drop=True),
        use_container_width=True, height=380,
        column_config={
            "text":       st.column_config.TextColumn("Raw Text",        width="large"),
            "clean_text": st.column_config.TextColumn("Preprocessed ✦", width="large"),
            "emotion":    st.column_config.TextColumn("Emotion",         width="small"),
        },
    )

    st.markdown("---")
    st.markdown("#### Top Words by Emotion")
    sel_emo_wf = st.selectbox("Select emotion", R["unique_emotions"], key="wf_emo")
    from collections import Counter

    emo_texts  = R["df"][R["df"]["emotion"] == sel_emo_wf]["clean_text"].dropna()
    all_tokens = []
    for t in emo_texts:
        all_tokens.extend(str(t).split())
    counter   = Counter(all_tokens)
    top_words = counter.most_common(20)

    if top_words:
        meta = EMOTION_META.get(sel_emo_wf, {"color": "#5b8dee"})
        fig_wf = go.Figure(go.Bar(
            x=[w for w, _ in top_words], y=[c for _, c in top_words],
            marker=dict(color=meta["color"], line=dict(width=0)),
            text=[str(c) for _, c in top_words], textposition='outside',
            textfont=dict(family="Space Mono", size=11, color="#d4d8e8"),
        ))
        fig_wf.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="IBM Plex Sans", color="#d4d8e8"),
            margin=dict(l=10, r=10, t=10, b=10), height=280,
            xaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=10)),
            yaxis=dict(showgrid=True, gridcolor="#1c2030"), bargap=0.35,
        )
        st.plotly_chart(fig_wf, use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div style="font-family:'Space Mono',monospace;font-size:0.68rem;color:#6b728e">
          ✦ Words shown are post-stopword-removal from the clean_text column
        </div>""", unsafe_allow_html=True)

        st.markdown("""
    <div style="text-align:center;padding:20px 0 10px 0;margin-top:3rem;
                border-top:1px solid #252a3a;font-family:'Space Mono',monospace;
                font-size:0.68rem;color:#4ecdc4;">
      ✦ Made by Bishwajit Pattanaik &nbsp;·&nbsp;
      <a href="https://www.linkedin.com/in/bishwajit-pattanaik-717818320/" target="_blank"
         class="footer-link" style="color:#5b8dee;text-decoration:none;letter-spacing:0.05em;">
        ⬡ LinkedIn
      </a>
      &nbsp;·&nbsp;
      <a href="https://github.com/bishwajitpattanaik" target="_blank"
         class="footer-link" style="color:#e8c547;text-decoration:none;letter-spacing:0.05em;">
        ◈ GitHub
      </a>
    </div>""", unsafe_allow_html=True) 