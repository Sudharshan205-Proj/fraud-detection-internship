# Fraud Detection Application Overview

## 1. Purpose

The Phase 10 application provides an interactive interface for evaluating individual financial transactions using the finalized Random Forest fraud detection model.

The application is implemented using Streamlit and connects directly to the model inference service.

## 2. Architecture

The application follows this workflow:

```text
User Transaction Input
        |
        v
Streamlit Application
        |
        v
FraudModelService
        |
        v
Feature Engineering
        |
        v
33-Feature Model Schema
        |
        v
Random Forest Model
        |
        v
Fraud Probability
        |
        v
Prediction
        |
        v
Investigation Priority
        |
        v
Streamlit Result