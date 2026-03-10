"""
Tests for GET / (root) endpoint
"""
import pytest


def test_root_redirects(client):
    """Test that root path redirects"""
    response = client.get("/", follow_redirects=False)
    
    # FastAPI returns 307 for RedirectResponse by default
    assert response.status_code in [307, 308, 302, 301]


def test_root_redirects_to_static_index(client):
    """Test that root redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    
    assert "location" in response.headers
    assert "/static/index.html" in response.headers["location"]


def test_root_redirect_followed(client):
    """Test following the redirect from root"""
    response = client.get("/", follow_redirects=True)
    
    # Should eventually return the static HTML content
    # Status code should be 200 after following redirect
    assert response.status_code == 200


def test_root_no_query_params(client):
    """Test root endpoint without query parameters"""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code in [307, 308, 302, 301]
    assert response.headers["location"] == "/static/index.html"
