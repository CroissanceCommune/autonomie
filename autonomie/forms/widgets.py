# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import deform


class CleanMappingWidget(deform.widget.MappingWidget):
    template = 'clean_mapping.pt'


class CleanSequenceWidget(deform.widget.SequenceWidget):
    template = 'clean_sequence.pt'


class FixedLenSequenceWidget(deform.widget.SequenceWidget):
    template = 'fixed_len_sequence.pt',
    item_template = 'fixed_len_sequence_item.pt'
