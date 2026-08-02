# 🤖 Reflexion Agent using LangGraph

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1C3C3C?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-Framework-0FA958?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-000000?style=for-the-badge)
![Tavily](https://img.shields.io/badge/Tavily-Web%20Search-blue?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-Data%20Validation-E92063?style=for-the-badge)

</p>

> A **Reflexion-based AI Agent** built with **LangGraph** that improves its own responses by **self-critiquing**, **researching the web**, and **iteratively refining** its answers.

---

# ✨ Features

✅ Drafts an initial response

✅ Reflects on its own answer

✅ Identifies missing information

✅ Generates intelligent web search queries

✅ Searches the web using Tavily

✅ Revises the answer using retrieved information

✅ Produces references with the final response

---

# 🧠 The Reflexion Workflow

Unlike a traditional chatbot that answers only once...

```
Question
   │
   ▼
 Answer
```

This agent follows a much more intelligent workflow.

```text
                    User Question
                          │
                          ▼
              📝 Initial Draft (LLM)
                          │
                          ▼
               🔍 Self Reflection
                          │
                          ▼
             🌐 Generate Search Queries
                          │
                          ▼
                🔎 Tavily Web Search
                          │
                          ▼
             📚 Retrieved Information
                          │
                          ▼
               ✨ Revised Answer
                          │
                          ▼
          🔁 Continue if more research needed
                          │
                          ▼
                    ✅ Final Answer
```

Think of it as how a human writes a technical article:

> **Write → Review → Research → Improve**

---

# 📂 Project Structure

```text
.
├── main.py              # Builds and runs the LangGraph workflow
├── chains.py            # Prompt templates & LLM chains
├── schemas.py           # Structured outputs (Pydantic)
├── tool_executor.py     # Executes Tavily searches
├── requirements.txt
└── README.md
```

---

# ⚙️ End-to-End Flow

Suppose the user asks:

> **"Write about AI-powered SOC startups and companies that have raised funding."**

---

## Step 1️⃣ Draft Response

The **First Responder** generates an initial answer.

Instead of returning only text, it also evaluates itself.

Example:

```text
Answer:
...

Reflection:
Missing latest funding information

Search Queries:

• AI SOC startups funding
• Autonomous SOC Series A
```

Notice something important...

The model **doesn't search the web itself**.

It only decides **what should be searched.**

---

## Step 2️⃣ Web Search

The Tool Executor receives those search queries.

```
AI SOC startups funding

↓

Tavily Search

↓

Latest Articles

↓

Funding Data
```

The search results are automatically added back into the conversation.

---

## Step 3️⃣ Reflection & Revision

Now the model has:

```
✔ User Question

✔ Initial Draft

✔ Self Critique

✔ Search Results
```

Using all this context, it rewrites its answer with:

- Better facts
- Latest information
- References
- Cleaner explanation

---

# 📖 Project Components

---

# 📄 schemas.py

Defines the structured format that the LLM must follow.

Instead of replying with plain text, the model fills a predefined schema.

## Reflection

```python
Reflection
```

Contains:

- Missing information
- Unnecessary information

Example

```
Missing:
Recent funding rounds

Superfluous:
Long SOC introduction
```

---

## AnswerQuestion

Returned by the **First Responder**.

Contains

```
Answer

Reflection

Search Queries
```

---

## ReviseAnswer

Extends `AnswerQuestion`

and additionally includes

```
References
```

for citation support.

---

# 🔗 chains.py

Creates the reasoning pipelines.

```
Prompt

↓

LLM

↓

Structured Output
```

There are two independent chains.

## 📝 First Responder

Responsible for:

- Writing the initial answer
- Critiquing itself
- Generating search queries

---

## ✨ Revisor

Responsible for:

- Reading search results
- Improving the answer
- Adding citations
- Producing references

---

## 🛠 bind_tools()

One of the most important concepts.

Instead of returning free-form text...

```
Here's my answer...
```

the LLM returns structured data.

```
AnswerQuestion

answer

reflection

search_queries
```

This makes the agent predictable and easy to automate.

---

# 🌐 tool_executor.py

This file connects the LLM to the outside world.

The LLM cannot browse the web.

Instead, it says:

> "Please search these topics."

Example

```
AI SOC funding

Autonomous SOC startups
```

The Tool Executor performs these searches using **Tavily**.

---

## run_queries()

Receives

```python
[
    "Query 1",
    "Query 2"
]
```

Runs all searches in parallel.

Returns search results.

---

## StructuredTool

Converts a normal Python function into a LangChain Tool.

Without this wrapper,

LangGraph cannot automatically invoke the function.

---

## ToolNode

This is the automation layer.

Instead of manually writing code to:

- Read tool calls
- Extract arguments
- Execute searches
- Store results

`ToolNode` performs all of these steps automatically.

---

# 🚀 main.py

This is the heart of the application.

It builds the LangGraph workflow.

```text
START
   │
   ▼
Draft
   │
   ▼
Execute Tools
   │
   ▼
Revise
   │
 ┌─┴─────────────┐
 │               │
 ▼               ▼
Search Again     END
```

---

## draft_node()

Uses the **First Responder** chain.

Produces

- Answer
- Reflection
- Search Queries

---

## execute_tools()

Executes every generated search query.

Returns search results.

---

## revise_node()

Improves the previous answer using the retrieved information.

---

## event_loop()

Controls when the graph should stop.

If the maximum number of iterations has been reached,

the workflow ends.

---

# 🎯 Complete Execution Example

```text
👤 User

│

▼

"Tell me about AI-powered SOC startups."

│

▼

📝 First Responder

│

├── Answer

├── Reflection

└── Search Queries

│

▼

🌐 Tool Executor

│

├── Search Query 1

├── Search Query 2

└── Tavily Results

│

▼

✨ Revisor

│

├── Improved Answer

├── References

└── Better Explanation

│

▼

✅ Final Response
```

---

# 💡 Why Use Reflexion?

Traditional LLMs generate only one response.

```
Question

↓

Answer
```

Reflexion Agents continuously improve themselves.

```
Question

↓

Draft

↓

Critique

↓

Research

↓

Improve

↓

Final Answer
```

This significantly improves:

- Accuracy
- Completeness
- Freshness of information
- Citation quality
- Reliability

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Programming Language |
| 🦜 LangChain | LLM Framework |
| 🕸 LangGraph | Agent Workflow & State Management |
| 🦙 Ollama | Local LLM Inference |
| 🌐 Tavily | Web Search |
| 📦 Pydantic | Structured Output Validation |

---

# 📚 Key Learnings

- Build multi-step AI agents using LangGraph
- Implement the Reflexion architecture
- Use structured outputs with Pydantic
- Execute external tools automatically with ToolNode
- Integrate real-time web search into an AI workflow
- Design iterative reasoning pipelines instead of one-shot prompting

---

# 🌟 Final Thoughts

This project demonstrates how modern AI agents can move beyond simple question-answering by incorporating **reflection**, **tool usage**, and **iterative improvement**. Rather than relying solely on the model's internal knowledge, the agent identifies gaps, gathers fresh information, and produces a more accurate, well-supported response—closely mirroring the way humans research and refine their work.