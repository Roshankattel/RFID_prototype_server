from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils

router = APIRouter(
    prefix="/merchants",
    tags=['Merchants']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MerchantResponse)
def create_user(merchant: schemas.MerchantCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    merchant.password = utils.hash(merchant.password)
    new_merchant = models.Merchant(**merchant.dict())
    db.add(new_merchant)
    db.commit()
    db.refresh(new_merchant)
    return new_merchant

@router.get("/{id}", response_model=schemas.MerchantResponse)
def get_merchant(id: int, db: Session = Depends(get_db)):
    merchant = db.query(models.Merchant).filter(models.Merchant.id == id).first()
    if not merchant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Merchant with id:{id} was not found")
    return merchant

@router.put("/{id}",response_model=schemas.MerchantResponse)
def update_merchant(id: int, updated_merchant: schemas.MerchantCreate, db: Session = Depends(get_db)):
    merchant_query  = db.query(models.Merchant).filter(models.Merchant.id == id)
    merchant = merchant_query.first()
    if merchant == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Merchant with id:{id} does not exit")
    merchant_query.update(updated_merchant.dict(),synchronize_session=False)
    db.commit()
    return merchant_query.first()