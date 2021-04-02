import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
client.remove_command('help')

hello_world = ['привет', 'hi', 'Hi', 'Hello', 'hello', 'qq', 'q', 'ky', 'Привет', 'здравствуйте',
               'Здравствуйте', 'Ку', 'здорова', 'Хеллоу', "хеллоу"]
antword = ['информация', 'команды', 'help',
           'Help', 'info', 'Info', 'что делать']

@client.event
async def on_ready():
    print('Connected')
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('Yandex.Lyceum | .help'))


@client.command(pass_context=True)
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(
        f'{author.mention}, приветствую, но не на немецком! | {author.mention}, привет! как дела?')

# auto role
@client.event
async def on_member_join(member):
    channel = client.get_channel(689176999578697755)
    role = discord.utils.get(member.guild.roles, id=689430828089868292)

    await member.add_roles(role)
    await channel.send(
        embed=discord.Embed(discription=f'Пользователь ''{member.name}'' присоединился к серверу!',
                            color=0x0c0c0c))

# ban
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Ban', color=discord.Color.red())

    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)

    emb.set_author(name=member.name)
    emb.add_field(name='Ban user',
                  value='Banned user: {}'.format(member.mention))
    emb.set_footer(
        text='Был забанен администратором{}'.format(ctx.author.name))

    await ctx.send(embed=emb)

# kick
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Kick', color=discord.Color.red())

    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)

    emb.set_author(name=member.name)
    emb.add_field(name='Kick user',
                  value='Kicked user: {}'.format(member.mention))
    emb.set_footer(text='Был кикнут администратором{}'.format(ctx.author.name))

    await ctx.send(embed=emb)

# get token
token = open('token.txt', 'r').readline()

client.run(token)
