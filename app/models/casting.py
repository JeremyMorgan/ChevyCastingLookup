from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Casting(Base):
    """SQLAlchemy model for Chevrolet casting data."""
    
    __tablename__ = "castings"

    id = Column(Integer, primary_key=True, index=True)
    years = Column(String, index=True, nullable=True)  # e.g., "1980-85"
    casting = Column(String, unique=True, index=True, nullable=False)  # Casting number
    cid = Column(Integer, nullable=True)  # Cubic Inch Displacement
    low_power = Column(String, nullable=True)  # Some values are "-"
    high_power = Column(String, nullable=True)  # Some values are "-"
    main_caps = Column(String, nullable=True)  # Some values are "-"
    comments = Column(String, nullable=True)
