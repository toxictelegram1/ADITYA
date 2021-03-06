# Aditya Halder // @AdityaHalder
# Toxic๐๐ฎ๐ฌ๐ข๐ // @wtf_realtoxic
import os
import aiofiles
import aiohttp
import ffmpeg
import random
import requests
from os import path
from modules import bot
from asyncio.queues import QueueEmpty
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from modules.cache.admins import set
from modules.clientbot import clientbot, queues
from modules.clientbot.clientbot import client as USER
from modules.helpers.admins import get_administrators
from youtube_search import YoutubeSearch
from modules import converter
from modules.downloaders import youtube
from modules.config import DURATION_LIMIT, que, SUDO_USERS
from modules.cache.admins import admins as a
from modules.helpers.filters import command, other_filters
from modules.helpers.command import commandpro
from modules.helpers.decorators import errors, authorized_users_only
from modules.database.dbchat import (get_served_chats, is_served_chat, add_served_chat)
from modules.helpers.errors import DurationLimitError
from modules.helpers.gets import get_url, get_file_name
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

# plus
chat_id = None
useer = "NaN"

themes = [
    "bgreen",
    "blue",
    "colorfull",
    "dgreen",
    "hgreen",
    "lgreen",
    "lyellow",
    "orange",
    "pink",
    "purple",
    "rainbow",
    "red",
    "sky",
    "thumbnail",
    "yellow",
]

def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    theme = random.choice(themes)
    image1 = Image.open("./background.png")
    image2 = Image.open(f"resource/{theme}.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("resource/font.otf", 32)
    draw.text((190, 550), f"Title: {title[:50]} ...", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Powered By: Toxic (@wtf_realtoxic)",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    commandpro(["play", "/play", "!play", ".play", "ply", "@", "#"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    await message.delete()

    lel = await message.reply("**๐ ๐๐๐๐ซ๐๐ก๐ข๐ง๐? ...**")

    if not await is_served_chat(message.chat.id):
        await lel.edit(f"**๐ฅ ๐๐จ๐ซ๐ซ๐ฒ ๐๐ก๐ข๐ฌ ๐บ ๐๐ฎ๐ฌ๐ข๐ ๐๐จ๐๐จ๐ญ\n๐๐ง๐ฅ๐ฒ ๐๐จ๐ซ ๐๐ซ๐๐ฆ๐ข๐ฎ๐ฆ ๐๐ฌ๐๐ซ๐ฌ โจ...\n\n๐ ๐๐ ๐๐จ๐ฎ โฅ๏ธ๐๐๐ง๐ญ ๐ธ ๐ญ๐จ ๐๐๐ ๐ข๐ง\n๐๐จ๐ฎ๐ซ ๐๐ซ๐จ๐ฎ๐ฉ ๐๐ก๐๐ง ๐๐จ๐ง๐ญ๐๐๐ญ ๐ท\nโฅ๏ธ ๐๐จ โช [Toxic](https://t.me/wtf_realtoxic) ...**", disable_web_page_preview=True)
        return await bot.leave_chat(message.chat.id)  
    if message.sender_chat:
        return await lel.edit("**๐ฅ ๐๐ฅ๐๐๐ฌ๐ ๐๐จ๐ง'๐ญ ๐๐ฌ๐ ๐๐ก๐๐ง๐ง๐๐ฅ ๐๐จ๐ซ ๐๐จ๐ฆ๐ฆ๐๐ง๐๐ฌ โจ ...**")  
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "โคอออโฅออก๐โ๐ง๐ผ๐๐ถ๐ฐ๐๏ธโโูููู โููููู๐ฆ๐๐ฎ๐ฌ๐ข๐๐โ๐ธ"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "**๐ฃ๐ฒ๐ต๐น๐ฒ ๐ฎ๐ฑ๐บ๐ถ๐ป ๐๐ผ๐ต ๐ฏ๐ฎ๐ป๐ฎ๐ผ...**")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "** ๐ฆ๐ผ๐ป๐ด ๐ฏ๐ฎ๐ท๐ฎ๐ป๐ฒ ๐ธ๐ฒ ๐น๐ถ๐๐ฒ ๐ฟ๐ฒ๐ฎ๐ฑ๐ ๐ต๐ ...**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"** ๐๐๐๐ถ๐๐๐ฎ๐ป๐ ๐ธ๐ผ ๐บ๐ฎ๐ป๐๐ฎ๐น๐น๐ ๐ฎ๐ฑ๐ฑ ๐ธ๐ฎ๐ฟ๐ผ ๐๐ฎ ๐ผ๐ป๐๐ฒ๐ฟ ๐๐ฒ ๐ฐ๐ผ๐ป๐๐ฎ๐ฐ๐ ๐ธ๐ฎ๐ฟ๐ผห [Toxic](https://t.me/wtf_realtoxic) โจ ...**")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"** ๐๐๐๐ถ๐๐๐ฎ๐ป๐ ๐ธ๐ผ ๐บ๐ฎ๐ป๐๐ฎ๐น๐น๐ ๐ฎ๐ฑ๐ฑ ๐ธ๐ฎ๐ฟ๐ผ ๐๐ฎ ๐ผ๐ป๐๐ฒ๐ฟ ๐๐ฒ ๐ฐ๐ผ๐ป๐๐ฎ๐ฐ๐ ๐ธ๐ฎ๐ฟ๐ผห [Toxic](https://t.me/wtf_realtoxic) โจ ...**")
        return
    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**๐ฅ ๐๐ฅ๐๐ฒ ๐ ๐๐ฎ๐ฌ๐ข๐ ๐ฟ ๐๐๐ฌ๐ฌ โก๏ธ\n๐ค ๐๐ก๐๐งโก๏ธ {DURATION_LIMIT} ๐ ๐๐ข๐ง๐ฎ๐ญ๐ ...**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/efa287d73d9d5dd3b1347.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="๐๐ฟ๐ผ๐๐ฝ",
                            url=f"https://t.me/Dangerouschatting")

                ]
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="๐๐ฟ๐ผ๐๐ฝ",
                            url=f"https://t.me/Dangerouschatting")

                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/efa287d73d9d5dd3b1347.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="๐๐ฟ๐ผ๐๐ฝ",
                            url=f"https://t.me/Dangerouschatting")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**๐ฅ ๐๐ฅ๐๐ฒ ๐ ๐๐ฎ๐ฌ๐ข๐ ๐ฟ ๐๐๐ฌ๐ฌ โก๏ธ\n๐ค ๐๐ก๐๐งโก๏ธ {DURATION_LIMIT} ๐ ๐๐ข๐ง๐ฎ๐ญ๐ ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**๐ค ๐๐ข๐ฏ๐ ๐ ๐๐ฎ๐ฌ๐ข๐ ๐ฟ ๐๐๐ฆ๐ ๐\n๐ ๐๐จ ๐ ๐๐ฅ๐๐ฒ ๐ฅ ๐๐จ๐ง๐? ๐ท...**"
            )
        await lel.edit("**๐ ๐๐ซ๐จ๐๐๐ฌ๐ฌ๐ข๐ง๐? ...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**๐ ๐๐ฎ๐ฌ๐ข๐ ๐ ๐๐จ๐ญ ๐ต ๐๐จ๐ฎ๐ง๐โ๏ธ\n๐ ๐๐ซ๐ฒ โจ๏ธ ๐๐ง๐จ๐ญ๐ก๐๐ซ ๐ท...**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="๐๐ฟ๐ผ๐๐ฝ",
                            url=f"https://t.me/Dangerouschatting")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**๐ฅ ๐๐ฅ๐๐ฒ ๐ ๐๐ฎ๐ฌ๐ข๐ ๐ฟ ๐๐๐ฌ๐ฌ โก๏ธ\n๐ค ๐๐ก๐๐งโก๏ธ {DURATION_LIMIT} ๐ ๐๐ข๐ง๐ฎ๐ญ๐ ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="๐ฅ ๐ง๐ผ๐๐ถ๐ฐ๐ค๐๐ฎ๐ฌ๐ข๐ ๐ฟ ๐๐ฎ๐๐ฎ๐๐โ๏ธ\n๐ ๐๐ญ ๐ ๐๐จ๐ฌ๐ข๐ญ๐ข๐จ๐ง ยป `{}` ๐ท ...**".format(position),
            reply_markup=keyboard,
        )
    else:
        await clientbot.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**๐ฅ ๐ง๐ผ๐๐ถ๐ฐ๐ค๐๐ฎ๐ฌ๐ข๐ ๐ธ ๐๐ฅ๐๐ฒ๐ข๐ง๐? ๐\n๐ ๐๐ฎ๐ซ๐ซ๐๐ง๐ญ ๐ ๐๐จ๐ง๐? ๐ฅ ...**".format(),
           )

    os.remove("final.png")
    return await lel.delete()
    
    
@Client.on_message(commandpro(["pause", "/pause", "!pause", ".pause", "pse"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await message.delete()
    await clientbot.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("**๐๐๐ฎ๐ฌ๐๐ ๐ท ...**")


@Client.on_message(commandpro(["resume", "/resume", "!resume", ".resume", "rsm"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await message.delete()
    await clientbot.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("**๐๐๐ฌ๐ฎ๐ฆ๐๐ ๐ท ...**")



@Client.on_message(commandpro(["skip", "/skip", "!skip", ".skip", "skp"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    await message.delete()
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**๐๐จ๐ญ๐ก๐ข๐ง๐? ๐๐ฅ๐๐ฒ๐ข๐ง๐? ๐ท ...**")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await clientbot.pytgcalls.leave_group_call(chat_id)
            await message.reply_text("**๐ฅ ๐๐ฆ๐ฉ๐ญ๐ฒ ๐๐ฎ๐๐ฎ๐, ๐๐๐๐ฏ๐ข๐ง๐? ๐๐ โจ...**")
        else:
            await message.reply_text("**๐๐ค๐ข๐ฉ๐ฉ๐๐ ๐ท ...**")
            await clientbot.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        clientbot.queues.get(chat_id)["file"],
                    ),
                ),
            )



@Client.on_message(commandpro(["stop", "end", "/stop", "/end", "!stop", "!end", ".stop", ".end", "stp"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    await message.delete()
    try:
        clientbot.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await clientbot.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("**๐๐ญ๐จ๐ฉ๐ฉ๐๐ ๐ท ...**")


@Client.on_message(commandpro(["reload", "/reload", "!reload", ".reload", "rld"]) & other_filters)
@errors
@authorized_users_only
async def update_admin(client, message):
    global a
    await message.delete()
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    a[message.chat.id] = new_admins
    await message.reply_text("**๐๐๐ฅ๐จ๐๐๐๐ ๐ท ...**")
