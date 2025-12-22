import re

from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from ..config import(
    DEFAULT_EMBEDDING_MODEL,
    LOCATION,
)

from .utils import check_corpus_exists


def _format_create_corpus_error(error_message: str) -> str:
    """Return a user-friendly error message for corpus creation failures."""
    normalized = error_message.lower()
    if "rag engine" in normalized and "restricted" in normalized:
        location = LOCATION or "the configured region"
        return (
            f"RAG Engine in {location} is restricted for new projects. "
            "Set GOOGLE_CLOUD_LOCATION in .env to an allowed region, then "
            "restart the server. If you need this region, request "
            "allowlisting via vertex-ai-rag-engine-support@google.com."
        )
    return f"Error creating corpus: {error_message}"

def create_corpus(
    corpus_name: str,
    tool_context: ToolContext,
) -> dict:
    """
    Create a new Vertex AI RAG corpus with the specified name.

    Args:
        corpus_name (str) : The name for the new corpus
        tool_context (ToolContext): The tool context for state management
    Returns:
        dict: Status information about the operation
    """

    if check_corpus_exists(corpus_name, tool_context):
        return{
            "status": "info",
            "message": f"Corpus '{corpus_name}' already exists",
            "corpus_name" : corpus_name,
            "corpus_created": False,
        }

    try:
        display_name = re.sub(r"[^a-zA-Z0-9_-]", "_", corpus_name)

        embedding_model_config = rag.RagEmbeddingModelConfig(
            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model = DEFAULT_EMBEDDING_MODEL
            )
        )

        rag_corpus = rag.create_corpus(
            display_name = display_name,
            backend_config = rag.RagVectorDbConfig(
                rag_embedding_model_config = embedding_model_config
            ),
        )

        tool_context.state[f"corpus_exists_{corpus_name}"] = True

        tool_context.state["current_corpus"] = corpus_name

        return{
            "status" : "Success",
            "message": f"Successfully created corpus '{corpus_name}'",
            "corpus_name" : rag_corpus.name,
            "display_name" : rag_corpus.display_name,
            "corpus_created" : True,
        }
    
    except Exception as e:
        error_message = str(e)
        return{
            "status" : "error",
            "message" : _format_create_corpus_error(error_message),
            "details" : error_message,
            "corpus_name" : corpus_name,
            "corpus_created" : False,
        }
