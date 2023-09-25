import discord, os, random, datetime, json, csv
from PIL import Image
from moviepy.editor import VideoFileClip as Video
from subprocess import Popen,PIPE


files = {}
client_intents = discord.Intents.default()
client_intents.message_content = True
client = discord.Client(intents=client_intents)


with open('config.json', encoding='utf-8') as f:
    config=json.load(f)
commands=config["commands"]
directories=config["directories"]
prefix=config["prefix"]
debug=config["debug"]

developing_alert="Пока что в разработке\nИди нахуй :D"

for directory in config['directories'].values():
    # print(directory)
    if not os.path.exists(directory):
        os.mkdir(directory)


def nice_output(func):
    def wrapper(*args,**kwargs):
        print('\n'+'-'*30)
        res=func(*args,**kwargs)
        print('-' * 30 + '\n')
        return res
    return wrapper


def sticker_names_to_filename(name_list):
    return "$".join(name_list)


def sticker_filename_to_names(filename):
    print(filename)
    return filename[filename.find('#')+1:filename.rfind('.')].split('$')


def filename_to_str(filename):
    name_list=sticker_filename_to_names(filename)
    return "\n".join(name_list)


@nice_output
def refresh_stickerlist():
    global files
    files={}
    filenames=os.listdir('stickers')
    for filename in filenames:
        files.update({filename.split('#')[0]:filename})
        for name in sticker_filename_to_names(filename):
            files.update({name:filename})
    # print(files)
    if debug:
        for k,v in sorted(files.items(),key=lambda x: int(x[1].split('#')[0])):
            print(f'{k:25} --- {v}')


async def stickerlist(msg):
    await msg.channel.send(developing_alert)

    # filenames = os.listdir('stickers')
    # for filename in filenames:
    #     await msg.channel.send(f'ID = {filename[:filename.find("#")]}\nНазвания:\n{filename_to_str(filename)[:-1]}',
    #                            file=discord.File('stickers/'+filename))


async def create_sticker(msg,args):
    if msg.attachments == []:
        await msg.channel.send(':x:Вы не прикрепили изображение:x:')
        return

    # print(msg.attachments)
    # print(msg.attachments[0])
    # print(dir(msg.attachments[0]))
    # print(msg.attachments[0].content_type)

    def find_free_id():
        filenames = os.listdir(directories["stickers_dir"])
        id_set=set()
        for filename in filenames:
            id_set.update({int(filename.split('#')[0])})

        return min(set(range(len(id_set)+2)).difference(id_set))

    content_type=msg.attachments[0].content_type.split('/')
    filename=directories['temp_directory']+'temp.'+content_type[1]
    await msg.attachments[0].save(filename)
    if content_type[0]=="image":
        img=Image.open(filename)
        x,y = img.size
        img.resize((160,int(160*y/x)),Image.LANCZOS)\
            .save(f'{directories["stickers_dir"]}{find_free_id()}#{sticker_names_to_filename(args)}.png')
        await msg.channel.send(':white_check_mark:Стикер успешно добавлен:white_check_mark:')
    elif content_type[0]=="video":
        await msg.channel.send(developing_alert)
        # video=Video(filename)
        # video.resize(width=160)
        # video.write_videofile(f'{directories["stickers_dir"]}{find_free_id()}#{sticker_names_to_filename(args)}.gif')
    else:
        await msg.channel.send(':x:Неизвестный формат файла:x:')
    refresh_stickerlist()


async def delete_sticker(msg,args):
    filename=files.get(args[0])
    os.remove(directories["stickers_dir"]+filename)
    refresh_stickerlist()
    await msg.channel.send(':white_check_mark:Стикер успешно удалён:white_check_mark:')


async def update_sticker(msg,args):
    filename = files.get(args[0])
    names = set(sticker_filename_to_names(filename))

    if args[1]=="+":
        names|=set(args[2:])

    elif args[1]=="-":
        names-=set(args[2:])

    elif args[1] in ["x", "х"]:
        names=set(args[2:])

    os.rename(directories["stickers_dir"]+filename,
              f'{directories["stickers_dir"]}{filename.split("#")[0]}#{sticker_names_to_filename(names)}.png')

    refresh_stickerlist()
    await msg.channel.send(':white_check_mark:Стикер успешно обновлён:white_check_mark:')


async def send_memes(msg):
    await msg.channel.send(developing_alert)

    # await msg.delete()
    # filenames = os.listdir(directories['memes_dir'])
    # for filename in filenames:
    #     if (os.path.getsize(directories['memes_dir']+filename)/1024/1024)<8:
    #         if filename[:3]=='sss':
    #             filename2 = '1' + filename
    #             os.rename(directories['memes_dir'] + filename, directories['memes_dir'] + filename2)
    #             filename=filename2
    #
    #         await msg.channel.send(file=discord.File(directories['memes_dir']+filename))
    #         os.remove(directories['memes_dir']+filename)


async def sticker_info(msg,args):
    filename=files.get(args[0])
    if filename:
        await msg.channel.send(f'ID = {filename.split("#")[0]}\nНазвания:\n{filename_to_str(filename)}',file=discord.File(directories["stickers_dir"] + filename))
    else:
        await msg.channel.send(':x:ERROR:x:')


async def get_message(message):
    prev_msg=await message.channel.fetch_message(message.reference.message_id)
    prev_msg2=await message.channel.fetch_message(prev_msg.reference.message_id)
    await message.channel.send(prev_msg2.jump_url)
    # await message.delete()


async def create_survey(message, self_activation=True):
    if self_activation:
        await message.clear_reactions()
        await message.add_reaction('✅')
        await message.add_reaction('❌')
    else:
        await message.delete()
        prev_message = await message.channel.fetch_message(message.reference.message_id)
        await prev_message.clear_reactions()
        await prev_message.add_reaction('✅')
        await prev_message.add_reaction('❌')


refresh_stickerlist()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # print(files)

@client.event
async def on_message(message):

    # print(message.author.name)
    # print(message.author.nick)

    message_text=message.content.lower()
    channel = message.channel
    message_body = message_text[message_text.find(' ') + 1:]

    if (message.author == client.user) or (message_text=='') or (not message_text):
        return

    if channel.id==1142192978593579058 and not message.author.bot:
        await create_survey(message, self_activation=True)

    if (message_text.startswith('стикер') or message_text.startswith('с ')) and message_body in files:
        # print(1)

        nick = message.author.nick or message.author.name
        file=discord.File(f'stickers/'+files[message_body])
        if message.reference:
            await message.delete()
            msg1= await message.channel.fetch_message(message.reference.message_id)
            await msg1.reply(nick,file=file)
        else:
            await message.delete()
            await message.channel.send(nick,file=file)

    elif message_text[0]==prefix:
        args_full = list(csv.reader([message_text[1:]],delimiter=' '))[0]
        if debug:
            print(args_full)
        command=args_full[0]
        args=args_full[1:]
        if command in commands['refresh_names']:
            refresh_stickerlist()
        elif command in commands['stickerlist']:
            await stickerlist(message)
        elif command in commands['sticker_info']:
            await sticker_info(message,args)
        elif command in commands['add_sticker']:
            await create_sticker(message,args)
        elif command in commands['delete_sticker']:
            await delete_sticker(message,args)
        elif command in commands['update_sticker']:
            await update_sticker(message,args)
        elif command in commands['send_memes']:
            await send_memes(message)
        elif command in commands['get']:
            await get_message(message)
        elif command in commands['create_survey']:
            await create_survey(message, self_activation=False)




# print(os.environ.get('DISCORD_TOKEN'))
client.run(os.environ.get('DISCORD_TOKEN'))
