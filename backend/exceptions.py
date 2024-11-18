from flask import make_response

class CustomException(Exception):
    def __init__(self, message="", statusCode=500):
        self.message = message
        self.statusCode = statusCode
    
    def toResponse(self):
        return make_response({
            "message": self.message
        }, self.statusCode)