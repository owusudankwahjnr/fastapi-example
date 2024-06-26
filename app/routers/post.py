from .. import schemas, models
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import  get_db
from .. import oauth2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int= 0, search: Optional[str]=''):
    # cursor.execute("""SELECT * FROM posts """)
    # posts =  cursor.fetchall()
    # if you want to a user to get only his posts
    # post = db.query(models.Post).filter(current_user.id == models.Post.owner_id ).all()

    # post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).first()

    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip)

    post = db.execute(post_query).mappings().all()
    

    return post
    


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # line below is the same as line above but line below is dynamic, which means will not need to always add parameters when you udate post class model or databse in models.py
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=List[schemas.PostOut])
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = find_post(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    post = db.execute(post_query).mappings().all()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")


    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
