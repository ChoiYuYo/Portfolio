"""Opens the source file of Python modules in a program of choice."""

import sys
from argparse import ArgumentParser, Action
import os
import os.path
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable    # noqa: F401
from importlib import import_module
from contextlib import contextmanager, ExitStack
from tempfile import NamedTemporaryFile
from subprocess import call

__author__ = """Eugene M. Kim"""
__email__ = 'astralblue@gmail.com'
__version__ = '0.1.3'


class Tool (metaclass=ABCMeta):
    """A tool."""

    @abstractmethod
    def open(self, modules):
        """
        Open the given *modules* with this tool.

        :param modules: fully-qualified module names to open.
        :type modules: iterable of `str`-ings
        """


class FileTool (Tool):
    """A tool that opens module source files."""

    def open(self, modules):
        """Open the given *modules*' source files with this tool."""
        with self.__sources(modules) as files:
            self._open_files(files)

    @classmethod
    @contextmanager
    def __sources(cls, modules):
        with ExitStack() as stack:
            yield tuple(stack.enter_context(cls.__source(module))
                        for module in modules)

    @classmethod
    @contextmanager
    def __source(cls, module):
        mod = import_module(module)
        for cm in (cls.__source_from_file_attr, cls.__source_from_loader):
            with cm(mod) as path:
                if path is not None:
                    yield path
                    break
        else:
            raise RuntimeError("cannot get source for {}".format(module))

    @classmethod
    @contextmanager
    def __source_from_file_attr(cls, mod):
        try:
            path = mod.__file__
        except AttributeError:
            yield None
            return
        if not os.access(path, os.R_OK):
            yield None
            return
        yield path

    @classmethod
    @contextmanager
    def __source_from_loader(cls, mod):
        try:
            loader = mod.__loader__
        except AttributeError:
            yield None
            return
        try:
            source = loader.get_source(mod.__name__)
        except Exception as e:
            yield None
            return
        with NamedTemporaryFile(mode='w') as f:
            f.write(source)
            f.flush()
            yield f.name

    @abstractmethod
    def _open_files(self, filenames):
        """
        Open the given files.

        :param filenames: names of the files to open.
        :type filenames: iterable of `str`-ings
        """


class ProgramTool (FileTool):
    """A program-based tool."""

    def _open_files(self, filenames):
        prog = self.get_prog()
        args = prog.split()
        if not args:
            raise ValueError("empty program: {!r}".format(prog))
        args.extend(filenames)
        call(args)

    @abstractmethod
    def get_prog(self):
        """
        Get the program with which to open files.

        To be implemented by subclasses.

        :return: the program and its arguments, whitespace-separated.
        :rtype: `str`
        """


class ProgLitTool (ProgramTool):
    """
    A tool that uses the given *prog*-ram.

    :param `str` prog: the program and its arguments, whitespace-separated.
    """

    def __init__(self, prog, *args, **kwargs):
        """Initialize this instance."""
        super().__init__(*args, **kwargs)
        self.__prog = prog

    def get_prog(self):
        """
        Get the literal program with which to open files.

        :return: the *prog*-ram given when this instance was created.
        :rtype: `str`
        """
        return self.__prog

    @property
    def prog(self):
        """The program to use."""
        return self.__prog

    def __str__(self):
        """Return a description of this program for use in help text."""
        return "{0.prog!r}".format(self)


class ProgEnvTool (ProgramTool):
    """
    A tool that takes its program from the given *env*-ironment variable.

    :param `str` env: the name of the environment variable.
    :param `str` default:
        the default program literal to use when the *env*-ironment variable is
        not set.  If `None` (default) and the variable is not set, lazily raise
        an exception, i.e. not here but in `get_prog()`.
    """

    def __init__(self, env, *args, default=None, **kwargs):
        """Initialize this instance."""
        super().__init__(*args, **kwargs)
        self.__env = env
        self.__default = default

    def get_prog(self):
        """
        Get the program literal from the environment variable for the instance.

        :return:
            the value of the environment variable for this instance; if not
            set, the default value.
        :rtype: `str`
        :raise `RuntimeError`:
            if the environment variable is not set and the default is `None`.
        """
        prog = os.environ.get(self.__env, self.__default)
        if prog is None:
            raise RuntimeError("program environment variable {} is not set"
                               .format(self.__env))
        return prog

    @property
    def env(self):
        """Name of the environment variable."""
        return self.__env

    @property
    def default(self):
        """Default to use when the environment varaible is not set."""
        return self.__default

    def __str__(self):
        """Return a description of this program for use in help text."""
        if self.default is None:
            return "${0.env}".format(self)
        else:
            return "${0.env}, or if not set, {0.default!r}".format(self)


KNOWN_TOOLS = (
        (('-E', '--editor'), ProgEnvTool('EDITOR', default='vi')),
        (('-V', '--visual'), ProgEnvTool('VISUAL', default='vi')),
        (('-P', '--pager'), ProgEnvTool('PAGER', default='more')),
        (('--vi',), ProgLitTool('vi')),
        (('--vim',), ProgLitTool('vim')),
        (('--emacs',), ProgLitTool('emacs')),
        (('--more',), ProgLitTool('more')),
        (('--less',), ProgLitTool('less')),
        (('--vi-read-only',), ProgLitTool('vi -R')),
        (('--vim-read-only',), ProgLitTool('vim -R')),
)


DEFAULT_TOOL = ProgEnvTool('PAGER', default='more')


def main():
    """The main body of this program."""
    parser = ArgumentParser(
            description="""
                Opens the source file of Python modules in an editor, a pager,
                or any other program of choice.
            """,
            epilog="""
                The default program is {}.
            """.format(DEFAULT_TOOL),
    )
    for opts, tool in KNOWN_TOOLS:
        parser.add_argument(*opts, dest='tool',
                            action='store_const', const=tool,
                            help="""use {}""".format(tool))
    parser.add_argument('-e', '--env', metavar='VAR[=DEFAULT]',
                        dest='tool', action=CustomProgEnvToolAction,
                        help="""use $VAR, or if not set, DEFAULT""")
    parser.add_argument('-p', '--program', metavar='PROG',
                        dest='tool', action=CustomProgLitToolAction,
                        help="""use PROG""")
    parser.add_argument('modules', nargs='+', metavar='MODULE',
                        help="""fully qualified name of module to open""")
    parser.set_defaults(tool=DEFAULT_TOOL)
    args = parser.parse_args()
    args.tool.open(args.modules)
    return 0


class CustomToolAction (Action, metaclass=ABCMeta):
    """A parser action that sets ``tool`` with a custom `Tool` instance."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Set ``tool`` with the custom tool returned by `get_tool()`."""
        setattr(namespace, 'tool', self.get_tool(values))

    @abstractmethod
    def get_tool(self, value):
        """
        Get a custom tool from the given argument *value*.

        :param `str` value:
            the argument value passed in from the `argument parser
            <argparse.ArgumentParser>`.  Its semantics are defined by actual
            implementation of this method, and varies from subclass to
            subclass.
        :return: a tool instance created from *value*.
        :rtype: `Tool`
        """


class CustomProgEnvToolAction (CustomToolAction):
    """An action that sets ``tool`` with a custom `ProgEnvTool` instance."""

    def get_tool(self, value):
        """
        Get a custom `ProgEnvTool` from the given *value*.

        :param `str` value:
            the environment variable name, optionally suffixed with an equal
            sign and the default value, e.g. ``EDITOR=vim``.
        :return: a tool instance created from *value*.
        :rtype: `ProgEnvTool`
        """
        if '=' in value:
            env, default = value.split('=', 1)
        else:
            env, default = value, None
        return ProgEnvTool(env, default=default)


class CustomProgLitToolAction (CustomToolAction):
    """An action that sets ``tool`` with a custom `ProgLitTool` instance."""

    def get_tool(self, value):
        """
        Get a custom `ProgLitTool` from the given *value*.

        :param `str` value:
            the literal program string (name and optional arguments), e.g.
            ``less -Sc``.
        :return: a tool instance created from *value*.
        :rtype: `ProgLitTool`
        """
        return ProgLitTool(value)


if __name__ == '__main__':
    sys.exit(main())
