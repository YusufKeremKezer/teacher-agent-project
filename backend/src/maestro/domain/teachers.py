from pydantic import BaseModel, Field
from typing import List
from pathlib import Path
import json


class TeacherExtract(BaseModel):
    """A class representing raw teacher data extracted from external sources.

    This class follows the structure of the teacher.json file and contains
    basic information about teacher before enrichment.

    Args:
        id (str): Unique identifier for the teacher.
        urls (List[str]): List of URLs with information about the teacher.
    """

    id: str = Field(description="Unique identifier for the teacher")
    urls: List[str] = Field(
        description="List of URLs with information about the teacher"
    )

    @classmethod
    def from_json(cls, metadata_file: Path) -> list["TeacherExtract"]:
        with open(metadata_file, "r") as f:
            teachers_data = json.load(f)

        return [cls(**teacher) for teacher in teachers_data]



class Teacher(BaseModel):

    id: str = Field(description="Unique identifier for the teacher")
    name: str = Field(description="Name of the teacher")
    expertise: List[str] = Field(default_factory=list, description="Area of expertise of the teacher")
    perspective: str = Field(
        "Information about the perspective of the teacher"
    )
    style: str = Field(description="Style of the teacher")


    
