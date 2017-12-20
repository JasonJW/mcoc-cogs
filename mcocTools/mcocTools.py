import discord
import re
import csv
import random
import os
import datetime
from operator import itemgetter, attrgetter
from .utils import chat_formatting as chat
from .utils.dataIO import dataIO
from cogs.utils import checks
from discord.ext import commands

EMOJIS = {"t5tech":"<:t5tech:344554971582431232>",
            "t5skill":"<:t5skill:344554971427241985>",
            "t5science":"<:t5science:344554972739928076>",
            "t5mystic":"<:t5mystic:344554971603402762>",
            "t5mutant":"<:t5mutant:344554971389362179>",
            "t5cosmic":"<:t5cosmic:344554971594752000>",
            "t5":"<:t5:344555007191810066>",
            "t4tech":"<:t4tech:344554971296956416>",
            "t4skill":"<:t4skill:344554971141767170>",
            "t4science":"<:t4science:344554971234172939>",
            "t4mystic":"<:t4mystic:344554971468922880>",
            "t4mutant":"<:t4mutant:344554971267858443>",
            "t4cosmic":"<:t4cosmic:344554971217264641>",
            "t4":"<:t4:344555006952865803>",
            "t3tech":"<:t3tech:344554971213070357>",
            "t3skill":"<:t3skill:344554972370829313>",
            "t3science":"<:t3science:344554971414659072>",
            "t3mystic":"<:t3mystic:344554971318059008>",
            "t3mutant":"<:t3mutant:344554970940702721>",
            "t3cosmic":"<:t3cosmic:344554971124989952>",
            "t3":"<:t3:344555006822973450>",
            "t2tech":"<:t2tech:344554971074658304>",
            "t2skill":"<:t2skill:344554971095629825>",
            "t2science":"<:t2science:344554970927857667>",
            "t2mystic":"<:t2mystic:344554971192098816>",
            "t2mutant":"<:t2mutant:344554971267858452>",
            "t2cosmic":"<:t2cosmic:344554970785513474>",
            "t2":"<:t2:344555006676041731>",
            "t1tech":"<:t1tech:344554970600964096>",
            "t1skill":"<:t1skill:344554970726531082>",
            "t1science":"<:t1science:344554970227539970>",
            "t1mystic":"<:t1mystic:344554970172882944>",
            "t1mutant":"<:t1mutant:344554969808240652>",
            "t1cosmic":"<:t1cosmic:344554969648726018>",
            "t1":"<:t1:344555006873305108>"}

class MCOCTools:
    '''Tools for Marvel Contest of Champions'''
    lookup_links = {
            'event': (
                '<http://simians.tk/MCOC-Sched>',
                '[Tiny MCoC Schedule](http://simians.tk/MCOC-Sched)',
                'Josh Morris Schedule',
                'https://d2jixqqjqj5d23.cloudfront.net/assets/developer/imgs/icons/google-spreadsheet-icon.png'),
            'rttl':(
                '<https://drive.google.com/file/d/0B4ozoShtX2kFcDV4R3lQb1hnVnc/view>',
                '[Road to the Labyrinth Opponent List](https://drive.google.com/file/d/0B4ozoShtX2kFcDV4R3lQb1hnVnc/view)',
                'by Regal Empire {OG Wolvz}',
                'http://svgur.com/s/48'),
            'hook': (
                '<http://hook.github.io/champions>',
                '[hook/Champions by gabriel](http://hook.github.io/champions)',
                'hook/champions for Collector',
                'https://assets-cdn.github.com/favicon.ico'),
            'spotlight': (
                '<http://simians.tk/MCoCspotlight>',
                '[MCOC Spotlight Dataset](http://simians.tk/MCoCspotlight)\nIf you would like to donate prestige, signatures or stats, join us at \n[MCOC Spotlight on Discord](https://discord.gg/wJqpYGS)'),
            'marvelsynergy': (
                '<http://www.marvelsynergy.com/team-builder>',
                '[Marvel Synergy Team Builder](http://www.marvelsynergy.com/team-builder)',
                'Marvel Synergy',
                'http://www.marvelsynergy.com/images/marvelsynergy.png'),
            'alsciende':(
                '<https://alsciende.github.io/masteries/v10.0.1/#>',
                '[Alsciende Mastery Tool](https://alsciende.github.io/masteries/v10.0.1/#)',
                'by u/alsciende',
                'https://assets-cdn.github.com/favicon.ico'),
            'simulator': (
                '<http://simians.tk/msimSDF>',
                '[-SDF- Mastery Simulator](http://simians.tk/msimSDF)'),
            'streak': (
                '<http://simians.tk/-sdf-streak>'
                '[Infinite Streak](http://simians.tk/-sdf-streak)'),
                #'http://simians.tk/SDFstreak')
    }
    mcolor = discord.Color.red()
    icon_sdf = 'https://raw.githubusercontent.com/JasonJW/mcoc-cogs/master/mcoc/data/sdf_icon.png'
    dataset = 'data/mcoc/masteries.csv'

    def __init__(self, bot):
        self.bot = bot

    def present(self, lookup):
        em=discord.Embed(color=self.mcolor,title='',description=lookup[1])
        print(len(lookup))
        if len(lookup) > 2:
            em.set_footer(text=lookup[2],icon_url=lookup[3])
        else:
            em.set_footer(text='Presented by [-SDF-]',icon_url=self.icon_sdf)
        return em

    @commands.command(pass_context=True,aliases={'collector','infocollector'})
    async def aboutcollector(self,ctx):
        """Shows info about Collector"""
        author_repo = "https://github.com/Twentysix26"
        red_repo = author_repo + "/Red-DiscordBot"
        server_url = "https://discord.gg/wJqpYGS"
        dpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        since = datetime.datetime(2016, 1, 2, 0, 0)
        days_since = (datetime.datetime.utcnow() - since).days
        dpy_version = "[{}]({})".format(discord.__version__, dpy_repo)
        py_version = "[{}.{}.{}]({})".format(*os.sys.version_info[:3],
                                             python_url)

        owner_set = self.bot.settings.owner is not None
        owner = self.bot.settings.owner if owner_set else None
        if owner:
            owner = discord.utils.get(self.bot.get_all_members(), id=owner)
            if not owner:
                try:
                    owner = await self.bot.get_user_info(self.bot.settings.owner)
                except:
                    owner = None
        if not owner:
            owner = "Unknown"

        about = (
            "Collector is an instance of [Red, an open source Discord bot]({}) "
            "created by [Twentysix]({}) and improved by many.\n\n"
            "The Collector Dev Team is backed by a passionate community who contributes and "
            "creates content for everyone to enjoy. [Join us today]({}) "
            "and help us improve!\n\n"
            "".format(red_repo, author_repo, server_url))
        devteam = ( "DeltaSigma#8530\n"
                    "JJW#8071\n"
                    )
        supportteam=('phil_wo#3733\nSpiderSebas#9910\nsuprmatt#2753\ntaoness#5565\n')
        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name="Instance owned by", value=str(owner))
        embed.add_field(name="Python", value=py_version)
        embed.add_field(name="discord.py", value=dpy_version)
        embed.add_field(name="About Collector", value=about, inline=False)
        embed.add_field(name='DuelsPartner',value='superflu0us#4587',inline=True)
        embed.add_field(name='LabyrinthPartner',value='Kiryu#5755',inline=True)
        embed.add_field(name='MapsPartner',value='jpags#5202',inline=True)
        embed.add_field(name="PrestigePartner",value='mutamatt#4704',inline=True)
        embed.add_field(name='CollectorSupportTeam', value=supportteam,inline=True)
        embed.add_field(name="CollectorDevTeam",value=devteam,inline=True)
        embed.set_footer(text="Bringing joy since 02 Jan 2016 (over "
                         "{} days ago!)".format(days_since))

        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

    # @checks.admin_or_permissions(manage_server=True)
    # @commands.command()
    # async def tickets(self):
    #     ticketsjson = 'data/tickets/tickets.json'
    #     tickets = dataIO.load_json(ticketsjson)
    #     em = discord.Embed(title='Tickets')
    #     cnt = 0
    #     ids = tickets.keys()
    #
    #     for ticket in :
    #         em.add_field(name='{} - filed by {}'.format(cnt, ticket['name'],value='{}\n id: {}'.format(ticket['message'],ticket)))
    #     await self.bot.say(embed=em)


    @commands.command(help=lookup_links['event'][0], aliases=['events','schedule',])
    async def event(self):
        x = 'event'
        lookup = self.lookup_links[x]
        await self.bot.say(embed=self.present(lookup))
        await self.bot.say('iOS dumblink:\n{}'.format(lookup[0]))

    @commands.command(help=lookup_links['spotlight'][0],)
    async def spotlight(self):
        x = 'spotlight'
        lookup = self.lookup_links[x]
        await self.bot.say(embed=self.present(lookup))
        await self.bot.say('iOS dumblink:\n{}'.format(lookup[0]))

    @commands.command(help=lookup_links['rttl'][0],)
    async def rttl(self):
        x = 'rttl'
        lookup = self.lookup_links[x]
        await self.bot.say(embed=self.present(lookup))
        await self.bot.say('iOS dumblink:\n{}'.format(lookup[0]))

    @commands.command(help=lookup_links['marvelsynergy'][0])
    async def marvelsynergy(self):
        x = 'marvelsynergy'
        lookup = self.lookup_links[x]
        await self.bot.say(embed=self.present(lookup))
        await self.bot.say('iOS dumblink:\n{}'.format(lookup[0]))

    @commands.command(help=lookup_links['simulator'][0],aliases=['msim'])
    async def simulator(self):
        x = 'simulator'
        lookup = self.lookup_links[x]
        await self.bot.say(embed=self.present(lookup))
        await self.bot.say('iOS dumblink:\n{}'.format(lookup[0]))

    @commands.command(help=lookup_links['alsciende'][0], aliases=('mrig',))
    async def alsciende(self):
        x = 'alsciende'
        lookup = self.lookup_links[x]
        await self.bot.say(embed=self.present(lookup))
        await self.bot.say('iOS dumblink:\n{}'.format(lookup[0]))

    @commands.command(help=lookup_links['streak'][0])
    async def streak(self):
        x='streak'
        lookup = self.lookup_links[x]
        await self.bot.say(embed=self.present(lookup))
        await self.bot.say('iOS dumblink:\n{}'.format(lookup[0]))

    @commands.command(help=lookup_links['hook'][0])
    async def hook(self):
        x = 'hook'
        lookup = self.lookup_links[x]
        await self.bot.say(embed=self.present(lookup))
        await self.bot.say('iOS dumblink:\n{}'.format(lookup[0]))

    @commands.command()
    async def keygen(self, prefix='SDCC17'):
        '''SDCC Code Generator
        No warranty :)'''
        letters='ABCDEFGHIJKLMNOPQURSTUVWXYZ'
        numbers='0123456789'
        package = []
        for i in range(0,9):
            lets='{}{}{}{}{}{}'.format(random.choice(letters),random.choice(letters),random.choice(numbers),random.choice(numbers),random.choice(letters),random.choice(letters))
            package.append(prefix+lets)
        em=discord.Embed(color=discord.Color.gold(),title='Email Code Generator',description='\n'.join(package))
        await self.bot.say(embed=em)

    def _get_text(self, mastery, rank):
        rows = csv_get_rows(self.dataset,'Mastery',mastery)
        for row in rows:
            text.append(row['Text'].format(row[str(rank)]))
        return text

    @checks.admin_or_permissions(manage_server=True, manage_roles=True)
    @commands.command(name='gaps', pass_context=True, hidden=True)
    async def _alliance_popup(self, ctx, *args):
        '''Guild | Alliance Popup System'''
        server = ctx.message.server
        everyone_perms = discord.PermissionOverwrite(target=server.default_role, read_messages = False)
        summoner_perms = discord.PermissionOverwrite(read_messages = True)
        alliance_perms = discord.PermissionOverwrite(read_messages = True)
        alliance_perms.change_nickname = True
        officer_perms = discord.PermissionOverwrite(read_messages = True)
        officer_perms.manage_server = True
        officer_perms.manage_roles = True
        officer_perms.kick_members = True
        officer_perms.ban_members = True
        officer_perms.manage_nicknames = True
        officer_perms.manage_webhooks = True
        officer_perms.view_audit_logs = True
        admin_perms = discord.PermissionOverwrite(administrator = True)

        roles = server.roles
        rolenames = []
        for r in roles:
            rolenames.append('{}'.format(r.name))
        aroles = ['officers', 'bg1', 'bg2', 'bg3', 'alliance', 'summoners']
        # message = await self.bot.say('Stage 1: Creating roles')
        if 'admin' not in rolenames:
            admin = await self.bot.create_role(server=server, name='admin', permissions=admin_perms, color=discord.Color.gold(), hoist=False, mentionable=False)
        if 'officers' not in rolenames:
            officers = await self.bot.create_role(server=server, name='officers', permissions=officer_perms, color=discord.Color.light_grey(), hoist=False, mentionable=True)
        if 'bg1' not in rolenames:
            bg1 = await self.bot.create_role(server=server, name='bg1', color=discord.Color.blue(), hoist=False, mentionable=True)
        if 'bg2' not in rolenames:
            bg2 = await self.bot.create_role(server=server, name='bg2', color=discord.Color.purple(), hoist=False, mentionable=True)
        if 'bg3' not in rolenames:
            bg3 = await self.bot.create_role(server=server, name='bg3', color=discord.Color.orange(), hoist=False, mentionable=True)
        if 'alliance' not in rolenames:
            alliance = await self.bot.create_role(server=server, name='alliance', permissions=alliance_perms, color=discord.Color.teal(), hoist=True, mentionable=True)
        if 'summoners' not in rolenames:
            summoners = await self.bot.create_role(server=server, name='summoners', permissions=summoner_perms, color=discord.Color.lighter_grey(), hoist=True, mentionable=True)

        roles = sorted(server.roles, key=lambda roles:roles.position, reverse=True)
        em = discord.Embed(color=discord.Color.red(), title='Guild Alliance Popup System', description='')
        positions = []
        for r in roles:
            positions.append('{} = {}'.format(r.position, r.mention))
            if r.name == 'officers':
                officers = r
            elif r.name == 'bg1':
                bg1 = r
            elif r.name == 'bg2':
                bg2 = r
            elif r.name == 'bg3':
                bg3 = r
            elif r.name == 'alliance':
                alliance = r
            elif r.name == 'summoners':
                summoners = r
            elif r.name == 'admin':
                admin = r

        em.add_field(name='Stage 1 Role Creation',value='\n'.join(positions),inline=False)
        await self.bot.say(embed=em)


        officerbg_perms = discord.PermissionOverwrite(target=officers, read_messages=True)
        alliancechat_perms = discord.PermissionOverwrite(target=alliance, read_messages=True)
        summonerchat_perms = discord.PermissionOverwrite(target=summoners, read_messages=True)
        bg1_perms = discord.PermissionOverwrite(target=bg1, read_messages=True)
        bg2_perms = discord.PermissionOverwrite(target=bg2, read_messages=True)
        bg3_perms = discord.PermissionOverwrite(target=bg3, read_messages=True)

        channellist = []
        for c in server.channels:
            channellist.append(c.name)
        make_channels = ('announcements', 'alliance-chatter', 'bg1aq', 'bg1aw', 'bg2aq', 'bg2aw', 'bg3aq', 'bg3aw')
        if 'announcements' not in channellist:
            await self.bot.create_channel(server=server, name='announcements', type=discord.ChannelType.text, overwrite=((server.default_role, everyone_perms), (alliance, alliancechat_perms), (officers, officerbg_perms)))
        if 'alliance-chatter' not in channellist:
            await self.bot.create_channel(server=server, name='alliance-chatter', type=discord.ChannelType.text, overwrite=((server.default_role, everyone_perms), (alliance, alliancechat_perms)))
        if 'bg1aq' not in channellist:
            await self.bot.create_channel(server=server, name='bg1aq', type=discord.ChannelType.text, overwrite=((officers, officerbg_perms),(bg1, bg1_perms)))
        if 'bg1aw' not in channellist:
            await self.bot.create_channel(server=server, name='bg1aw', type=discord.ChannelType.text, overwrite=((officers, officerbg_perms),(bg1, bg1_perms)))
        if 'bg2aq' not in channellist:
            await self.bot.create_channel(server=server, name='bg2aq', type=discord.ChannelType.text, overwrite=((officers, officerbg_perms),(bg2, bg2_perms)))
        if 'bg2aw' not in channellist:
            await self.bot.create_channel(server=server, name='bg2aw', type=discord.ChannelType.text, overwrite=((officers, officerbg_perms),(bg2, bg2_perms)))
        if 'bg3aq' not in channellist:
            await self.bot.create_channel(server=server, name='bg3aq', type=discord.ChannelType.text, overwrite=((officers, officerbg_perms),(bg3, bg3_perms)))
        if 'bg3aw' not in channellist:
            await self.bot.create_channel(server=server, name='bg3aw', type=discord.ChannelType.text, overwrite=((officers, officerbg_perms),(bg3, bg3_perms)))

        channels= sorted(server.channels, key=lambda channels:channels.position, reverse=False)
        channelnames=[]
        for c in channels:
            channelnames.append('{} = {} '.format(c.position, c.mention))
        em = discord.Embed(color=discord.Color.red(), title='Guild Alliance Popup System', description='')
        em.add_field(name='Stage 2 Create Channels',value='\n'.join(channelnames),inline=False)
        await self.bot.say(embed=em)


    # @checks.admin_or_permissions(manage_server=True, manage_roles=True)
    # @commands.command(name='setup', pass_context=True)
    # async def collectorsetup(self,ctx,*args):
    #     '''Server Setup Guide
    #     Collector Role Requires admin
    #     '''
        # 1) Check Roles present
        # 2) Check Role Permissions
        # 3) Check Role Order
        # Manage Messages required for Cleanup
        # Manage Server required for Role Creation / Deletion
        # Manage Roles required for Role assignment / removal
        # 2 ) Check roles
        # 3 ) Check role order
        # check1 = await self.setup_phase_one(ctx)
        # if check1:
        #     await self.bot.say(embed=discord.Embed(color=discord.color.red(),
        #                         title='Collector Setup Protocol',
        #                         description='☑ setup_phase_one '))



    # async def setup_phase_one(self, ctx):
    #     '''Check Server ROLES'''
    #     # repeat_phase = await self.setup_phase_one(ctx)
    #     # next_phase = await self.setup_phase_two(ctx)
    #
    #     server = ctx.message.server
    #     roles = server.roles
    #     rolenames = []
    #     phase = True
    #     for r in roles:
    #         rolenames.append(r.name)
    #     required_roles={'Collector','officers','bg1','bg2','bg3','LEGEND','100%LOL','LOL','RTL','ROL','100%Act4','Summoner','TestRole1','TestRole2'}
    #     roles_fields={'officers': {True, discord.Color.lighter_grey(),},
    #                 'bg1':{True, discord.Color.blue(), },
    #                 'bg2':{True, discord.Color.purple(), },
    #                 'bg3':{True, discord.Color.orange(), },
    #                 'TestRole1':{True, discord.Color.default(), },
    #                 'TestRole2':{True, discord.Color.light_grey()},
    #                 }
    #     stageone=['Setup Conditions 1:\nRoles Required for Guild Setup:',]
    #     for i in required_roles:
    #         if i in rolenames:
    #             stageone.append('☑️ {}'.format(i))
    #         else:
    #             stageone.append('❌ {}'.format(i))
    #             phase = False
    #     desc = '\n'.join(stageone)
    #     if phase == False:
    #         em=discord.Embed(color=discord.Color.red(),title='Server Setup Protocol [1]',description=desc)
    #         em.add_field(name='Corrective Action', value='Roles are missing. Create missing roles and Rerun test.\n🔁 == Rerun test\n❌ == Cancel setup')
    #         message = await self.bot.send_message(ctx.message.channel, embed=em)
    #         await self.bot.add_reaction(message,'\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS}')
    #         await self.bot.add_reaction(message,'\N{CROSS MARK}')
    #         await self.bot.add_reaction(message, '\N{BLACK RIGHT-POINTING TRIANGLE}')
    #         react = await self.bot.wait_for_reaction(message=message, user=ctx.message.author, timeout=120, emoji=['\N{CROSS MARK}','\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS}','\N{BLACK RIGHT-POINTING TRIANGLE}'])
    #         if react is None or react.reaction.emoji == '\N{CROSS MARK}':
    #             try:
    #                 await self.bot.delete_message(message)
    #             except:
    #                 pass
    #             return None
    #         elif react.reaction.emoji == '\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS}':
    #             await self.bot.delete_message(message)
    #             return await self.setup_phase_one(ctx)
    #         elif react.reaction.emoji == '\N{BLACK RIGHT-POINTING TRIANGLE}':
    #             await self.bot.delete_message(message)
    #             return await self.setup_phase_two(ctx)
    #     elif phase == True:
    #         await setup_phase_two
    #
    # async def setup_phase_two(self, ctx):
    #     '''Check Role ORDER'''
    #     server = ctx.message.server
    #     roles = sorted(server.roles, key=lambda roles:roles.position, reverse=True)
    #     required_roles = ('Collector','officers','bg1','bg2','bg3','LEGEND','100%LOL','LOL','RTL','ROL','100%Act4','Summoner', 'everyone')
    #     said = []
    #     em = discord.Embed(color=discord.Color.red(), title='Role Order Prerequisite',description='Role: Collector')
    #     positions = []
    #     for r in roles:
    #         positions.append('{} = {}'.format(r.position, r.name))
    #     em.add_field(name='Role Position on Server',value=chat.box('\n'.join(positions)),inline=False)
    #     said.append(await self.bot.say(embed=em))
    #     order = []
    #     c=len(required_roles)-1
    #     for r in required_roles:
    #         order.append('{} = {}'.format(c, r))
    #         c-=1
    #     em = discord.Embed(color=discord.Color.red(), title='',description='')
    #     em.add_field(name='Correct Role Positions', value =chat.box('\n'.join(order)),inline=False)
    #     perm_order = []
    #     phase = True
    #     for i in range(0,len(required_roles)-2):
    #         j = i+1
    #         if required_roles[j] > required_roles[i]:
    #             phase = False
    #             # perm_order.append('{} should be above {}'.format(required_roles[i],required_roles[j]))
    #     if phase == False:
    #         # em=discord.Embed(color=discord.Color.red(),title='Server Setup Protocol [2]',description=desc)
    #         em.add_field(name='Corrective Action', value='Roles are out of order. Adjust role order and Rerun test.')
    #         # em.add_field(name='',value='\n'.join(perm_order))
    #         message = await self.bot.send_message(ctx.message.channel, embed=em)
    #         said.append(message)
    #         await self.bot.add_reaction(message,'\N{BLACK LEFT-POINTING TRIANGLE}')
    #         await self.bot.add_reaction(message,'\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS}')
    #         await self.bot.add_reaction(message,'\N{CROSS MARK}')
    #         await self.bot.add_reaction(message, '\N{BLACK RIGHT-POINTING TRIANGLE}')
    #         react = await self.bot.wait_for_reaction(message=message, user=ctx.message.author, timeout=120, emoji=['\N{CROSS MARK}','\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS}','\N{BLACK RIGHT-POINTING TRIANGLE}'])
    #         if react is None or react.reaction.emoji == '\N{CROSS MARK}':
    #             try:
    #                 for message in said:
    #                     await self.bot.delete_message(message)
    #             except:
    #                 pass
    #             return None
    #         elif react.reaction.emoji == '\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS}':
    #             for message in said:
    #                 await self.bot.delete_message(message)
    #             return await self.setup_phase_two(ctx)
    #         elif react.reaction.emoji == '\N{BLACK RIGHT-POINTING TRIANGLE}':
    #             for message in said:
    #                 await self.bot.delete_message(message)
    #             return await self.setup_phase_three(ctx)
    #         elif react.reaction.emoji == '\N{BLACK LEFT-POINTING TRIANGLE}':
    #             for message in said:
    #                 await self.bot.delete_message(message)
    #             return await self.setup_phase_one(ctx)
    #     elif phase == True:
    #         await setup_phase_three
    #
    # async def setup_phase_three(self, ctx):
    #     '''Check Role Permissions'''
    #     message = await self.bot.say('initiate phase three')


def load_csv(filename):
    return csv.DictReader(open(filename))

def get_csv_row(filecsv, column, match_val, default=None):
    print(match_val)
    csvfile = load_csv(filecsv)
    for row in csvfile:
        if row[column] == match_val:
            if default is not None:
                for k, v in row.items():
                    if v == '':
                        row[k] = default
            return row

def get_csv_rows(filecsv, column, match_val, default=None):
    print(match_val)
    csvfile = load_csv(filecsv)
    package =[]
    for row in csvfile:
        if row[column] == match_val:
            if default is not None:
                for k, v in row.items():
                    if v == '':
                        row[k] = default
            package.append(row)
    return package

def tabulate(table_data, width, rotate=True, header_sep=True):
    rows = []
    cells_in_row = None
    for i in iter_rows(table_data, rotate):
        if cells_in_row is None:
            cells_in_row = len(i)
        elif cells_in_row != len(i):
            raise IndexError("Array is not uniform")
        rows.append('|'.join(['{:^{width}}']*len(i)).format(*i, width=width))
    if header_sep:
        rows.insert(1, '|'.join(['-' * width] * cells_in_row))
    return chat.box('\n'.join(rows))



def setup(bot):
    bot.add_cog(MCOCTools(bot))
