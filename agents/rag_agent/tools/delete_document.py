from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from .utils import check_corpus_exists, get_corpus_resource_name


def delete_document(
    corpus_name: str,
    document_id: str,
    tool_context: ToolContext,
) -> dict:
    """
        Delete a specific document from a Vertex AI RAG corpus

        Args:
            corpus_name (str) : The full resource of the corpus containing the document.
                                Preferably use the resource_name from list_corpus results.

            document_id (str) : The ID of the specific document/file to delete. This can be
                                obtained from get_corpus_info results.
            
            tool_context (ToolCOntext): The tool context

        Returns:
            dict: Status information about the deletion operation
    """


    if not check_corpus_exists(corpus_name, tool_context):
        return{
            "status": "error",
            "message": f"Corpus '{corpus_name}' does not exist",
            "corpus_name" : corpus_name,
            "document_id" : document_id,
        }

    try:
        corpus_resource_name = get_corpus_resource_name(corpus_name)

        rag_file_path = f"{corpus_resource_name}/ragFiles/{document_id}"
        rag.delete_file(rag_file_path)

        return {
            "status": "sucess",
            "message" : f"Sucessfully deleted document '{document_id}' from corpus '{corpus_name}' ",
            "corpus_name":corpus_name,
            "document_id" : document_id,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error deleting document: {str(e)}",
            "corpus_name" : corpus_name,
            "document_id" : document_id,
        }