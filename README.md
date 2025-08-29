# Phishing Detection using Machine Learning

A simple end‑to‑end project that trains an ML model to classify URLs as **phishing** or **legitimate**, and serves the model behind a lightweight web UI.

---

## ✨ Features
- URL dataset (`phishing_site_urls.csv`) for training/experimentation.
- Jupyter notebook (`Phishing-detector.ipynb`) with data prep, vectorization, model training, and export.
- Serialized artifacts (`vectorizer.pkl`, `phishing.pkl`) for inference.
- Minimal Flask app (`app.py`) with HTML templates and static assets to demo predictions.
- MIT licensed.

---

## 🗂️ Project Structure
```
Phishing-Detection-using-Machine-Learning/
├─ app.py                  # Flask web app for inference
├─ Phishing-detector.ipynb # Notebook for EDA + training + export
├─ phishing_site_urls.csv  # Sample URL dataset
├─ vectorizer.pkl          # Fitted text/URL vectorizer
├─ phishing.pkl            # Trained ML model
├─ templates/              # HTML templates for the web UI
├─ static/                 # CSS/JS/assets for the web UI
├─ Pipfile                 # (Optional) Pipenv environment definition
└─ LICENSE                 # MIT License
```

> **Note**: Re‑train the model from the notebook if you change preprocessing, features, or algorithms. Re‑export `vectorizer.pkl` and `phishing.pkl` and place them beside `app.py`.

---

## 🚀 Quickstart

### 1) Clone
```bash
git clone https://github.com/G0wda/Phishing-Detection-using-Machine-Learning.git
cd Phishing-Detection-using-Machine-Learning
```

### 2) Set up Python env
**Option A — Pipenv (preferred if you use the provided `Pipfile`)**
```bash
pip install --upgrade pip pipenv
pipenv install
pipenv shell
```

**Option B — venv + pip**
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install common deps for this project
pip install flask scikit-learn pandas numpy joblib
# (Install jupyter/lab if you want to run the notebook)
pip install jupyter
```

### 3) Run the web app
```bash
python app.py
```
Open: http://127.0.0.1:5000

**Usage**: Paste a URL in the form and submit → you’ll get a predicted label (e.g., *Phishing* or *Legitimate*) and/or probability.

---

## 🧠 Training & Re‑training
1. Launch Jupyter and open `Phishing-detector.ipynb`:
   ```bash
   jupyter notebook
   ```
2. Steps you’ll typically see in the notebook:
   - Load `phishing_site_urls.csv` (and any other sources you add).
   - Clean/normalize URLs (lowercase, strip schemes, handle query strings, etc.).
   - Vectorize text/URL tokens (e.g., TF‑IDF over character/word n‑grams).
   - Fit one or more classifiers; tune with CV.
   - Evaluate with accuracy, precision/recall, F1, ROC‑AUC, confusion matrix.
   - Persist artifacts with `joblib`/`pickle`:
     ```python
     import joblib
     joblib.dump(vectorizer, 'vectorizer.pkl')
     joblib.dump(model, 'phishing.pkl')
     ```
3. Copy the exported `vectorizer.pkl` and `phishing.pkl` to the project root (beside `app.py`).

> **Tip**: Keep track of your preprocessing choices in the notebook (e.g., how you tokenize or strip URL parts). The **vectorizer** you export must match what you use at inference time in the Flask app.

---

## 🧾 Dataset
- The repository includes `phishing_site_urls.csv` as a starting point. You can augment it with fresh phishing/benign URLs (e.g., newer feeds or internal datasets).
- Always deduplicate and **split by domain/time** to reduce leakage.
- Consider balancing classes during training if the dataset is skewed.

### Suggested schema (typical for URL datasets)
| column         | type   | description                                  |
|----------------|--------|----------------------------------------------|
| url            | str    | Full URL (string)                             |
| label          | int/str| 1/0 or phishing/legitimate                    |
| source(optional)| str   | Where the URL came from (feed, crawl, etc.)   |
| ts(optional)   | datetime | When it was observed                        |

---

## 🧩 Inference Flow (Flask)
1. User submits a URL via the web form.
2. `app.py` loads `vectorizer.pkl` and `phishing.pkl` once at startup.
3. App applies **the same preprocessing** used during training.
4. URL → `vectorizer.transform([...])` → `model.predict` / `model.predict_proba`.
5. Result rendered in a template under `templates/`.

> **Environment variables**: If you deploy, you can expose host/port via `FLASK_ENV`, `FLASK_DEBUG`, or a `.env` file as needed.

---

## ✅ Testing the App
- Try a few obviously benign domains: `https://www.wikipedia.org`, `https://www.apple.com`.
- Try known‑bad samples from your dataset (don’t click them!).
- Check edge cases: 
  - Very short domains, IDNs, long query strings, obfuscated URLs, multiple subdomains, unusual TLDs.
  - URLs without scheme (`example.com/login`), with IP addresses, or data URIs.

---

## 📦 Packaging / Deployment
- **Local**: run `python app.py` or `flask run`.
- **Production**: 
  - Serve Flask behind a WSGI server (e.g., `gunicorn`) or containerize.
  - Mount `vectorizer.pkl` and `phishing.pkl` as read‑only.
  - Add health checks and basic logging.
  - Consider a background job to refresh the model on a schedule.

### Example `Dockerfile` (optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask scikit-learn pandas numpy joblib
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## 🔒 Security Notes
- Treat **untrusted URLs** as hostile input; never fetch them server‑side in this demo app.
- Don’t display user‑submitted URLs without HTML‑escaping.
- Log minimally; avoid storing sensitive data.
- Models can be **evasion‑prone**; pair with rule‑based checks and reputation systems in real deployments.

---

## 🧭 Roadmap Ideas
- Add a REST endpoint that returns JSON (`/api/predict`).
- Add confidence scores and threshold tuning.
- Expand features: WHOIS, DNS, hosting ASN, TLS, page‑level cues (if you safely fetch content with a sandbox).
- Track model versioning (MLflow) and add CI for lint/tests.
- Provide a `requirements.txt` for non‑Pipenv users.

---

## 🛠️ Troubleshooting
- **`ModuleNotFoundError`** → ensure your virtual environment is active and deps are installed.
- **`ValueError: feature mismatch`** → your runtime vectorizer/model don’t match the training pipeline; re‑export both.
- **Flask not reloading** → set `FLASK_DEBUG=1` or use `--reload` with your runner.

---

## 📄 License
MIT — see `LICENSE`.

---

## 🙌 Acknowledgements
- Thanks to the open‑source community for datasets and tooling.
- Built with Python, scikit‑learn, Flask, and Jupyter Notebook.
