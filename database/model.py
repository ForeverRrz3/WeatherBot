from sqlalchemy import String,Float,Text,DateTime,func,Boolean
from sqlalchemy.orm import Mapped,DeclarativeBase,mapped_column

class Base(DeclarativeBase):

    create: Mapped[DateTime] = mapped_column(DateTime,default=func.now())

class Base_town(Base):
    __tablename__ = "town"

    id: Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    region: Mapped[str] = mapped_column(String(100),nullable=False)

