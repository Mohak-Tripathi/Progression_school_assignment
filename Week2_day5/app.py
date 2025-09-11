# app.py
# Streamlit chat app using OpenAI Responses API
# Features: streaming, model/temperature controls, system prompt editor,
# auto-summarised memory, export/import, basic analytics (turns, tokens if available)

import os
import json
from typing import List, Dict, Optional
from dataclasses import dataclass



import streamlit as st
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI, APIError, APIStatusError, APIConnectionError

# ---------- Setup ----------
st.set_page_config(page_title="Chat with Memory · Streamlit + OpenAI", page_icon="💬", layout="wide")
# load_dotenv()


# # Find the closest .env by walking up from the current working dir
# dotenv_path = find_dotenv(filename=".env", usecwd=True)
# if dotenv_path:
#     load_dotenv(dotenv_path, override=False)
# else:
#     # Fallback: do nothing if not found (Streamlit secrets may still be used)
#        # Optional fallback: explicitly check one level above this file
#     pass

# def get_api_key() -> Optional[str]:
#     # Prefer Streamlit secrets; fall back to env
#     if "OPENAI_API_KEY" in st.secrets:
#         return st.secrets["OPENAI_API_KEY"]
#     return os.getenv("OPENAI_API_KEY")

# def make_client() -> OpenAI:
#     # The OpenAI() constructor will read env var by default; pass explicitly if we have it
#     key = get_api_key()
#     if key:
#         return OpenAI(api_key=key)
#     return OpenAI()





def get_api_key() -> Optional[str]:
    # 1) Hardcoded for local testing
    if OPENAI_KEY and OPENAI_KEY.startswith("sk-"):
        return OPENAI_KEY
    # 2) Otherwise use secrets/env
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    return os.getenv("OPENAI_API_KEY")


# ⚠️ Hardcode your key here (for testing only!)
# Replace with your actual key string
OPENAI_KEY = ""

def make_client() -> OpenAI:
    return OpenAI(api_key=OPENAI_KEY)

client = make_client()




 

# ---------- Defaults & session state ----------
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."
DEFAULT_MODEL = "gpt-4.1-mini"  # fast & cheap; you can switch in the sidebar
SUPPORTED_MODELS = [
    "gpt-4.1-mini",
    "gpt-4o-mini",
    "gpt-4o",
    "o4-mini",
]

@dataclass
class TurnUsage:
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None

def _init_state():
    st.session_state.setdefault("messages", [])           # List[Dict[str,str]] with roles: "user" | "assistant"
    st.session_state.setdefault("history_summary", "")    # str: condensed summary of earlier turns
    st.session_state.setdefault("usages", [])             # List[TurnUsage]
    st.session_state.setdefault("model", DEFAULT_MODEL)
    st.session_state.setdefault("temperature", 0.4)
    st.session_state.setdefault("max_output_tokens", 512)
    st.session_state.setdefault("streaming", True)
    st.session_state.setdefault("auto_summarise", True)
    st.session_state.setdefault("summary_threshold", 16)  # summarise when > N messages
    st.session_state.setdefault("system_prompt", DEFAULT_SYSTEM_PROMPT)

_init_state()
client = make_client()

# ---------- Sidebar controls ----------
with st.sidebar:
    st.header("⚙️ Settings")
    key_ok = bool(get_api_key())
    st.success("API key loaded") if key_ok else st.error("Add OPENAI_API_KEY in st.secrets or .env")

    st.session_state.model = st.selectbox("Model", SUPPORTED_MODELS, index=SUPPORTED_MODELS.index(st.session_state.model) if st.session_state.model in SUPPORTED_MODELS else 0)
    st.session_state.temperature = st.slider("Temperature", 0.0, 1.0, st.session_state.temperature, 0.05)
    st.session_state.max_output_tokens = st.slider("Max output tokens", 64, 4096, st.session_state.max_output_tokens, 64)
    st.session_state.streaming = st.toggle("Stream tokens live", value=st.session_state.streaming)
    st.session_state.auto_summarise = st.toggle("Auto-summarise long chats", value=st.session_state.auto_summarise)
    st.session_state.summary_threshold = st.slider("Summarise when messages exceed", 8, 64, st.session_state.summary_threshold, 1)

    st.write("**System prompt**")
    st.session_state.system_prompt = st.text_area(
        " ", value=st.session_state.system_prompt, height=90, label_visibility="collapsed"
    )

    st.divider()
    st.subheader("📦 Import / Export")
    colA, colB = st.columns(2)
    with colA:
        if st.button("🧹 New chat"):
            st.session_state.messages = []
            st.session_state.usages = []
            st.session_state.history_summary = ""
            st.rerun()
    with colB:
        # Export current transcript
        export_payload = {
            "system_prompt": st.session_state.system_prompt,
            "model": st.session_state.model,
            "messages": st.session_state.messages,
            "history_summary": st.session_state.history_summary,
        }
        st.download_button("⬇️ Export JSON", data=json.dumps(export_payload, ensure_ascii=False, indent=2),
                           file_name="chat_export.json", mime="application/json")

    uploaded = st.file_uploader("Import a previous chat (.json)", type=["json"])
    if uploaded:
        try:
            data = json.load(uploaded)
            st.session_state.system_prompt = data.get("system_prompt", DEFAULT_SYSTEM_PROMPT)
            st.session_state.model = data.get("model", DEFAULT_MODEL)
            st.session_state.messages = data.get("messages", [])
            st.session_state.history_summary = data.get("history_summary", "")
            st.session_state.usages = []  # reset usage for imported content
            st.success("Chat imported.")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to import: {e}")

    st.divider()
    st.subheader("📊 Session analytics")
    total_turns = len([m for m in st.session_state.messages if m["role"] == "user"])
    token_in = sum((u.input_tokens or 0) for u in st.session_state.usages)
    token_out = sum((u.output_tokens or 0) for u in st.session_state.usages)
    st.metric("User turns", total_turns)
    st.metric("Input tokens", token_in)
    st.metric("Output tokens", token_out)

    # Quick “tokens per turn” chart if we have data
    if st.session_state.usages:
        st.line_chart(
            {
                "input_tokens": [u.input_tokens or None for u in st.session_state.usages],
                "output_tokens": [u.output_tokens or None for u in st.session_state.usages],
            }
        )

# ---------- Helper: auto summarise older history ----------
def maybe_summarise_history():
    if not st.session_state.auto_summarise:
        return
    # Only summarise if we have many messages; ignore assistant-only messages
    if len(st.session_state.messages) <= st.session_state.summary_threshold:
        return
    try:
        # Keep the most recent 8 visible; summarise the rest
        visible_tail = 8
        head = st.session_state.messages[:-visible_tail]
        tail = st.session_state.messages[-visible_tail:]

        # Build a compact plain-text transcript for summary
        head_str = "\n".join([f"{m['role']}: {m['content']}" for m in head if m["role"] in ("user", "assistant")])

        summarise_prompt = [
            {"role": "system", "content": "Summarise earlier conversation into concise bullet points that preserve tasks, decisions, constraints, and style preferences. Keep under 150 words."},
            {"role": "user", "content": head_str[:8000]},  # guardrail
        ]
        resp = client.responses.create(
            model=st.session_state.model,
            input=summarise_prompt,
            temperature=0.2,
            max_output_tokens=200,
            store=False,
        )
        summary = resp.output_text.strip()
        # Save summary and shrink visible history
        st.session_state.history_summary = summary
        st.session_state.messages = tail
    except Exception as e:
        # Non-fatal; just skip summarisation
        st.toast(f"Summary skipped: {e}", icon="⚠️")

# ---------- Helper: call model ----------
def call_model(messages: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Calls OpenAI Responses API with streaming or non-streaming depending on toggle.
    Returns dict: {"answer": str, "usage": TurnUsage|None}
    """
    # Build the input list: optional summary header + full recent turns
    input_items: List[Dict[str, str]] = []
    if st.session_state.history_summary:
        input_items.append({
            "role": "system",
            "content": f"Conversation summary for context:\n{st.session_state.history_summary}"
        })
    # Add actual turns
    input_items.extend(messages)

    usage_obj = None
    answer = ""

    try:
        if st.session_state.streaming:
            # Stream token deltas; show incrementally
            stream = client.responses.create(
                model=st.session_state.model,
                instructions=st.session_state.system_prompt,
                input=input_items,
                temperature=st.session_state.temperature,
                max_output_tokens=st.session_state.max_output_tokens,
                stream=True,
                store=False,
            )

            # Render incremental text
            with st.chat_message("assistant"):
                placeholder = st.empty()
                for event in stream:
                    t = getattr(event, "type", "")
                    if t == "response.output_text.delta":
                        delta = getattr(event, "delta", "")
                        if delta:
                            answer += delta
                            placeholder.markdown(answer)
                # Final render to ensure it's on screen even if no deltas were sent
                if answer.strip() == "":
                    placeholder.markdown("_(no text returned)_")
        else:
            # Non-streaming: simpler and yields usage
            resp = client.responses.create(
                model=st.session_state.model,
                instructions=st.session_state.system_prompt,
                input=input_items,
                temperature=st.session_state.temperature,
                max_output_tokens=st.session_state.max_output_tokens,
                store=False,
            )
            answer = resp.output_text or ""
            # Extract usage if available
            try:
                usage = getattr(resp, "usage", None)
                usage_obj = TurnUsage(
                    input_tokens=getattr(usage, "input_tokens", None) if usage else None,
                    output_tokens=getattr(usage, "output_tokens", None) if usage else None,
                )
            except Exception:
                usage_obj = None

    except APIConnectionError as e:
        answer = f"Network error: {e}"
    except APIStatusError as e:
        # e.status_code and e.response available
        answer = f"API error ({e.status_code}): {getattr(e, 'message', str(e))}"
    except APIError as e:
        answer = f"OpenAI error: {e}"
    except Exception as e:
        answer = f"Unexpected error: {e}"

    return {"answer": answer, "usage": usage_obj}

# ---------- Header ----------
st.title("💬 Streamlit Chat with Memory")
st.caption("OpenAI Responses API · streaming, summaries, and simple analytics")

# ---------- Render existing transcript ----------
for m in st.session_state.messages:
    if m["role"] == "user":
        with st.chat_message("user"):
            st.markdown(m["content"])
    elif m["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(m["content"])

# ---------- Chat input & flow ----------
user_msg = st.chat_input("Tell me what is going on in your mind? (type 'exit' to quit)")

if user_msg:
    if user_msg.strip().lower() == "exit":
        st.stop()

    # 1) Push user message
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    # 2) Summarise if needed (before the next call to keep context tight)
    maybe_summarise_history()

    # 3) Call model
    result = call_model(st.session_state.messages)

    # 4) Append assistant result to history
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})

    # 5) Record usage (if available)
    st.session_state.usages.append(result["usage"] or TurnUsage())

# Footer note
st.markdown(
    """
    <hr style='opacity:0.2'/>
    <small>
    Tip: toggle <b>Stream tokens live</b> off to see token usage per turn (the API reports usage in non-streaming mode).<br/>
    Keep your key safe—use <code>st.secrets</code> in production.
    </small>
    """,
    unsafe_allow_html=True,
)
