"""
Phase 10 - Fraud Detection Streamlit Application.
"""

import os
import sys

import streamlit as st

from app.model_service import FraudModelService
from app.utils import (
    get_investigation_priority,
    get_priority_description,
)

# Automatically find and add the root repository directory to the Python path
# to resolve the 'ModuleNotFoundError: No module named app' error.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🔍",
    layout="wide",
)


@st.cache_resource
def get_model_service():
    """Load and cache the fraud detection model service."""
    return FraudModelService()


def main():
    """Run the Streamlit fraud detection application."""

    st.title("Fraud Detection System")

    st.write(
        """
        This application uses a machine-learning model to identify
        potentially suspicious financial transactions.
        """
    )

    st.info(
        """
        Model predictions are intended to support investigation and
        prioritization. A prediction is not proof that a transaction
        is fraudulent.
        """
    )

    try:
        model_service = get_model_service()

    except FileNotFoundError:
        st.error(
            """
            The trained Random Forest model could not be found.

            Please train and save the model before starting the
            application.
            """
        )
        st.stop()

    st.header("Transaction Analysis")

    col1, col2 = st.columns(2)

    with col1:
        transaction_type = st.selectbox(
            "Transaction Type",
            [
                "PAYMENT",
                "TRANSFER",
                "CASH_OUT",
                "DEBIT",
                "CASH_IN",
            ],
        )

        amount = st.number_input(
            "Transaction Amount",
            min_value=0.0,
            value=1000.0,
            step=100.0,
        )

        step = st.number_input(
            "Time Step",
            min_value=0,
            value=1,
            step=1,
        )

    with col2:
        old_balance_org = st.number_input(
            "Origin Balance Before",
            min_value=0.0,
            value=5000.0,
            step=100.0,
        )

        new_balance_org = st.number_input(
            "Origin Balance After",
            min_value=0.0,
            value=4000.0,
            step=100.0,
        )

        old_balance_dest = st.number_input(
            "Destination Balance Before",
            min_value=0.0,
            value=1000.0,
            step=100.0,
        )

        new_balance_dest = st.number_input(
            "Destination Balance After",
            min_value=0.0,
            value=2000.0,
            step=100.0,
        )

    if st.button(
        "Analyze Transaction",
        type="primary",
    ):
        transaction = {
            "step": step,
            "type": transaction_type,
            "amount": amount,
            "oldbalanceOrg": old_balance_org,
            "newbalanceOrig": new_balance_org,
            "oldbalanceDest": old_balance_dest,
            "newbalanceDest": new_balance_dest,
        }

        try:
            result = model_service.predict(transaction)

            probability = result["fraud_probability"]
            prediction = result["prediction"]

            priority = get_investigation_priority(
                probability
            )

            priority_description = get_priority_description(
                priority
            )

            st.divider()

            st.header("Analysis Result")

            result_col1, result_col2, result_col3 = st.columns(3)

            with result_col1:
                st.metric(
                    "Fraud Probability",
                    f"{probability:.2%}",
                )

            with result_col2:
                st.metric(
                    "Prediction",
                    (
                        "Potential Fraud"
                        if prediction == 1
                        else "Likely Legitimate"
                    ),
                )

            with result_col3:
                st.metric(
                    "Investigation Priority",
                    priority,
                )

            st.subheader("Interpretation")

            if prediction == 1:
                st.warning(
                    "The model identified this transaction "
                    "as potentially fraudulent."
                )
            else:
                st.success(
                    "The model identified this transaction "
                    "as likely legitimate."
                )

            st.write(priority_description)

            st.caption(
                """
                Responsible use: this prediction should be treated
                as decision-support information and should not be
                used as the sole basis for taking action against a
                customer.
                """
            )

        except (ValueError, KeyError, TypeError) as exc:
            st.error(
                f"Unable to analyze transaction: {exc}"
            )


if __name__ == "__main__":
    main()
