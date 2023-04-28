from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from Translator.aiogram.types import InlineKeyboardMarkup

token = '5836472658:AAExNQCogcOS5-DF0caNseHqAzLlbkl6SNc'

bot = Bot(token=token)
dp = Dispatcher(bot)





@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    await message.answer("Welcome To My Bot")
    await message.answer("The Bot Download Video or Audio from Youtube")


@dp.message_handler(Text(startswith='http'))
async def youtube(message: types.Message):
    link = message.text
    url = YouTube(link)
    from io import BytesIO
    buffer = BytesIO()
    inline = [
        [(f'{url.fmt_streams[0].resolution}', '1'), (f'{url.fmt_streams[1].resolution}', '2'),
         (f'{url.fmt_streams[2].resolution}', '3')],
        [('mp3', '4')]
    ]
    ikm = InlineKeyboardMarkup()
    for button in inline:
        ikm.add(*[InlineKeyboardButton(data, callback_data=callback_data) for data, callback_data in button])
    if url.check_availability() is None:
        await message.answer_photo(url.thumbnail_url,
            caption=f"📹 {url.title}\n"
                    f"💥     {url.fmt_streams[0].resolution} :         {url.fmt_streams[0].filesize_mb} mb\n" 
                    f"💥     {url.fmt_streams[1].resolution} :        {url.fmt_streams[1].filesize_mb} mb\n"
                    f"💥     {url.fmt_streams[2].resolution} :         {url.fmt_streams[2].filesize_mb} mb\n"
                    f"💥     mp3 :         {url.streams.get_audio_only().filesize_mb} mb",reply_markup=ikm)

    else:
        await message.answer("Xatolik")
    @dp.callback_query_handler()
    async def main(message : types.CallbackQuery):
        if message.data == '4':
            stream = url.streams.get_audio_only()
            stream.stream_to_buffer(buffer=buffer)
            buffer.seek(0)
            await bot.send_audio(chat_id=message.from_user.id,audio=buffer)
        if message.data == '1':
            video = url.fmt_streams[0]
            video.stream_to_buffer(buffer=buffer)
            buffer.seek(0)
        if message.data == '2':
            video = url.fmt_streams[1]
            video.stream_to_buffer(buffer=buffer)
            buffer.seek(0)

        if message.data == '3':
            video = url.fmt_streams[2]
            video.stream_to_buffer(buffer=buffer)
            buffer.seek(0)
        await bot.send_video(chat_id=message.from_user.id,video=buffer)

executor.start_polling(dp, skip_updates=True)

# from pytube import YouTube
#
# url = YouTube('https://www.youtube.com/shorts/3hAD0wObviI')
# stream = url.streams.get_highest_resolution()
# filename = stream.download()
