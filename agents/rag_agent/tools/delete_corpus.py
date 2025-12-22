from math import e
from google.adk.tools.tool_context import ToolContext
from vertexai import rag

from .utils import check_corpus_exists, get_corpus_resource_name

def delete_corpus(
    corpus_name: str,
    confirm: bool,
    tool_context: ToolContext,
) -> dict:
    """
    Delete a vertext AI RAG corpus when it is no longer needed.
    Requires confirmation to prevent accidental deletion.

    Args:
        corpus_name (str): The full resource name of the corpus to delete
        Preferably use the resource_name from list_corpora results.
        confirm(bool): Must be set to True to confirm deletion
        tool_context (ToolContext): The tool context

    Returns:
        dict: Status information about the deletion operation
    """

    if not check_corpus_exists(corpus_name, tool_context):
        return {
            "status": "error",
            "message" : f"Corpus '{corpus_name}' does not exist",
            "corpus_name": corpus_name,
        }

    try:
        corpus_resource_name = get_corpus_resource_name(corpus_name)

        rag.delete_corpus(corpus_resource_name)

        state_key = f"corpus_exists_{corpus_name}"
        if state_key in tool_context.state:
            tool_context.state[state_key] = False
        
        return{
            "status": "success",
            "message": f"sucessfully deleted corpus '{corpus_name}' ",
            "corpus_name": corpus_name,
        }

    except Exception as e:
        return {
            "status" : "error",
            "message" : f"Error deleting corpus: {str(e)}",
            "corpus_name": corpus_name,
        }
