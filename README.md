# tda-price-fighter
 This algo helps you to get the best fills possible (at least better than TOS market orders)
  NOTE: THIS IS A OLD VERSION AND MIGHT BE BROKEN*
 
 
 Since I had nothing better to do over this three day weekend I coded an order execution algo for you td degens out there, this algo helps you to get the best fills    possible (at least better than TOS market orders), as of right now this algo only allows you to buy and sell equities(im working on derivative trading with this algo) and as time progress I will try my best to add more features along the way. And if you have any questions regarding this algo or anything else feel free to ping me up

github rep: 
 https://github.com/alexgolec/tda-api

Documents for reference and debugging:
 https://tda-api.readthedocs.io/en/stable/getting-started.html


Requirements:
 Python,
 Stable internet connection,
 Security with a decent spread

How to configure:
1)    Before you do anything, download the github rep and copy main.py and config.py to the downloaded path
2)    create an account and an application(click myApps and then click newApp) on the TD Ameritrade developer website(https://developer.tdameritrade.com/). After registering you'll receive an API key, also known as a Client Id, which will have  to copy to the config.py file.
3)    You'll also want to make sure that your callback URI(redirect_uri) is set to https://localhost/ on your TD Ameritrade developer website account
4)    Go to config.py file and paste your Client Id and your TD account id
5)    Run main.py, and if you see an prompt asking you to enter the ticker symbol of the security you want to trade, then you should be good to go

 NOTE: As I have coded this over the 3 day holiday so expect some bugs and if you do find some and manage to fix them, ping me up and I will fix it in my version as well(if not done already), also since I have coded this over a very short period of time, the algo as of right now is not the most optimized out there, so expect it to be jittery, buggy and the code to be a little bit confusing (I have tried my best to comment all the major parts of the code).

 NOTE 2:  this algo works the best when the spreads are tight, and if you are planning to use it for trading securities with spreads all over the place expect to wait for some time before getting a fill.

 DISCLAIMER: I AM NOT RESPONISBLE FOR ANYTHING THAT YOU DO WITH THIS ALGO

 I hope this helps you in getting better fills!
