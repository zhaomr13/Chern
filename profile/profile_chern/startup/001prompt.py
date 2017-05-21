
# @register_cell_magic
# @register_line_magic
# def cd(line):
# "my line magic"
# return line



from IPython.terminal.prompts import Prompts, Token
import os

class ChernPrompt(Prompts):
    def __init__(self, ip):
        super(ChernPrompt, self).__init__(ip)
        self.current_project = ""

    def get_current_project(self):
        return "demo"

    def in_prompt_tokens(self, cli=None):
        return [(Token, self.get_current_project() ), (Token.Prompt, ' >>>')]

ip = get_ipython()
ip.prompts = ChernPrompt(ip)
# ip.define_magic("cd", cd)
