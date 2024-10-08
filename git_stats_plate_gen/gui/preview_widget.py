import datetime
from typing import Optional, Tuple

from PySide6.QtCharts import QBarCategoryAxis, QChart, QHorizontalBarSeries, QBarSet
from PySide6.QtWidgets import QWidget

from git_stats_plate_gen.gui.ui.ui_preview_widget import Ui_Form


class PreviewWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._set = QBarSet("Language Statistics, LOC (Lines of Code)")

        self._series = QHorizontalBarSeries()
        self._series.setLabelsVisible(True)
        self._series.append(self._set)

        self._chart = QChart()
        self._set_chart_title()
        self._chart.addSeries(self._series)
        self._axis = QBarCategoryAxis()
        self._chart.createDefaultAxes()
        self._chart.axisX().setLabelFormat('%d')
        self._chart.setAxisY(self._axis, self._series)

        self.ui.chart_view.setChart(self._chart)

    def _set_chart_title(self, generated_at_utc: datetime.datetime = None):
        link = 'https://github.com/DiPaolo/git-stats-plate-gen'

        generated_at_utc_str = ''
        if generated_at_utc is not None:
            date_str = f'{generated_at_utc.year:04}-{generated_at_utc.month:02}-{generated_at_utc.day:02}'
            generated_at_utc_str = f' at {date_str}'

        self._chart.setTitle(f"Generated by git-stats-plate-gen (<a href='{link}'>{link}</a>){generated_at_utc_str}")

    def set_data(self, datetime_utc: datetime.datetime, lang_stats, min_percent: float = 1.0):
        if lang_stats is None:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_no_data)
            return

        stats_dict = dict(lang_stats.items())
        stats = {key: value['lines'] for (key, value) in stats_dict.items() if 'lines' in value}

        if stats is None:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_no_data)
            return

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_chart)

        stats = dict(sorted(stats.items(), key=lambda x: x[1]))
        total_loc = sum(stats.values())

        for _ in range(0, self._set.count()):
            self._set.remove(0)

        categories = []
        for lang, loc in stats.items():
            percent = loc * 100 / total_loc
            if percent < min_percent:
                continue

            self._set.append(loc)
            categories.append(f'{lang} ({round(loc * 100 / total_loc)}%)')

        self._axis.clear()
        self._axis.append(categories)

        right_border = max(stats.values())

        def get_round_values(val: int) -> int:
            """
            Calculates the values used for graph setup: the right border with some extra space on
            the right side

            E.g.:
              for input 8773 it will return 8800
              for input 30871 the function will return 31000
            :param val:
            :return:
            """

            # decimal_order, round_to_decimal_order, upper_decimal_order
            #
            # special case for *:
            #  e.g.,
            #  86 is rounded to 10's (86 -> 90)
            #  132 is also rounded to 10's, not 100's (132 -> 140)
            #  but 1032 will be rounded to 100's (1032 -> 1100)
            orders = [
                (1, 1, 10),
                (10, 10, 100),
                (100, 10, 1000),  # (*)
                (1000, 100, 10000),
                (10000, 10000, 100000),
                (100000, 10000, 1000000),
                (1000000, 100000, 10000000),
                (10000000, 1000000, 100000000),
                (100000000, 10000000, 100000000),
            ]

            for cur_order in orders:
                round_to_decimal_order = cur_order[1]
                upper_decimal_order = cur_order[2]
                if val < upper_decimal_order:
                    rounded_to_upper = int(
                        (val + round_to_decimal_order) / round_to_decimal_order) * round_to_decimal_order
                    return rounded_to_upper

            # smth. went wrong (val is unexpectedly large); return as is
            return round(val)

        right_border_new = get_round_values(right_border)

        self._set_chart_title(datetime_utc)
        self._chart.axisX().setRange(0, right_border_new)
        self._chart.axisX().setTickCount(5)

    def save_image(self, file_path: str, size: Optional[Tuple[int, int]] = None) -> bool:
        if size:
            return self.ui.chart_view.grab().scaled(size[0], size[1]).save(file_path)
        else:
            return self.ui.chart_view.grab().save(file_path)
