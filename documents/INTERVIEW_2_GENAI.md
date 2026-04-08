# Interview 2 - Generative AI Discussion

## Table of Contents

1. [Overview](#overview)
2. [Sample Questions and Answer Guidance](#sample-questions-and-answer-guidance)
3. [Next Steps](#next-steps)

---

## Overview

This will be a 30 minute conversation with a Databricks leader on GenAI, in particular focusing on past projects that you've worked on with GenAI solutions and your general philosophy to GenAI problems.

## Sample Questions and Answer Guidance

### Tell me about the GenAI projects you've worked on

- Make sure you have 1-2 GenAI projects ready and you can quickly recap:
  - The business problem
  - The solution you built (high-level) and why you chose that solution
  - The impact of the solution/customer reception

### How do you typically evaluate the GenAI models you're working on?

- Good article to chat through some of the more quantifiable options available: https://dagshub.com/blog/llm-evaluation-metrics/
- Discussing human-in-the-loop feedback through the interfaces that Databricks offers to facilitate that is also valuable here

### If you had a RAG system that was underperforming, what steps would you take to diagnose and remedy that?

- One option here is checking retrieval quality - if retrieval quality turns out to be an issue, one can experiment with different retrieval methodology, or using a more specific embedding model (or potentially one trained yourself, if all else fails)

### If you have a new GenAI problem, how would you go about architecting and iterating on a solution?

**General philosophy**: The simplest solution that performs well is preferred

**Step 1: Validate if GenAI is actually necessary**
- If its a problem that has shown promise in being solved with traditional ML and there is sufficient data to learn from, then it may well be better to go with that - many customers are eager to go with GenAI immediately and its important to educate on the situations where its actually necessary

**Step 2: If GenAI is necessary, define your evaluation criteria**
- Human-in-the-loop feedback or some of the metrics discussed earlier if a golden dataset is available
- Try to use the simplest options first, measuring performance to ensure that adding more complexity results in a gain

**Things to try in order of complexity:**
1. Plain LLM, out of the box
2. LLM out of the box with prompt engineering
3. LLM with RAG, potentially customizing the RAG pipeline with custom retrieval logic and/or embedding model
4. Agentic system
5. Fine tuning an LLM (last resort because of cost, need for a massive amount of data)

## Next Steps

- Use the points above to come up with relevant stories and your talking points around them
- When you feel ready, contact Steve for a mock interview

