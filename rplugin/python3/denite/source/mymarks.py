# ============================================================================
# FILE: neomarks.py
# AUTHOR: takashi (takashi1coq at gmail.com)
# License: MIT license
# ============================================================================

from .mark import Source as Mark
from denite.kind.file import Kind as File

class Source(Mark):

    def __init__(self,  vim):
        super().__init__(vim)
        self.name = 'mymarks'
        self.kind = Kind(vim)

    def _get_marks(self, context):

        # file marks

        lower_marks = [chr(c) for c in range(ord('a'), ord('z'))]
        upper_marks = [chr(c) for c in range(ord('A'), ord('Z'))]
        num_marks = [str(n) for n in range(1, 10)]
        others_marks = ['\'', '`', '\"', '[', ']', '^', '.', '<', '>']

        if len(context['args']) == 4:
            if context['args'][0] == '':
                lower_marks = []
            if context['args'][1] == '':
                upper_marks = []
            if context['args'][2] == '':
                num_marks = []
            if context['args'][3] == '':
                others_marks = []

        marks_str = lower_marks + upper_marks + num_marks + others_marks

        mark_list = []

        # mark order same as :marks
        for m in marks_str:

            mark_info = [bufnum, lnum, col, off] = self.vim.call(
                'getpos', '\'' + m)
            if self.empty_mark(mark_info):
                continue

            bufname = self.vim.call('bufname',
                                    bufnum if bufnum != 0 else '%')
            path = self.vim.call('fnamemodify', bufname, ':p')
            if bufnum == 0:
                file_or_text = 'text: ' + self.vim.call('getline', lnum)
            else:
                file_or_text = 'file: ' + path

            mark_list.append({
                'word': '{:>3} {:>5} {:>5}  {}'
                .format(m, lnum, col, file_or_text),
                'action__path': path,
                'action__line': lnum,
                'action__col': col,
                'mark': m,
            })
        return mark_list

    def gather_candidates(self, context):
        return self._get_marks(context)
