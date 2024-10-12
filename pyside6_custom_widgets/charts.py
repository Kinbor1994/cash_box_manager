from imports import QChart, QChartView, QPainter, QColor, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis, QPieSeries, QWidget, QVBoxLayout, Qt

class BarChartWidget(QWidget):
    """A custom widget for displaying bar charts.

    This widget visualizes data as a bar chart, allowing customization of the chart's
    title and axis labels.

    Args:
        data (list): The data to be displayed in the chart.
        title (str, optional): The title of the chart. Defaults to "Title".
        xlabel (str, optional): The label for the x-axis. Defaults to "X Axis".
        ylabel (str, optional): The label for the y-axis. Defaults to "Y Axis".
        parent (QWidget, optional): The parent widget of this widget. Defaults to None.
    """

    def __init__(self, data,  category_attr="category", value_attr='value', title="Title", xlabel="X Axis", ylabel="Y Axis", parent=None):
        """Initialize the BarChartWidget with the provided data and labels."""
        super().__init__(parent)
        self.data = data
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

        self.setup_ui(category_attr=category_attr, value_attr=value_attr)
    
    def setup_ui(self, category_attr="category", value_attr='value'):
        """Set up the user interface for the bar chart widget."""
        self.bar_set = QBarSet(self.ylabel)
        for elm in self.data:
            self.bar_set.append(getattr(elm, value_attr))

        self.series = QBarSeries()
        self.series.append(self.bar_set)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(self.title)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeLight)

        categories = [f"{getattr(elm, category_attr)}" for elm in self.data]
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(categories)
        self.axis_x.setTitleText(self.xlabel)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(self.ylabel)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.bar_set.setColor(QColor("#4CAF50"))
        self.bar_set.setBorderColor(QColor("#388E3C"))

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)
        
    def update_bar_set_data(self, value_attr='value'):
        """Update the data in the bar set with the current data."""
        self.series.clear()

        new_bar_set = QBarSet(self.ylabel)
        for elm in self.data:
            new_bar_set.append(getattr(elm, value_attr))

        self.series.append(new_bar_set)
        new_bar_set.setColor(QColor("#4CAF50"))
        new_bar_set.setBorderColor(QColor("#388E3C"))
        
    def update_categories(self, category_attr='category'):
        """Update the categories (x-axis labels) based on the current data."""
        self.categories = [f"{getattr(elm, category_attr)}" for elm in self.data]
        self.axis_x.clear()
        self.axis_x.append(self.categories)
        
    def update_chart(self, new_data):
        """Update the chart with new data and refresh the display.

        Args:
            new_data (list): The new data to be used for the chart.
        """
        self.data = new_data
        self.update_bar_set_data()
        self.update_categories()
        self.chart_view.repaint()
        
class PieChartWidget(QWidget):
    """A custom widget for displaying pie charts.

    This widget visualizes data as a pie chart, allowing customization of the chart's title.

    Args:
        data (list): The data to be displayed in the chart.
        title (str, optional): The title of the chart. Defaults to "My Title".
        parent (QWidget, optional): The parent widget of this widget. Defaults to None.
    """

    def __init__(self, data, title="My Title",  category_attr="category", value_attr='value', parent=None):
        """Initialize the PieChartWidget with the provided data and title."""
        super().__init__(parent)
        self.data = data
        self.title = title
        self.category_attr = category_attr
        self.value_attr = value_attr
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface for the pie chart widget."""
        self.series = QPieSeries()
        for instance in self.data:
            self.series.append(str(getattr(instance, self.category_attr)), getattr(instance, self.value_attr))

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle(self.title)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        for slice in self.series.slices():
            slice.setLabelVisible(True)

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def update_pie_chart_data(self):
        """Update the data in the pie chart with the current data."""
        self.series.clear()

        for instance in self.data:
            self.series.append(str(getattr(instance, self.category_attr)), getattr(instance, self.value_attr))

    def update_slices(self):
        """Update the slices in the pie chart to make labels visible."""
        for slice in self.series.slices():
            slice.setLabelVisible(True)

    def update_chart(self, new_data):
        """Update the pie chart with new data and refresh the display.

        Args:
            new_data (list): The new data to be used for the chart.
        """
        self.data = new_data
        self.update_pie_chart_data()
        self.update_slices()
        self.chart_view.repaint()
