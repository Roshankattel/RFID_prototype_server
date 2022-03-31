from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import schemas, models, utils, oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.TokenResponse)
def login(merchant_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    merchat = db.query(models.Merchant).filter(
        models.Merchant.email == merchant_credentials.username).first()

    if not merchat:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(merchant_credentials.password, merchat.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create a token
    access_token = oauth2.create_access_token(data={"merchant_id": merchat.id})
    # retutn token
    return {"access_token": access_token, "token_type": "bearer"}