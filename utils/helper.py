"""
utils/helper.py

Helper utilities for AI Code Reviewer:
- split_large_code(code): split code into safe-sized chunks (by lines)
- create_prompt(code_chunk, mode="auto"): produce a structured prompt for the LLM
- detect_language(code): lightweight language detection (python/javascript/cpp/unknown)
"""

from typing import List
import re

# CONFIG
CHUNK_SIZE_LINES = 120  # lines per chunk (adjustable)


def split_large_code(code: str, chunk_size: int = CHUNK_SIZE_LINES) -> List[str]:
    """
    Split code into chunks by lines. Returns list of code chunks.
    If code is small, returns single-item list.
    """
    lines = code.splitlines()
    if len(lines) <= chunk_size:
        return [code]
    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk = "\n".join(lines[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def detect_language(code: str) -> str:
    """
    Very lightweight detection by some keywords. Returns 'python', 'javascript', 'cpp' or 'unknown'.
    """
    first_200 = code[:200].lower()
    if re.search(r'\bdef\b|\bimport\b|\bself\b|:\s*$', first_200, re.M):
        return "python"
    if re.search(r'\bfunction\b|\bconsole\.log\b|\bconst\b|\blet\b|\b=>', first_200):
        return "javascript"
    if re.search(r'#include|std::|cout<<|int main\(|->', first_200):
        return "cpp"
    return "unknown"


def create_prompt(code: str, mode: str = "auto") -> str:
    """
    Create a structured prompt for the LLM.
    mode:
      - "auto": decide between detailed or summary based on code length
      - "detailed": ask for line-by-line / thorough review
      - "summary": ask for high-level summary and major issues only
    The prompt requests Markdown-formatted response with **bold** and *italic* emphasis and code blocks.
    """
    # Basic info
    lang = detect_language(code)
    line_count = len(code.splitlines())

    # Decide mode if auto
    if mode == "auto":
        if line_count <= 120:
            mode = "detailed"
        else:
            mode = "summary"

    # System / instruction
    header = (
        "You are an expert software developer and code reviewer.\n\n"
        "Analyze the following code and produce a helpful, structured review using Markdown. "
        "Use **bold** for important findings, *italic* for names (like function or variable names), and "
        "include code blocks (```language\n...\n```) for suggested fixes or corrected code.\n\n"
    )

    # Mode-specific instructions
    if mode == "detailed":
        body = (
            "Deliver:\n"
            "1. **Summary:** One-paragraph summary of what the code does.\n"
            "2. **Issues:** A numbered list of any syntax errors, logic bugs, security vulnerabilities, or best-practice violations. Use **bold** for issues.\n"
            "3. **Line-by-line notes (if applicable):** short remarks pointing to specific lines or functions.\n"
            "4. **Suggestions & Fixes:** For each important issue, provide a suggested fix as a code block. Keep fixes minimal and ready-to-run when possible.\n"
            "5. **Improvements:** Brief recommendations for refactoring, performance, readability, and testing.\n"
        )
    else:  # summary
        body = (
            "Deliver a concise review focused on major issues and high-level suggestions:\n"
            "1. **Summary:** Short paragraph.\n"
            "2. **Major Issues:** Top 6 issues (logic, security, architecture, obvious bugs).\n"
            "3. **Suggested Fixes:** Provide example fixes for the most critical issues as code blocks.\n"
            "4. **Refactoring Advice:** Recommend structural changes or where to focus deeper review.\n"
        )

    # Language hint
    lang_hint = f"\nLanguage detected: **{lang}**.\n\n" if lang != "unknown" else "\n"

    prompt = (
        header +
        f"Context: The reviewer should be concise and practical. The user expects **clearly formatted** Markdown output with emphasis as described.\n\n"
        + lang_hint +
        body +
        "\n\nCODE:\n```" + (lang if lang != "unknown" else "") + "\n" + code + "\n```\n\n"
        "Important: If you mention specific line numbers, assume the code block starts at line 1.\n"
        "If suggesting fixes, show only the minimal corrected snippet and explain why the change is needed.\n"
    )

    return prompt


# If run as script, quick self-test
if __name__ == "__main__":
    sample = "def add(a,b):\n return a+b\n"
    print("Chunks:", split_large_code(sample))
    print("Lang:", detect_language(sample))
    print("Prompt preview:\n", create_prompt(sample, mode="detailed")[:800])
