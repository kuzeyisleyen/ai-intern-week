from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path


LOGGER = logging.getLogger(__name__)

SUPPORTED_SUFFIXES = {".md", ".txt"}


class CorpusLoadError(RuntimeError):
    """Corpus klasörü veya corpus dosyaları yüklenemediğinde kullanılır."""


@dataclass(frozen=True)
class Document:
    source: str
    document_id: str
    topic: str
    text: str

def is_supported_file(path: Path) -> bool:

    return path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES


def derive_document_id(path: Path) -> str:

    return path.stem

def derive_topic(document_id: str) -> str:

    return document_id

def read_document_text(path: Path) -> str:

    try:
        with open(path,"r",encoding="utf-8") as f:
            content = f.read()
            return content.strip()
        
    except (OSError,UnicodeError) as e :
        raise CorpusLoadError(f"{path} dosyası okunmadı.Hata : {e}") from e


def load_documents(corpus_directory: str | Path) -> list[Document]:

    corpus_path = Path(corpus_directory)

    if not corpus_path.exists() or not corpus_path.is_dir():
        raise CorpusLoadError("Corpus yolu geçersiz veya bulunamadı")

    supported_files = [p for p in corpus_path.iterdir() if is_supported_file(p)]
    supported_files.sort(key=lambda p : p.name)

    if not supported_files:
        raise CorpusLoadError(f"'{corpus_path} klasöründe desteklenen corpus dosyası bulunamadı.")

    documents = []
    for file_path in supported_files:
        text = read_document_text(file_path)

        if not text: 
            LOGGER.warning( "Boş corpus dosyası atlanıyor: %s",
    file_path.name,) 
            continue

        source = file_path.name
        doc_id = derive_document_id(file_path)
        topic = derive_topic(doc_id)

        document = Document(
            source=source,
            document_id=doc_id,
            topic=topic,
            text=text
        )
        documents.append(document)
    return documents
