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