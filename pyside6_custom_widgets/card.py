from imports import QWidget, QVBoxLayout, QColor, QHBoxLayout, QGraphicsDropShadowEffect
import qtawesome as qta
from .label import Label
from utils.qss_file_loader import load_stylesheet


class DashboardCardWidget(QWidget):
    """
    Custom widget for displaying dashboard card information with an icon, title, and content.

    Args:
        title (str): The title text of the card.
        content (str): The main content of the card.
        icon_name (str, optional): The name of the QtAwesome icon. Defaults to 'fa5s.info-circle'.
    """

    def __init__(
        self, icon_name, title="", content="", theme_name="primary", icon_color="white", parent=None
    ):
        super().__init__(parent)
        self.setMinimumSize(250, 145)
        self.setMaximumSize(350, 145)
        style = load_stylesheet("styles/dashboard_card_widget.qss")
        self.setStyleSheet(style)
        self.add_shadow()
        # Create layout
        m_layout = QVBoxLayout()
        m_layout.setContentsMargins(5, 5, 5, 5)
        m_layout.setSpacing(0)
        title_layout = QHBoxLayout()
        # Create icon using QtAwesome
        icon_label = Label(
            text="", icon_name=icon_name, theme_name=theme_name, icon_color=icon_color
        )
        icon_label.setFixedSize(45, 45)

        # Create title and content layout
        title_label = Label(text=title, theme_name=theme_name)
        title_label.setFixedHeight(45)
        self.content_label = Label(text=content, theme_name=theme_name)
        self.content_label.setFixedHeight(50)
        detail_label = Label(text="....")

        title_label.set_property("class", "card_title")
        self.content_label.set_property("class", "card_content")

        # Add title and content to the layout
        title_layout.addWidget(title_label)
        title_layout.addWidget(icon_label)
        m_layout.addLayout(title_layout)
        m_layout.addWidget(self.content_label)
        m_layout.addWidget(detail_label)

        # Set the layout for the widget
        self.setLayout(m_layout)

    def add_shadow(self):
        """
        Adds a drop shadow effect to the widget using QGraphicsDropShadowEffect.
        """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)  # Adjust the blur to create a soft shadow
        shadow.setXOffset(3)  # Horizontal offset for the shadow
        shadow.setYOffset(3)  # Vertical offset for the shadow
        shadow.setColor(QColor(0, 0, 0, 80))  # A darker shadow with more transparency

        self.setGraphicsEffect(shadow)
    
    def set_content(self, content):
        """
        Met à jour le contenu du widget avec la nouvelle valeur.

        Args:
            content (str): Le nouveau contenu à afficher dans le widget.
        """
        self.content_label.set_text(content)


if __name__ == "__main__":
    import sys
    from imports import QApplication

    app = QApplication([])
    win = DashboardCardWidget(
        icon_name="fa.users",
        title="Bonjour",
        content="50 000 F CFA",
        theme_name="dark",
        icon_color="blue",
    )
    win.show()
    sys.exit(app.exec())
