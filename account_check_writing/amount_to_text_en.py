# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

import logging
from openerp.tools.translate import _
from openerp.tools import amount_to_text_en

_logger = logging.getLogger(__name__)

def amount_to_text(number, currency):
    number = '%.2f' % number
    list = str(number).split('.')
    start_word = amount_to_text_en.english_number(int(list[0]))
    end_word = "%d/%d"%(int(list[1]),100)
    return ' '.join(filter(None, [start_word, 'and', end_word]))


_translate_funcs = {'en' : amount_to_text}

def amount_to_text(nbr, lang='en', currency='euro'):
    """ Converts an integer to its textual representation, using th
    e language set in the context if any.
    """
    if not _translate_funcs.has_key(lang):
        _logger.warning(_("no translation function found for lang: '%s'"), lang)
        lang = 'en'
    return _translate_funcs[lang](abs(nbr), currency)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
