import hmac
import hashlib 
import requests
import json

class PaymentTransaction:
    def __init__(self, amount, account, expiration_date, capture, cvv2, transaction, batch_id, industry_type, card_entry_method):
        self.amount = amount
        self.account = account
        self.expiration_date = expiration_date
        self.capture = capture
        self.cvv2 = cvv2
        self.transaction = transaction
        self.batch_id = batch_id
        self.industry_type = industry_type
        self.card_entry_method = card_entry_method

    def send_payment_request(self, epi_id, epi_key):
        print('**************************')
        print('Processing your payment...')
        payload = {
            'amount': self.amount,
            'account': self.account,
            'expirationDate': self.expiration_date,
            'capture': self.capture,
            'cvv2': self.cvv2,
            'transaction': self.transaction,
            'batchID': self.batch_id,
            'industryType': self.industry_type,
            'cardEntryMethod': self.card_entry_method
        }

        concat_payload = '/sale' + json.dumps(payload)

        epi_signature = hmac.new(epi_key, concat_payload.encode(), hashlib.sha256).hexdigest()

        headers={
            'Content-Type': 'application/json',
            'EPI-Id': epi_id,
            'EPI-Signature': epi_signature
        }

        response = requests.post('https://epi.epxuap.com/sale', data=json.dumps(payload), headers=headers)

        return response.json()
    
    
# Prompt user for payment details
amount = float(input('Enter amount: '))
account = input('Enter account number: ')
expiration_date = input('Enter expiration date (MMYY): ')
capture = True if input('Capture payment now? (y/n): ').lower() == 'y' else False
cvv2 = input('Enter CVV2: ')
transaction = int(input('Enter transaction ID: '))
batch_id = int(input('Enter batch ID: '))
industry_type = input('Enter industry type: ')
card_entry_method = input('Enter card entry method: ')

transaction = PaymentTransaction(amount, account, expiration_date, capture, cvv2, transaction, batch_id, industry_type, card_entry_method)
epi_id = b'<YOUR-EPI-ID>'
epi_key = b'<YOUR-EPI-KEY>'
response = transaction.send_payment_request(epi_id, epi_key)

print('******************************')

print('Payment status:', response['data']['text'])

print('------------------------------')

print('Payment details:', response)

print('******************************')