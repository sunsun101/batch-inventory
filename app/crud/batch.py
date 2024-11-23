"""
crud.py

Logic for crud apis
"""
import uuid
from typing import Optional, List
from fastapi import Depends, Query
from sqlmodel import Session, select
from app.database import get_session
from app.models import Batch
from app.schemas import BatchCreate, BatchUpdate
from app.models import Product


def create_batch(db: Session, batch_data: BatchCreate) -> Batch:
    """
    Add a new batch

    Args:
        db (Session): session library
        batch_data (BatchCreate): data required to create a batch

    Returns:
        BatchResponse: Newly created batch with a unique batch number
    """

    product = db.exec(select(Product).filter(
        Product.name == batch_data.product)).first()

    if not product:
        product = Product(
            name=batch_data.product,
            price=batch_data.purchase_price
        )
        db.add(product)
        db.commit()
        db.refresh(product)

    batch_number = str(uuid.uuid4())
    batch_data_dict = batch_data.model_dump(
        exclude_unset=True, exclude={"product", "purchase_price"})
    batch = Batch(batch_number=batch_number, **
                  batch_data_dict, product_id=product.id)
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def fetch_batches(
    product: Optional[str] = None,
    warehouse: Optional[str] = None,
    min_quantity: Optional[int] = Query(None, ge=0),
    max_quantity: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_session)
) -> List[Batch]:
    """
    Fetch all batches from the database with optional filters.

    Args:
        db (Session): The database session.
        product (Optional[str]): Product name filter.
        warehouse (Optional[str]): Warehouse name filter.
        min_quantity (Optional[int]): Minimum quantity filter.
        max_quantity (Optional[int]): Maximum quantity filter.

    Returns:
        List[BatchResponse]: A list of batches matching the filters.
    """
    query = select(Batch).join(Product, Batch.product_id == Product.id)

    if product:
        query = query.where(Product.name == product)
    if warehouse:
        query = query.where(Batch.warehouse == warehouse)
    if min_quantity is not None:
        query = query.where(Batch.quantity >= min_quantity)
    if max_quantity is not None:
        query = query.where(Batch.quantity <= max_quantity)

    result = db.exec(query)
    return result.all()


def update_batch_quantity(db: Session, batch_data: BatchUpdate) -> Batch:
    """
    Update the batch quantity.

    Args:
        db (Session): The database session.
        batch_data (BatchUpdate): The data to update, including batch number and new quantity.

    Returns:
        Batch: The updated batch object with new quantity.
    """
    batch = db.exec(select(Batch).filter(
        Batch.batch_number == batch_data.batch_number)).first()

    if batch:
        batch.quantity = batch_data.quantity
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch
    else:
        return None
