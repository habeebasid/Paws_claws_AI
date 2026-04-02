# 🐾 Paws & Claws AI — Cats vs Dogs Classifier

A deep learning web app that classifies images as **cats or dogs** using a Convolutional Neural Network (CNN) built with TensorFlow/Keras, served via a sleek Streamlit interface.

---

## ✨ Live Demo

> 🔗 **[Try it on Streamlit Cloud](https://your-app-link.streamlit.app)** ← replace after deploying

---

## 📸 Preview

| Upload | Result |
|--------|--------|
| Drop any cat or dog photo | Get an instant prediction with confidence score |

---

## 🧠 Model Architecture

Built from scratch using a 4-block CNN:

```
Input (150×150×3)
   ↓
Conv2D(32) → MaxPooling
   ↓
Conv2D(64) → MaxPooling
   ↓
Conv2D(128) → MaxPooling
   ↓
Conv2D(128) → MaxPooling
   ↓
Flatten → Dense(512) → Dense(1, sigmoid)
```

- **Loss:** Binary Crossentropy  
- **Optimizer:** Adam  
- **Output:** 0 = Cat, 1 = Dog  
- **Input size:** 150 × 150 pixels  
- **Dataset:** [Kaggle Dogs vs Cats](https://www.kaggle.com/datasets/salader/dogsvscats)

---

## 🗂 Project Structure

```
CNN/
├── app.py                      # Streamlit app
├── Cats_vs_Dogs.ipynb          # Training notebook
├── cats_vs_dogs_model.keras    # Saved model (not in git)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/cats-vs-dogs.git
cd cats-vs-dogs
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv ds-env
source ds-env/bin/activate        # Mac/Linux
ds-env\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your trained model
Train the model by running all cells in `Cats_vs_Dogs.ipynb`, then make sure `cats_vs_dogs_model.keras` is in the root folder.

### 5. Launch the app
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub (without the `.keras` model file — it's too large)
2. Host the model on **Google Drive** or **Hugging Face Hub**
3. Add a download snippet at the top of `app.py` to fetch it at runtime
4. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → connect your repo
5. Set **Main file path** to `app.py` → Deploy

---

## 📦 Tech Stack

| Tool | Purpose |
|------|---------|
| TensorFlow / Keras | Model training & inference |
| Streamlit | Web app interface |
| Pillow | Image preprocessing |
| scikit-learn | Evaluation metrics |
| Kaggle API | Dataset download |
| OpenCV | Image utilities |

---

## 📊 Training Details

| Parameter | Value |
|-----------|-------|
| Image size | 150 × 150 |
| Batch size | 20 |
| Validation split | 20% |
| Activation (output) | Sigmoid |
| Dataset | Dogs vs Cats (Kaggle) |

---

## 🙋‍♀️ Author

**Habiba**  
Built as a hands-on CNN project — trained on MacBook, deployed on the cloud.

---

## 📄 License

MIT — feel free to fork, modify, and build on it.
