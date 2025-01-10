import math
from discord.ext import commands
import discord
from discord import ui

class FunctionPageSource(object):
    def __init__(self, num_pages, format_page):
        self.num_pages = num_pages
        self.format_page = format_page.__get__(self)

    def is_paginating(self):
        return self.num_pages > 1

    async def get_page(self, page_number):
        return page_number

    def get_max_pages(self):
        return self.num_pages

class AsyncListPageSource(object):
    def __init__(self, data, title=None, show_index=False, prepare_page=lambda self, items: None,
                 format_item=str, per_page=20, count=None):
        self.data = data
        self.title = title
        self.show_index = show_index
        self.prepare_page = prepare_page.__get__(self)
        self.format_item = format_item.__get__(self)
        self.per_page = per_page
        self.count = count

    def get_max_pages(self):
        if self.count is None:
            return None
        return math.ceil(self.count / self.per_page)

    async def get_page(self, page_number):
        start = page_number * self.per_page
        end = start + self.per_page
        return await self.data[start:end]

    async def format_page(self, menu, entries):
        self.prepare_page(entries)
        lines = [
            f"{i+1}. {self.format_item(x)}" if self.show_index else self.format_item(x)
            for i, x in enumerate(entries, start=menu.current_page * self.per_page)
        ]
        start = menu.current_page * self.per_page

        footer = menu.ctx._(
            "pagination-showing-entries-count" if self.count is not None else "pagination-showing-entries",
            start=start + 1,
            end=start + len(lines),
            total=self.count,
        )
        embed = menu.ctx.bot.Embed(
            title=self.title,
            description="\n".join(lines)[:4096],
        )
        embed.set_footer(text=footer)
        return embed

class ContinuablePages(discord.ui.View):
    def __init__(self, source, *, timeout=180, allow_last=True, allow_go=True):
        super().__init__(timeout=timeout)
        self.source = source
        self.current_page = 0
        self.ctx = None
        self.message = None
        self.allow_last = allow_last
        self.allow_go = allow_go

    async def start(self, ctx):
        self.ctx = ctx
        page = await self.source.get_page(0)
        kwargs = await self.get_kwargs_for_page(page)
        self.message = await ctx.send(**kwargs, view=self)

    async def get_kwargs_for_page(self, page):
        return {
            'embed': await self.source.format_page(self, page)
        }

    async def show_page(self, page_number):
        page = await self.source.get_page(page_number)
        self.current_page = page_number
        kwargs = await self.get_kwargs_for_page(page)
        await self.message.edit(**kwargs, view=self)

    async def show_checked_page(self, page_number):
        max_pages = self.source.get_max_pages()
        try:
            if max_pages is None:
                await self.show_page(page_number)
            elif page_number < 0 and not self.allow_last:
                await self.ctx.send(self.ctx._("pagination-last-jumping-unsupported"))
            else:
                await self.show_page(page_number % max_pages)
        except IndexError:
            pass

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.grey)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.defer()

    @discord.ui.button(label='Next', style=discord.ButtonStyle.grey)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_checked_page(self.current_page + 1)
        await interaction.response.defer()

    async def continue_at(self, ctx, page, *, channel=None, wait=False):
        self.stop()
        max_pages = self.source.get_max_pages()
        if max_pages is None:
            self.current_page = page
        else:
            self.current_page = page % self.source.get_max_pages()
        self.message = None
        await self.start(ctx)
