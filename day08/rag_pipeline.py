from __future__ import annotations

import re
from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import Protocol

from day08.context_builder import BuiltContext, build_context
from day08.retriever import RetrievedChunk, Retriever

SYSTEM_PROMPT = """Yalnız verilen CONTEXT içindeki bilgilere dayanarak cevap ver.

- Context yeterli değilse bunu açıkça söyle.
- Uydurma kaynak üretme.
- Kullandığın kaynak etiketlerini [S1], [S2] biçiminde belirt."""

EMPTY_CONTEXT_ANSWER = "Context bu soruyu cevaplamak için yeterli değil."


def validate_citations(answer: str, valid_labels: Collection[str]) -> list[str]:
    """Cevap içindeki geçersiz (uydurma) kaynak etiketlerini tespit eder."""
    found_labels = set(re.findall(r'\[(S\d+)\]', answer))
    invalid_labels = [label for label in found_labels if label not in valid_labels]
    return invalid_labels


class GenerationClient(Protocol):
    """Pipeline'ın ihtiyaç duyduğu en küçük generation client sözleşmesi."""
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Promptlardan model cevabını üretir."""
        ...


class RAGPipelineError(RuntimeError):
    """RAG hattı tamamlanamadığında kullanılır."""


@dataclass(frozen=True)
class RAGResult:
    """Tek bir RAG çalışmasının gözlemlenebilir sonucu."""
    question: str
    answer: str
    retrieved_chunks: tuple[RetrievedChunk, ...]
    context: BuiltContext

    @property
    def valid_labels(self) -> frozenset[str]:
        """Bu çalışmada modelin kullanabileceği citation label'ları."""
        return self.context.valid_labels

    @property
    def invalid_citations(self) -> list[str]:
        """Modelin cevapta kullandığı ama context'te olmayan uydurma etiketler."""
        return validate_citations(self.answer, self.valid_labels)
    @property
    def extracted_citations(self) -> set[str]:
        """Cevap içindeki tüm kaynak etiketlerini çıkarır."""
        return set(re.findall(r'\[(S\d+)\]', self.answer))

    @property
    def is_missing_citations(self) -> bool:
        """Context verilmesine rağmen model hiç kaynak etiketi kullanmamış mı?"""
        if len(self.retrieved_chunks) > 0 and self.answer != EMPTY_CONTEXT_ANSWER:
            return len(self.extracted_citations) == 0
        return False


def validate_question(question: str) -> str:
    """Kullanıcı sorusunu doğrular ve kenar boşluklarını temizler."""
    if not isinstance(question, str):
        raise TypeError("Question string tipinde olmalıdır.")
    clean_question = question.strip()
    if not clean_question:
        raise ValueError("Question boş olamaz")
    return clean_question


def build_user_prompt(question: str, context: BuiltContext) -> str:
    """Context ve soruyu Ollama user message biçiminde birleştirir."""
    clean_question = validate_question(question)
    if not isinstance(context, BuiltContext):
        raise TypeError("context bir BuiltContext nesnesi olmalıdır")
    prompt = (
        f"CONTEXT:\n"
        f"{context.text}\n\n"
        f"QUESTION:\n"
        f"{clean_question}"
    )
    return prompt


class RAGPipeline:
    """Retrieval, context construction ve generation akışını yönetir."""

    def __init__(
        self,
        retriever: Retriever,
        generation_client: GenerationClient,
    ) -> None:
        self.retriever = retriever
        self.generation_client = generation_client

    def answer(
        self,
        question: str,
        top_k: int | None = None,
        filters: Mapping[str, str] | None = None,
    ) -> RAGResult:
        """Soruyu corpus içeriğine dayalı olarak cevaplar."""
        clean_question = validate_question(question)

        retrieved_list = self.retriever.retrieve(
            query=clean_question,
            top_k=top_k,
            filters=filters
        )
        retrieved_chunks = tuple(retrieved_list)
        context = build_context(retrieved_chunks)

        if not retrieved_chunks:
            return RAGResult(
                question=clean_question,
                answer=EMPTY_CONTEXT_ANSWER,
                retrieved_chunks=retrieved_chunks,
                context=context
            )
            
        user_prompt = build_user_prompt(clean_question, context)

        try:
            raw_answer = self.generation_client.generate(SYSTEM_PROMPT, user_prompt)
        except Exception as e: 
            raise RAGPipelineError(f"LLM cevap üretemedi: {e}") from e

        if not isinstance(raw_answer, str) or not raw_answer.strip():
            raise RAGPipelineError(
                "Generation tamamlandı ancak model boş veya geçersiz formatta bir cevap döndürdü."
            )
            
        clean_answer = raw_answer.strip()

        return RAGResult(
            question=clean_question,
            answer=clean_answer,
            retrieved_chunks=retrieved_chunks,
            context=context
        )