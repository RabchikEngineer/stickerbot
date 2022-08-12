import discord, os, random, datetime
from PIL import Image



files = {}
client = discord.Client()
delete_nicks=['Кеплер-452b']
delete_messages=False
delete_chance=0

if not os.path.exists('stickers'):
    os.mkdir('stickers')
if not os.path.exists('memes'):
    os.mkdir('memes')



def names_to_filename(name_list):
    st = ''
    for i in name_list:
        st += f'{i}$'
    return st

def filename_to_str(filename):
    name_list=filename[filename.find('#')+1:filename.find('.')].split('$')
    st=''
    for i in name_list:
        st+=f'{i}\n'
    return st

def messages_to_str(msg_list):
    str=''
    for i in msg_list:
        str+=(i+'\n')
    return str



def refresh_stickerlist():
    global files
    filenames=os.listdir('stickers')
    for filename in filenames:
        for name in filename[filename.find('#')+1:filename.find('.')].split('$'):
            files.update({name:filename})
    # print(files)

async def stickerlist(channel):
    filenames = os.listdir('stickers')
    for filename in filenames:
        await channel.send(f'ID = {filename[:filename.find("#")]}\nНазвания:\n{filename_to_str(filename)[:-1]}',file=discord.File('stickers/'+filename))


async def create_sticker(msg,args):
    if msg.attachments == []:
        await msg.channel.send(':x:Вы не прикрепили изображение:x:')

    def find_free_id():
        filenames = os.listdir('stickers')
        id_list=[]
        for filename in filenames:
            id_list.append(int(filename[:filename.find("#")]))
        max_id=max(*id_list)
        for id in range(max_id):
            if not id in id_list:
                return id
        return max_id+1

    await msg.attachments[0].save('temp.png')
    img=Image.open('temp.png')
    x,y = img.size
    img.resize((160,int(160*y/x)),Image.LANCZOS).save(f'stickers/{find_free_id()}#{names_to_filename(args)[:-1]}.png')
    await msg.channel.send(':white_check_mark:Стикер успешно добавлен:white_check_mark:')
    refresh_stickerlist()

async def delete_sticker(msg,args):
    try:
        id=int(args[0])
        filenames = os.listdir('stickers')
        for filename in filenames:
            if filename[:filename.find("#")] == str(id):
                os.remove(f'stickers/{filename}')
    except:
        name=args[0]
        os.remove(f'stickers/{files.get(name)}')

    refresh_stickerlist()
    await msg.channel.send(':white_check_mark:Стикер успешно удалён:white_check_mark:')


async def update_sticker(msg,args):
    print(args)
    id = int(args[0])
    filenames = os.listdir('stickers')
    for filename in filenames:
        if filename[:filename.find("#")] == str(id):
            os.rename(f'stickers/{filename}',f'stickers/{filename[:filename.find("#")+1]+names_to_filename(args[1:])}.png')

    refresh_stickerlist()
    await msg.channel.send(':white_check_mark:Стикер успешно обновлён:white_check_mark:')


async def send_memes(msg):
    await msg.delete()
    filenames = os.listdir('memes')
    for filename in filenames:
        if (os.path.getsize('memes/'+filename)/1024/1024)<8:
            await msg.channel.send(file=discord.File('memes/'+filename))
            os.remove('memes/'+filename)


async def sticker_info(msg,args):
    filenm=''
    try:
        id=int(args[0])
        filenames = os.listdir('stickers')
        for filename in filenames:
            if filename[:filename.find("#")] == str(id):
                filenm=filename
    except:
        name=args[0]
        filenm=files[name]
    if filenm != '':
        await msg.channel.send(f'ID = {filenm[:filenm.find("#")]}\nНазвания:\n{filename_to_str(filenm)[:-1]}',file=discord.File('stickers/' + filenm))
    else:
        await msg.channel.send(':x:ERROR:x:')

async def delete_messages(message):
    global delete_messages
    global delete_chance
    args = message.content.lower().split(' ')[1:]
    # print(args)
    ans = ":x:ERROR:x:"
    if args[0] == 'status':
        if len(args) == 1:
            ans = delete_messages
        elif args[1] == 'set':
            if args[2] == 'true' or args[2] == 'enabled':
                delete_messages = True
                ans = 'Теперь сообщения будут удаляться'
            elif args[2] == 'false' or args[2] == 'disabled':
                delete_messages = False
                ans = 'Теперь сообщения не будут удаляться'
    elif args[0] == 'peoples' or args[0] == 'members':
        if args[1] == 'list':
            ans = delete_nicks
        elif args[1] == 'add':
            nick = message.content.split(' ')[3]
            delete_nicks.append(nick)
            ans = f':white_check_mark:{nick} успешно добавлен в список пидоров:white_check_mark:'
        elif args[1] == 'remove' or args[1] == 'delete':
            nick = message.content.split(' ')[3]
            # print(nick)
            delete_nicks.remove(nick)
            ans = f':white_check_mark:{nick} успешно удалён из списка пидоров:white_check_mark:'
    elif args[0] == 'chance':
        if args[1] == 'get':
            ans = f'Шанс {delete_chance * 100}%'
        elif args[1] == 'set':
            delete_chance = float(args[2]) / 100
            ans = f":white_check_mark:Шанс теперь {delete_chance * 100}%:white_check_mark:"
    await message.channel.send(ans)

async def deleted_list(message):
    args = message.content.lower().split(' ')[1:]
    # print(args)
    if len(args) != 0:
        with open('deleted_messages.txt', 'r') as f:
            await message.channel.send(messages_to_str([x for x in f.read().split('\n') if x!=''][-int(args[0]):]))
    else:
        with open('deleted_messages.txt', 'r') as f:
            await message.channel.send(messages_to_str(f.read().split('\n')))
    await message.delete()


refresh_stickerlist()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # global delete_messages
    global delete_nicks
    # global delete_chance

    # print(message.author.name)
    # print(message.author.nick)
    if (message.author == client.user) or (message.content=='') or (not message.content):
        return
    channel=message.channel

    # print(message.content)
    # if message.reference:
    #     msg1= await message.channel.fetch_message(message.reference.message_id)
    #     # print(msg1)

    # print(message.content)
    # print(message.content[message.content.find(' ') + 1:].lower())
    # print(message.content.lower().startswith('с'))
    if delete_messages and message.author.name in delete_nicks:
        if random.random() < delete_chance:
            with open('deleted_messages.txt', 'a') as f:
                f.write(f'{datetime.datetime.now()} {client.get_channel(message.channel.id)} {message.author.name} {message.clean_content}\n')
            await message.delete()

    if message.content.startswith('say'):
        await message.channel.send('Hello!')

    elif (message.content.lower().startswith('стикер') or message.content.lower().startswith('с')) and message.content[message.content.find(' ')+1:].lower() in files:
        # await message.channel.send(files[message.content[7:]])


        if message.author.nick==None:
            nick=message.author.name
        else:
            nick=message.author.nick
        if message.reference:
            await message.delete()
            msg1= await message.channel.fetch_message(message.reference.message_id)

            await msg1.reply(nick,file=discord.File('stickers/'+files[message.content[message.content.find(' ')+1:].lower()]))
        else:
            await message.delete()
            await message.channel.send(nick,file=discord.File('stickers/'+files[message.content[message.content.find(' ')+1:].lower()]))
    elif message.content.lower()[0]=='$':
        command=message.content.lower()[1:].split(' ')[0]
        args=message.content.lower()[1:].replace(command+" ", '').replace(', ', ',').split(',')
        # print(args)
        if command=='refresh_names':
            refresh_stickerlist()
        elif command=='stickerlist':
            await stickerlist(channel)
        elif command=='stickerinfo':
            await sticker_info(message,args)
        elif command=='add_sticker' or command=='create_sticker':
            await create_sticker(message,args)
        elif command=='remove_sticker' or command=='remove_sticker':
            await delete_sticker(message,args)
        elif command=='update_sticker':
            await update_sticker(message,args)
        elif command=='send_memes':
            await send_memes(message)
        elif command=='delete_messages' and message.author.name=="И̴̕̕Н̸̓͘Ж̴̓̚и̵́̽н̸̓͝И̴̕͠Р̵͛̒":
            await delete_messages(message)
        elif command == "deleted_list":
            await deleted_list(message)




# print(os.environ.get('DISCORD_TOKEN'))
client.run(os.environ.get('DISCORD_TOKEN'))
