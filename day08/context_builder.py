from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from day08.retriever import RetrievedChunk

@dataclass(frozen=True)
class BuiltContext:
    text: str
    label_to_chunk: Mapping[str, RetrievedChunk]

    @property
    def valid_labels(self) -> frozenset[str]:
        return frozenset(self.label_to_chunk.keys())

def make_source_label(position: int) -> str:

    if isinstance(position,bool) or not isinstance(position,int):
        raise TypeError("Position bool olmayan bir tam sayı olmalıdır.")
    if position < 0 :
        raise ValueError("Position 0 dan küçük olamaz.")
    number = position + 1
    return f"S{number}"

def format_context_block(label: str, chunk: RetrievedChunk) -> str:

    if not isinstance(label, str):
        raise TypeError(f"label string olmalıdır; alınan tip: {type(label).__name__}")
    
    if not label.strip():
        raise ValueError("label boş veya sadece boşluklardan oluşamaz.")

    if not isinstance(chunk, RetrievedChunk):
        raise TypeError(f"chunk bir RetrievedChunk nesnesi olmalıdır; alınan tip: {type(chunk).__name__}")

    context_block = (
        f"[{label}]\n"
        f"Source: {chunk.source}\n"
        f"Chunk: {chunk.chunk_id}\n"
        f"Text:\n"
        f"{chunk.text}"
    )

    return context_block
    
def build_context(chunks: Sequence[RetrievedChunk]) -> BuiltContext:

    if not isinstance(chunks, Sequence) or isinstance(chunks, (str, bytes)):
        raise TypeError(f"chunks bir Sequence (liste/tuple) olmalıdır, str veya bytes kabul edilmez; alınan tip: {type(chunks).__name__}")

    blocks = []
    label_to_chunk = {}

    for position, chunk in enumerate(chunks):
        
        if not isinstance(chunk, RetrievedChunk):
            raise TypeError(f"Sequence içindeki her eleman RetrievedChunk olmalıdır; alınan tip: {type(chunk).__name__}")
            
        label = make_source_label(position)
        
        if label in label_to_chunk:
            raise ValueError(f"Kritik Hata: '{label}' etiketi zaten oluşturulmuş!")
            
        block_text = format_context_block(label, chunk)
        blocks.append(block_text)
        
        label_to_chunk[label] = chunk

    context_text = "\n\n".join(blocks)

    return BuiltContext(
        text=context_text,
        label_to_chunk=label_to_chunk
    )

