from bot.main import bot


async def download_file(file, file_path):
    await bot.download(file, destination=file_path, timeout=30)
