# BetterBoiBot

## Project Description:

BetterBoiBot is a Python Discord bot that I developed as a bit of a fun project
for my friends and I to utilize in our Discord calls. Feel free to use him as
well, fork and modify him, or do whatever you so choose!

## How to Install and Run:
Fork this project and register a bot with Discord's Developer Portal. Then, acquire the bot's token and permissions int to place into a file '.env' in the
main project folder. Finally, run bot.py (or host via a hosting service like Heroku.)

## How to Use:
As server admin, invite the bot to your server using the following OAuth URL:
https://discord.com/api/oauth2/authorize?client_id=923347751754944532&permissions=1644971949559&scope=bot%20applications.commands

Commands are called by typing the prefix '3b!' and then a command name. Below is
a list of commands:

play <url or search term>: BetterBoiBot will play either the audio of a youtube video at the link provided, or the first search from youtube for that search term.

poll <msg, desc, opt>: Create a poll with header <msg>, paragraph description <desc>, and number of options <opt> (2-5).

poll_yesno <msg>: Create a poll with header <msg> and description "React to this message with ✅ for Yes, ❌ for No."

votekick <user>: Vote to kick a user democratically. *TESTING*

kick <user>: Forcefully kick a user if you have the privileges. *TESTING*

queue <url>: Enter audio from youtube into a queue

skip: Skip the currently playing audio.

stop: Stop playing all media.

voteskip: Elect to skip current media democratically.

## Credits:
discord.py: https://github.com/Rapptz/discord.py

youtube_dl: https://pypi.org/project/youtube_dl/

Django: https://www.djangoproject.com/

BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/


## License:
MIT License

Copyright (c) 2022 BetterBoiBot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
