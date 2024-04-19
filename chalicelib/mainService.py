import os
import json
import datetime
from datetime import timezone
import requests
import uuid
from chalice import Blueprint
from chalice import Response
from chalicelib.miscFunctions import writeToKafka 
from time import strftime
import boto3

mainService = Blueprint(__name__)

HM_SERVER_BASE_ADDRESS = os.environ["HM_SERVER_BASE_ADDRESS"]
HM_API_KEY = os.environ["HM_API_KEY"]
GODREJ_PRODS = os.environ["GODREJ_PRODS"]
API_KEY = os.environ["API_KEY"]

DEBUG_LOGS_ENABLE = True 

@mainService.route('/v4/{prodId}', methods=['POST'], cors=True)
def createDevice(prodId):

    responseMessage = {}
    responseSubMessage = {}

    try:
        print(GODREJ_PRODS)

        headers = mainService.current_request.headers
        payload = mainService.current_request.json_body
        api_key = headers['x-api-key']

        if api_key == API_KEY:

            url = HM_SERVER_BASE_ADDRESS + '/v4/' + prodId
            headers = {'Accept': '*/*','Content-Type':'application/json','x-api-key':HM_API_KEY}

            response = requests.post(url=url,json=payload,headers=headers)        
            resStatusCode = response.status_code

            if resStatusCode == 200:

                if prodId in GODREJ_PRODS:
                
                    try :

                        message = payload
                        print(message)

                        writeToKafka(message)

                        resMessage = response.json()
                        return Response(body=resMessage, status_code=200, headers={'Content-Type': 'application/json'})

                    except Exception as e:

                        responseSubMessage['errorCode'] = 1004
                        responseSubMessage['errorMessage'] = str(e)
                        responseMessage['type'] = 'error'
                        responseMessage['message'] = responseSubMessage
                        return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})

            else:

                responseSubMessage['errorCode'] = 1003
                responseSubMessage['errorMessage'] = 'Not expected response from hardware management'
                responseSubMessage['originErrorMessage'] = response.json()
                responseMessage['type'] = 'error'
                responseMessage['message'] = responseSubMessage
                return Response(body=responseMessage, status_code=resStatusCode, headers={'Content-Type': 'application/json'})
            
        else:

            responseSubMessage['errorCode'] = 1002
            responseSubMessage['errorMessage'] = 'User authentication failed.'
            responseMessage['type'] = 'error'
            responseMessage['message'] = responseSubMessage
            return Response(body=resMessage, status_code=401, headers={'Content-Type': 'application/json'})

    except Exception as e:

        responseSubMessage['errorCode'] = 1001
        responseSubMessage['errorMessage'] = str(e)
        responseMessage['type'] = 'error'
        responseMessage['message'] = responseSubMessage
        return Response(body=responseMessage, status_code=400, headers={'Content-Type': 'application/json'})