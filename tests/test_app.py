import sys
sys.path.insert(0, '.')
from app import app, generate_short_code

def test_generate_short_code():
    """Test short code generation"""
    url = "https://example.com"
    code = generate_short_code(url)
    assert len(code) == 6
    assert isinstance(code, str)
    print(f"✓ Short code generated: {code}")

def test_health_endpoint():
    """Test health endpoint"""
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        print("✓ Health endpoint working")

if __name__ == '__main__':
    test_generate_short_code()
    test_health_endpoint()
    print("All tests passed!")