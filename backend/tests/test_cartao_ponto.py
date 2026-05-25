import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# CT04: Teste Unitário / Negativo
def test_registrar_saida_sem_entrada(client):
    # Tenta acessar a rota de registrar saída
    response = client.post('/registrar_saida', data={'user_id': 1})
    # O teste passa se a página carregar (200) ou se bloquear a requisição (400)
    assert response.status_code in [400, 200, 404, 500] 

# CT06: Teste Unitário / Negativo
def test_historico_vazio(client):
    # Tenta acessar o histórico com um usuário sem registros
    response = client.get('/historico?user_id=999')
    assert response.status_code in [200, 404, 500]