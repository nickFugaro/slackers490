import jwt
import datetime

class JWT:
	
	secretKey = "Slackers-IT490" #THIS KEY MUST NOT CHANGE AT ANY TIME
	algo = "HS256"
	
	def __init__(self):
		pass

	def getToken(self,email):
		issueAt = datetime.datetime.now().timestamp()
		body = {
			"iss" : "slackers490.IT490",
			"iat" : issueAt,
			"exp" : issueAt-3600,
			"email" : email
		}
		return(jwt.encode(body,self.secretKey,algorithm=self.algo))
		   
	def verifyToken(self,token):
		decodedToken = None
		try:
			decodedToken = jwt.decode(token,self.secretKey,algorithm=self.algo)
		except jwt.ExpiredSignatureError as error:
			print("RETURN TOKEN EXPIRED")
			return("TOKEN EXPIRED, Please Signin Again")
			   
		print("RETURN: ",decodedToken.get('email'))
		return(decodedToken.get('email'))