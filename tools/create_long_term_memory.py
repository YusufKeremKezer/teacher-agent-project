from pathlib import Path


from ..src.maestro.application.long_term_memory import LongTermMemoryCreator
from ..src.maestro.config import settings
from ..src.maestro.domain.teachers import TeacherExtract


def main(metadata_file: Path) -> None:
    """CLI command to create long-term memory for teachers.

    Args:
        metadata_file: Path to the teachers extraction metadata JSON file.
    """
    teachers = TeacherExtract.from_json(metadata_file)

    long_term_memory_creator = LongTermMemoryCreator.build_from_settings()
    long_term_memory_creator(teachers)


if __name__ == "__main__":
    main(metadata_file=Path('api/src/maestro/application/data/teacher_urls.json'))
