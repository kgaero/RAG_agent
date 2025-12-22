import types

import agents.rag_agent.tools.rag_query as rag_query


class _DummyContext:
  def __init__(self):
    self.source_uri = "gs://bucket/file"
    self.source_display_name = "file"
    self.text = "content"
    self.score = 0.9


class _DummyContexts:
  def __init__(self):
    self.contexts = [_DummyContext()]


class _DummyResponse:
  def __init__(self):
    self.contexts = _DummyContexts()


class _DummyResource:
  def __init__(self, rag_corpus=None):
    self.rag_corpus = rag_corpus


class _DummyResources(_DummyResource):
  pass


def _setup_common(monkeypatch):
  monkeypatch.setattr(rag_query, "check_corpus_exists", lambda *_: True)
  monkeypatch.setattr(rag_query, "get_corpus_resource_name", lambda *_: "res")


def test_rag_query_uses_ragresource_when_available(monkeypatch):
  _setup_common(monkeypatch)

  def _retrieval_query(*, rag_resources, text, rag_retrieval_config):
    assert isinstance(rag_resources[0], _DummyResource)
    assert rag_resources[0].rag_corpus == "res"
    return _DummyResponse()

  monkeypatch.setattr(rag_query.rag, "RagResource", _DummyResource)
  if hasattr(rag_query.rag, "RagResources"):
    monkeypatch.delattr(rag_query.rag, "RagResources", raising=False)
  monkeypatch.setattr(rag_query.rag, "retrieval_query", _retrieval_query)

  result = rag_query.rag_query("business", "question", types.SimpleNamespace(state={}))

  assert result["status"] == "success"
  assert result["results_count"] == 1


def test_rag_query_prefers_ragresources_when_present(monkeypatch):
  _setup_common(monkeypatch)

  def _retrieval_query(*, rag_resources, text, rag_retrieval_config):
    assert isinstance(rag_resources[0], _DummyResources)
    assert rag_resources[0].rag_corpus == "res"
    return _DummyResponse()

  monkeypatch.setattr(rag_query.rag, "RagResource", _DummyResource)
  monkeypatch.setattr(rag_query.rag, "RagResources", _DummyResources)
  monkeypatch.setattr(rag_query.rag, "retrieval_query", _retrieval_query)

  result = rag_query.rag_query("business", "question", types.SimpleNamespace(state={}))

  assert result["status"] == "success"
  assert result["results_count"] == 1
