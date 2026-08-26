from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from day08.loader import Document


@dataclass(frozen=True)
class ChunkConfig:
    chunk_size: int = 600
    overlap: int = 100

    @property
    def step(self) -> int:
        """İki ardışık chunk başlangıcı arasındaki karakter sayısı."""

        return self.chunk_size - self.overlap

@dataclass(frozen=True)
class Chunk:
    source: str
    document_id: str
    chunk_id: str
    chunk_index: int
    topic: str
    text: str


def validate_chunk_config(config: ChunkConfig) -> None:

    if not config.chunk_size > 0 : 
        raise ValueError("Chunk size 0 dan büyük olmalıdır.")
    if config.overlap < 0 :
        raise ValueError("overlap sıfır veya sıfırdan büyük olmalıdır")
    if config.overlap >= config.chunk_size:
        raise ValueError("overlap chunk size dan daha küçük olmalıdır.")

def chunk_text(text: str, config: ChunkConfig) -> list[str]:

    validate_chunk_config(config)
    if not text or not text.strip():
        return[]
    chunks = []

    start = 0
    text_lengt = len(text)

    while start < text_lengt:
        end =min(start + config.chunk_size,text_lengt)
        chunks.append(text[start:end])
        if end >= text_lengt:
            break

        start += config.step

    return chunks

def chunk_document(document: Document, config: ChunkConfig) -> list[Chunk]:
 
    raw_chunks = chunk_text(document.text,config)
    chunks = []
    for chunk_index ,text_pierce in enumerate(raw_chunks):
        chunk_id = f"{document.document_id}:{chunk_index}"

        chunk = Chunk(
            source= document.source,
            document_id=document.document_id,
            chunk_id=chunk_id,
            chunk_index=chunk_index,
            topic=document.topic,
            text= text_pierce
        )
        chunks.append(chunk)
    return chunks

def chunk_documents(documents: Iterable[Document],config: ChunkConfig,) -> list[Chunk]:

    all_chunks = []
    for document in documents:
        document_chunks = chunk_document(document,config)
        all_chunks.extend(document_chunks)

    return all_chunks
