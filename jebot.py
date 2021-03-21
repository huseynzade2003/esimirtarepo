import os
import aiohttp
from pyrogram import filters, Client
from pytube import YouTube
from youtubesearchpython import VideosSearch
from sample_config import Config
from ut import get_arg

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent


Jebot = Client(
   "Hüsü Song🎶",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()

@Jebot.on_message(filters.private & ~filters.bot & ~filters.command("help") & ~filters.command("start") & ~filters.command("s"))  

async def song(client, message):

    message.chat.id
    user_id = message.from_user["id"]
    args = message.text.split(None, 1)
    args = str(args)

    args = args + " " + "song"
    
    status = await message.reply(
             text="<b>Mahnınız yüklənir. zəhmət olmasa gözləyin😁\n\nQurucum: @Mr_HD_20⚡</b>",
             disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        "Qrupumuz✅", url="https://t.me/creativmafia")
                                ]]
                        ),
               parse_mode="html",
        reply_to_message_id=message.message_id
      )
    video_link = yt_search(args)
    if not video_link:
        await status.edit("<b>Bu mahnı tapılmadı 😑</b>")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("<b>Mahnını yükləmək alınmadı 🤕</b>")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await Jebot.send_chat_action(message.chat.id, "upload_audio")
    await Jebot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")    
    
    
    
@Jebot.on_message(filters.command("s"))
async def song(client, message):
    message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("<b>Mahnı adı daxil edin❗\n\nMisal: Elvin Nasir Canan`</b>")
        return ""
    status = await message.reply(
             text="<b>Mahnınız yüklənir, xahiş edirəm gözləyin👀\n\n@Mr_HD_20 tərəfindən yaradıldım⚡</b>",
             disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        "Qrupumuz✅", url="https://t.me/creativechat")
                                ]]
                        ),
               parse_mode="html",
        reply_to_message_id=message.message_id
      )
    video_link = yt_search(args)
    if not video_link:
        await status.edit("<b>Mahnı tapılmadı 😑</b>")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("<b>Mahnını yükləmək alınmadı 🤕</b>")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await Jebot.send_chat_action(message.chat.id, "upload_audio")
    await Jebot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")

@Jebot.on_message(filters.command("start"))
async def start(client, message):
   if message.chat.type == 'private':
       await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>Hey Salam, Mən Hüsü Song🎶 Bot
İstifadəsi: Sadəcə mahnı adı

@Mr_HD_20 tərəfindən yaradıldım⚡

Məni necə istifadə edəcəyinizi öyrənmək üçün kömək düyməsini vurun</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "🆘Kömək🆘", callback_data="help"),
                                        InlineKeyboardButton(
                                            "✨Qrupumuz✨", url="https://t.me/creativmafia")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html",
            reply_to_message_id=message.message_id
        )
   else:

       await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>Mahnı Yükləyici Aktivdir\n\n</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "Kömək", callback_data="help")
                                        
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html",
            reply_to_message_id=message.message_id
        )

@Jebot.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':   
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>Mahnı yükləmək üçün bir mahnı adı göndərin

~ @Mr_HD_20</b>""",
            reply_to_message_id=message.message_id
        )
    else:
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="<b>Mahnı Yükləyicidən istifadə\n\nMahnı adı daxil edin❗\n\nMisal: `Elvin Nasir Canan`</b>",
            reply_to_message_id=message.message_id
        )     
        

@Jebot.on_callback_query()
async def button(Jebot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(Jebot, update.message)

print(
    """
Bot başladı!

Qoşulun @CreativMafia
"""
)

Jebot.run()
