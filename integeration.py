from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
from config import lol
class Card():
    def __init__(self,cardNumner,expirationDate,cardCode):
        self.cardNumber=cardNumner
        self.expirationDate=expirationDate
        self.cardCode=cardCode
    def createCard(self):
        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber =self.cardNumber
        creditCard.expirationDate = self.expirationDate
        creditCard.cardCode = self.cardCode

        return creditCard



class Payment():

    def __init__(self, creditCard):
        self.creditCard = creditCard

    def createPayment(self):
        payment = apicontractsv1.paymentType()
        payment.creditCard = self.creditCard
        return payment

class Order():
    def __init__(self,invoiceNumber,description=""):
        self.invoiceNumber=invoiceNumber
        self.description=description

    def createOrder(self):
        order = apicontractsv1.orderType()
        order.invoiceNumber=self.invoiceNumber
        order.description=self.description
        return order
class CustomerAddress():

    def __init__(self,firstName,lastName,company,address,city,state,zip,country):
        self.firstName = firstName
        self.lastName = lastName
        self.company = company
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country

    def AddCustmerAddress(self):
        customerAddress = apicontractsv1.customerAddressType()
        customerAddress.firstName =self.firstName
        customerAddress.lastName = self.lastName
        customerAddress.company = self.company
        customerAddress.address = self.address
        customerAddress.city = self.city
        customerAddress.state = self.state
        customerAddress.zip = self.zip
        customerAddress.country = self.country
        return customerAddress

class CustomerData():

    def __init__(self,type,id,email):
        self.type=type
        self.email=email
        self.id=id

    def createCustomerData(self):
        customerData = apicontractsv1.customerDataType()
        customerData.type = self.type
        customerData.id = self.id
        customerData.email = self.email


class DSettings():
    def __init__(self,settingName,settingValue):
        self.settingName=settingName
        self.setingValue=settingValue

    def createDsettings(self):
        duplicateWindowSetting = apicontractsv1.settingType()
        duplicateWindowSetting.settingName = self.settingName
        duplicateWindowSetting.settingValue = self.setingValue

        return duplicateWindowSetting



class Transaction():

        def __init__(self,transactionType,amount,transaction_payment,transaction_order, customeraddress, customerdata,bsettings ,line_items):
            self.transactionrequest = apicontractsv1.transactionRequestType()
            self.transactionrequest.transactionType = transactionType
            self.transactionrequest.amount = amount
            self.transactionrequest.payment = transaction_payment
            self.transactionrequest.order = transaction_order
            self.transactionrequest.billTo = customeraddress
            self.transactionrequest.customer = customerdata
            self.transactionrequest.transactionSettings = bsettings
            self.transactionrequest.lineItems = line_items

        def createTransaction(self):

            return self.transactionrequest

        def createTransactionRequest(self):
            merchantAuth = apicontractsv1.merchantAuthenticationType()
            merchantAuth.name = lol.API_LOGIN_ID
            merchantAuth.transactionKey = lol.TRANSACTION_KEY
            createtransactionrequest = apicontractsv1.createTransactionRequest()
            createtransactionrequest.merchantAuthentication = merchantAuth
            createtransactionrequest.refId = "MerchantID-0001"
            createtransactionrequest.transactionRequest = self.transactionrequest
            createtransactioncontroller = createTransactionController(
                createtransactionrequest)
            createtransactioncontroller.execute()

            response = createtransactioncontroller.getresponse()
            return response

        def parseresponse(self,response):
            if response is not None:

                if response.messages.resultCode == "Ok":

                    # Since the API request was successful, look for a transaction response
                    # and parse it to display the results of authorizing the card
                    if hasattr(response.transactionResponse, 'messages') is True:
                        print(
                            'Successfully created transaction with Transaction ID: %s'
                            % response.transactionResponse.transId)


                        print('Transaction Response Code: %s' %
                              response.transactionResponse.responseCode)
                        print('Message Code: %s' %
                              response.transactionResponse.messages.message[0].code)
                        print('Description: %s' % response.transactionResponse.
                              messages.message[0].description)

                        return 'Successfully created transaction with Transaction ID: %s'+ response.transactionResponse.messages.message[0].description
                    else:
                        print('Failed Transaction.')
                        if hasattr(response.transactionResponse, 'errors') is True:
                            print('Error Code:  %s' % str(response.transactionResponse.
                                                          errors.error[0].errorCode))
                            print(
                                'Error message: %s' %
                                response.transactionResponse.errors.error[0].errorText)
                # Or, print errors if the API request wasn't successful
                else:
                    print('Failed Transaction.')
                    if hasattr(response, 'transactionResponse') is True and hasattr(
                            response.transactionResponse, 'errors') is True:
                        print('Error Code: %s' % str(
                            response.transactionResponse.errors.error[0].errorCode))
                        print('Error message: %s' %
                              response.transactionResponse.errors.error[0].errorText)
                    else:
                        print('Error Code: %s' %
                              response.messages.message[0]['code'].text)
                        print('Error message: %s' %
                              response.messages.message[0]['text'].text)
            else:
                print('Null Response.')





