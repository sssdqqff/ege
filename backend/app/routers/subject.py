from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from ..services import SubjectService
from ..schemas import SubjectResponse, SubjectCreate, SubjectUpdate

router = APIRouter(prefix="/subjects", tags=["subjects"])


def get_subject_service(db: AsyncSession = Depends(get_db)):
    return SubjectService(db)


@router.get("", response_model=List[SubjectResponse], status_code=status.HTTP_200_OK)
async def get_all_subjects(service: SubjectService = Depends(get_subject_service)):
    return await service.get_all_subjects()


@router.get("/{subject_id}", response_model=SubjectResponse, status_code=status.HTTP_200_OK)
async def get_subject_by_id(subject_id: int, service: SubjectService = Depends(get_subject_service)):
    return await service.get_subject_by_id(subject_id)


@router.post("", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(subject_data: SubjectCreate, service: SubjectService = Depends(get_subject_service)):
    return await service.create_subject(subject_data)


@router.put("/{subject_id}", response_model=SubjectResponse, status_code=status.HTTP_200_OK)
async def update_subject(subject_id: int, subject_data: SubjectUpdate, service: SubjectService = Depends(get_subject_service)):
    return await service.update_subject(subject_id, subject_data)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(subject_id: int, service: SubjectService = Depends(get_subject_service)):
    await service.delete_subject(subject_id)