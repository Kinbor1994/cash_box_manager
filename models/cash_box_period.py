from sqlalchemy import Column, Date, Enum, Float, func

from models.base_model import BaseModel


class CashBoxPeriod(BaseModel):
    __tablename__ = "cash_box_period"
    __verbose_name__ = "Exercice"
    
    start_date = Column(
        Date,
        default=func.now(),
        nullable=False,
        info={
            "verbose_name": "Date début",
            "tab_col_index": 2,
        },
    )
    end_date = Column(
        Date,
        nullable=True,
        info={
            "verbose_name": "Date de cloture",
            "tab_col_index": 3,
        },
    )
    initial_amount = Column(
        Float,
        nullable=False,
        info={
            "verbose_name": "Solde Initial",
            "column_type": "numeric",
            "tab_col_index": 4,
        },
    )
    ending_balance = Column(
        Float,
        nullable=True,
        info={
            "verbose_name": "Solde Final",
            "column_type": "numeric",
            "tab_col_index": 5,
        },
    )
    is_open = Column(
        Enum("Ouvert", "Fermé", name="status_enum"),
        nullable=False,
        info={
            "verbose_name": "Statut",
            "column_type": "enum",
            "tab_col_index": 6,
        },
    )

    def __str__(self):
        return f"(id={self.id}, start_date={self.start_date}, end_date={self.end_date}, initial_amount={self.initial_amount}, ending_balance={self.ending_balance}, is_open={self.is_open.title})"

    def __repr__(self):
        return f"<CashBoxPeriod(id={self.id}, start_date={self.start_date}, end_date={self.end_date}, initial_amount={self.initial_amount}, ending_balance={self.ending_balance}, is_open={self.is_open.title})>"
