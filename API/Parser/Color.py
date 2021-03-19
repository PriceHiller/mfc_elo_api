#!/usr/bin/env python3

# -*- Coding: UTF-8 -*- #
# -*- System: Linux -*- #
# -*- Usage:  *.py  -*- #

#
#  Copyright (c) 2021. Jacob B. Sanders, Cloud Hybrid LLC. & Affiliates.
#
#  Redistribution and use in source and binary forms, with or without modification, are permitted
#  provided that the following conditions are met:
#
#  1.  Redistributions of source code must retain the above copyright notice, this list of
#      conditions and the following disclaimer.
#  2.  Redistributions in binary form must reproduce the above copyright notice, this list of
#      conditions and the following disclaimer in the documentation and/or other materials
#      provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
#  OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
#  AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#  OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
#  OF SUCH DAMAGE.
#

"""
Color Standard-Output - Module
"""

import os
import pty
import sys
import time
import shlex
import subprocess
import dataclasses

__all__ = [
    "TTY"
]

Dataclass = dataclasses.dataclass

Abstraction: Dataclass = dataclasses.dataclass(
    frozen = True,
    unsafe_hash = True,
    order = False,
    init = True
)

Schema: Dataclass = dataclasses.dataclass(
    frozen = True,
    unsafe_hash = True,
    order = False,
    init = False
)

@Abstraction
class Colors:
    """
    TTY color escape sequences to Color Parameterized *Compatible, Raw-String input
    with compatible buffers.

    Colors should be instantiated for use as a class Composition.

    *Let "Compatible" be defined as a system's specific, default string encoding
    type.
    """

    black = lambda String: "\33[30m" + str(String) + "\033[0m"
    red = lambda String: "\33[31m" + str(String) + "\033[0m"
    green = lambda String: "\33[32m" + str(String) + "\033[0m"
    yellow = lambda String: "\33[33m" + str(String) + "\033[0m"
    blue = lambda String: "\33[34m" + str(String) + "\033[0m"
    violet = lambda String: "\33[35m" + str(String) + "\033[0m"
    beige = lambda String: "\33[36m" + str(String) + "\033[0m"
    white = lambda String: "\33[37m" + str(String) + "\033[0m"

@Abstraction
class Modifier:
    """
    TTY color escape sequences to Format String Parameterized input
    with compatible buffers.

    Modifier should be instantiated for use as a class Composition.
    """

    end = lambda String: "\33[0m" + str(String) + "\033[0m"
    bold = lambda String: "\33[1m" + str(String) + "\033[0m"
    italic = lambda String: "\33[3m" + str(String) + "\033[0m"
    url = lambda String: "\33[4m" + str(String) + "\033[0m"
    blink = lambda String: "\33[5m" + str(String) + "\033[0m"
    selected = lambda String: "\33[7m" + str(String) + "\033[0m"
    underline = lambda String: "\033[4m" + str(String) + "\033[0m"

@Schema
class TTY(object):
    """
    Abstract TTY color escape sequences to style Color with compatible buffers.

    There is no need to instantiate this class unless extending the class's
    capabilities.
    """

    Color: Colors = Colors()
    Format: Modifier = Modifier()

    Columns = lambda: os.get_terminal_size().columns
    Rows = lambda: os.get_terminal_size().lines

    reset = "\033[0m"

    # ==> Backwards Compatibility with Interfaced Libraries

    end = lambda String: "\33[0m" + str(String) + "\033[0m"
    bold = lambda String: "\33[1m" + str(String) + "\033[0m"
    italic = lambda String: "\33[3m" + str(String) + "\033[0m"
    url = lambda String: "\33[4m" + str(String) + "\033[0m"
    blink = lambda String: "\33[5m" + str(String) + "\033[0m"
    selected = lambda String: "\33[7m" + str(String) + "\033[0m"
    black = lambda String: "\33[30m" + str(String) + "\033[0m"
    red = lambda String: "\33[31m" + str(String) + "\033[0m"
    green = lambda String: "\33[32m" + str(String) + "\033[0m"
    yellow = lambda String: "\33[33m" + str(String) + "\033[0m"
    blue = lambda String: "\33[34m" + str(String) + "\033[0m"
    violet = lambda String: "\33[35m" + str(String) + "\033[0m"
    beige = lambda String: "\33[36m" + str(String) + "\033[0m"
    white = lambda String: "\33[37m" + str(String) + "\033[0m"

    underline = lambda String: "\033[4m" + str(String) + "\033[0m"

    @staticmethod
    def Flush():
        sys.stdout.flush()

    @staticmethod
    def Clear():
        """
        Clear
        ------------------------------------------------------------------ :80 -
        Write a "Cleared" Line to Standard-Output.

        Specifically, Output:
            1. A Line-Feed Reset Character
            2. " " * a Controlling [S]TTY Terminal's # of Columns
                - See https://www.gnu.org/software/coreutils/manual/html_node/Special.html
                - https://www.unix.com/shell-programming-and-scripting/96249-posix-way-getting-columns-tty-2.html
            3. An Additional Line-Feed Reset Character
            4. Lastly, Flush Standard-Output
        """

        sys.stdout.write("\r")
        sys.stdout.write(" " * TTY.Columns())
        sys.stdout.write("\r")

        TTY.Flush()

    @property
    def EOF(self) -> str:       return self.reset

    @property
    def EOL(self) -> str:       return self.reset

    @property
    def Reset(self) -> str:     return self.reset

    @property
    def X(self) -> str:         return self.reset

    @property
    def System(self) -> str:
        return sys.platform.casefold()

    def __getattribute__(self, name):
        if self.System == "win32":
            raise NotImplementedError("Cannot Use POSIX Color Escape Sequences")

        return super().__getattribute__(name)

    def __getattr__(self, name):
        if self.System == "win32":
            raise NotImplementedError("Cannot Use POSIX Color Escape Sequences")

        return getattr(self, name, R"")

    @classmethod
    def Shell(cls):
        """
        Function is primarily only used for demonstration purposes only.
        """

        Settings = ("TTY.Wrapper", "wb+")

        with open(*Settings) as File:
            def read(fd):
                """
                Replace *Bracketed Replace Mode* from Darwin, MacOS or BSD
                System(s) Identified via the following Control Characters:
                    - 
                    - [?2004h
                    - [?2004l
                """

                buffer = os.read(fd, 1024).replace(
                    bytes("", encoding = "UTF-8"),
                    bytes("", encoding = "UTF-8")
                ).replace(
                    bytes("[?2004h", encoding = "UTF-8"),
                    bytes("", encoding = "UTF-8")
                ).replace(
                    bytes("[?2004l", encoding = "UTF-8"),
                    bytes("", encoding = "UTF-8")
                )

                File.write(buffer)

                return buffer

            print("Sub-Shell: {0}".format(Settings[0]))
            print(" - Press Enter after exit() to Continue")
            print()

            pty.spawn(sys.executable, read)

if __name__ == "__main__":
    ### Usage (Bash)
    ### >>> $ python[3] Parser/Color.py
    ###     ...

    TTY.Shell()

    print("Color.py Module Unit Test".center(TTY.Columns(), " "))

    print(TTY.Columns() * "-")

    print("TTY Validation")

    assert os.isatty(sys.stdout.fileno())

    print(" - Successful")

    print("TTY Columns: \n {0}".format(
        "-" + " " + "%i" % TTY.Columns()
    ))

    print("TTY Rows: \n {0}".format(
        "-" + " " + "%i" % TTY.Rows()
    ))

    print(TTY.Columns() * "-")

    print(TTY.bold(
        "bold"
    ))
    print(TTY.italic(
        "italic"
    ))
    print(TTY.url(
        "url"
    ))
    print(TTY.blink(
        "blink"
    ))
    print(TTY.selected(
        "selected"
    ))
    print(TTY.black(
        "black"
    ))
    print(TTY.red(
        "red"
    ))
    print(TTY.green(
        "green"
    ))
    print(TTY.yellow(
        "yellow"
    ))
    print(TTY.blue(
        "blue"
    ))
    print(TTY.violet(
        "violet"
    ))
    print(TTY.beige(
        "beige"
    ))
    print(TTY.white(
        "white"
    ))
