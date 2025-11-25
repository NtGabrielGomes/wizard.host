from flask import Flask
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__, static_folder='../../front/static', template_folder='../../front/templates')
app.secret_key = "WUrIaunzuViAkK64lModnl1609T"
serializer = URLSafeTimedSerializer(app.secret_key)