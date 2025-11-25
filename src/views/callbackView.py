from flask import request, jsonify
from src.models.userView import Users
from src.Factory.database import db
import hashlib
import hmac
from src.controllers.buyCoinsController import usd_to_btc

PLISIO_SECRET_KEY = 'P0tmYEGqzCI5aAe38aH8l8wKWtf_xjpBcLDonX4iEm781HpZI9RABCaxCJUiVctd'

def plisio_callback():
    # Obter todos os parâmetros POST
    data = request.form.to_dict()
    
    # Verificar se o callback é autêntico
    verify_hash = data.get('verify_hash')
    if not verify_hash:
        return jsonify({'status': 'error', 'message': 'Missing verify_hash'}), 400
    
    # Gerar nosso próprio hash para verificação
    generated_hash = hmac.new(
        PLISIO_SECRET_KEY.encode('utf-8'),
        ''.join(f'{k}={v}' for k, v in sorted(data.items()) if k != 'verify_hash').encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
    
    if not hmac.compare_digest(generated_hash, verify_hash):
        return jsonify({'status': 'error', 'message': 'Invalid hash'}), 400
    

    # Se chegou aqui, o callback é autêntico
    order_number = data.get('order_number')
    status = data.get('status')
    amount = data.get('amount')
    currency = data.get('currency')
    
    if not order_number or ':' not in order_number:
        return jsonify({'status': 'error', 'message': 'Invalid order_number format'}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({'status': 'error', 'message': 'Invalid amount'}), 400
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Amount must be a number'}), 400

    # Aqui você processa o pagamento com base no status
    if status == 'completed':
        # Pagamento confirmado - creditar o usuário
        try:
            # Encontre o usuário com base no order_number

            user_id = int(order_number.split(':')[0])  # Extrai o user_id do order_number
            user = Users.query.get(user_id)
            
            if user:
                # Adicione os créditos ao usuário
                amount_in_dolar = usd_to_btc(amount) / 5  # Assuming 1 coin = $5.00
                user.cash += amount_in_dolar  # ou o valor apropriado
                db.session.commit()
                return jsonify({'status': 'success'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'User not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        # Outros status podem ser tratados aqui
        return jsonify({'status': 'info', 'message': f'Payment status: {status}'}), 200

