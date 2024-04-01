from .. import schemas, models, utils
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        user_exist = db.query(models.User).filter(models.User.email == new_user.email).one()
    except:
        user_exist = None

    if user_exist != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exsit!")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id: {id} does not exist!")
    
    
    
    return user
