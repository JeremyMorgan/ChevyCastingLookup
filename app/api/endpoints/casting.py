from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.casting import Casting as CastingModel
from app.schemas.casting import Casting, CastingCreate, CastingUpdate

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


@router.post("/", response_model=Casting)
def create_casting(
    casting: CastingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new casting.
    """
    # Check if casting with the same number already exists
    db_casting = db.query(CastingModel).filter(
        CastingModel.casting == casting.casting
    ).first()
    
    if db_casting:
        raise HTTPException(
            status_code=400,
            detail=f"Casting with number {casting.casting} already exists"
        )
    
    # Create new casting
    db_casting = CastingModel(**casting.dict())
    db.add(db_casting)
    db.commit()
    db.refresh(db_casting)
    
    return db_casting


@router.put("/{casting_id}", response_model=Casting)
def update_casting(
    casting_id: str,
    casting: CastingUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing casting.
    """
    db_casting = db.query(CastingModel).filter(
        CastingModel.casting == casting_id
    ).first()
    
    if db_casting is None:
        raise HTTPException(
            status_code=404,
            detail=f"Casting with number {casting_id} not found"
        )
    
    # Update casting attributes
    update_data = casting.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_casting, key, value)
    
    db.commit()
    db.refresh(db_casting)
    
    return db_casting


@router.delete("/{casting_id}", response_model=Casting)
def delete_casting(
    casting_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a casting.
    """
    db_casting = db.query(CastingModel).filter(
        CastingModel.casting == casting_id
    ).first()
    
    if db_casting is None:
        raise HTTPException(
            status_code=404,
            detail=f"Casting with number {casting_id} not found"
        )
    
    db.delete(db_casting)
    db.commit()
    
    return db_casting


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
