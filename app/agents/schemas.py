
from pydantic import BaseModel, Field


class MemeIdea(BaseModel):
    topic: str = Field(description="Argomento del meme")
    text_top: str = Field(description="Testo superiore del meme")
    text_bottom: str = Field(description="Testo inferiore del meme")
    description: str = Field(description="Descrizione dell'idea del meme")


class MemeIdeas(BaseModel):
    ideas: list[MemeIdea] = Field(
        description="Lista delle idee per meme generate"
    )


class MemeEvaluation(BaseModel):
    creativity: int = Field(
        ge=1,
        le=10,
        description="Valutazione della creatività del meme"
    )
    humor: int = Field(
        ge=1,
        le=10,
        description="Valutazione del potenziale umoristico"
    )
    originality: int = Field(
        ge=1,
        le=10,
        description="Valutazione dell'originalità"
    )
    feedback: str = Field(
        description="Breve spiegazione della valutazione"
    )


class MemeRevision(BaseModel):
    text_top: str = Field(
        description="Nuovo testo superiore del meme"
    )
    text_bottom: str = Field(
        description="Nuovo testo inferiore del meme"
    )
    description: str = Field(
        description="Nuova descrizione del meme"
    )


class TrendVerification(BaseModel):
    verified: bool = Field(
        description="Indica se il trend è sufficientemente supportato dalle informazioni disponibili"
    )
    confidence: int = Field(
        ge=1,
        le=10,
        description="Livello di confidenza della verifica da 1 a 10"
    )
    reasoning: str = Field(
        description="Motivazione sintetica dell'esito della verifica"
    )


class TrendRanking(BaseModel):
    actuality: int = Field(
        ge=1,
        le=10,
        description="Quanto è attuale il trend"
    )

    interest: int = Field(
        ge=1,
        le=10,
        description="Quanto può interessare agli utenti"
    )

    humor: int = Field(
        ge=1,
        le=10,
        description="Quanto si presta alla creazione di meme divertenti"
    )

    reasoning: str = Field(
        description="Breve motivazione dei punteggi assegnati"
    )
