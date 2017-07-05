# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader
from azure.cli.core.sdk.util import CliCommandType

import azure.cli.command_modules.extension._help  # pylint: disable=unused-import


class ExtensionCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        super(ExtensionCommandsLoader, self).__init__(cli_ctx=cli_ctx)
        self.module_name = __name__

    def load_command_table(self, args):
        if not super(ExtensionCommandsLoader, self).load_command_table(args):
            return

        extension_custom = CliCommandType(operations_tmpl='azure.cli.command_modules.extension.custom#{}')

        with self.command_group('extension', extension_custom) as g:
            g.command('add', 'add_extension')
            g.command('remove', 'remove_extension')
            g.command('list', 'list_extensions')
            g.command('show', 'show_extension')

        return self.command_table

    # pylint: disable=line-too-long
    def load_arguments(self, command):
        if not super(ExtensionCommandsLoader, self).load_arguments(command):
            return

        from argcomplete.completers import FilesCompleter
        from azure.cli.core.extension import get_extension_names

        def extension_name_completion_list(prefix, **kwargs):  # pylint: disable=unused-argument
            return get_extension_names()

        with self.argument_context('extension') as c:
            c.argument('extension_name', options_list=['--name', '-n'], help='Name of extension', completer=extension_name_completion_list)

        with self.argument_context('extension add') as c:
            c.argument('extension_name', completer=None)
            c.argument('source', options_list=['--source', '-s'], help='Filepath or URL to an extension', completer=FilesCompleter())
