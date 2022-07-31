import discord
from discord.ext import commands

config = {
    'token': 'OTQwMjk1MzI0MDk2OTQ2MjM3.G-4cX_.Lsl4QeQtv0LQjS4ntueZKxGeDM3Ec5Cwna4SyY',
    'prefix': '/',
}

files = {'ну и ну': 'забрать одна кошка жена'}


bot = commands.Bot(command_prefix=config['prefix'])

@bot.event
async def on_ready():
    print('ready')
    # await ctx.send(ctx.content)




# @bot.command()
# async def sticker(event,*args):
#     print('2')
#     print(type(event))
#     print(dir(event))
#     print()
#     print(event)
#     print()
#     # print(event.context)
#     print()
#     print(args)
#     if event.author!=bot.user:
#         # print(event.content[7:])
#         if event.content[:6]=='стикер' and event.content[7:] in files:
#             await event.send('11')

@bot.command()
async def snd(event,*args):
    await event.send(args[0])

@bot.command()
async def test(event,*args):
    print(args)
    await event.send(args[0])\

@bot.command()
async def adas(event,*args):
    print(args)
    await event.send(args[0])


@bot.event
async def hello(ctx):
    print(111111)
    await ctx.send("Hi")

# @bot.event
# async def on_message(ctx):
#     # print('1')
#     # print(type(ctx))
#     ctx.send('11')
#     # if ctx.author != bot.user:
#     #     await ctx.reply('d')
#     # await ctx.send(ctx.content)


# @bot.command() # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
# async def hello(event): # Создаём функцию и передаём аргумент event.
#     author = event.message.author # Объявляем переменную author и записываем туда информацию об авторе.
#
#     await event.send(f'Hello, {author.mention}!') # Выводим сооб




bot.run(config['token'])