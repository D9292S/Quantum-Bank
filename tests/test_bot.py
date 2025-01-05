import unittest
from unittest.mock import AsyncMock, patch, MagicMock

class TestMyBot(unittest.TestCase):
    def setUp(self):
        self.bot = MagicMock()

    @patch('discord.ext.commands.Bot.send_message')
    async def test_ping_command(self, mock_send):
        ctx = AsyncMock()
        await self.bot.ping(ctx)
        mock_send.assert_called_with(ctx, "Pong!")
