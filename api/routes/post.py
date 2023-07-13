from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.exc import IntegrityError
from starlette import status

from api.dependencies.users import validate_user
from config import PAGINATION_DEFAULT_LIMIT, PAGINATION_MIN_LIMIT, PAGINATION_MAX_LIMIT
from schemas.post import PostSchema, PostCreateSchema, PostUpdateSchema
from services.post import PostService

router = APIRouter(tags=["Posts"])


# CREATE POST
@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreateSchema, user_id=Depends(validate_user)):
    try:
        return await PostService.create_post(post_data, user_id)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# GET POSTS
@router.get("/", response_model=list[PostSchema])
async def get_posts(skip: int = Query(0, ge=0),
                    limit: int | None = Query(PAGINATION_DEFAULT_LIMIT,
                                              ge=PAGINATION_MIN_LIMIT,
                                              le=PAGINATION_MAX_LIMIT)):
    return await PostService.get_posts(skip, limit)


# GET POST
@router.get("/{id}", response_model=PostSchema)
async def get_post(id: UUID):
    post = await PostService.get_post(id=id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


# UPDATE POST
@router.patch("/{id}", response_model=PostSchema)
async def update_post(id: UUID, body: PostUpdateSchema, _=Depends(validate_user)):
    post = await PostService.update_post(id, body)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


# DELETE POST
@router.delete("/{id}")
async def delete_post(id: UUID, _=Depends(validate_user)):
    post = await PostService.delete_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
