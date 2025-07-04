class TeacherNameNotFound(ValueError):
    def __init__(self, teacher_id: str):
        super().__init__(f"Teacher name not found for ID: '{teacher_id}'. Please check if the ID is correct and exists in TEACHER_NAMES.")

class TeacherPerspectiveNotFound(ValueError):
    def __init__(self, teacher_id: str):
        super().__init__(f"Perspective not found for teacher ID: '{teacher_id}'. Ensure it is included in TEACHER_PERSPECTIVES.")

class TeacherStyleNotFound(ValueError):
    def __init__(self, teacher_id: str):
        super().__init__(f"Style not found for teacher ID: '{teacher_id}'. Ensure it is defined in TEACHER_STYLES.")

class TeacherExpertiseNotFound(ValueError):
    def __init__(self, teacher_id: str):
        super().__init__(f"Expertise not found for teacher ID: '{teacher_id}'. Make sure it exists in TEACHER_EXPERTISE.")
