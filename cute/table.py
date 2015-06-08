from PyQt5.QtCore import Qt, QRect, QPoint
from hamcrest.core.base_matcher import BaseMatcher


class TableMatcher(BaseMatcher):
    def __init__(self, wrapped_matcher):
        self._matcher = wrapped_matcher

    def _matches(self, widget):
        return self._matcher.matches(Table(widget))

    def describe_to(self, description):
        self._matcher.describe_to(description)

    def describe_mismatch(self, widget, mismatch_description):
        self._matcher.describe_mismatch(Table(widget), mismatch_description)


class TableManipulation:
    def __init__(self, wrapped_manipulation):
        self._manipulation = wrapped_manipulation

    def __call__(self, widget):
        return self._manipulation(Table(widget))


class Table:
    def __init__(self, widget):
        self._table = widget

    def _logical_col(self, visual_col):
        return self._table.horizontalHeader().logicalIndex(visual_col)

    def _logical_row(self, visual_row):
        return self._table.verticalHeader().logicalIndex(visual_row)

    def visual_row(self, logical_row):
        return self._table.verticalHeader().visualIndex(logical_row)

    def cell_text(self, row, col):
        return self._table.model().data(self.index(row, col), Qt.DisplayRole)

    def cells(self, row):
        return [self.cell_text(row, column) for column in range(self.column_count())]

    def all_cells(self):
        return [self.cells(row) for row in range(self.row_count())]

    def header_text(self, col):
        return self._table.model().headerData(self._logical_col(col), Qt.Horizontal, Qt.DisplayRole)

    def headers(self):
        return [self.header_text(column) for column in range(self.column_count())]

    def column_count(self):
        return self._table.model().columnCount()

    def row_count(self):
        return self._table.model().rowCount()

    def widget_at(self, row, col):
        return self._table.indexWidget(self.index(row, col))

    def index(self, row, col):
        return self._table.model().index(self._logical_row(row), self._logical_col(col))

    def cell_bounds(self, row, col):
        bounds = self._table.visualRect(self.index(row, col)).translated(self._table.verticalHeader().width(),
                                                                         self._table.horizontalHeader().height())
        return self._absolute(bounds)

    def cell_center(self, row, col):
        return self.cell_bounds(row, col).center()

    def vertical_header_bounds(self, row):
        x = 0
        y = self._table.horizontalHeader().height() + self._table.rowViewportPosition(self._logical_row(row))
        width = self._table.verticalHeader().width()
        height = self._table.rowHeight(self._logical_row(row))
        return self._absolute(QRect(x, y, width, height))

    def _absolute(self, rect):
        return rect.translated(self._table.mapToGlobal(QPoint(0, 0)))

    def scroll_to(self, row, col):
        self._table.scrollTo(self.index(row, col))

    def selected_row(self):
        return self.visual_row(self._table.currentIndex().row())
