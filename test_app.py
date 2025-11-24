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

    # 1) Teste rota que retorna dados públicos
    def test_public_data(self):
        response = self.client.get('/data')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)

    # 2) Teste rota POST com corpo JSON (ex: somar números)
    def test_sum_numbers(self):
        payload = {"a": 5, "b": 7}
        response = self.client.post('/sum', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("result"), 12)

    # 3) Teste rota protegida com token válido
    def test_protected_with_token(self):
        # Primeiro obtém o token
        login = self.client.post('/login')
        token = login.json.get("access_token")

        # Usa o token na rota protegida
        response = self.client.get(
            '/protected',
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json)

if __name__ == '__main__':
    unittest.main()

