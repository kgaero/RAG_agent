from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "agents" / "rag_agent" / "config.py"
AGENT_PATH = ROOT / "agents" / "rag_agent" / "agent.py"


def _read_text(path: Path) -> str:
  return path.read_text(encoding="utf-8")


def test_default_llm_model_is_gemini():
  text = _read_text(CONFIG_PATH)
  match = re.search(
      r"DEFAULT_LLM_MODEL\s*=\s*os\\.environ\\.get\([^,]+,\s*\"([^\"]+)\"\)",
      text,
  )
  assert match, "DEFAULT_LLM_MODEL must read env with a default value."
  assert match.group(1).startswith("gemini-"), (
      "DEFAULT_LLM_MODEL default must be a Gemini model name."
  )


def test_agent_uses_default_llm_model():
  text = _read_text(AGENT_PATH)
  assert "DEFAULT_LLM_MODEL" in text
  assert re.search(r"model\s*=\s*DEFAULT_LLM_MODEL", text)
