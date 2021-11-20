from forwardscoverbot import utils
from forwardscoverbot import dbwrapper
from forwardscoverbot import keyboards
from forwardscoverbot import messages

from telegram import MessageEntity
from telegram import ParseMode
from telegram import constants as t_consts
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext.dispatcher import run_async

import html


def help_command(update, context):
    keyboard = keyboards.github_link_kb()
    text = (
        "<b>Apakah Anda ingin mengirim pesan kepada seseorang atau di grup, tetapi Anda ingin menghindari\n"
        "bahwa seseorang bisa menyebarkan namamu? Gunakan Bot ini untuk meneruskan\n"
        "pesan kamu</b>.\n\nKirimkan di sini apa yang Anda inginkan dan Anda akan mendapatkan pesan yang sama\n"
        "kembali, untuk meneruskan pesan ke tempat yang Anda inginkan dan label penerusan akan digantikan\n"
        "Nama dari bot.\n\n<i>Ini juga berfungsi jika Anda mengirim pesan atau meneruskan pesan.\n"
        "Itu juga mempertahankan gaya pemformatan teks yang sama.</i>\n\n"
        "<b>Perintah yang didukung:</b>\n"
        "/disablewebpagepreview\n"
        "/removecaption\n"
        "/addcaption\n"
        "/removebuttons\n"
        "/addbuttons"
    )
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)



def disable_web_page_preview(update, context):
    if not update.message.reply_to_message:
        text = ("Perintah ini memungkinkan untuk menghapus pratinjau halaman web dari pesan dengan tautan.\n\nGunakan membalas pesan yang sudah digemakan bot dan Anda ingin menonaktifkan pratinjau dengan perintah ini.")
        update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.text:
        text = "Pesan ini tidak memiliki pratinjau halaman web"
        update.message.reply_to_message.reply_text(text=text, quote=True)
        return

    entities_list = [MessageEntity.URL, MessageEntity.TEXT_LINK]
    entities = update.message.reply_to_message.parse_entities(entities_list)
    if len(entities) == 0:
        text = "Pesan ini tidak memiliki pratinjau halaman web"
        update.message.reply_to_message.reply_text(text=text, quote=True)
        return

    messages.process_message(update=update, context=context, message=update.message.reply_to_message, disable_web_page_preview=True)



def remove_caption(update, context):
    if not update.message.reply_to_message:
        text = (
            "Perintah ini mengizinkan untuk menghapus caption dari sebuah pesan. Balas dengan perintah ini ke pijatan di mana Anda ingin menghapus caption. Pastikan pesan tersebut memiliki caption."
        )
        update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.caption:
        text = "Pesan ini tidak memiliki caption, jadi apa yang harus saya hapus? Gunakan perintah ini untuk pesan yang memiliki caption."
        context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id,
            quote=True
        )
        return

    messages.process_message(update=update, context=context, message=update.message.reply_to_message, remove_caption=True)



def remove_buttons(update, context):
    if not update.message.reply_to_message:
        text = (
             "Perintah ini memungkinkan untuk menghapus tombol dari pesan. Balas dengan perintah ini ke pijatan di mana Anda ingin menghapus tombol. Pastikan pesan memiliki tombol."
        )
        update.message.reply_text(text=text)
        return

    if not update.message.reply_to_message.reply_markup:
        text = "Pesan ini tidak memiliki tombol, jadi apa yang harus saya hapus? Gunakan perintah ini untuk pesan yang memiliki tombol."
        context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id,
            quote=True
        )
        return

    messages.process_message(update=update, context=context, message=update.message.reply_to_message, remove_buttons=True)    



def add_caption(update, context):
    if not update.message.reply_to_message:
        text = (
            "<b>Perintah ini mengizinkan untuk menambahkan caption ke pesan. Balas dengan perintah ini dan caption setelah pijatan di mana Anda ingin menambahkan caption.</b>\n\n<i>Jika pesan sudah memiliki caption, perintah ini akan menimpa caption saat ini dengan yang baru.\njika pesan tidak mendukung caption, tidak akan ditambahkan, tidak ada kesalahan yang dikembalikan</i>\n\n\n"
            "<i>Catatan: jika pesan tersebut tidak sesuai dengan keinginan Anda, Anda dapat mengeditnya untuk menambahkan caption. Perintah ini ditujukan jika misalnya Anda meneruskan dari saluran file besar yang tidak ingin Anda unduh dan unggah lagi.</i>"
        )
        update.message.reply_text(text=text, parse_mode='HTML')
        return

    caption = " ".join(update.message.text.split(" ")[1:])
    caption_html = " ".join(update.message.text_html.split(" ")[1:])

    if len(caption) > t_consts.MAX_CAPTION_LENGTH:
        text = "Caption ini terlalu panjang. maksimum yang diizinkan: {} karakter. Harap coba lagi menghapus karakter {}.".format(
            t_consts.MAX_CAPTION_LENGTH,
            len(caption) - t_consts.MAX_CAPTION_LENGTH
        )
        context.bot.sendMessage(
            chat_id=update.message.from_user.id,
            text=text,
            reply_to_message_id=update.message.reply_to_message.message_id,
            quote=True
        )
        return

    messages.process_message(update=update, context=context, message=update.message.reply_to_message, custom_caption=caption_html)



def add_buttons(update, context):
    usage = (
        "<b>Dengan menggunakan perintah ini, Anda dapat menambahkan tombol ke pesan.</b>\nBalas dengan perintah ini ke pesan yang ingin Anda tambahkan tombolnya. Contoh:\n\n"
        "<code>/addbuttons first link=https://telegram.org && second link same row=https://google.it &&& third link new row=https://t.me</code>"
        "\n\nJadi format tombol adalah [teks]=[tautan]. Tombol pada baris yang sama dipisahkan oleh && dan pada baris baru dipisahkan oleh &&&."
        )
    if not update.message.reply_to_message or len(context.args) < 1:
        update.message.reply_text(text=usage, parse_mode='HTML')
        return
    
    param = ' '.join(context.args)
    rows = param.split('&&&')
    lst = []
    for row in rows:
        try:
            row_lst = []
            row_buttons = row.split('&&')
            for button in row_buttons:
                text, link = button.split('=')
                text = text.strip()
                link = link.strip()
                button = InlineKeyboardButton(text=text, url=link)
                
                row_lst.append(button)
            lst.append(row_lst)
        except Exception as e:
            error = 'KESALAHAN format tombol'
            update.message.reply_text(text=error, parse_mode='HTML')
    keyboard = InlineKeyboardMarkup(lst)
    messages.process_message(update=update, context=context, message=update.message.reply_to_message, custom_reply_markup=keyboard)
    

@utils.only_admin
def stats(update, context):
    update.message.reply_text(text=dbwrapper.stats_text(), parse_mode=ParseMode.HTML)



