@bot.tree.command(name="minesweeper", description="Play Minesweeper")
@app_commands.user_install()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(boardsize="the size of the board, square", mines="mine count")
async def minesweeper(ctx: discord.Interaction, boardsize: int = 9, mines: int = None):
    if mines is None:
        mines = (boardsize**2)//8
    if mines > (boardsize**2)-4:
        mines = (boardsize**2)-4

    await ctx.response.send_message(f"# `{leftpad(str(mines), 3, "0")}`{emoj["l"]}{emoj["l"]}{emoj["g"]}{emoj["l"]}{emoj["l"]}`000`")

    boardtemp = []
    for num in range(boardsize):
        boardtemp.append("0")

    board = []
    for num in range(boardsize):
        board.append(boardtemp[:])

    for mine in range(mines):
        x = random.randint(0, boardsize-1)
        y = random.randint(0, boardsize-1)
        while board[y][x] == "e" or (x < 2 and y < 2):
            x = random.randint(0, boardsize-1)
            y = random.randint(0, boardsize-1)
        board[y][x] = "e"

    for cy in range(boardsize):
        for cx in range(boardsize):
            if board[cy][cx] == "e":
                continue

            mines = 0

            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue

                    ny = cy + dy
                    nx = cx + dx

                    if 0 <= nx < boardsize and 0 <= ny < boardsize:
                        if board[ny][nx] == "e":
                            mines += 1

            board[cy][cx] = str(mines)

    lines = []
    fubbers = [None]
    for arrey in board:
        m = ""
        for char in arrey:
            m += char
        for char in emoj:
            m = m.replace(char, "||"+emoj[char]+"||")

        lines.append(m)
        if len("\n".join(lines)) > 2000:
            lines = [lines[-1]]
            fubbers.append(None)
        fubbers[-1] = "\n".join(lines)

    sentcmd = None
    for g in fubbers:
        sentcmd = await ctx.channel.send(g[:2000])

    await sentcmd.add_reaction(emoj["f"])
    await sentcmd.add_reaction(emoj["b"])

@bot.tree.command(name="minesweeper-help", description="How to play minesweeper?")
async def minesweeper_help(ctx: discord.Interaction):
    res = f"""
Minesweeper Rules:
1. If you find a {emoj["e"]}, you lose.
2. Please don't cheat, if you post the solution, you may be banned depending on the server's mods.
3. Once you reveal every tile that isn't a mine (in this 9x9 board, there is 10), you win.
4. React {emoj["f"]} if you win, and {emoj["b"]} if you lose.
5. The top left corner is always safe, so start there.
"""
    await ctx.response.send_message(res)