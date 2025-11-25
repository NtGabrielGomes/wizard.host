
#+--------------------------------+
#|         Dependencias:          |
#|            Global              |
#|              ↓                 |
#|         Controllers            |
#|              ↓                 |
#|            Views               |
#+--------------------------------+
from flask import Flask
#Controllers

from src.controllers import *
#Views
from src.views import *

def init_routes(app: Flask):
    app.route('/login')(login)  # Assuming login_page is merged into login
    app.route('/auth', methods=["POST", "GET"])(login)
    app.route('/dashboard')(dashboard)
    app.route('/logout')(logout)
    app.route('/registry', methods=['POST', 'GET'])(register)
    app.route('/pay')(pay)
    app.route('/api/buy-coins', methods=['POST'])(buy_coins)
    app.route('/register')(registro)
    app.route('/')(index)
    app.route('/callback')(plisio_callback)
    app.errorhandler(404)(page_not_found)