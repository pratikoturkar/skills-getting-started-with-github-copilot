"""
Tests for the root endpoint (GET /).
"""

import pytest


def test_root_redirects_to_static_index(client):
    """
    Test that GET / redirects to /static/index.html
    """
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/static/index.html" in response.headers.get("location", "")


def test_root_redirect_with_follow(client):
    """
    Test that GET / eventually reaches index.html
    """
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert "Mergington" in response.text or "<!DOCTYPE" in response.text
