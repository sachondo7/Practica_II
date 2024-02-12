import unittest
from unittest.mock import patch
from func_mercados.api.api_client import authenticate

class TestApiClient(unittest.TestCase):
    @patch('requests.post')
    def test_authenticate(self, mock_post):
        # Configura la respuesta simulada
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'token': 'test_token'}

        # Llama a la función que quieres probar
        token = authenticate()

        # Verifica que la función devolvió el resultado esperado
        self.assertEqual(token, 'test_token')

if __name__ == '__main__':
    unittest.main()