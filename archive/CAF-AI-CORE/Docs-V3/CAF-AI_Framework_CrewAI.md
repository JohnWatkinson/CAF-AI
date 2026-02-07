# CAF-AI Agent Framework (CrewAI-Based)
**Version:** v1  
**Date:** 2025-05-08  
**Purpose:** A modular, topic-specialist AI framework for automating tasks typically handled by a commercialista office using CrewAI best practices.

---

## 1. Project Structure

```
CAF-AI/
├── Code/
│   ├── agents/
│   │   └── imu/
│   │       └── IMUResearchAgent.py
│   │       └── IMUAnswerAgent.py
│   │   └── f24/
│   │       └── F24ResearchAgent.py
│   │       └── F24AnswerAgent.py
│   │   └── ...
│   ├── tasks/
│   │   └── imu/
│   │       └── IMUInsightLoaderTask.py
│   │       └── IMUAnswerTask.py
│   │   └── f24/
│   │       └── F24InsightLoaderTask.py
│   │       └── F24AnswerTask.py
│   ├── tools/
│   ├── utils/
│   └── run_caf_crew.py
├── knowledge/
│   └── insights/
│       └── questions/
│           └── imu_qnas.json
│           └── f24_qnas.json
│       └── chroma/
├── missions/
│   └── inputs/
│   └── outputs/
├── requirements.txt
└── README.md
```

---

## 2. Core Agent Roles

### Research Agents
Each one loads insights into ChromaDB from structured Q&A.
- `IMUResearchAgent` → `IMUInsightLoaderTask`
- `F24ResearchAgent` → `F24InsightLoaderTask`
- Future: BonusCasa, Detrazioni, etc.

### Answer Agent
Central or topic-specific, depending on needs.
- `CAFAnswerAgent` → `AnswerTaxQuestionTask`
- Accepts user input → Classifies topic → Queries KB → Returns best answer (or fallback)

---

## 3. Workflow Summary

1. **Research Crew (One-Off or Periodic)**
   - Runs all research agents → populates / updates ChromaDB
   - Scheduled or triggered on demand

2. **Answer Crew (Live System)**
   - One entry point: user asks a question (chat, CLI, WhatsApp)
   - `CAFAnswerAgent` classifies topic
   - Delegates to correct AnswerTask or directly queries ChromaDB
   - Returns best answer with fallback logic if uncertain

---

## 4. Best Practices (Inherited from Marketing-AI)

- Separate each topic into its own `agents/` and `tasks/` folder
- Use consistent naming for agent-task pairs
- Use `metadata` fields in Q&A files: `"region"`, `"tax_type"`, `"year"`
- Embed only clean, reliable insights (no hallucination allowed)
- All KB queries go through ChromaDB
- Output is explainable and trustworthy (important for legal compliance)

---

## 5. Future Extensions

- Add `NotificationAgent` for tax deadlines
- Add `DocumentGeneratorAgent` (e.g. pre-fill F24, IMU receipt)
- Add `ClientFileManagerTool` to track Q&A logs per user
- Add `ResearchAlertAgent` to auto-check for law or deadline changes monthly

