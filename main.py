import requests
import asyncio
import telegram
import re
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
vk_token = "8cf490fc8cf490fc8cf490fc1f8fe26bb988cf48cf490fce959977c8b5df9fb89ac8bf7"
vk_version = 5.199

async def getPost(post_id):
        params = {
  "posts": post_id[0],
  "access_token": vk_token,
  "v": vk_version
}
        response = requests.get('https://api.vk.ru/method/wall.getById', params)
        responseJSON = json.loads(response.text)
        return responseJSON

def parsePost(resp):
    post_text = resp["response"]["items"][0]["text"]
    post_media = resp["response"]["items"][0]["attachments"]
    media = []
    for items in post_media:
        if items["type"] == "photo":
             size_len = len(items["photo"]["sizes"])
             m_element = telegram.InputMediaPhoto(media=items["photo"]["sizes"][size_len - 1]["url"], )
             media += [m_element]
    return {"text": post_text, "media": media}

async def startFunc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send me the link and I will give you a meme!")



async def getLink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Give me a second...")
    post_id = re.findall(r'-?\d+_?-?\d+', update.message.text)
    resp = await getPost(post_id= post_id)
    parsed = parsePost(resp)
    # print(parsed)
    if parsed["media"]:
        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=parsed["media"], caption=parsed["text"])
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=parsed["text"])
    
    


async def getOther(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Give me a link to VK post")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6416908428:AAF65gD-0pijzojstfgjHTgCRTHhOmTn-oo').build()
    
    start_handler = CommandHandler('start', startFunc)
    application.add_handler(start_handler)

    link_handler = MessageHandler(filters.Regex(r'.*vk\.\w+\/.*'), getLink)
    application.add_handler(link_handler)

    other_handler = link_handler = MessageHandler(filters.TEXT, getOther)
    application.add_handler(other_handler)
    
    application.run_polling()

# VK

# print(response.status_code)
# print(response.text)