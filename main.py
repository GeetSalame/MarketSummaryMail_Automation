import yfinance as yf       #stocks API
import smtplib              #mail API
from serpapi import GoogleSearch  #Nifty API
from datetime import date       #current date

today = date.today()

#---------------------- stock details fetching functions
def checkValidStockName(stock_name:str)->bool:
    try:
        stock = yf.Ticker(stock_name)
        stock.info['currentPrice']
        return 1
    except KeyError:
        print(f"\nName Error : '{stock_name[:-3]}' Invalid stock name entered. Please enter valid stock name.")
        return 0
    except:
        print("\nSomething went wrong!")
        return 0

def getLTP(stock_name:str) -> float:
    try:
        stock = yf.Ticker(stock_name)
        return (stock.info['currentPrice'])
    except:
        print("\nError : Something went wrong while fetching LTP of given Stock!")

def getCurrency(stock_name:str)->str:
    try:
        stock = yf.Ticker(stock_name)
        return stock.info['currency']
    except:
        print("\nError : Something went wrong while fetching currency type of given Stock!")

def getPreviousClose(stock_name:str)->float:
    try:
        stock = yf.Ticker(stock_name)
        return stock.info['previousClose']
    except:
        print("\nError : Something went wrong while fetching previous close of given Stock!")

def getMovement(stock_name:str)->bool:
    try:
        if(getLTP(stock_name)>=getPreviousClose(stock_name)):
            return 1
        else:
            return 0
    except:
        print("\nError : Something went wrong while fetching Up/Down movement of given Stock!")

def getMovementP(stock_name:str)->float:
    try:
        return round(((getLTP(stock_name)-getPreviousClose(stock_name))/getPreviousClose(stock_name))*100, 2)
    except:
        print("\nError : Something went wrong while fetching % change of given Stock!")

#------------------ fetching Nifty value from Google finance API
params = {
  "engine": "google_finance",
  "q": "NIFTY_50:INDEXNSE",
  "api_key": "fc6efab7ff3331c2edf8ec433f87affcb5aa3083fb9fed3970e7419a5a1f0b11"
}

search = GoogleSearch(params)
results = search.get_dict()

Nifty50Obj = {
    "price" : results["summary"]["price"],
    "movement" : results["summary"]["price_movement"]["movement"],
    "percentage" : round(results["summary"]["price_movement"]["percentage"], 2)
}

mailSubject = f"Your daily Stock Market update is here. {today.strftime('%b-%d-%Y')}"

# adding nifty50
mailBody =  f"Nifty50 : {Nifty50Obj['price']} INR ({Nifty50Obj['percentage']}%)\n"

# adding chosen stocks details
mailBody+="\nHere are your chosen stocks todays summary:\n"

#--------------------- fetching input stock names
try:
  with open("stockList.txt") as f:
      for stock in f:
        stocksArray = stock.split(";")
except:
   print("File access Error : \nSomething went wrong while accesing the file 'stockList.txt\n'")

for stock_name in stocksArray:
    stock_name+=".NS"
    try:
        if checkValidStockName(stock_name):
            if getMovement(stock_name):
                mailBody+=f"{stock_name[:-3].upper()}: {getLTP(stock_name)} {getCurrency(stock_name)}, \t\t(+{getMovementP(stock_name)}%)\n"
            else:
                mailBody+=f"{stock_name[:-3].upper()}: {getLTP(stock_name)} {getCurrency(stock_name)}, \t\t({getMovementP(stock_name)}%)\n"
    except:
        print("Something went wrong!!")

mailBody+="\n\nModestly Yours,\nStocks Summary Automation Bot\nMade by Geet Salame\nlinkedin.com/in/geetsalame"
#-------------------- Mailing
print("Mail : \n", mailBody)

# sending the mail
senderMail = "geetsalame156@gmail.com"
receiverMail = "geetsalame156@gmail.com"

mailMsg = f"Subject: {mailSubject}\n\n{mailBody}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(senderMail, "gdrknenzgnjlxpim")

print(f"\nMail status : {senderMail} sending a mail to {receiverMail}")

server.sendmail(senderMail, receiverMail, mailMsg)

print("Mail status : Email sent!!!")
