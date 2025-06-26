from typing import Optional

from pydantic import BaseModel, Field


class CastingBase(BaseModel):
    """Base schema for Chevrolet casting data."""
    
    casting: str = Field(..., description="Unique casting number")
    years: Optional[str] = Field(None, description="Production years range (e.g., '1980-85')")
    cid: Optional[int] = Field(None, description="Cubic Inch Displacement")
    low_power: Optional[str] = Field(None, description="Low power rating")
    high_power: Optional[str] = Field(None, description="High power rating")
    main_caps: Optional[str] = Field(None, description="Number of main caps")
    comments: Optional[str] = Field(None, description="Additional comments or notes")


class CastingCreate(CastingBase):
    """Schema for creating a new casting."""
    pass


class CastingUpdate(BaseModel):
    """Schema for updating an existing casting."""
    
    years: Optional[str] = None
    cid: Optional[int] = None
    low_power: Optional[str] = None
    high_power: Optional[str] = None
    main_caps: Optional[str] = None
    comments: Optional[str] = None


class CastingInDB(CastingBase):
    """Schema for casting data in the database."""
    
    id: int

    class Config:
        orm_mode = True


class Casting(CastingInDB):
    """Schema for casting data returned by the API."""
    pass
