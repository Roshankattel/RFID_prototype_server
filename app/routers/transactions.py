from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix="/transactions",
    tags=['Transactions']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.TransactionResponse)
def create_transaction (transaction :schemas.TransactionCreate,db: Session = Depends(get_db),
                 current_merchant: int = Depends(oauth2.get_current_merchant)):
  
    user_query = db.query(models.User).filter(models.User.tag_data==transaction.tag_data)
    user = user_query.first()
    if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with given tag_id not found")

    if not transaction.recharge_request: 
        if (user.amount < transaction.amount):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Not enough balance with user")
        user.amount = user.amount-transaction.amount
    else :
        user.amount = user.amount+transaction.amount

    #update amount of merchant 
    merchant_query = db.query(models.Merchant).filter(models.Merchant.id==current_merchant.id)
    merchant = merchant_query.first()
    if transaction.recharge_request:  
        if  merchant.amount < transaction.amount:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f"Not enough balance with Merchant")
        merchant.amount = merchant.amount - transaction.amount
    else:
        merchant.amount = merchant.amount + transaction.amount
    new_transaction = models.Transaction(merchant_id= current_merchant.id, user_id = user.id, amount = transaction.amount, recharge_request=transaction.recharge_request)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return(new_transaction)