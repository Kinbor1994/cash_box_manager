from imports import QChart, QChartView, QPainter, QColor, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis, QPieSeries, QWidget, QVBoxLayout, Qt
from sqlalchemy.engine.row import Row

from utils.utils import get_month_name

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

    def __init__(self, data, category_attr=None, value_attr=None, title="Title", xlabel="X Axis", ylabel="Y Axis", parent=None):
        """Initialize the BarChartWidget with the provided data and labels."""
        super().__init__(parent)
        self.data = data
        self.category_attr = category_attr
        self.value_attr = value_attr
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface for the bar chart widget."""
        self.bar_set = QBarSet(self.ylabel)
        self.series = QBarSeries()
        
        self.process_data()
        self.series.append(self.bar_set)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(self.title)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeLight)

        self.categories = self.extract_categories()
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)
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

    def process_data(self):
        """Process the data and populate the bar set with values."""
        self.series.clear()
        for item in self.data:
            if isinstance(item, Row) and len(item) == 2:
                # Data in tuple format, e.g., (category, value)
                _, value = item
                self.bar_set.append(value)
            elif isinstance(item, dict):
                # Data in dictionary format, e.g., {'category': 'Food', 'value': 100}
                value = item.get(self.value_attr, 0)
                self.bar_set.append(value)
            else:
                # Default case for list of objects with attributes
                self.bar_set.append(getattr(item, self.value_attr))

    def extract_categories(self):
        """Extract categories (x-axis labels) from the data."""
        categories = []
        for item in self.data:
            if isinstance(item, Row) and len(item) == 2:
                # Data in tuple format
                category, _ = item
                categories.append(str(category))
            elif isinstance(item, dict):
                # Data in dictionary format
                category = item.get(self.category_attr, 'Unknown')
                categories.append(str(category))
            else:
                # Default case for list of objects with attributes
                categories.append(str(getattr(item, self.category_attr)))
        return categories

    def update_chart(self, new_data):
        """Update the chart with new data and refresh the display.

        Args:
            new_data (list): The new data to be used for the chart.
        """
        self.data = new_data
        self.process_data()
        self.categories = self.extract_categories()
        self.axis_x.clear()
        self.axis_x.append(self.categories)
        self.chart_view.repaint()

class BarChartWidget2(QWidget):
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
        
class BarChartWidgetWithTwoDataSets(QWidget):
    """A custom widget for displaying bar charts with two data sets for income and expenses.

    This widget visualizes data as a bar chart, allowing customization of the chart's
    title and axis labels.

    Args:
        income_data (list): The income data to be displayed in the chart.
        expense_data (list): The expense data to be displayed in the chart.
        title (str, optional): The title of the chart. Defaults to "Title".
        xlabel (str, optional): The label for the x-axis. Defaults to "X Axis".
        ylabel (str, optional): The label for the y-axis. Defaults to "Y Axis".
        parent (QWidget, optional): The parent widget of this widget. Defaults to None.
    """

    def __init__(self, income_data, expense_data, title="Monthly Income vs Expenses", xlabel="Month", ylabel="Amount", parent=None):
        """Initialize the BarChartWidget with the provided data and labels."""
        super().__init__(parent)
        self.income_data = income_data
        self.expense_data = expense_data
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface for the bar chart widget."""
        # Create the bar sets for income and expenses
        self.income_bar_set = QBarSet("Income")
        self.expense_bar_set = QBarSet("Expense")

        self.series = QBarSeries()
        self.process_data()
        self.series.append(self.income_bar_set)
        self.series.append(self.expense_bar_set)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle(self.title)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeLight)

        self.categories = self.extract_categories()
        self.axis_x = QBarCategoryAxis()
        self.axis_x.append(self.categories)
        self.axis_x.setTitleText(self.xlabel)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(self.ylabel)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        # Set colors for the bar sets
        self.income_bar_set.setColor(QColor("#4CAF50"))  # Green for income
        self.income_bar_set.setBorderColor(QColor("#388E3C"))
        self.expense_bar_set.setColor(QColor("#F44336"))  # Red for expense
        self.expense_bar_set.setBorderColor(QColor("#D32F2F"))

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def process_data(self):
        """Process the income and expense data and populate the bar sets with values."""
        self.income_bar_set.remove(0, self.income_bar_set.count())
        self.expense_bar_set.remove(0, self.expense_bar_set.count())
        
        # Ensure that the data is aligned by month
        months = set(item.month for item in self.income_data).union(item.month for item in self.expense_data)
        sorted_months = sorted(months)

        income_dict = {item.month: item.total_income for item in self.income_data}
        expense_dict = {item.month: item.total_expense for item in self.expense_data}

        for month in sorted_months:
            self.income_bar_set.append(income_dict.get(month, 0))
            self.expense_bar_set.append(expense_dict.get(month, 0))

    def extract_categories(self):
        """Extract categories (x-axis labels) from the data."""
        months = set(item.month for item in self.income_data).union(item.month for item in self.expense_data)
        sorted_months = sorted(months)
        return [f"{get_month_name(int(month))}" for month in sorted_months]

    def update_chart(self, new_income_data, new_expense_data):
        """Update the chart with new data and refresh the display.

        Args:
            new_income_data (list): The new income data to be used for the chart.
            new_expense_data (list): The new expense data to be used for the chart.
        """
        self.income_data = new_income_data
        self.expense_data = new_expense_data
        self.process_data()
        self.categories = self.extract_categories()
        self.axis_x.clear()
        self.axis_x.append(self.categories)
        self.chart_view.repaint()


class PieChartWidget(QWidget):
    """A custom widget for displaying pie charts with support for various data formats.

    This widget visualizes data as a pie chart, allowing customization of the chart's title.
    It can handle data as a list of objects, tuples, or dictionaries.

    Args:
        data (list): The data to be displayed in the chart.
        title (str, optional): The title of the chart. Defaults to "My Title".
        category_attr (str, optional): The attribute or key for categories. Defaults to "category".
        value_attr (str, optional): The attribute or key for values. Defaults to 'value'.
        parent (QWidget, optional): The parent widget of this widget. Defaults to None.
    """

    def __init__(self, data, title="My Title", category_attr=None, value_attr=None, parent=None):
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
        self.process_data()

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

    def process_data(self):
        """Process the data and add it to the pie chart series."""
        self.series.clear()
        for item in self.data:
            if isinstance(item, Row) and len(item) == 2:
                # If the data is in tuple format, e.g., (category, value)
                category, value = item
                self.series.append(str(category), value)
            elif isinstance(item, dict):
                # If the data is in dictionary format, e.g., {'category': 'Food', 'value': 100}
                category = item.get(self.category_attr, 'Unknown')
                value = item.get(self.value_attr, 0)
                self.series.append(str(category), value)
            else:
                # Default case for list of objects with attributes
                self.series.append(str(getattr(item, self.category_attr)), getattr(item, self.value_attr))

    def update_chart(self, new_data):
        """Update the pie chart with new data and refresh the display.

        Args:
            new_data (list): The new data to be used for the chart.
        """
        self.data = new_data
        self.process_data()
        self.chart_view.repaint()

class PieChartWidget2(QWidget):
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
