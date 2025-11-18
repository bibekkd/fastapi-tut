from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema, models, token
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # allow login by username or email
    user = db.query(models.User).filter(
        models.User.email == request.username).first()

    if not user:
        # user not found
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # verify password
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    

@router.post("/signup")
def signup():
    return {"message": "Signup endpoint"}