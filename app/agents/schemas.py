
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
