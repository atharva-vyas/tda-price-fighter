import os
import sys
import tda
from tda import auth, client
from tda.client import Client
from tda.auth import easy_client
from tda.orders.equities import equity_buy_limit
from tda.orders.common import Duration, Session
from tda.orders.common import OrderType
from tda.orders.generic import OrderBuilder
from tda.orders.options import OptionSymbol
from datetime import timedelta
from datetime import date
from time import sleep
import datetime
import calendar
import json
import config

try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path='C:/Python38-64/Lib/site-packages/chromedriver') as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path, config.account_id)



#EXECUTER
tickerInput = input("ENTER TICKER SYMBOL \n -> ")
ticker = tickerInput.upper()

security = input("ENTER THE SECURITY TYPE YOU WOULD LIKE TO TRADE \n  (1)	DERIVATIVES\n  (2)	EQUITIES \n -> ")

#DERIVATIVES
if security == '1':
	optionCP = input("ENTER THE DERIVATIVE DIRECTION \n  (1)	CALL\n  (2)	PUT \n -> ")

	#CALL
	if optionCP == '1':

		#STRIKE PRICE SELECTOR
		contract_type = client.Client.Options.ContractType.CALL
		strikePrice = int(input("ENTER STRIKE PRICE\n -> "))
		strike = "%0.1f" % strikePrice

		#DTE CALCULATOR
		days_to_expirationInput =  input("ENTER DAYS TILL EXPIRATION FOR YOUR CONTRACT\n -> ")
		days_to_expiration = int(days_to_expirationInput)
		today = datetime.date.today() + timedelta(days=days_to_expiration)
		days_to_expirationSTR = str(today)
		days_to_expirationDTE = days_to_expirationSTR + ':' + days_to_expirationInput

		#CONTRACT SIZE
		contractSize = input("ENTER THE NUMBER OF CONTRACTS YOU WOULD LIKE TO TRADE\n -> ")


		#DATE
		DTEyear = int(today.strftime('%Y'))
		DTEday = int(today.strftime('%d'))
		DTEmonth = int(today.strftime('%m'))
		print('datetime.date year=' + str(DTEyear), 'month=' + str(DTEmonth), 'day=' + str(DTEday))

		#CONTRACT LAST PRICE
		response = c.get_option_chain(ticker) 
		json_data = json.loads(response.text)
		lastPrice = json_data['callExpDateMap'][days_to_expirationDTE][strike][0]['last']

		#ORDER BUILDER
		symbolCall1 = OptionSymbol(ticker, datetime.date(year=DTEyear, month=DTEmonth, day=DTEday), 'C', strike).build()
		symbolCall = str(symbolCall1).split('.')[0]

		#ORDER EXECUTER
		#tda.orders.options.option_buy_to_open_limit(symbolCall, int(contractSize), int(lastPrice))
		#print('\norder sent\n')
		print('THIS IS A WORK IN PROGESS(if you still want to continue open the code and remove the # sign on line 76 ')
		print('\nORDER DETAILS FOR CONTRACT:', symbolCall, '\nTICKER SYMB.', ticker, '\nSTRIKE PRICE', strike, '\nDATE', days_to_expirationSTR, '\nDTE', days_to_expirationInput, '\nLAST TRADING PRICE', lastPrice)

#EQUITY
if security == '2':
	equityLS = input("ENTER THE EQUITY DIRECTION \n  (1)	LONG\n  (2)	SHORT \n -> ")

	#LONG
	if equityLS == '1':
		equitySize = input("ENTER SHARE SIZE \n (minimum 1) -> ")
		response = c.get_quote(ticker)
		json_data = json.loads(response.text)
		lastPrice = json_data[ticker]['lastPrice']
		print(ticker, equitySize, lastPrice)
		tda.orders.equities.equity_buy_limit(ticker, int(equitySize), int(lastPrice))
		print('\norder sent\n')

		#FIGHTER LONG

		response = c.get_account(config.account_id, fields=client.Client.Account.Fields.ORDERS)
		json_data = json.loads(response.text)
		status = json_data['securitiesAccount']['orderStrategies'][0]['status']
		print(json.dumps(response.json(), indent=4))
		order_id = int(json_data['securitiesAccount']['orderStrategies'][0]['orderId'])
		sleep(0.5)

		while status == 'WORKING': #Working: The order is being processed at the exchange.
			
			#os.system("cls")
			print('Order not filled, redeploying fighter.')
			print(order_id, ticker, equitySize, lastPrice)
			Client.cancel_order(order_id, config.account_id)
			tda.orders.equities.equity_buy_limit(ticker, int(equitySize), int(lastPrice))
			print('\norder sent\n')
		
		while status == 'CANCELED': #Canceled: The order has been canceled successfully.
			print('\n orderID:', order_id)
			statusCanceled0= input('The last order has been canceled, do you want to retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				tda.orders.equities.equity_buy_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')

			else:
			 	sys.exit()
		
		while status == 'EXPIRED': #Expired: Order's time in force is up.
			print('\norderID:', order_id)
			statusCanceled0= input('The last order has expired, do you want to retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				tda.orders.equities.equity_buy_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()
		
		while status == 'REJECTED': #Rejected: The order is rejected by the exchange.
			print('\norderID:', order_id)
			statusCanceled0= input('The last order has been rejected by the exchange, do you want to retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				tda.orders.equities.equity_buy_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()

		while status == 'QUEUED': #Queued: The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.
			print('\norderID:', order_id)
			statusCanceled0= input('The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.\ndo you want to cancel and retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				Client.cancel_order(order_id, config.account_id)
				tda.orders.equities.equity_buy_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()

		while status == 'FILLED': #Queued: Order processing is finished and the order is fully or partially filled.
			print('\norderID:', order_id)
			quantity = int(json_data['securitiesAccount']['orderStrategies'][0]['quantity'])
			filledQuantity = int(json_data['securitiesAccount']['orderStrategies'][0]['filledQuantity'])
			remainingQuantity = int(json_data['securitiesAccount']['orderStrategies'][0]['remainingQuantity'])
			successQuantity = quantitiy ,'/', filledQuantity
			if quantity == filledQuantity and remainingQuantity == 0:
				print('Order processing is finished and the order is fully filled. \n(', successQuantity, ')filled')
			else:
				statusCanceled0= input('Order processing is finished and the order is partially filled.\ndo you want to fill the rest? (y/n) \n ->')
				statusCanceled = statusCanceled0.lower()
				if statusCanceled == 'y':
					response = c.get_quote(ticker)
					json_data = json.loads(response.text)
					FailedLastPrice = json_data[ticker]['lastPrice']
					print(ticker, remainingQuantity, FailedLastPrice)
					Client.cancel_order(order_id, config.account_id)
					tda.orders.equities.equity_buy_limit(ticker, int(remainingQuantity), int(FailedLastPrice))
					print('\norder sent\n')
				else:
					sys.exit()

		while status == 'ACCEPTED': #Accepted: The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.
			print('\norderID:', order_id)
			statusCanceled0= input('The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.\ndo you want to cancel and retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				Client.cancel_order(order_id, config.account_id)
				tda.orders.equities.equity_buy_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()

		while status == 'REPLACED': #Queued: The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.
			print('\norderID:', order_id)
			statusCanceled0= input('The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.\ndo you want to cancel and retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				Client.cancel_order(order_id, config.account_id)
				tda.orders.equities.equity_buy_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()

		while status == 'PENDING_ACTIVATION': #PENDING_ACTIVATION:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'PENDING_CANCEL': #PENDING_CANCEL:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'PENDING_REPLACE': #PENDING_REPLACE:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'AWAITING_CONDITION': #AWAITING_CONDITION:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'AWAITING_MANUAL_REVIEW': #AWAITING_MANUAL_REVIEW:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'AWAITING_PARENT_ORDER': #AWAITING_PARENT_ORDER:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'AWAITING_UR_OUR': #AWAITING_UR_OUR:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		else:
			print('UNKNOWN ERROR\nexiting in 3 secs.')
			sleep(3)
			sys.exit()

	#SHORT
	if equityLS == '2':
		equitySize = input("ENTER SHARE SIZE TO SELL \n (minimum 1) -> ")
		response = c.get_quote(ticker)
		json_data = json.loads(response.text)
		lastPrice = json_data[ticker]['lastPrice']
		print(ticker, equitySize, lastPrice)
		tda.orders.equities.equity_sell_limit(ticker, int(equitySize), int(lastPrice))
		print('\norder sent\n')

		#FIGHTER SHORT
		response = c.get_account(config.account_id, fields=client.Client.Account.Fields.ORDERS)
		json_data = json.loads(response.text)
		status = json_data['securitiesAccount']['orderStrategies'][0]['status']
		#print(json.dumps(response.json(), indent=4))

		order_id = int(json_data['securitiesAccount']['orderStrategies'][0]['orderId'])
		sleep(0.5)

		while status == 'WORKING': #Working: The order is being processed at the exchange.
			
			os.system("cls")
			print('Order not filled, redeploying fighter.')
			print(order_id, ticker, equitySize, lastPrice)
			Client.cancel_order(order_id, config.account_id)
			tda.orders.equities.equity_sell_limit(ticker, int(equitySize), int(lastPrice))
			print('\norder sent\n')
		
		while status == 'CANCELED': #Canceled: The order has been canceled successfully.
			print('\n orderID:', order_id)
			statusCanceled0= input('The last order has been canceled, do you want to retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				tda.orders.equities.equity_sell_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
			 	sys.exit()
		
		while status == 'EXPIRED': #Expired: Order's time in force is up.
			print('\norderID:', order_id)
			statusCanceled0= input('The last order has expired, do you want to retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				tda.orders.equities.equity_sell_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()
		
		while status == 'REJECTED': #Rejected: The order is rejected by the exchange.
			print('\norderID:', order_id)
			statusCanceled0= input('The last order has been rejected by the exchange, do you want to retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				tda.orders.equities.equity_sell_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()

		while status == 'QUEUED': #Queued: The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.
			print('\norderID:', order_id)
			statusCanceled0= input('The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.\ndo you want to cancel and retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				Client.cancel_order(order_id, config.account_id)
				tda.orders.equities.equity_sell_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()

		while status == 'FILLED': #Queued: Order processing is finished and the order is fully or partially filled.
			print('\norderID:', order_id)
			quantity = int(json_data['securitiesAccount']['orderStrategies'][0]['quantity'])
			filledQuantity = int(json_data['securitiesAccount']['orderStrategies'][0]['filledQuantity'])
			remainingQuantity = int(json_data['securitiesAccount']['orderStrategies'][0]['remainingQuantity'])
			successQuantity = quantitiy ,'/', filledQuantity
			if quantity == filledQuantity and remainingQuantity == 0:
				print('Order processing is finished and the order is fully filled. \n(', successQuantity, ')filled')
			else:
				statusCanceled0= input('Order processing is finished and the order is partially filled.\ndo you want to fill the rest? (y/n) \n ->')
				statusCanceled = statusCanceled0.lower()
				if statusCanceled == 'y':
					response = c.get_quote(ticker)
					json_data = json.loads(response.text)
					FailedLastPrice = json_data[ticker]['lastPrice']
					print(ticker, remainingQuantity, FailedLastPrice)
					Client.cancel_order(order_id, config.account_id)
					tda.orders.equities.equity_sell_limit(ticker, int(remainingQuantity), int(FailedLastPrice))
					print('\norder sent\n')
				else:
					sys.exit()

		while status == 'ACCEPTED': #Accepted: The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.
			print('\norderID:', order_id)
			statusCanceled0= input('The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.\ndo you want to cancel and retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				print(ticker, equitySize, FailedLastPrice)
				Client.cancel_order(order_id, config.account_id)
				tda.orders.equities.equity_sell_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()

		while status == 'REPLACED': #Queued: The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.
			print('\norderID:', order_id)
			statusCanceled0= input('The submitted order is waiting for processing which cannot be performed now, e.g., due to trading hours limitations.\ndo you want to cancel and retry? (y/n) \n ->')
			statusCanceled = statusCanceled0.lower()
			if statusCanceled == 'y':
				response = c.get_quote(ticker)
				json_data = json.loads(response.text)
				FailedLastPrice = json_data[ticker]['lastPrice']
				#print(ticker, equitySize, FailedLastPrice)
				Client.cancel_order(order_id, config.account_id)
				tda.orders.equities.equity_sell_limit(ticker, int(equitySize), int(FailedLastPrice))
				print('\norder sent\n')
			else:
				sys.exit()

		while status == 'PENDING_ACTIVATION': #PENDING_ACTIVATION:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'PENDING_CANCEL': #PENDING_CANCEL:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'PENDING_REPLACE': #PENDING_REPLACE:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'AWAITING_CONDITION': #AWAITING_CONDITION:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'AWAITING_MANUAL_REVIEW': #AWAITING_MANUAL_REVIEW:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'AWAITING_PARENT_ORDER': #AWAITING_PARENT_ORDER:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		while status == 'AWAITING_UR_OUR': #AWAITING_UR_OUR:
			print('\norderID:', order_id)
			print('\nunknown ERROR:', status)

		else:
			print('UNKNOWN ERROR\nexiting in 3 secs.')
			sleep(3)
			sys.exit()

