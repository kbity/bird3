@bot.tree.command(name="real", description="Real")
async def real(interaction: discord.Interaction):
    await interaction.response.send_message("https://i.imgur.com/4OEHzSz.png")

@bot.tree.command(name="percent", description="The amount of something someone is")
@app_commands.describe(user="Select a user", property="Enter a property, twin")
async def percent(interaction: discord.Interaction, user: discord.User, property: str):
    await interaction.response.send_message(f"<@{user.id}> is {random.randint(0,100)}% {property}, imo", allowed_mentions=discord.AllowedMentions.none())

@bot.tree.command(name="bird", description="bird")
async def real(interaction: discord.Interaction):
    await interaction.response.send_message(emoj["bird"])

@bot.tree.command(name="tinynitro", description="Creates a Fake Nitro Gift that is Really Small")
@app_commands.describe(message="The message to send when the button is clicked")
async def tinynitro(ctx: discord.Interaction, message: str = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
    desk = f"**{ctx.user}** has gifted you Nitro for **0 months**!"
    embed = discord.Embed(title="You've been gifted a subscription!", description=desk)
    embed.set_footer(text="‎"+"  "*(len(desk))+"Expires in 0 hours")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/782434583974248511/793316025244057630/nitroregular.png")

    async def confirm_button_thingy(ctx2: discord.Interaction):
        await ctx2.user.send(message)
        await ctx2.response.edit_message(view=None)

    confirm = discord.ui.Button(label=f"Accept", style=discord.ButtonStyle.success)
    confirm.callback = confirm_button_thingy
    view = discord.ui.View()
    view.add_item(confirm)

    await ctx.channel.send(embed=embed, view=view)
    await ctx.response.send_message("HEADS UP: This is a Fake Gift. Gifts like these are Fake and are Using Embeds. a Real Gift is longer than what you can make with embeds (or a decent bit tall if your monitor is too short but tall enough). They will never look like this or like a typical Embed you get from a YouTube Video, a website or the like.", ephemeral=True)