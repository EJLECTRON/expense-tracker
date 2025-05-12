from sqlalchemy import (
    Integer, String, DateTime, ForeignKey,
    func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,   relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'CATEGORIES'

    id: Mapped[int] = mapped_column("ID", Integer, primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column("NAME", String(50), nullable=False, unique=True, default='MISCELLANEOUS')

    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="category_obj",
        cascade="all, delete",
        passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"<Category(name='{self.name}')>"


class Expense(Base):
    __tablename__ = 'EXPENSES'

    id: Mapped[int] = mapped_column("ID", Integer, primary_key=True, autoincrement=True, unique=True)
    title: Mapped[str] = mapped_column("TITLE", String(20), nullable=False)
    amount: Mapped[int] = mapped_column("AMOUNT", Integer, nullable=False)
    time_of_transaction: Mapped[DateTime] = mapped_column("TIME_OF_TRANSACTION", DateTime, nullable=False, default=func.now())
    category: Mapped[str] = mapped_column("CATEGORY", String(50), ForeignKey("CATEGORIES.NAME", onupdate="CASCADE", ondelete="SET DEFAULT"), nullable=False)
    description: Mapped[str | None] = mapped_column("DESCRIPTION", String(511))

    category_obj: Mapped["Category"] = relationship(back_populates="expenses")

    def __repr__(self) -> str:
        return f"<Expense(title='{self.title}', amount={self.amount}, category='{self.category}')>"

__all__ = ['Base', 'Category', 'Expense']
