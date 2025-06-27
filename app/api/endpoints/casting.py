from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.casting import Casting as CastingModel
from app.schemas.casting import Casting

router = APIRouter()


@router.get("/", response_model=List[Casting])
def get_castings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of castings with pagination.
    """
    castings = db.query(CastingModel).offset(skip).limit(limit).all()
    return castings


@router.get("/{casting_id}", response_model=Casting)
def get_casting_by_id(
    casting_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific casting by its casting number.
    """
    casting = db.query(CastingModel).filter(
        CastingModel.casting == casting_id
    ).first()
    
    if casting is None:
        raise HTTPException(
            status_code=404,
            detail=f"Casting with number {casting_id} not found"
        )
    
    return casting



@router.get("/search/", response_model=List[Casting])
def search_castings(
    years: Optional[str] = None,
    cid: Optional[int] = None,
    main_caps: Optional[str] = None,
    comments: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Search for castings based on various criteria.
    """
    query = db.query(CastingModel)
    
    if years:
        query = query.filter(CastingModel.years.ilike(f"%{years}%"))
    
    if cid:
        query = query.filter(CastingModel.cid == cid)
    
    if main_caps:
        query = query.filter(CastingModel.main_caps.ilike(f"%{main_caps}%"))
    
    if comments:
        query = query.filter(CastingModel.comments.ilike(f"%{comments}%"))
    
    castings = query.offset(skip).limit(limit).all()
    
    return castings
