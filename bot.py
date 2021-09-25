from __future__ import annotations
from typing import List

import json
import sys
import traceback

import diskord
from diskord.ext import commands

EXTENSIONS = (
    'cogs.dkc',
    'cogs.utility',
)

class BotKord(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.ignored_extensions: List[str] = kwargs.pop('ignored_extensions', [])

        with open('config.json', 'r') as f:
            config = json.loads(f.read())

        self.config: Dict[str, ...] = config

        super().__init__(*args, **kwargs)

    def run(self):
        token = self.config['token']
        if not token:
            raise diskord.LoginFailure('token was not added in config.json')

        for extension in EXTENSIONS:
            if not extension in self.ignored_extensions:
                try:
                    self.load_extension(extension)
                except Exception:
                    traceback.print_exc()

        super().run(self.config['token'])

    # Events

    async def on_ready(self):
        print(f'Logged in as: {self.user.name}#{self.user.discriminator}')

if __name__ == '__main__':
    if '--overwrite-application-commands' in sys.argv:
        overwrite_application_commands = True
    else:
        overwrite_application_commands = False

    bot = BotKord(
        command_prefix='!',
        overwrite_application_commands=overwrite_application_commands,
        intents=diskord.Intents.all()
        )
    bot.run()