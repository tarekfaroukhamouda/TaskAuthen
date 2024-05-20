import json

from flask import Flask,request,jsonify
from config import lol
import imp
import os
import sys
from flask import Response
from integeration import *
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
app = Flask(__name__)

@app.route('/', methods=['POST'])
def transaction():
    if request.is_json:
        data = request.get_json()


        # Get form data from the request
    elif request.form:
        data = request.form.to_dict()


        # Get raw data from the request
    else:
        data = request.data.decode('utf-8')
        return jsonify({'message': 'Raw data received', 'data': data}), 200

    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = lol.API_LOGIN_ID
    merchantAuth.transactionKey =lol.TRANSACTION_KEY
    try:
        creditCard=Card(data['card_number'],data['expired_date'],data['card_code'])
        creditCard=creditCard.createCard()
    except:
        return Response("Error while creating card",status=400)


    try:
        payment=Payment(creditCard)
        payment=payment.createPayment()
    except:
        return Response("Error while creating payment",status=400)

    try:
        order=Order(data['invoice_code'],data['order_description'])
        order=order.createOrder()
    except:
        return Response("Error while creating order",status=400)


    try:
        customeraddress = CustomerAddress(data['customer']['first_name'],data['customer']['last_name'],data['customer']['company'],data['customer']['address'],data['customer']['city'],data['customer']['state'],data['customer']['zip'],data['customer']['country'])
        customeraddress=customeraddress.AddCustmerAddress()
    except:
        return Response("Error while creating customer address",status=400)

    try:
        customerdata=CustomerData(data['customer']['type'],data['customer']['id'],data['customer']['email'])
        customerdata=customerdata.createCustomerData()
    except:
        return Response("Error while creating customer data",status=400)

    settings = apicontractsv1.ArrayOfSetting()

    try:
        duplicateWindowSetting = apicontractsv1.settingType()
        duplicateWindowSetting.settingName = "duplicateWindow"
        duplicateWindowSetting.settingValue = "600"
        settings.setting.append(duplicateWindowSetting)
    except:
        return Response("Error while creating settings", status=400)
    try:
        line_items = apicontractsv1.ArrayOfLineItem()
        for item in data['items']:
                    line_item = apicontractsv1.lineItemType()
                    line_item.itemId = item['id']
                    line_item.name = item['name']
                    line_item.description = item['description']
                    line_item.quantity = item['quantity']
                    line_item.unitPrice = item['price']
                    line_items.lineItem.append(line_item)

    except:
        return Response("Error while creating items", status=400)

    # Create a transactionRequestType object and add the previous objects to it.
    try:
        transactionrequest=Transaction("authCaptureTransaction",data['amount'],payment,order,customeraddress,customerdata,settings,line_items)
        transactionrequest=transactionrequest.createTransaction()
        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId = "MerchantID-0001"
        createtransactionrequest.transactionRequest = transactionrequest
        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()
        response = createtransactioncontroller.getresponse()
    except:
        return Response("Error while creating transaction", status=400)

    if response is not None:
        # Check to see if the API request was successfully received and acted upon
        if response.messages.resultCode == "Ok":

            # Since the API request was successful, look for a transaction response
            # and parse it to display the results of authorizing the card
            if hasattr(response.transactionResponse, 'messages') is True:
                return Response(json.dumps({"description":str(response.transactionResponse.messages.message[0].description),
                                 "statuscode":str(response.transactionResponse.responseCode),
                                 "transaction_id":str(response.transactionResponse.transId)
                                 }))
            else:
                print('Failed Transaction.')
                if hasattr(response.transactionResponse, 'errors') is True:
                    print('Error Code:  %s' % str(response.transactionResponse.
                                                  errors.error[0].errorCode))
                    print(
                        'Error message: %s' %
                        response.transactionResponse.errors.error[0].errorText)
                    return Response({"error_code": str(response.transactionResponse.
                                                  errors.error[0].errorCode),
                                     "error_message": str(response.transactionResponse.errors.error[0].errorText)})

        else:
            if hasattr(response, 'transactionResponse') is True and hasattr(
                    response.transactionResponse, 'errors') is True:
                return Response({"error_code": str(response.transactionResponse.
                                                   errors.error[0].errorCode),
                                 "error_message": str(response.transactionResponse.errors.error[0].errorText)})
            else:
                print('Error Code: %s' %
                      response.messages.message[0]['code'].text)
                print('Error message: %s' %
                      response.messages.message[0]['text'].text)
                return Response(json.dumps({"error_code": str(response.messages.message[0]['code'].text),
                                 "error_message": str(response.messages.message[0]['text'].text)}))
    else:
        return Response({"message": "Null Response"})

if __name__ == "__main__":
    app.run(debug=True)