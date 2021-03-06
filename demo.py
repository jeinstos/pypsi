#
# Copyright (c) 2014, Adam Meily
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# * Neither the name of the {organization} nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from pypsi.shell import Shell
from pypsi.base import Command
#from pypsi.plugins.alias import AliasPlugin
from pypsi.plugins.cmd import CmdPlugin
from pypsi.plugins.block import BlockPlugin
from pypsi.plugins.hexcode import HexCodePlugin
from pypsi.commands.macro import MacroCommand
from pypsi.commands.system import SystemCommand
from pypsi.plugins.multiline import MultilinePlugin
from pypsi.commands.xargs import XArgsCommand
from pypsi.commands.exit import ExitCommand
from pypsi.plugins.variable import VariablePlugin
from pypsi.plugins.history import HistoryPlugin
from pypsi.commands.echo import EchoCommand
from pypsi.commands.include import IncludeCommand
from pypsi.commands.help import HelpCommand, Topic
from pypsi.commands.tip import TipCommand
from pypsi.stream import AnsiStdout
from pypsi import topics
import sys

ShellTopic = """These commands are built into the Pypsi shell (all glory and honor to the pypsi shell).
This is a single newline

and This is a double"""



class TestCommand(Command):

    def __init__(self, name='test', **kwargs):
        super(TestCommand, self).__init__(name=name, **kwargs)

    def run(self, shell, args, ctx):
        print("TEST!")
        return 0


class DemoShell(Shell):

    test_cmd = TestCommand()
    echo_cmd = EchoCommand()
    block_plugin = BlockPlugin()
    hexcode_plugin = HexCodePlugin()
    macro_cmd = MacroCommand()
    system_cmd = SystemCommand()
    ml_plugin = MultilinePlugin()
    xargs_cmd = XArgsCommand()
    exit_cmd = ExitCommand()
    history_plugin = HistoryPlugin()
    include_cmd = IncludeCommand()
    cmd_plugin = CmdPlugin(cmd_args=1)
    tip_cmd = TipCommand()
    help_cmd = HelpCommand(
        topics=(
            Topic('builtin', 'Builtin Commands & Features', ShellTopic),
            topics.IoRedirection
        )
    )
    var_plugin = VariablePlugin(case_sensitive=False, env=False)

    def __init__(self):
        super(DemoShell, self).__init__()
        self.tip_cmd.load_tips("./demo-tips.txt")
        self.tip_cmd.load_motd("./demo-motd.txt")
        self.prompt = "{gray}[$time]{r} {cyan}pypsi{r} {green})>{r} ".format(
            gray=AnsiStdout.gray, r=AnsiStdout.reset, cyan=AnsiStdout.cyan,
            green=AnsiStdout.green
        )
        self.fallback_cmd = self.system_cmd

    def on_cmdloop_begin(self):
        print(AnsiStdout.clear_screen)
        self.tip_cmd.print_motd(self)
        print()
        print(AnsiStdout.green, "Tip of the Day".center(self.width), sep='')
        print('>' * self.width, AnsiStdout.reset, sep='')
        self.tip_cmd.print_random_tip(self, False)
        print(AnsiStdout.green, '<' * self.width, AnsiStdout.reset, sep='')
        print()

    def do_cmddoc(self, args):
        '''
        This is some long description for the cmdargs command.
        '''
        print("do_cmdargs(", args, ")")
        return 0

    def help_cmdout(self):
        print("this is the help message for the cmdout command")

    def do_cmdout(self, args):
        print("do_cmdout(", args, ")")
        return 0


if __name__ == '__main__':
    shell = DemoShell()
    shell.cmdloop()
