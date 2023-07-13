from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.exc import IntegrityError
from starlette import status

from api.dependencies.users import validate_user
from config import PAGINATION_DEFAULT_LIMIT, PAGINATION_MIN_LIMIT, PAGINATION_MAX_LIMIT
from schemas.attachment import AttachmentSchema, AttachmentCreateSchema, AttachmentUpdateSchema
from services.attachment import AttachmentService

router = APIRouter(tags=["Attachments"])


# CREATE ATTACHMENT
@router.post("/", response_model=AttachmentSchema, status_code=status.HTTP_201_CREATED)
async def create_attachment(attachment_data: AttachmentCreateSchema, _=Depends(validate_user)):
    try:
        return await AttachmentService.create_attachment(attachment_data)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# GET ATTACHMENTS
@router.get("/", response_model=list[AttachmentSchema])
async def get_attachments(skip: int = Query(0, ge=0),
                          limit: int | None = Query(PAGINATION_DEFAULT_LIMIT,
                                                    ge=PAGINATION_MIN_LIMIT,
                                                    le=PAGINATION_MAX_LIMIT)):
    return await AttachmentService.get_attachments(skip, limit)


# GET ATTACHMENT
@router.get("/{id}", response_model=AttachmentSchema)
async def get_attachment(id: UUID):
    attachment = await AttachmentService.get_attachment(id=id)
    if not attachment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    return attachment


# UPDATE ATTACHMENT
@router.patch("/{id}", response_model=AttachmentSchema)
async def update_attachment(id: UUID, body: AttachmentUpdateSchema, _=Depends(validate_user)):
    attachment = await AttachmentService.update_attachment(id, body)
    if attachment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    return attachment


# DELETE ATTACHMENT
@router.delete("/{id}")
async def delete_attachment(id: UUID, _=Depends(validate_user)):
    attachment = await AttachmentService.delete_attachment(id)
    if attachment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
