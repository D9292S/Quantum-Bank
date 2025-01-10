from discord.ext import commands
from discord import app_commands

class FlagCommand(app_commands.Command):
    @property
    def old_signature(self):
        if self.usage is not None:
            return self.usage

        params = self.clean_params
        if not params:
            return ""

        result = []
        for name, param in params.items():
            greedy = isinstance(param.annotation, commands.Greedy)

            if param.default is not param.empty:
                should_print = param.default if isinstance(param.default, str) else param.default is not None
                if should_print:
                    result.append(
                        f"[{name}={param.default}]" if not greedy else f"[{name}={param.default}]..."
                    )
                    continue
                else:
                    result.append(f"[{name}]")

            elif param.kind == param.VAR_POSITIONAL:
                result.append(f"[{name}...]")
            elif greedy:
                result.append(f"[{name}]...")
            elif commands.is_typing_optional(param.annotation):
                result.append(f"[{name}]")
            elif param.kind == param.VAR_KEYWORD:
                pass
            else:
                result.append(f"<{name}>")

        return " ".join(result)

def command(**kwargs):
    def inner(func):
        cls = kwargs.get("cls", FlagCommand)
        return cls(func, **kwargs)

    return inner
