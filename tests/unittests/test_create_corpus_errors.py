from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CREATE_CORPUS_PATH = (
  ROOT / "agents" / "rag_agent" / "tools" / "create_corpus.py"
)


def _read_text(path: Path) -> str:
  return path.read_text(encoding="utf-8")


def test_create_corpus_error_mentions_region_override():
  text = _read_text(CREATE_CORPUS_PATH)
  assert "GOOGLE_CLOUD_LOCATION" in text
  assert "vertex-ai-rag-engine-support@google.com" in text


def test_create_corpus_error_includes_details_field():
  text = _read_text(CREATE_CORPUS_PATH)
  assert "\"details\"" in text
