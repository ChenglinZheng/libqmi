#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*-
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2012 Lanedo GmbH
#

import string
import utils
from Variable import Variable

"""
Variable type for signed/unsigned Integers
('guint8', 'gint8', 'guint16', 'gint16', 'guint32', 'gint32', 'guint64', 'gint64' formats)
"""
class VariableInteger(Variable):

    """
    Constructor
    """
    def __init__(self, dictionary):

        # Call the parent constructor
        Variable.__init__(self, dictionary)

        self.private_format = self.format
        self.public_format = dictionary['public-format'] if 'public-format' in dictionary else self.private_format


    """
    Read a single integer from the raw byte buffer
    """
    def emit_buffer_read(self, f, line_prefix, variable_name, buffer_name, buffer_len):
        translations = { 'lp'             : line_prefix,
                         'public_format'  : self.public_format,
                         'private_format' : self.private_format,
                         'variable_name'  : variable_name,
                         'buffer_name'    : buffer_name,
                         'buffer_len'     : buffer_len }

        if self.private_format == self.public_format:
            template = (
                '${lp}/* Read the ${private_format} variable from the buffer */\n'
                '${lp}qmi_utils_read_${private_format}_from_buffer (\n'
                '${lp}    &${buffer_name},\n'
                '${lp}    &${buffer_len},\n'
                '${lp}    &(${variable_name}));\n')
        else:
            template = (
                '${lp}{\n'
                '${lp}    ${private_format} tmp;\n'
                '\n'
                '${lp}    /* Read the ${private_format} variable from the buffer */\n'
                '${lp}    qmi_utils_read_${private_format}_from_buffer (\n'
                '${lp}        &${buffer_name},\n'
                '${lp}        &${buffer_len},\n'
                '${lp}        &tmp);\n'
                '${lp}    ${variable_name} = (${public_format})tmp;\n'
                '${lp}}\n')
        f.write(string.Template(template).substitute(translations))


    """
    Write a single integer to the raw byte buffer
    """
    def emit_buffer_write(self, f, line_prefix, variable_name, buffer_name, buffer_len):
        translations = { 'lp'             : line_prefix,
                         'private_format' : self.private_format,
                         'variable_name'  : variable_name,
                         'buffer_name'    : buffer_name,
                         'buffer_len'     : buffer_len }
        if self.private_format == self.public_format:
            template = (
                '${lp}/* Write the ${private_format} variable to the buffer */\n'
                '${lp}qmi_utils_write_${private_format}_to_buffer (\n'
                '${lp}    &${buffer_name},\n'
                '${lp}    &${buffer_len},\n'
                '${lp}    &(${variable_name}));\n')
        else:
            template = (
                '${lp}{\n'
                '${lp}    ${private_format} tmp;\n'
                '\n'
                '${lp}    tmp = (${private_format})${variable_name};\n'
                '${lp}    /* Write the ${private_format} variable to the buffer */\n'
                '${lp}    qmi_utils_write_${private_format}_to_buffer (\n'
                '${lp}        &${buffer_name},\n'
                '${lp}        &${buffer_len},\n'
                '${lp}        &tmp);\n'
                '${lp}}\n')
        f.write(string.Template(template).substitute(translations))


    """
    Get the integer as a printable string.
    """
    def emit_get_printable(self, f, line_prefix, printable, buffer_name, buffer_len):
        common_format = ''
        common_cast = ''
        if self.private_format == 'guint8':
            common_format = '%u'
            common_cast = '(guint)'
        elif self.private_format == 'guint16':
            common_format = '%" G_GUINT16_FORMAT "'
        elif self.private_format == 'guint32':
            common_format = '%" G_GUINT32_FORMAT "'
        elif self.private_format == 'guint64':
            common_format = '%" G_GUINT64_FORMAT "'
        elif self.private_format == 'gint8':
            common_format = '%d'
            common_cast = '(gint)'
        elif self.private_format == 'gint16':
            common_format = '%" G_GINT16_FORMAT "'
        elif self.private_format == 'gint32':
            common_format = '%" G_GINT32_FORMAT "'
        elif self.private_format == 'gint64':
            common_format = '%" G_GINT64_FORMAT "'

        translations = { 'lp'             : line_prefix,
                         'private_format' : self.private_format,
                         'printable'      : printable,
                         'buffer_name'    : buffer_name,
                         'buffer_len'     : buffer_len,
                         'common_format'  : common_format,
                         'common_cast'    : common_cast }

        template = (
            '\n'
            '${lp}{\n'
            '${lp}    ${private_format} tmp;\n'
            '\n'
            '${lp}    /* Read the ${private_format} variable from the buffer */\n'
            '${lp}    qmi_utils_read_${private_format}_from_buffer (\n'
            '${lp}        &${buffer_name},\n'
            '${lp}        &${buffer_len},\n'
            '${lp}        &tmp);\n'
            '\n'
            '${lp}    g_string_append_printf (${printable}, "${common_format}", ${common_cast}tmp);\n'
            '${lp}}\n')
        f.write(string.Template(template).substitute(translations))


    """
    Variable declaration
    """
    def build_variable_declaration(self, line_prefix, variable_name):
        translations = { 'lp'             : line_prefix,
                         'private_format' : self.private_format,
                         'name'           : variable_name }

        template = (
            '${lp}${private_format} ${name};\n')
        return string.Template(template).substitute(translations)


    """
    Getter for the integer type
    """
    def build_getter_declaration(self, line_prefix, variable_name):
        translations = { 'lp'            : line_prefix,
                         'public_format' : self.public_format,
                         'name'          : variable_name }

        template = (
            '${lp}${public_format} *${name},\n')
        return string.Template(template).substitute(translations)


    """
    Documentation for the getter
    """
    def build_getter_documentation(self, line_prefix, variable_name):
        translations = { 'lp'            : line_prefix,
                         'public_format' : self.public_format,
                         'name'          : variable_name }

        template = (
            '${lp}@${name}: a placeholder for the output #${public_format}, or #NULL if not required.\n')
        return string.Template(template).substitute(translations)

    """
    Builds the Integer getter implementation
    """
    def build_getter_implementation(self, line_prefix, variable_name_from, variable_name_to, to_is_reference):
        needs_cast = True if self.public_format != self.private_format else False
        translations = { 'lp'       : line_prefix,
                         'from'     : variable_name_from,
                         'to'       : variable_name_to,
                         'cast_ini' : '(' + self.public_format + ')(' if needs_cast else '',
                         'cast_end' : ')' if needs_cast else '' }

        if to_is_reference:
            template = (
                '${lp}if (${to})\n'
                '${lp}    *${to} = ${cast_ini}${from}${cast_end};\n')
            return string.Template(template).substitute(translations)
        else:
            template = (
                '${lp}${to} = ${cast_ini}${from}${cast_end};\n')
            return string.Template(template).substitute(translations)


    """
    Setter for the integer type
    """
    def build_setter_declaration(self, line_prefix, variable_name):
        translations = { 'lp'            : line_prefix,
                         'public_format' : self.public_format,
                         'name'          : variable_name }

        template = (
            '${lp}${public_format} ${name},\n')
        return string.Template(template).substitute(translations)


    """
    Documentation for the setter
    """
    def build_setter_documentation(self, line_prefix, variable_name):
        translations = { 'lp'            : line_prefix,
                         'public_format' : self.public_format,
                         'name'          : variable_name }

        template = (
            '${lp}@${name}: a #${public_format}.\n')
        return string.Template(template).substitute(translations)


    """
    Implementation of the setter
    """
    def build_setter_implementation(self, line_prefix, variable_name_from, variable_name_to):
        needs_cast = True if self.public_format != self.private_format else False
        translations = { 'lp'       : line_prefix,
                         'from'     : variable_name_from,
                         'to'       : variable_name_to,
                         'cast_ini' : '(' + self.private_format + ')(' if needs_cast else '',
                         'cast_end' : ')' if needs_cast else '' }

        template = (
            '${lp}${to} = ${cast_ini}${from}${cast_end};\n')
        return string.Template(template).substitute(translations)
