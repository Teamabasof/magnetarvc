# @Bir_Beyfendi tarafından yapılmıştır.


import os
from pytgcalls import GroupCall
import ffmpeg
from config import API_ID, API_HASH, SESSION_NAME, OWNER_ID, SUDO_USERS
from datetime import datetime
from pyrogram import filters, Client, idle

VOICE_CHATS = {}
DEFAULT_DOWNLOAD_DIR = 'downloads/vcbot/'

API_ID = Config.API_ID
API_HASH = Config.API_HASH
SESSION_NAME = Config.SESSION_NAME
OWNER_ID = Config.OWNER_ID
SUDO_USERS = Config.SUDO_USERS

app = Client(SESSION_NAME, API_ID, API_HASH)


self_or_contact_filter = filters.create(
    lambda
    _,
    __,
    message:
    (message.from_user and message.from_user.is_contact) or message.outgoing
)


# start mesajı
@app.on_message(filters.command('start') & self_or_contact_filter)
async def start(client, message):
      if message.from_user.id not in SUDO_USERS or message.from_user.id != OWNER_ID:
        return await message.reply("Üzgünüm ama bu hesabı kullanamazsın. Kendine [buradan](https://github.com/BirBeyfendi/magnetarvc) bir hesap kurabilirsin!")
      else:
        await message.reply("**Selam!** \n**Ben** `Magnetar Müzik Çalar` **Hesabıyım.** \n**Komutlarım Basittir.** \n\n**Komutlarım:** \n**Start, Ping, Baslat, Beklet, Sesekatil, Sestenayril** 🎵 \n\nKendinize bir hesap oluşturmak isterseniz [buraya](https://github.com/BirBeyfendi/magnetarvc) tıklayın. \n**Keyifli Müzik Dinlemeler Dilerim Efendim.**")

# ping kontrolcüsü
@app.on_message(filters.command('ping') & self_or_contact_filter)
async def ping(client, message):
    if message.from_user.id not in SUDO_USERS or message.from_user.id != OWNER_ID:
      return await message.reply("Üzgünüm ama bu hesabı kullanamazsın. Kendine [buradan](https://github.com/BirBeyfendi/magnetarvc) bir hesap kurabilirsin!")
    else:
        start = datetime.now()
        end = datetime.now()
        m_s = (end - start).microseconds / 1000
        await message.reply(f'**Ping:**\n `{m_s} ms`')

# sesleri oynatır ve durdurulan ses akışını devam ettirir
@app.on_message(filters.command('baslat') & self_or_contact_filter)
async def play_track(client, message):
    if message.from_user.id not in SUDO_USERS or message.from_user.id != OWNER_ID:
      return await message.reply("Üzgünüm ama bu hesabı kullanamazsın. Kendine [buradan](https://github.com/BirBeyfendi/magnetarvc) bir hesap kurabilirsin!")
    else:
        if not message.reply_to_message or not message.reply_to_message.audio:
            return
        input_filename = os.path.join(
            client.workdir, DEFAULT_DOWNLOAD_DIR,
            'input.raw',
        )
    audio = message.reply_to_message.audio
    audio_original = await message.reply_to_message.download()
    a = await message.reply('İndiriliyor...')
    ffmpeg.input(audio_original).output(
        input_filename,
        format='s16le',
        acodec='pcm_s16le',
        ac=2, ar='48k',
    ).overwrite_output().run()
    os.remove(audio_original)
    if VOICE_CHATS and message.chat.id in VOICE_CHATS:
        text = f'▶️ Şu an {message.chat.title} grubunda **{audio.title}** müziği `Magnetar Müzik Çalar` tarafından oynatılıyor...'
    else:
        try:
            group_call = GroupCall(client, input_filename)
            await group_call.start(message.chat.id)
        except RuntimeError:
            await message.reply('Sesli Sohbet Aktif Değil')
            return
        VOICE_CHATS[message.chat.id] = group_call
    await a.delete()
    await message.reply(f'▶️ Şu an {message.chat.title} grubunda **{audio.title}** müziği `Magnetar Müzik Çalar` tarafından oynatılıyor...')

# sesli sohbetteki müziği durdurur
@app.on_message(filters.command('beklet') & self_or_contact_filter)
async def stop_playing(_, message):
    if message.from_user.id not in SUDO_USERS or message.from_user.id != OWNER_ID:
      return await message.reply("Üzgünüm ama bu hesabı kullanamazsın. Kendine [buradan](https://github.com/BirBeyfendi/magnetarvc) bir hesap kurabilirsin!")
    else:
        group_call = VOICE_CHATS[message.chat.id]
        group_call.stop_playout()
        os.remove('downloads/vcbot/input.raw')
        await message.reply('Şarkıyı Durdurdum ▶️')

# sesli sohbete katılır
@app.on_message(filters.command('sesekatil') & self_or_contact_filter)
async def join_voice_chat(client, message):
    if message.from_user.id not in SUDO_USERS or message.from_user.id != OWNER_ID:
      return await message.reply("Üzgünüm ama bu hesabı kullanamazsın. Kendine [buradan](https://github.com/BirBeyfendi/magnetarvc) bir hesap kurabilirsin!")
    else:
        input_filename = os.path.join(
        client.workdir, DEFAULT_DOWNLOAD_DIR,
        'input.raw',
    )
    if message.chat.id in VOICE_CHATS:
        await message.reply('Zaten Sesli Sohbetteyim 🌟')
        return
    chat_id = message.chat.id
    try:
        group_call = GroupCall(client, input_filename)
        await group_call.start(chat_id)
    except RuntimeError:
        await message.reply('Hata ⚠️')
        return
    VOICE_CHATS[chat_id] = group_call
    await message.reply('Sesli Sohbete Başarıyla Katıldım ✅')

# sesli sohbetten ayrılır
@app.on_message(filters.command('sestenayril') & self_or_contact_filter)
async def leave_voice_chat(client, message):
    if message.from_user.id not in SUDO_USERS or message.from_user.id != OWNER_ID:
      return await message.reply("Üzgünüm ama bu hesabı kullanamazsın. Kendine [buradan](https://github.com/BirBeyfendi/magnetarvc) bir hesap kurabilirsin!")
    else:
        chat_id = message.chat.id
        group_call = VOICE_CHATS[chat_id]
        await group_call.stop()
        VOICE_CHATS.pop(chat_id, None)
        await message.reply('Sesli sohbetten başarıyla ayrıldım ✅')

app.start()
print('>>> MAGNETAR MÜZİK BAŞLATILDI <<<')
idle()
app.stop()
print('\n>>> MAGNETAR MÜZİK DURDURULDU <<<')
