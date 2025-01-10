import os
import aiohttp
import asyncio
from dotenv import load_dotenv
from supabase import create_client

# Carregar variáveis de ambiente
load_dotenv()

# Função para criar cliente Supabase
def criar_cliente_supabase():
    url = os.getenv("SUPABASE_URL")
    chave_api = os.getenv("SUPABASE_KEY")
    
    if not url or not chave_api:
        raise ValueError("A URL ou chave de API não foram encontradas nas variáveis de ambiente.")
    
    return create_client(url, chave_api)

# Função assíncrona para buscar pedidos da API do Mercado Livre
async def buscar_pedidos(access_token, seller_id, api_url, supabase, session):
    headers = {"Authorization": f"Bearer {access_token}"}
    offset = 0
    limit = 50
    total = 10

    # Função para buscar pedidos
    while offset < total:
        url = f"{api_url}/orders/search?seller={seller_id}&offset={offset}&limit={limit}"

        try:
            # Fazendo a requisição para a API
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    pedidos = data.get('results', [])
                    total = data.get('paging', {}).get('total', 0)

                    for pedido in pedidos:
                        order_id = pedido.get("id", "")
                        date_created = pedido.get("date_created", "")
                        # A lógica de manipulação dos dados vai aqui

                else:
                    print(f"Erro ao acessar pedidos. Status da resposta: {response.status}")
                    break

        except Exception as e:
            print(f"Erro ao conectar com a API: {e}")
            break

        offset += limit

# Função principal assíncrona
async def main(req, res):
    # Criar cliente do Supabase
    supabase = criar_cliente_supabase()

    contas = [
        {"nome": "TOYS", "client_id": os.getenv("CLIENT_ID_TOYS"), "client_secret": os.getenv("CLIENT_SECRET_TOYS"), "access_token": os.getenv("ACCESS_TOKEN_TOYS"), "refresh_token": os.getenv("REFRESH_TOKEN_TOYS"), "seller_id": os.getenv("SELLER_ID_TOYS")},
    ]
    
    api_url = os.getenv("API_URL")

    async with aiohttp.ClientSession() as session:
        tasks = []

        for conta in contas:
            tasks.append(buscar_pedidos(conta["access_token"], conta["seller_id"], api_url, supabase, session))

        # Executa todas as tarefas de forma assíncrona
        await asyncio.gather(*tasks)

    return res.status(200).send("Pedidos processados com sucesso!")

# A função main será usada como a função de entrada da Vercel
def handler(req, res):
    asyncio.run(main(req, res))
