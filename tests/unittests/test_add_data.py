import types

import agents.rag_agent.tools.add_data as add_data


class _DummyImportResult:
  def __init__(self, count: int):
    self.imported_rag_files_count = count


class _DummyRag:
  class ChunkingConfig:
    def __init__(self, chunk_size: int, chunk_overlap: int):
      self.chunk_size = chunk_size
      self.chunk_overlap = chunk_overlap

  class TransformationConfig:
    def __init__(self, chunking_config):
      self.chunking_config = chunking_config

  def __init__(self):
    self.last_import = None

  def import_files(
      self,
      corpus_resource_name,
      paths,
      transformation_config=None,
      max_embedding_requests_per_min=None,
  ):
    self.last_import = types.SimpleNamespace(
        corpus_resource_name=corpus_resource_name,
        paths=paths,
        transformation_config=transformation_config,
        max_embedding_requests_per_min=max_embedding_requests_per_min,
    )
    return _DummyImportResult(len(paths))


class _DummyToolContext:
  def __init__(self):
    self.state = {}


def _setup_mocks(monkeypatch):
  dummy_rag = _DummyRag()
  monkeypatch.setattr(add_data, "rag", dummy_rag)
  monkeypatch.setattr(add_data, "check_corpus_exists", lambda *_: True)
  monkeypatch.setattr(add_data, "get_corpus_resource_name", lambda *_: "res")
  return dummy_rag


def test_add_data_accepts_drive_urls(monkeypatch):
  _setup_mocks(monkeypatch)
  tool_context = _DummyToolContext()

  result = add_data.add_data(
      "business",
      ["https://drive.google.com/file/d/abc123/view"],
      tool_context,
  )

  assert result["status"] == "success"
  assert result["invalid_paths"] == []
  assert result["conversions"] == []
  assert result["paths"] == ["https://drive.google.com/file/d/abc123/view"]
  assert result["files_added"] == 1


def test_add_data_converts_docs_urls(monkeypatch):
  _setup_mocks(monkeypatch)
  tool_context = _DummyToolContext()

  result = add_data.add_data(
      "business",
      ["https://docs.google.com/document/d/doc123/edit"],
      tool_context,
  )

  assert result["status"] == "success"
  assert result["invalid_paths"] == []
  assert result["paths"] == ["https://drive.google.com/file/d/doc123/view"]
  assert len(result["conversions"]) == 1


def test_add_data_rejects_invalid_urls(monkeypatch):
  _setup_mocks(monkeypatch)
  tool_context = _DummyToolContext()

  result = add_data.add_data(
      "business",
      ["https://example.com/file"],
      tool_context,
  )

  assert result["status"] == "error"
  assert result["invalid_paths"]
