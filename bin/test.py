from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

@register_cell_magic
# @register_line_magic
def cd(line):
    "my line magic"
    return line



from IPython.terminal.prompts import Prompts, Token
import os

class MyPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        return [(Token, os.getcwd()),
            (Token.Prompt, ' >>>')]

ip = get_ipython()
ip.prompts = MyPrompt(ip)
# ip.define_magic("cd", cd)
