import telebot
from telebot import types
import requests

TOKEN = "*******"
bot = telebot.TeleBot(TOKEN)

MY_WALLET = "0xf104a07d8a87f4aa98ea28baf19d727a00666fd1"

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_price = types.KeyboardButton("Prices")
    btn_scan = types.KeyboardButton("Scan Token")
    btn_vip = types.KeyboardButton("VIP Access")
    btn_support = types.KeyboardButton("Support")
    markup.add(btn_price, btn_scan, btn_vip, btn_support)
    
    msg = "Welcome to UniFast Crypto Bot! Choose an option:"
    bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Prices")
def get_prices(message):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,solana,toncoin&vs_currencies=usd"
        res = requests.get(url, timeout=10).json()
        btc = res.get('bitcoin', {}).get('usd', 'N/A')
        eth = res.get('ethereum', {}).get('usd', 'N/A')
        sol = res.get('solana', {}).get('usd', 'N/A')
        bnb = res.get('binancecoin', {}).get('usd', 'N/A')
        ton = res.get('toncoin', {}).get('usd', 'N/A')
        
        text = f"Live Prices:\n\nBTC: ${btc}\nETH: ${eth}\nSOL: ${sol}\nBNB: ${bnb}\nTON: ${ton}"
        bot.send_message(message.chat.id, text)
    except Exception:
        bot.send_message(message.chat.id, "Error fetching prices. Please try again.")

@bot.message_handler(func=lambda msg: msg.text == "VIP Access")
def vip_info(message):
    text = (
        "VIP Subscription (Signals & Gems)\n\n"
        "Price: 20 USDT (Monthly)\n\n"
        "Deposit Wallet (BSC / BEP20):\n"
        f"{MY_WALLET}\n\n"
        "Send TXID or screenshot to Support after deposit."
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda msg: msg.text == "Support")
def support_info(message):
    bot.send_message(message.chat.id, "Support contact: @UniFastDeFiBot")

@bot.message_handler(func=lambda msg: msg.text == "Scan Token")
def scan_prompt(message):
    bot.send_message(message.chat.id, "Send smart contract address to scan.")

print("Bot is running...")
bot.infinity_polling()
