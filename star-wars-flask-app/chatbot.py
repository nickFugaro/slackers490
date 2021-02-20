import random
import requests

class ChatBot:
  def __init__(self, message):
    self.message = message
  def chatBotResponse(self):  
    message = self.message
    core = message.split()
    if message[0] and message[1] == '!':
        if '!!about' == core[0] and len(core)==1:
            returnMessage = 'Yoda Bot my name is, here to help you with given tasks you may need help with I am! Hrmmm... With you may the force be.'
        elif '!!help' == core[0] and len(core)==1:
            returnMessage = 'I can help you with the following commands:\n' + '-!!about: A little bit about me this will tell! Hrmmm.\n' + '-!!help: I will return a list of all the things I can help you with. Hrmmm.\n' + '-!!funtranslate - Return a message, I can, in a fun language!\n' + '-!!quote - Returns a a famous quote from our beloved franchise!\n' + '-!!force - You if you are one with the force I will tell. Yes, hrrmmm.!\n'
        elif '!!funtranslate' == core[0]:
            try:
                translateThis = str(message.partition('funtranslate')[2])
                req = requests.get('https://api.funtranslations.com/translate/yoda.json?text=' + translateThis)
                json = req.json()
                returnMessage = json['contents']['translated']
            except:
                returnMessage = 'Able to retrieve this message for you young padawan, I was not.'
        elif '!!force' == core[0] and len(core)==1:
            num = random.randint(1,2)
            if num == 1:
                returnMessage = 'One with the force you are.'
            if num == 2:
                returnMessage = 'One with the force you are not.'
        elif '!!quote' == core[0] and len(core)==1:
            req = requests.get('http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote')
            json = req.json()
            returnMessage = json['starWarsQuote']
        else:
            returnMessage = 'Know what you are speaking of young padawan, I do not.'
    else:
        returnMessage = "<img style={{ height: \"100px\", width: \"100px\"}} src=\"" + message +"\"/>" 
    
    return returnMessage


    