from flask import Flask, jsonify, make_response, request, session
from model import db, Payment
from flask_restful import Api, Resource, reqparse
import datetime
from flask_migrate import Migrate
from flask_cors import CORS
import requests
from requests.auth import HTTPBasicAuth
import base64
import json

app = Flask(__name__)
api = Api(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.json.compact = False

CORS(app, supports_credentials=True)

migrate = Migrate(app, db)

db.init_app(app)

class Make_Payment(Resource):
    
    @staticmethod
    def post():

        # phone_number = request.json['phone']
        # amount = request.json['amount']
        parser = reqparse.RequestParser()
        parser.add_argument('phone', type=str, required = True)
        parser.add_argument('amount', type=str, required=True)
        args = parser.parse_args()

        phone_number = args['phone']
        amount = args['amount']

        consumer_key ="L0AOjNH8t6nKqV7nyvS1FG14dC85wLWs5akJfEDfdrfPXN4e"
        consumer_secret = "qTH60LCRSKPlGjsuWzEjjLGsca3ewlNYhgsm7evp5XLXqOJCfCt1EE8CGNoomQqB"
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer " + data['access_token']
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        bussiness_shortcode = '174379'
        data_to_encode = bussiness_shortcode + passkey + timestamp
        encoded_data = base64.b64encode(data_to_encode.encode())
        password = encoded_data.decode('utf-8')

        request = {
            "BusinessShortCode": bussiness_shortcode,
            "Password": password,
            "Timestamp": timestamp, # timestamp format: 20190317202903 yyyyMMhhmmss 
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": f"254{phone_number[1:]}",
            "PartyB": bussiness_shortcode,
            "PhoneNumber": f"254{phone_number[1:]}",
            "CallBackURL": "https://mydomain.com/pat",
            "AccountReference": "Limited",
            "TransactionDesc": "Payment of Jackson"
        }

        stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        headers = {"Authorization": access_token, "Content-Type": "application/json"}

        #making STK push request

        response = requests.post(stk_url,json=request,headers=headers)

        if response.status_code > 299:
            mpesa_response = {
                'message':'Failed'
            }
            final_response = make_response(
                jsonify(mpesa_response)
            )

            return final_response
        else:
            message = {
                'message':'Successful'
            }
            response = make_response(
                jsonify(message)
            )

            new_data = Payment(
                number = phone_number,
                amount = amount
            )

            db.session.add(new_data)
            db.session.commit()

            return response
        
        

api.add_resource(Make_Payment, '/payment')

if __name__ == "__main__":
    app.run(debug=True)
