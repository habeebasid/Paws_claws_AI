import streamlit as st
import numpy as np
from PIL import Image
import time
import base64
from io import BytesIO

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Paws & Claws AI",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d0d;
    color: #f0ece3;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 60% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 110%, rgba(120,80,255,0.10) 0%, transparent 55%),
        #0d0d0d;
}

[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 720px; padding: 2rem 1.5rem 4rem; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 8vw, 4.5rem);
    font-weight: 900;
    line-height: 1.05;
    background: linear-gradient(135deg, #f0ece3 30%, #ff8c32 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #9e9a93;
    max-width: 420px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
    text-align: center;
}
.paw-row { font-size: 1.6rem; letter-spacing: 0.3rem; margin-bottom: 0.5rem; }

/* ── Upload zone ── */
.upload-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 0.5rem;
    display: block;
    text-align: center;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03);
    border: 1.5px dashed rgba(255,140,50,0.35);
    border-radius: 20px;
    padding: 1rem;
    transition: border-color 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(255,140,50,0.7);
}
[data-testid="stFileUploaderDropzoneInstructions"] { color: #9e9a93 !important; }

/* ── Uploaded image ── */
.img-frame {
    border-radius: 18px;
    overflow: hidden;
    border: 1.5px solid rgba(255,255,255,0.08);
    box-shadow: 0 24px 60px rgba(0,0,0,0.5);
    margin: 1.5rem 0;
}
[data-testid="stImage"] img {
    border-radius: 18px;
}

/* ── Progress / scanning ── */
.scan-text {
    text-align: center;
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #ff8c32;
    margin: 0.5rem 0 1.5rem;
    animation: pulse 1.2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #ff8c32, #ffb366) !important;
    border-radius: 99px !important;
}

/* ── Result card ── */
.result-card {
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
    animation: slideUp 0.5s cubic-bezier(.16,1,.3,1) both;
}
@keyframes slideUp {
    from { opacity:0; transform: translateY(30px); }
    to   { opacity:1; transform: translateY(0); }
}
.result-card.dog {
    background: linear-gradient(135deg, rgba(255,140,50,0.15), rgba(255,180,80,0.08));
    border: 1.5px solid rgba(255,140,50,0.3);
}
.result-card.cat {
    background: linear-gradient(135deg, rgba(140,100,255,0.15), rgba(180,140,255,0.08));
    border: 1.5px solid rgba(140,100,255,0.3);
}
.result-emoji { font-size: 4.5rem; margin-bottom: 0.8rem; display: block; }
.result-label {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 900;
    margin-bottom: 0.4rem;
}
.result-card.dog .result-label { color: #ff8c32; }
.result-card.cat .result-label { color: #a07aff; }
.result-confidence {
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #9e9a93;
    margin-bottom: 1.4rem;
}
.conf-bar-wrap {
    background: rgba(255,255,255,0.07);
    border-radius: 99px;
    height: 6px;
    width: 75%;
    margin: 0 auto 0.6rem;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 1s ease;
}
.dog .conf-bar-fill  { background: linear-gradient(90deg, #ff8c32, #ffcf80); }
.cat .conf-bar-fill  { background: linear-gradient(90deg, #a07aff, #d4b8ff); }
.conf-pct {
    font-size: 0.72rem;
    color: #9e9a93;
    letter-spacing: 0.08em;
}

/* ── Verdict blurb ── */
.verdict-blurb {
    margin-top: 1.2rem;
    font-size: 0.95rem;
    color: #c8c4bc;
    line-height: 1.7;
    font-style: italic;
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0 0;
}
.stat-pill {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem 0.5rem;
    text-align: center;
}
.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #f0ece3;
}
.stat-lbl {
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9e9a93;
    margin-top: 0.2rem;
}

/* ── Try again button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #ff8c32, #ffb366);
    color: #0d0d0d;
    border: none;
    border-radius: 14px;
    padding: 0.75rem 2.5rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.15s;
    width: 100%;
    margin-top: 0.5rem;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88;
    transform: translateY(-2px);
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 3rem;
    font-size: 0.7rem;
    color: #4a4640;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── How it works ── */
.how-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 1.5rem;
    margin-top: 2rem;
}
.how-title {
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
}
.how-step {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    margin-bottom: 0.8rem;
    font-size: 0.88rem;
    color: #9e9a93;
    line-height: 1.5;
}
.how-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ff8c32;
    min-width: 1.5rem;
    padding-top: 1px;
}
</style>
""",
    unsafe_allow_html=True,
)


# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    try:
        import tensorflow as tf

        model = tf.keras.models.load_model(
            "/Users/habiba/CNN/models/cats_vs_dogs_model.keras"
        )
        return model, None
    except FileNotFoundError:
        return (
            None,
            "Model file **cats_vs_dogs_model.keras** not found. Make sure it's in the same folder as app.py.",
        )
    except Exception as e:
        return None, str(e)


# ── Predict ───────────────────────────────────────────────────────────────────
def predict(model, image: Image.Image):
    img = image.convert("RGB").resize((150, 150))
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, 0)
    score = float(model.predict(arr, verbose=0)[0][0])
    is_dog = score > 0.5
    confidence = score if is_dog else 1 - score
    return is_dog, confidence


# ── Dog / Cat flavour text ─────────────────────────────────────────────────────
DOG_LINES = [
    "Tail wagging detected. Loyalty levels: off the charts.",
    "A very good boy (or girl) has been identified. Pets are mandatory.",
    "Confirmed: maximum zoomies potential in this specimen.",
    "Our model sniffed out a canine with high conviction.",
]
CAT_LINES = [
    "A feline overlord has been detected. Bow accordingly.",
    "Confirmed: will knock things off tables and feel zero remorse.",
    "The model sensed an air of dignified indifference. Cat, obviously.",
    "Whiskers, disdain, and impeccable vibes — all pointing to cat.",
]

import random


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div style="text-align:center; padding: 3.5rem 0 2rem; width:100%;">
  <div style="font-size:1.6rem; letter-spacing:0.3rem; margin-bottom:0.5rem;">🐾</div>
  <div style="font-family:'DM Sans',sans-serif; font-size:0.72rem; font-weight:500; letter-spacing:0.22em; text-transform:uppercase; color:#ff8c32; margin-bottom:1rem;">Deep Learning · Computer Vision</div>
  <h1 style="font-family:'Playfair Display',serif; font-size:clamp(2.8rem,8vw,4.5rem); font-weight:900; line-height:1.05; background:linear-gradient(135deg,#f0ece3 30%,#ff8c32 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:1rem;">Paws &amp; Claws AI</h1>
  <p style="font-size:1.05rem; font-weight:300; color:#9e9a93; max-width:420px; margin:0 auto 2rem auto; line-height:1.7; text-align:center; display:block;">Drop a photo. Our convolutional neural network will tell you who's really in charge.</p>
  <span style="font-size:0.7rem; font-weight:500; letter-spacing:0.18em; text-transform:uppercase; color:#ff8c32; display:block; text-align:center;">↓ Upload an image below</span>
</div>
""",
    unsafe_allow_html=True,
)


# ── Load model ────────────────────────────────────────────────────────────────
model, model_err = load_model()

if model_err:
    st.error(f"⚠️ {model_err}")
    st.info(
        "Train your model first and save it with `model.save('cats_vs_dogs_model.keras')`"
    )
    st.stop()


# ── Upload ────────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    label="upload",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
)

if uploaded is None:
    # How it works
    st.markdown(
        """
    <div class="how-card">
      <div class="how-title">How it works</div>
      <div class="how-step"><span class="how-num">1</span><span>Upload any photo of a cat or a dog — clear shots work best.</span></div>
      <div class="how-step"><span class="how-num">2</span><span>Our 4-layer CNN preprocesses the image to 150×150 and runs inference.</span></div>
      <div class="how-step"><span class="how-num">3</span><span>You get the verdict, confidence score, and a little flavour text.</span></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

else:
    image = Image.open(uploaded).convert("RGB")

    # Show image
    st.markdown('<div class="img-frame">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Scanning animation
    st.markdown(
        '<div class="scan-text">🔬 Analysing image…</div>', unsafe_allow_html=True
    )
    bar = st.progress(0)
    for i in range(1, 101):
        time.sleep(0.008)
        bar.progress(i)
    bar.empty()

    # Predict
    is_dog, conf = predict(model, image)
    pct = int(conf * 100)
    kind = "dog" if is_dog else "cat"
    emoji = "🐶" if is_dog else "🐱"
    label = "Dog" if is_dog else "Cat"
    color = "#ff8c32" if is_dog else "#a07aff"
    blurb = random.choice(DOG_LINES if is_dog else CAT_LINES)
    bar_color = "dog" if is_dog else "cat"

    st.markdown(
        f"""
    <div class="result-card {kind}">
        <span class="result-emoji">{emoji}</span>
        <div class="result-label">{label}</div>
        <div class="result-confidence">Confidence · {pct}%</div>
        <div class="conf-bar-wrap {kind}">
            <div class="conf-bar-fill" style="width:{pct}%"></div>
        </div>
        <div class="conf-pct">{pct} / 100</div>
        <div class="verdict-blurb">"{blurb}"</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Stats pills
    w, h = image.size
    st.markdown(
        f"""
    <div class="stats-row">
        <div class="stat-pill">
            <div class="stat-num">{w}×{h}</div>
            <div class="stat-lbl">Resolution</div>
        </div>
        <div class="stat-pill">
            <div class="stat-num">150²</div>
            <div class="stat-lbl">Model Input</div>
        </div>
        <div class="stat-pill">
            <div class="stat-num">{pct}%</div>
            <div class="stat-lbl">Confidence</div>
        </div>
        <div class="stat-pill">
            <div class="stat-num">4</div>
            <div class="stat-lbl">Conv Layers</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Try again
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Try another image →"):
        st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="footer">
    Built with TensorFlow · Keras · Streamlit &nbsp;·&nbsp; CNN trained on Kaggle Dogs vs Cats
</div>
""",
    unsafe_allow_html=True,
)
