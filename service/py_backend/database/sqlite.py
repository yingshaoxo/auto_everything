from typing import List, Optional

import databases
from fastapi.datastructures import UploadFile
from fastapi.params import File

import sqlalchemy

from fastapi import FastAPI
from pydantic import BaseModel


class ErrorOutput(BaseModel):
    error: str


class SuccessOutput(BaseModel):
    success: str


class StartProcessInput(BaseModel):
    project_id: int
    job: str


class ProjectIDInput(BaseModel):
    project_id: int


class ProjectInput(BaseModel):
    title: str
    status: int
    input: Optional[str]


class ProjectOutput(BaseModel):
    id: int
    title: str
    status: int
    input: Optional[str]
    output: Optional[str]


class MyDatabase:
    def __init__(self, DATABASE_URL: str) -> None:
        # DATABASE_URL = "sqlite:///./test.db"
        self.database = databases.Database(DATABASE_URL)
        self.metadata = sqlalchemy.MetaData()

        self.projects = sqlalchemy.Table(
            "projects",
            self.metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("title", sqlalchemy.String),

            sqlalchemy.Column("status", sqlalchemy.Integer),

            sqlalchemy.Column("input", sqlalchemy.String),
            sqlalchemy.Column("output", sqlalchemy.String),
        )

        self.engine = sqlalchemy.create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )

        self.metadata.create_all(self.engine)

    def checkIfProjectExistByID(self, projectID: int) -> bool:
        query = self.projects.select().where(self.projects.c.id == projectID)
        return self.database.fetch_one(query) is not None

    async def getAProjectByID(self, projectID: int) -> ProjectOutput:
        query = self.projects.select().where(self.projects.c.id == projectID)
        return await self.database.fetch_one(query)

    async def updateOutputOfAProject(
        self, projectID: int, output: str
    ) -> ProjectOutput:
        query = self.projects.update().where(
            self.projects.c.id == projectID
        ).values(output=output)
        await self.database.execute(query)

        return await self.getAProjectByID(projectID)

    async def setStatusOfAProject(self, projectID: int, status: int) -> ProjectOutput:
        query = self.projects.update().where(
            self.projects.c.id == projectID
        ).values(status=status)
        await self.database.execute(query)

        return await self.getAProjectByID(projectID)

    async def getProjectByInputOrOutputFilePath(self, filePath: str) -> ProjectOutput:
        query = self.projects.select().where(self.projects.c.output == filePath or self.projects.c.input == filePath)
        return await self.database.fetch_one(query)
