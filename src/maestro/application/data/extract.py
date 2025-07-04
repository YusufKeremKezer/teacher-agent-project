from typing import Generator

from langchain_community.document_loaders import WebBaseLoader, WikipediaLoader
from langchain_core.documents import Document
from tqdm import tqdm

from maestro.domain.teachers import Teacher, TeacherExtract
from maestro.domain.teacher_factory import TeacherFactory


def get_extraction_generator(
    teachers: list[TeacherExtract],
) -> Generator[tuple[Teacher, list[Document]], None, None]:
    """Extract documents for a list of teachers, yielding one at a time.

    Args:
        teachers: A list of TeacherExtract objects containing teacher information.

    Yields:
        tuple[Teacher, list[Document]]: A tuple containing the teacher object and a list of
            documents extracted for that teacher.
    """

    progress_bar = tqdm(
        teachers,
        desc="Extracting docs",
        unit="teacher",
        bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}",
        ncols=100,
        position=0,
        leave=True,
    )

    teacher_factory = TeacherFactory()
    for teacher_extract in progress_bar:
        teacher = teacher_factory.get_teacher(teacher_extract.id)
        progress_bar.set_postfix_str(f"Teacher: {teacher.name}")

        teacher_docs = extract(teacher, teacher_extract.urls)

        yield (teacher, teacher_docs)


def extract(teacher: Teacher, extract_urls: list[str]) -> list[Document]:
    """Extract documents for a single teacher from all sources and deduplicate them.

    Args:
        teacher: Teacher object containing teacher information.
        extract_urls: List of URLs to extract content from.

    Returns:
        list[Document]: List of deduplicated documents extracted for the teacher.
    """

    docs = []

    docs.extend(extract_wikipedia(teacher))
    docs.extend(extract_personal_urls(teacher, extract_urls))

    return docs


def extract_wikipedia(teacher: Teacher) -> list[Document]:
    """Extract documents for a single teacher from Wikipedia.

    Args:
        teacher: Teacher object containing teacher information.

    Returns:
        list[Document]: List of documents extracted from Wikipedia for the teacher.
    """

    loader = WikipediaLoader(
        query=teacher.name,
        lang="en",
        load_max_docs=1,
        doc_content_chars_max=1000000,
    )
    docs = loader.load()

    for doc in docs:
        doc.metadata["teacher_id"] = teacher.id
        doc.metadata["teacher_name"] = teacher.name

    return docs


def extract_personal_urls(
    teacher: Teacher, urls: list[str]
) -> list[Document]:
    """Extract documents for a single teacher from personal or official web pages.

    Args:
        teacher: Teacher object containing teacher information.
        urls: List of URLs to extract content from.

    Returns:
        list[Document]: List of documents extracted from personal websites or blogs for the teacher.
    """

    def extract_paragraphs_and_headers(soup) -> str:
        # List of sections we want to remove (generic, can be expanded if needed)
        excluded_sections = [
            "footer",
            "header",
            "nav",
        ]

        for section_name in excluded_sections:
            for section in soup.find_all(id=section_name):
                section.decompose()

            for section in soup.find_all(class_=section_name):
                section.decompose()

            for section in soup.find_all(
                lambda tag: tag.has_attr("id") and section_name in tag["id"].lower()
            ):
                section.decompose()

            for section in soup.find_all(
                lambda tag: tag.has_attr("class")
                and any(section_name in cls.lower() for cls in tag["class"])
            ):
                section.decompose()

        content = []
        for element in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
            content.append(element.get_text())

        return "\n\n".join(content)

    # Filter out empty or whitespace-only URLs
    urls = [u.strip() for u in urls if u and u.strip()]

    if len(urls) == 0:
        return []

    loader = WebBaseLoader(show_progress=False)
    soups = loader.scrape_all(urls)

    documents = []
    for url, soup in zip(urls, soups):
        text = extract_paragraphs_and_headers(soup)
        metadata = {
            "source": url,
            "teacher_id": teacher.id,
            "teacher_name": teacher.name,
        }

        if title := soup.find("title"):
            metadata["title"] = title.get_text().strip(" \n")

        documents.append(Document(page_content=text, metadata=metadata))

    return documents


if __name__ == "__main__":
    chollet = TeacherFactory().get_teacher("chollet")
    docs = extract_personal_urls(
        chollet,
        [
            "https://fchollet.com",
            "https://fchollet.com",
        ],
    )
    print(docs)
