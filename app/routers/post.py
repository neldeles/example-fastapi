from typing import List

import fastapi
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str | None = "",
):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """insert into posts (title, content, published) values (%s, %s, %s) returning *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    # sourcery skip: reintroduce-else, swap-if-else-branches, use-named-expression
    # cursor.execute("""select * from posts where id = %s""", (str(id),))
    # if post := cursor.fetchone():
    #     return {"post_detail": post}
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    # cursor.execute("""delete from posts where id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post is None:
    #     raise fastapi.HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id: {id} does not exist",
    #     )
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_result = post_query.first()

    if post_result is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    if post_result.owner_id != current_user.id:
        raise fastapi.HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """update posts set title = %s, content = %s, published = %s where id = %s returning *""",
    #     (
    #         post.title,
    #         post.content,
    #         post.published,
    #         str(id),
    #     ),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post is None:
    #     raise fastapi.HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id: {id} does not exist",
    #     )
    # return {"data": updated_post}
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_result = post_query.first()

    if post_result is None:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    print(post_result.owner_id, current_user.id)
    if post_result.owner_id != current_user.id:
        raise fastapi.HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
