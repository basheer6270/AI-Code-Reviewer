const reviewBtn = document.getElementById("review-btn");
const clearBtn = document.getElementById("clear-btn");
const codeInput = document.getElementById("code-input");
const summaryBox = document.getElementById("summary-output");
const faultsBox = document.getElementById("faults-output");
const suggestionsBox = document.getElementById("suggestions-output");

reviewBtn.addEventListener("click", async () => {
  const code = codeInput.value.trim();
  if (!code) {
    alert("Please paste your code first!");
    return;
  }

  summaryBox.innerHTML = "<em>⏳ Analyzing your code...</em>";
  faultsBox.innerHTML = "";
  suggestionsBox.innerHTML = "";

  try {
    const res = await fetch("/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, mode: "auto" }),
    });

    const data = await res.json();
    const text = data.response || "";

    // 🧠 Smart Parser: Extract sections from AI output
    let summary = "";
    let faults = "";
    let suggestions = "";

    const summaryMatch = text.match(/(?:Summary[:\-]|\*\*Summary\*\*|1\.)\s*([\s\S]*?)(?=(?:Faults|Errors|2\.|Suggestions|3\.|$))/i);
    const faultsMatch = text.match(/(?:Faults[:\-]|Errors[:\-]|\*\*Faults\*\*|2\.)\s*([\s\S]*?)(?=(?:Suggestions|3\.|$))/i);
    const suggestionsMatch = text.match(/(?:Suggestions[:\-]|\*\*Suggestions\*\*|3\.)\s*([\s\S]*)/i);

    if (summaryMatch) summary = summaryMatch[1].trim();
    if (faultsMatch) faults = faultsMatch[1].trim();
    if (suggestionsMatch) suggestions = suggestionsMatch[1].trim();

    // 🧩 Fallback if nothing matched
    if (!summary && !faults && !suggestions) {
      summary = "⚠️ AI response format unrecognized.";
      faults = text;
      suggestions = "Try again or adjust prompt.";
    }

    summaryBox.innerHTML = summary || "No summary found.";
    faultsBox.innerHTML = faults || "No faults detected.";
    suggestionsBox.innerHTML = suggestions || "No suggestions found.";
  } catch (err) {
    summaryBox.innerHTML = "⚠️ Error: " + err.message;
  }
});

clearBtn.addEventListener("click", () => {
  codeInput.value = "";
  summaryBox.innerHTML = "No summary yet.";
  faultsBox.innerHTML = "No faults detected.";
  suggestionsBox.innerHTML = "No suggestions yet.";
});
