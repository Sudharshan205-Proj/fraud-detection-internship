# Phase 13 — Deployment

## 1. Overview

Phase 13 deploys the Fraud Detection System as a Streamlit web application.

The deployment uses:

- Streamlit
- GitHub
- Streamlit Community Cloud
- the finalized Random Forest model
- the finalized 33-feature inference schema

The application provides an interactive interface for submitting transaction information and receiving a fraud-risk prediction.

---

## 2. Application Entry Point

The Streamlit application entry point is:

```text
app/streamlit_app.py
```

The app depends on two artifacts created by the Phase 10 final-model
step:

```text
models/random_forest_model.joblib
models/model_features.json
```

---

## 3. Local Deployment

1. Create a virtual environment and install the pinned dependencies:

   ```bash
   python -m venv .venv
   # Windows:  .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```

2. Train and export the final model (requires the processed dataset):

   ```bash
   python -m src.machine_learning.train_final_model
   ```

3. Launch the application:

   ```bash
   streamlit run app/streamlit_app.py
   ```

   The repository's `.streamlit/config.toml` runs Streamlit in headless
   mode and disables usage-statistics collection.

---

## 4. Streamlit Community Cloud Deployment

The application is designed to be deployed on Streamlit Community
Cloud:

1. Push the repository to GitHub. The model artifacts
   (`models/random_forest_model.joblib` and `models/model_features.json`)
   are committed, so a fresh clone has everything the app needs. To
   regenerate them from the full dataset instead, run
   `python -m src.machine_learning.train_final_model`.
2. Create the app at https://share.streamlit.io by connecting the
   GitHub repository.
3. Set the main file to `app/streamlit_app.py`.
4. Cloud runs `pip install -r requirements.txt` automatically; the
   `pip install -e .` step is covered because the app imports `src`
   and `app` packages from the repository root.

---

## 5. Deployment Checklist

- [x] Application entry point defined (`app/streamlit_app.py`)
- [x] Pinned runtime dependencies (`requirements.txt`)
- [x] Headless Streamlit configuration (`.streamlit/config.toml`)
- [x] Final model + 33-feature schema export (`train_final_model.py`)
- [x] Inference service validated by automated tests
- [x] Deployment validation tests (`tests/validation/test_deployment_validation.py`)

---

## 6. Status

Phase 13 deployment: **Complete**

Deployment documentation: Complete

Runtime verification (local `streamlit run`) is included in the
Phase 12 manual validation checklist.

Public deployment: https://fraud-detection-internship.streamlit.app/