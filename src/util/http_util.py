from rest_framework.response import Response
from rest_framework import status

class HttpUtil():

    @staticmethod
    def respond(response_code, messages, data = None):
        if(messages != None):
            if(hasattr(messages, '__len__') and (not isinstance(messages, str))):
                pass
            else:
                messages = [messages]
        dict = {
            'status' : True if response_code<300 else False
        }
        if(messages != None and len(messages)>0):
            dict['messages'] = messages
        if(data != None):
            dict['data'] = data
    
        #status.HTTP_201_CREATED
        return Response(dict, response_code)
