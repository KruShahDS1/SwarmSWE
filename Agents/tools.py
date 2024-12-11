from utils import SwarmTool, SwarmState
from typing import Annotated

class ViewDocument(SwarmTool):
    """
    Retrieves a document for inspection/review. This tool is used by the assistant to view the document.
    """
    def run(self, document_name: str, state: Annotated[SwarmState, dict]) -> str:
        documents = state.get("documents", {})
        if document_name in documents:
            return documents[document_name]
        elif document_name in documents.get("code", {}):
            return documents["code"][document_name]
        else:
            return "document not found"


class UpdateDocument(SwarmTool):
    """
    Updates a document. This tool is used by the assistant to modify the content of an existing document.
    """
    def run(self, document_name: str, content: str, state: Annotated[SwarmState, dict]) -> SwarmState:
        documents = state.setdefault("documents", {})
        if document_name in documents or document_name in documents.get("code", {}):
            documents[document_name] = content
        else:
            return "document not found"
        return state


class AddDocument(SwarmTool):
    """
    Adds a new document. This tool is used by the assistant to create a new document.
    """
    def run(self, document_name: str, content: str, state: Annotated[SwarmState, dict]) -> SwarmState:
        documents = state.setdefault("documents", {})
        documents[document_name] = content
        return state


class DeleteDocument(SwarmTool):
    """
    Deletes a document. This tool is used by the assistant to remove a document from the state.
    """
    def run(self, document_name: str, state: Annotated[SwarmState, dict]) -> SwarmState:
        documents = state.get("documents", {})
        if document_name in documents:
            del documents[document_name]
        elif document_name in documents.get("code", {}):
            del documents["code"][document_name]
        else:
            return "document not found"
        return state


class BashCommand(SwarmTool):
    """
    Executes a bash command and returns the output.
    """
    def run(self, command: str, state: Annotated[SwarmState, dict]) -> str:
        import subprocess
        try:
            output = subprocess.check_output(command, shell=True, text=True)
            return output
        except subprocess.CalledProcessError as e:
            return e.output

# Registering tools in the SWARM framework
tools = [
    ViewDocument(),
    UpdateDocument(),
    AddDocument(),
    DeleteDocument(),
    BashCommand()
]
