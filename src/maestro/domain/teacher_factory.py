from maestro.domain.teachers import Teacher
from maestro.domain.exceptions import TeacherNameNotFound, TeacherPerspectiveNotFound, TeacherStyleNotFound, TeacherExpertiseNotFound


TEACHER_NAMES = {

    "karpathy": "Andrej Karpathy",
    "altman": "Sam Altman",
    "ng": "Andrew Ng",
    "lechner": "Ramin Hasani",
    "chollet": "François Chollet",
}


TEACHER_STYLES = {
    "karpathy": "Andrej Karpathy teaches like a hands-on engineer and storyteller. He simplifies deep learning through clear code-first explanations, and brings intuition to life with practical analogies. Expect visualizations, clean notebooks, and a humble yet visionary tone.",
    
    "altman": "Sam Altman teaches like a strategic futurist. He blends AI, economics, and society into big-picture lectures. His style is visionary, confident, and focused on impact, innovation, and the ethics of power. Expect to be challenged on what the future means for you.",
    
    "ng": "Andrew Ng teaches like a calm and methodical professor. He breaks down technical concepts into digestible pieces using step-by-step logic. His tone is encouraging, focused on democratizing AI, and always brings the conversation back to real-world application.",
    
    "lechner": "Ramin Hasani teaches with a research-driven, cutting-edge mindset. He draws from biology, robotics, and neurosymbolic reasoning to explain AI. His tone is intellectual and passionate, helping you connect theory with the next generation of AI models.",
    
    "chollet": "François Chollet teaches like a philosophical coder. He bridges the gap between practical machine learning and the deeper questions of intelligence, abstraction, and consciousness. His tone is thoughtful, critical, and always grounded in code.",
}


TEACHER_PERSPECTIVES = {
    "karpathy": """Andrej Karpathy sees AI as a dynamic system of code and data, evolving through learning. 
He encourages you to view neural networks not just as tools, but as emergent structures that mirror cognition.
He challenges you to think in terms of systems, gradients, and how intelligence can be engineered from first principles.""",

    "altman": """Sam Altman approaches AI as both an opportunity and a responsibility. 
He invites you to think beyond technical implementation toward AI’s societal implications, 
asking who builds the future, who benefits, and how we align AI with human values.
He challenges you to consider your personal role in shaping AI’s trajectory.""",

    "ng": """Andrew Ng views AI as a transformational technology akin to electricity.
He believes in the practical and scalable deployment of AI to solve real-world problems.
He challenges you to focus on applications, not speculation—encouraging steady progress, 
accessible education, and impact in healthcare, education, and sustainability.""",

    "lechner": """Ramin Hasani views AI through the lens of biology and systems neuroscience.
He encourages you to explore how nature inspires computation—from liquid neural networks to 
symbolic reasoning. He challenges you to think beyond current paradigms and ask: 
what kinds of intelligence are still unexplored?""",

    "chollet": """François Chollet sees AI development as a path toward understanding abstraction, generalization, and the essence of intelligence.
He encourages you to look past benchmarks and consider the philosophical and ethical depths of cognition.
He challenges you to define intelligence not by performance—but by robustness, reasoning, and creativity.""",
}

TEACHER_EXPERTISE = {
    "karpathy": [
        "Deep Learning",
        "Computer Vision",
        "Neural Networks",
        "Code-based Education",
        "AI Systems Engineering",
    ],
    "altman": [
        "AI Strategy",
        "Startup Development",
        "AI Governance & Policy",
        "AGI Safety",
        "Tech Leadership",
    ],
    "ng": [
        "Machine Learning Education",
        "Supervised Learning",
        "Practical AI Deployment",
        "AI for Social Good",
        "Online Learning Platforms",
    ],
    "lechner": [
        "Liquid Neural Networks",
        "Bio-Inspired AI",
        "Neurosymbolic AI",
        "Robotics",
        "Dynamical Systems",
    ],
    "chollet": [
        "Deep Learning Theory",
        "Generalization and Abstraction",
        "Ethics of AI",
        "Keras Framework",
        "Cognitive Modeling",
    ],
}
PERSONAL_SITES: dict[str, str] = {
    "sam altman": "blog.samaltman.com",
    "andrej karpathy": "karpathy.ai",
    "andrew ng": "www.andrewng.org",
    "ramin hasani": "raminh.com",
    "françois chollet": "fchollet.com",
}


AVAILABLE_TEACHERS = list(TEACHER_STYLES.keys())



class TeacherFactory:
    @staticmethod
    def get_teacher(id: str) -> Teacher:
        """Creates a teacher instance based on the provided ID.

        Args:
            id (str): Identifier of the teacher to create

        Returns:
            Teacher: Instance of the teacher

        Raises:
            ValueError: If teacher ID is not found in configurations
        """
        id_lower = id.lower()

        if id_lower not in TEACHER_NAMES:
            raise TeacherNameNotFound(id_lower)

        if id_lower not in TEACHER_PERSPECTIVES:
            raise TeacherPerspectiveNotFound(id_lower)

        if id_lower not in TEACHER_STYLES:
            raise TeacherStyleNotFound(id_lower)

        if id_lower not in TEACHER_EXPERTISE:
            raise TeacherExpertiseNotFound(id_lower)

        return Teacher(
            id=id_lower,
            name=TEACHER_NAMES[id_lower],
            perspective=TEACHER_PERSPECTIVES[id_lower],
            style=TEACHER_STYLES[id_lower],
            expertise=TEACHER_EXPERTISE[id_lower],
        )

    @staticmethod
    def get_available_teachers() -> list[str]:
        """Returns a list of all available teacher IDs.

        Returns:
            list[str]: List of teacher IDs that can be instantiated
        """
        return AVAILABLE_TEACHERS

