import discord,os
from PIL import Image


files = {}
client = discord.Client()

if not os.path.exists('stickers'):
    os.mkdir('stickers')



def names_to_str(name_list):
    st = ''
    for i in name_list:
        st += f'{i}$'
    return st


def refresh_stickerlist():
    filenames=os.listdir('stickers')
    for filename in filenames:
        for name in filename[filename.find('#')+1:filename.find('.')].split('$'):
            files.update({name:filename})
    # print(files)

async def stickerlist(channel):

    def namelist_to_str(filename):
        name_list=filename[filename.find('#')+1:filename.find('.')].split('$')
        st=''
        for i in name_list:
            st+=f'{i}\n'
        return st

    filenames = os.listdir('stickers')
    for filename in filenames:
        await channel.send(f'ID = {filename[:filename.find("#")]}\nНазвания:\n{namelist_to_str(filename)[:-1]}',file=discord.File('stickers/'+filename))


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
    img.resize((160,int(160*y/x)),Image.LANCZOS).save(f'stickers/{find_free_id()}#{names_to_str(args)[:-1]}.png')
    await msg.channel.send(':white_check_mark:Стикер успешно добавлен:white_check_mark:')
    refresh_stickerlist()

async def delete_sticker(msg,args):
    try:
        id=int(args[0])
        filenames = os.listdir('stickers')
        for filename in filenames:
            if filename[0] == str(id):
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
        if filename[0] == str(id):
            os.rename(f'stickers/{filename}',f'stickers/{filename[:filename.find("#")+1]+names_to_str(args[1:])}.png')

    refresh_stickerlist()
    await msg.channel.send(':white_check_mark:Стикер успешно обновлён:white_check_mark:')



refresh_stickerlist()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # print(message.content)
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


    if message.content.startswith('say'):
        await message.channel.send('Hello!')

    elif (message.content.lower().startswith('стикер') or message.content.lower().startswith('с')) and message.content[message.content.find(' ')+1:].lower() in files:
        # await message.channel.send(files[message.content[7:]])



        if message.reference:
            await message.delete()
            msg1= await message.channel.fetch_message(message.reference.message_id)

            await msg1.reply(message.author.name,file=discord.File('stickers/'+files[message.content[message.content.find(' ')+1:].lower()]))
        else:
            await message.delete()
            await message.channel.send(message.author.name,file=discord.File('stickers/'+files[message.content[message.content.find(' ')+1:].lower()]))

    elif message.content.lower()[0]=='$':
        command=message.content.lower()[1:].split(' ')[0]
        args=message.content.lower()[1:].replace(command+" ", '').replace(', ', ',').split(',')
        # print(args)
        if command=='refresh_names':
            refresh_stickerlist()
        elif command=='stickerlist':
            await stickerlist(channel)
        elif command=='add_sticker':
            refresh_stickerlist()
            await create_sticker(message,args)
        elif command=='remove_sticker':
            await delete_sticker(message,args)
        elif command=='update_sticker':
            await update_sticker(message,args)
            




client.run('OTQwMjk1MzI0MDk2OTQ2MjM3.G-4cX_.Lsl4QeQtv0LQjS4ntueZKxGeDM3Ec5Cwna4SyY')