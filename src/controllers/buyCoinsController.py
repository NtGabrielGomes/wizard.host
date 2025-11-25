from flask import request, jsonify
from src.models.userView import Users
from src.Factory.database import db
from src.Factory.flaskInit import serializer
import requests
import random
from datetime import datetime


def usd_to_btc(usd_amount):
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price', params={
            'ids': 'bitcoin',
            'vs_currencies': 'usd'
        })
        response.raise_for_status() 
        exchange_rate = response.json()['bitcoin']['usd']
        btc = usd_amount / exchange_rate
        return btc
    except requests.RequestException as e:
        raise Exception(f"Erro ao obter a taxa de câmbio: {str(e)}")

def generate_pseudo_random_int(user_id, min_val=1, max_val=1000000):
    timestamp = datetime.utcnow().isoformat()
    seed_string = f"{user_id}:{timestamp}"
    random.seed(seed_string)
    return random.randint(min_val, max_val)
 
def buy_coins():
    # Verifica se o usuário está autenticado
    token = request.cookies.get('token')
    if not token:
        return jsonify({"message": "Usuário não autenticado."}), 401

    try:
        user_id = serializer.loads(token, salt='login', max_age=30*24*60*60)
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado."}), 404
    except Exception:
        return jsonify({"message": "Token inválido ou expirado."}), 401

    # coins
    data = request.get_json()
    coins = data.get('coins', 0)

    # Valida a quantidade de coins
    if not isinstance(coins, int) or coins <= 0 or coins < 1 or coins > 60:
        return jsonify({"message": "Quantidade de coins inválida."}), 400


    dolar = coins * 5  # Assuming 1 coin = $5.00
    dolar += 1.5 * (dolar / 100)  # Adding 1.5% fee
    btc = usd_to_btc(dolar)
    # Create Plisio invoice
    try:
        r = requests.get(
            'https://api.plisio.net/api/v1/invoices/new?',
            params={
                'source_currency': 'USD',
                'amount': btc,
                'order_number': generate_pseudo_random_int(user),
                'currency': 'BTC',
                'email': user.email if user.email else '',
                'order_name': f'Purchase {coins} coins',
                'callback_url': 'http://127.0.0.1/dashboard/callback',
                'api_key': 'P0tmYEGqzCI5aAe38aH8l8wKWtf_xjpBcLDonX4iEm781HpZI9RABCaxCJUiVctd'
            }
        )

        if r.status_code != 200:
            return jsonify({"message": "Erro ao criar a fatura."}), 500

        plisio_response = r.json()
        payment_url = plisio_response.get('data', {}).get('invoice_url')
        wallet_hash = plisio_response.get('data', {}).get('wallet_hash')
        qr_code = plisio_response.get('data', {}).get('qr_code')

        if not payment_url or not wallet_hash or not qr_code:
            return jsonify({"message": "Resposta inválida da Plisio."}), 500

        # Prepare response data using Plisio's base64 QR code
        payments_data = {
            'payment_url': payment_url,
            'qr_code': f'{qr_code}',
            'wallet_hash': wallet_hash,
            'btc-amount-popup': btc
        }
        
        return jsonify(payments_data), 200
        
    except requests.RequestException as e:
        return jsonify({"message": f"Erro ao comunicar com Plisio: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"message": f"Erro inesperado: {str(e)}"}), 500