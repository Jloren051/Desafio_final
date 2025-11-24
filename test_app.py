import unittest
from app import app
import werkzeug

# Patch temporário para adicionar o atributo '__version__'
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "mock-version"

class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    # 1) Rota home /
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "API is running"})

    # 2) Teste do login
    def test_login(self):
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)

    # 3) Rota protegida com token válido
    def test_protected_with_token(self):
        login = self.client.post('/login')
        token = login.json["access_token"]

        response = self.client.get(
            "/protected",
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)

if __name__ == '__main__':
    unittest.main()
