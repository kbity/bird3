@bot.tree.command(name="ping", description="check latency (png pronounciation)")
async def ping(interaction: discord.Interaction):
    try:
        now = datetime.datetime.now()

        await interaction.response.defer()

        delta = datetime.datetime.now() - now
        number = int(delta.total_seconds() * 1000)

        res = "ping"
        if number < 20:
            res = f"{number}ms, wow, that's some low latency!"
        elif number < 70:
            res = f"{number}ms, that's alright"
        elif number < 200:
            res = f"{number}ms, that's... not good"
        elif number < 500:
            res = f"{number}ms, what the fuck is this"
        elif number < 1000:
            res = f"{number}ms, oh god"
        else:
            res = f"{number}ms, how the fuck did this command even work"

        await interaction.followup.send(res)
    except Exception as e:
        await interaction.channel.send(res)

@bot.tree.command(name="say", description="Hello I am a Bird")
async def say(ctx: discord.Interaction, msg: str, replyid: str = None, replyping: bool = False, attachment: discord.Attachment = None):
    if not ctx.user.id in say_whitelist and not ctx.user.guild_permissions.manage_guild:
        return await ctx.response.send_message("ok BRAINFUMBLER *converts all your code into brainfuck*", ephemeral=True)
    userisnepotist = ctx.user.id in say_whitelist
    await ctx.response.defer(ephemeral=True)
    replyto = None
    file = None
    if attachment:
        data = await attachment.read()
        buffer = io.BytesIO(data)
        file = discord.File(fp=buffer, filename=attachment.filename)
    if replyid:
        try:
            replyto = await ctx.channel.fetch_message(replyid)
        except Exception as e:
            return await ctx.followup.send(f"error {e}")
    msg = msg.replace("\\n", "\n")
    if not userisnepotist:
        msg = msg[:1950]+f"\n-# sent by <@{ctx.user.id}>"
    else:
        msg = msg[:2000]
    if replyto:
        if replyping:
            await replyto.reply(msg, file=file)
        else:
            await replyto.reply(msg, file=file, allowed_mentions=discord.AllowedMentions.none())
    else:
        await ctx.channel.send(msg, file=file, allowed_mentions=discord.AllowedMentions.none())
        await ctx.followup.send(f"sent")

@bot.tree.command(name="avatar", description="gets a user's avatar")
@app_commands.describe(user="Select a user")
async def avatar(interaction: discord.Interaction, user: discord.User = None, server: bool = False):
    if user is None:
        user = interaction.user
    if server:
        s = "server "
        av = user.display_avatar.url.replace(".webp", ".png")
    else:
        s = ""
        av = user.avatar.url.replace(".webp", ".png")

    await interaction.response.send_message(f"{s}avatar of {user}: {av}")

@bot.tree.command(name="ver", description="get bird version")
async def ver(interaction: discord.Interaction):
    # outdated - discord.Color.red()
    # up to date - discord.Color.green()
    # error in version checking - discord.Color.yellow()
    # development version - discord.Color.blue()
    embed = discord.Embed(title=f'bird v{version}', color=discord.Color.blue(), description="-- Development Version --")
    await interaction.response.send_message(embed=embed)