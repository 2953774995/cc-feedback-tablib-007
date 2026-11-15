"""Tablib - Markdown table export support.

   Generates a Markdown table from the dataset, as understood by GitHub and
   most internal documentation/wiki engines. The format is export-only.
"""


class MarkdownFormat:
    title = 'md'
    extensions = ('md',)

    @classmethod
    def export_set(cls, dataset):
        """Returns Markdown table representation of dataset.

        :param dataset: dataset to serialize
        :type dataset: tablib.core.Dataset
        """

        lines = []
        if dataset.headers:
            lines.append(cls._serialize_row(dataset.headers))
            lines.append(cls._serialize_separator(dataset.width))
        lines.extend(cls._serialize_row(row) for row in dataset)
        return '\n'.join(lines)

    @classmethod
    def _serialize_row(cls, row):
        return '| {} |'.format(' | '.join(cls._escape_cell(item) for item in row))

    @classmethod
    def _serialize_separator(cls, width):
        return '| {} |'.format(' | '.join(['---'] * width))

    @classmethod
    def _escape_cell(cls, item):
        """Escapes pipes and flattens newlines so the cell cannot break the table."""
        if item is None:
            return ''
        text = str(item)
        text = text.replace('\r\n', '<br>').replace('\r', '<br>').replace('\n', '<br>')
        return text.replace('|', '\\|')
