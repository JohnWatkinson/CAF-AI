CAF AI Notes


V1 - CAF-AI (chatbot)
V2 - CAF-AI-Agent (agents)
V3 - CAF-AI-CORE (chromadb)


CAF-AI
    CrewAI, RAG, Chromadb KB, Human in the loop, learning, Agents, UI

CAF / Commercialista app
    Customer goes on the website, asks questions about anything to do with taxes, pensions, anything a commercialista or CAF would handle and gets answers and insights.

TODO:
    Much better web scraper.. missing pdf, links, list format
    Needs a logger for the ingestion
    Ongoing - ingesting the data. stuck, /home/john/AI/CAF-AI-CORE/Code/knowledge/approved/torino_site_faq-tasi-domande-frequenti.md.. Need to split the file and then send to the llm
    - split the file but this should be added to the scrapper. I'm using 10K size to split manually




For now there in utils/query for the kb or for the agents(run_caf_crew.py). --query and write your question

KB is filled either manually
    - In Knowledge/raw you can put any .md file. It does have to have this list:
        ---
        topic: imu
        region: italy
        type: procedure
        created_by: john
        retrieved_at: 2025-05-12
        source: internal_notes
        ---
    - This tells the system what it is and is used as metadata for the kb
    - Then run the run_ingestion_crew.py with a file name to import the file

First the question will check the kb, if it doesn't find a good answer it will ask chectgpt, return the answer and put in /responses the qna. This can then be reviewed and checked later and then imported.

The question is first checked by the CAFFrontDeskAgent and then passed to the relevant agent for processing.

25/5/2025
    ingestion comes from marketing-ai-core

Failed to ingest
    imu_torino_sitepages.md
