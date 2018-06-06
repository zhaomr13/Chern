
# @register_cell_magic
# @register_line_magic
# def cd(line):
# "my line magic"
# return line



from IPython.terminal.prompts import Prompts, Token
import os
from Chern.interface.ChernManager import get_manager
from Chern.kernel.ChernDatabase import ChernDatabase

cherndb = ChernDatabase.instance()
class ChernPrompt(Prompts):
    def __init__(self, ip):
        super(ChernPrompt, self).__init__(ip)
        self.manager = get_manager()

    def get_prompt_name(self):
        current_project_name = self.manager.get_current_project()
        if current_project_name == "/":
            return "[Chern]"
        else:
            return "["+current_project_name+"] ["+os.path.relpath(manager.c.path, cherndb.project_path())+"]\n"

    def in_prompt_tokens(self, cli=None):
        return [(Token, self.get_prompt_name() ), (Token.Prompt, ' >>> ')]

ip = get_ipython()
ip.prompts = ChernPrompt(ip)
