"""
batch.py

APIs for batches
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.schemas import BatchCreate, BatchResponse, BatchUpdate
from app.crud import create_batch, fetch_batches, update_batch_quantity


router = APIRouter()


@router.post("/batch/", response_model=BatchResponse)
def add_batch(batch: BatchCreate, db: Session = Depends(get_session)):
    """
    API to add a new batch
    """
    return create_batch(db, batch)


@router.get("/batches", response_model=List[BatchResponse])
def get_batches(
    product: Optional[str] = None,
    warehouse: Optional[str] = None,
    min_quantity: Optional[int] = Query(None, ge=0),
    max_quantity: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_session)
):
    """
    API to fetch all batches with optional filters.
    """
    return fetch_batches(product, warehouse, min_quantity, max_quantity, db)


@router.put("/batch/update", response_model=BatchResponse)
def update_batch_quantity_endpoint(
    batch_data: BatchUpdate,
    db: Session = Depends(get_session)
):
    """
    API to update the quantity of a batch based on the batch number.

    Args:
        batch_data (BatchUpdate): The request body containing the batch number and new quantity.
        db (Session): The database session.

    Returns:
        BatchResponse: The updated batch details with the new quantity.
    """
    updated_batch = update_batch_quantity(db, batch_data)

    if updated_batch:
        return updated_batch
    else:
        raise HTTPException(status_code=404, detail="Batch not found")
