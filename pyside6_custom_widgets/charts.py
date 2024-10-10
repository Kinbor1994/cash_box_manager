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
        
#TODO Revoir cette partie
class PieChartWidget(QWidget):
    """
    A customizable and reusable pie chart widget using PySide6's QChart.

    Attributes:
        chart (QChart): The chart object that holds the pie series and displays the data.
        chart_view (QChartView): The view that renders the chart.
        series (QPieSeries): The pie series that represents the data.
    """

    def __init__(self, parent=None):
        """
        Initializes the PieChartWidget.

        Args:
            parent (QWidget, optional): The parent widget of this pie chart widget. Defaults to None.
        """
        super().__init__(parent)
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.series = QPieSeries()
        
        self.chart.addSeries(self.series)
        self.chart.setTitle("Pie Chart")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def update_data(self, data_dict):
        """
        Updates the pie chart with new data.

        Args:
            data_dict (dict): A dictionary with category labels as keys and numerical values as values.
        """
        self.series.clear()
        for category, value in data_dict.items():
            self.series.append(category, value)

        self.chart.setTitle("Pie Chart Updated")

if __name__ == "__main__":
    import sys
    from imports import QApplication
    app = QApplication([])
    win = QWidget()
    layout = QVBoxLayout()
    # Example data for BarChartWidget
    bar_chart_widget = BarChartWidget()
    data = {"Category 1": 10, "Category 2": 15, "Category 3": 8}
    bar_chart_widget.update_data(data)
    layout.addWidget(bar_chart_widget)
    # Example data for PieChartWidget
    pie_chart_widget = PieChartWidget()
    data = {"Apples": 30, "Oranges": 40, "Bananas": 20}
    pie_chart_widget.update_data(data)
    layout.addWidget(pie_chart_widget)
    win.setLayout(layout)
    win.show()
    sys.exit(app.exec())