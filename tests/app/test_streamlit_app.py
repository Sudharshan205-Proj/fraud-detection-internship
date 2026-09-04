"""
Tests for the Phase 10 Streamlit application.
"""


def test_streamlit_application_imports():
    import app.streamlit_app

    assert app.streamlit_app.main is not None
