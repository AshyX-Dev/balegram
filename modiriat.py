token = "362716073:yVfajbcw3YOn1Ljz5WS1ERcRIcoDmwos75QEmXFJ"
admins = [ 554324725, ... ]

from balegram import AsyncClient
from balegram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from balegram.client import asyncio
from pytz import timezone
from datetime import datetime
import os
import random

bot = AsyncClient(token)
tmzone = timezone("Asia/Tehran")

close_markup = InlineKeyboardMarkup()
close_markup.addKeyboard(
    InlineKeyboardButton(
        "• بستن •",
        callback_data='close'
    )
)


week_days = {
    0: "دوشنبه",
    1: "سه شنبه",
    2: "چهارشنبه",
    3: "پنجشنبه",
    4: "جمعه",
    5: "شنبه",
    6: "یکشنبه"
}

months = {
    1: "فروردین",
    2: "اردیبهشت",
    3: "خرداد",
    4: "تیر",
    5: "مرداد",
    6: "شهریور",
    7: "مهر",
    8: "آبان",
    9: "آذر",
    10: "دی",
    11: "بهمن",
    12: "اسفند"
}

def getTime() -> datetime:
    return datetime.now(tmzone)

@bot.on("message")
async def onMessage(message: Message):
    print(message.text)
    if message.text.startswith("/start"):
        makrup = InlineKeyboardMarkup()
        makrup.addKeyboard(
            InlineKeyboardButton(
                "• Source Code •",
                "https://github.com/Rubier-Project/" # Add repo endpoint
            ),
            InlineKeyboardButton(
                "• راهنما •",
                callback_data="seeHelp"
            )
        )
        await message.asyncReply(
            "به ربات مدیریت گروه خوش آمدید ! برای دیدن راهنما از گزینه 'راهنما' استفاده کنید",
            makrup
        )

    if message.chat.type in ( "group" ):
        if len(message.new_chat_members) != 0:
            # if income_messages['welcome'] == None:
            await bot.sendMessage(message.chat.id, f"کاربر {message.new_chat_members[-1].first_name} به گپ {message.chat.title} خوش اومدی")
            # else:
            #     time = getTime()
            #     await bot.sendMessage(message.chat.id, income_messages['welcome'].replace(
            #     "#time", time.strftime("%H:%M:%S")
            # ).replace(
            #     "#hour", time.strftime("%H")
            # ).replace(
            #     "#min", time.strftime("%M")
            # ).replace(
            #     "#sec", time.strftime("%S")
            # ).replace(
            #     "#title", message.chat.title
            # ).replace(
            #     "#id", str(message.chat.id)
            # ).replace(
            #     "#link", message.chat.invite_link
            # ).replace(
            #     "#user_first_name", message.new_chat_members[0].first_name
            # ).replace(
            #     "#user_last_name", message.new_chat_members[0].last_name
            # ).replace(
            #     "#user_id", str(message.new_chat_members[0].id)
            # ).replace(
            #     "#user_username", message.new_chat_members[0].username
            # ))

        elif not message.left_chat_member.result == {}:
            #if income_messages['leave'] == None:
            await bot.sendMessage(message.chat.id, f"کاربر {message.left_chat_member.first_name} از گروه خارج شد")
            #else:
            #     time = getTime()
            #     b = await bot.sendMessage(message.chat.id, income_messages['leave'].replace(
            #     "#time", time.strftime("%H:%M:%S")
            # ).replace(
            #     "#hour", time.strftime("%H")
            # ).replace(
            #     "#min", time.strftime("%M")
            # ).replace(
            #     "#sec", time.strftime("%S")
            # ).replace(
            #     "#title", message.chat.title
            # ).replace(
            #     "#id", str(message.chat.id)
            # ).replace(
            #     "#link", message.chat.invite_link
            # ).replace(
            #     "#user_first_name", message.left_chat_member.first_name
            # ).replace(
            #     "#user_last_name", message.left_chat_member.last_name
            # ).replace(
            #     "#user_id", str(message.left_chat_member.id)
            # ).replace(
            #     "#user_username", message.left_chat_member.username
            # ))
                
            #     print(b)

        elif message.text in ("time", "تایم", "ساعت", "تاریخ"):
            time = getTime()
            await message.asyncReply(
                f"🍃 روز {week_days[time.weekday()]}\n🍷 ماه {months[abs(time.month - 12)]}\n🍾 سال {time.year - 622}\n\n🛰 ساعت {time.strftime('%H:%M:%S')}",
                close_markup
            )

        elif message.text == "پروفایل":
            if message.from_reply_message.result != {}:
                try:
                    ch = await bot.getChat(message.from_reply_message.from_user.id)
                    if ch.photo.result == {}:
                        await message.asyncReply(
                            f"🧣 اسم: {ch.first_name} - {ch.last_name}\n💻 آیدی عددی: {ch.id}\n👁 آیدی: {ch.username}"
                        )
                    else:
                        photo = await bot.getFile(ch.photo.small_file_id)
                        fname = f"photo_{random.randint(100, 999999)}"
                        await bot.downloadFile(
                            photo.path,
                            fname
                        )
                        if os.path.exists(fname):
                            await message.asyncReplyPhoto(fname, f"🧣 اسم: {ch.first_name} - {ch.last_name}\n💻 آیدی عددی: {ch.id}\n👁 آیدی: {ch.username}")
                            os.unlink(fname)
                        else:
                            await message.asyncReply(
                                f"🧣 اسم: {ch.first_name} - {ch.last_name}\n💻 آیدی عددی: {ch.id}\n👁 آیدی: {ch.username}"
                            )
                except Exception as ErrorGetProfile:
                    await message.asyncReply(f"خطا حین دریافت پروفایل {ErrorGetProfile}", close_markup)
            else: await message.asyncReply("روی پیامی ریپلای زده نشده است")

        if message.from_user.id in admins:

            if message.text.startswith("حذف"):
                if message.from_reply_message.result == {}:
                    length = message.text[3:].strip()
                    if not length.isdigit():await message.asyncReply("خطای ورودی", close_markup)
                    else:
                        msg = await message.asyncReply("درحال دریافت پیام ها ...")
                        if msg['ok']:
                            msg = Message(token, {"message": msg['result']})
                            msg.message_id -= 1
                            for _ in range(int(length)):
                                msg.message_id -= 1
                                try:
                                    await bot.deleteMessage(message.chat.id, msg.message_id)
                                except:pass
                            
                            await bot.sendMessage(
                                message.chat.id,
                                f"تعداد {length} پیام از گپ پاک شد",
                                reply_markup=close_markup
                            )

                else:
                    try:
                        await bot.deleteMessage(message.chat.id, message.from_reply_message.message_id)
                    except Exception as ErrorDeleting:
                        await message.asyncReply(f"خطا حین پاک کردن\n{ErrorDeleting}", close_markup)
            
            elif message.text == "لینک":
                chat = await bot.getChat(message.chat.id)
                if chat.photo.result == {}:
                    members = await bot.getChatMembersCount(message.chat.id)
                    await message.asyncReply(
                        f"🎫 لینک گپ: {chat.invite_link}\n👁 اسم گپ: {chat.title}\n👥 تعداد اعضا: {members.get('result', 'غیر قابل دریافت')}",
                        close_markup
                    )
                else:
                    photo = await bot.getFile(chat.photo.small_file_id)
                    fname = f"photo_{random.randint(100, 999999)}"
                    await bot.downloadFile(
                        photo.path,
                        fname
                    )

                    if os.path.exists(fname):
                        await message.asyncReplyPhoto(
                            fname,
                            f"🎫 لینک گپ: {chat.invite_link}\n👁 اسم گپ: {chat.title}\n👥 تعداد اعضا: {members.get('result', 'غیر قابل دریافت')}"
                        )
                        os.unlink(fname)
                    else:await message.asyncReply(f"🎫 لینک گپ: {chat.invite_link}\n👁 اسم گپ: {chat.title}\n👥 تعداد اعضا: {members.get('result', 'غیر قابل دریافت')}", close_markup)
            
            elif message.text in ( "پین", "سنجاق" ):
                if message.from_reply_message.result != {}:
                    try:
                        await bot.pinMessage(
                            message.chat.id,
                            message.from_reply_message.message_id
                        )
                    except Exception as ErrorPin:
                        await message.asyncReply(f"خطا حین پین {ErrorPin}", close_markup)
                else: await message.asyncReply("روی پیامی ریپلای زده نشده است")

            elif message.text in ( "برداشتن پین", "برداشتن سنجاق" ):
                if message.from_reply_message.result != {}:
                    try:
                        await bot.unpinMessage(
                            message.chat.id,
                            message.from_reply_message.message_id
                        )
                    except Exception as ErrorUnpin:
                        await message.asyncReply(f"خطا حین برداشتن پین {ErrorUnpin}", close_markup)
                else:
                    yn_markup = InlineKeyboardMarkup()
                    yn_markup.addKeyboard(
                        InlineKeyboardButton("بله", callback_data=f"unpinAll_{message.from_user.id}"),
                        InlineKeyboardButton("خیر", callback_data="close")
                    )
                    await message.asyncReply("آیا مایل به برداشتن تمام سنجاق ها هستید؟", yn_markup)
            
            elif message.text in ("بن", "ریم", "سیک"):
                if message.from_reply_message.result != {}:
                    if not message.from_reply_message.from_user.id in admins:
                        try:
                            await bot.banChatMember(
                                message.chat.id,
                                message.from_reply_message.from_user.id
                            )
                        except Exception as ErrorBan:
                            await message.asyncReply(f"خطا حین ریمو کردن کاربر {ErrorBan}", close_markup)
                    else: await message.asyncReply(f"کاربر جز ادمین های بات میباشد")
                else: await message.asyncReply("روی پیامی ریپلای زده نشده است")

            elif message.text in ( "ان بن", "آن بن" ):
                if message.from_reply_message.result != {}:
                    if not message.from_reply_message.text.isdigit():
                        try:
                            await bot.unbanChatmember(
                                message.chat.id,
                                message.from_reply_message.from_user.id
                            )
                        except Exception as ErrorBan:
                            await message.asyncReply(f"خطا حین ان بن کردن کاربر {ErrorBan}", close_markup)
                    else:
                        try:
                            await bot.unbanChatmember(
                                message.chat.id,
                                int(message.from_reply_message.text)
                            )
                        except Exception as ErrorBan:
                            await message.asyncReply(f"خطا حین ان بن کردن کاربر {ErrorBan}", close_markup)
                else: await message.asyncReply("روی پیامی ریپلای زده نشده است")

            elif message.text == "ترفیع":
                if message.from_reply_message.result != {}:
                    if not message.from_reply_message.from_user.id in admins:
                        admins.append(message.from_reply_message.from_user.id)
                        await message.asyncReply(f"کاربر با آیدی عددی {message.from_reply_message.from_user.id} به ادمین های ربات پیوست", close_markup)
                    else: await message.asyncReply("کاربر در حال حاضر ادمین است")
                else: await message.asyncReply("روی پیامی ریپلای زده نشده است")

            elif message.text == "ترفیع حذف ترفیع":
                if message.from_reply_message.result != {}:
                    if message.from_reply_message.from_user.id in admins:
                        admins.remove(message.from_reply_message.from_user.id)
                        await message.asyncReply(f"کاربر با آیدی عددی {message.from_reply_message.from_user.id} از ادمین های ربات برداشته شد", close_markup)
                    else: await message.asyncReply("کاربر در حال حاضر ادمین نمیباشد")
                else: await message.asyncReply("روی پیامی ریپلای زده نشده است")

@bot.on("callback_query")
async def onQuery(message: Message):
    if message.callback_query.data == "seeHelp":
        await bot.editMessageText(
            message.callback_query.clicked_from_chat,
            "/start - استارت ربات\nلینک - ارسال اطلاعات گپ\nتایم یا تاریخ یا ساعت یا time - ارسال تاریخ\nحذف - اگه روی پیامی ریپلای بشه اون رو حذف میکنه, اگه عددی جلوش نوشته بشه به همون مقدار پیام هارو پاک میکنه\nسنجاق یا پین - روی یه پیام ریپلای بزنید تا سنجاق شود\nبرداشتن سنجاق یا برداشتن پین - درصورت ریپلای زدن اون پیام رو از حالت سنجاق خارج میکنه,در غیر این صورت question box نمایش داده خواهد شد\nبن یا ر یم یا سیک - حذف کردن کاربر از گپ در صورت ریپلای روی پیامی که حاوی آیدی عددی کاربر هم باشد قبول است\nحذف بن - حذف بن کاربر\nپروفایل - نمایش اطلاعات کاربر\nترفیع - اضافه کردن کاربر به ادمین های ربات\nحذف ترفیع - برداشتن کاربر از لیست مدیران",
            message.callback_query.clicked_message.message_id,
            close_markup
        )

    elif message.callback_query.data == "close":
        await bot.deleteMessage(
            message.callback_query.clicked_from_chat,
            message.callback_query.clicked_message.message_id
        )

    elif message.callback_query.data.startswith("unpinAll"):
        ch_id = int(message.callback_query.data.split("_")[-1])
        if message.callback_query.from_user.id == ch_id:
            try:
                await bot.unpinAllMessage(message.callback_query.clicked_from_chat)
            except Exception as ErrorUnpin:
                await bot.sendMessage(message.callback_query.clicked_from_chat, f"خطا حین برداشتن پین {ErrorUnpin}", reply_markup=close_markup)

if __name__ == "__main__":
    asyncio.run(bot.run())