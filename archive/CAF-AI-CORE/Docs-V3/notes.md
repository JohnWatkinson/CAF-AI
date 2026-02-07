


CAF
    https://www.amministrazionicomunali.it/main/



ngrok - github
    Google aunthenticated
    Token: 2wuaVea7nSIIA9odmm9yKrN6Bmg_47bHKRQuqSaTPzrE7KSEp
    https://c0a9-5-90-97-148.ngrok-free.app
    ep_2wubx7QFiq3P25EhSroKj2MTxN4


    curl -X POST https://c0a9-5-90-97-148.ngrok-free.app/ask \
      -H "Content-Type: application/json" \
      -d '{"query": "Chi deve pagare l IMU a Torino?"}'

Vercel
    Environment Vars
        NEXT_PUBLIC_API_URL: https://c0a9-5-90-97-148.ngrok-free.app
    Public:
        https://caf-ai-core.vercel.app


Code
    Frontend
        .env.local
            NEXT_PUBLIC_API_URL=https://c0a9-5-90-97-148.ngrok-free.app





V5
Imports .md and json files and classifies them
/knowledge
    /raw - json, md
    /qnas - thse are json comeing from either the query_caf_agent.py or from the frontend. We can then review the qna

(.venv) john@CAPRICA:~/AI/CAF-AI-CORE/Code$ python knowledge_ingestion/run_ingestion_crew.py --file knowledge/raw/italy_tax_deadlines_2025.md
$ python knowledge_ingestion/run_ingestion_crew.py --file knowledge/raw/imu_formula_calculation_guide_2025-05-12.md
    - this imports the file into the kb..

$ python tests/list_ids_caf_kb.py - to double check

To query just the db
$ python tests/query_caf_kb.py --query "Quando si paga l'IMU?" --topic imu --region torino

$ python run_caf_crew.py --query "Qual è l’età pensionabile in Italia per gli uomini e per le donne?"
$ python run_caf_crew.py --query "Qual è il codice tributo per pagare l'IMU su un terreno agricolo a Torino?"



### 🔁 When someone wants to test

For the frntend on a webpage
1. Start backend
    $ uvicorn main:app --host 0.0.0.0 --port 8000
2. Start ngrok
    $ ngrok http 8000
    Copy this link to the NEXT_PUBLIC_API_URL environment variable in Vercel
    https://c0a9-5-90-97-148.ngrok-free.app
    https://6b65-5-90-97-148.ngrok-free.app
    https://b1fd-5-90-100-250.ngrok-free.app
3. Push changes to update vercel
    - to update
4. Frontend
    - https://caf-ai-core-cteq0e460-john-watkinsons-projects.vercel.app

- If it doesn't find the answer in the kb, it creates the qna in /home/john/AI/CAF-AI-CORE/Code/knowledge/responses
- Check and then run to ingest it into the kb
- python knowledge_ingestion/run_ingestion_crew.py --file knowledge/responses/...

before i changed the md file to json and then imported that.. not sure why it changed...





(.venv) john@CAPRICA:~/AI/CAF-AI-CORE/Code$ python run_caf_crew.py --query "Calcola IMU con rendita catastale 1000, coefficiente 160, aliquota 0.76%, possesso 50%, 183 giorni, sconto 25%"
🔍 Query: Calcola IMU con rendita catastale 1000, coefficiente 160, aliquota 0.76%, possesso 50%, 183 giorni, sconto 25%

[LLM] Sending prompt to OpenAI...
🔍 Query: Calcola IMU con rendita catastale 1000, coefficiente 160, aliquota 0.76%, possesso 50%, 183 giorni, sconto 25%

🤖 Generating answer with LLM...
[LLM] Sending prompt to OpenAI...

💬 Answer:
Per calcolare l'IMU per un immobile con le caratteristiche da te fornite, seguiamo i passaggi della procedura:

1. Calcoliamo prima la rendita catastale rivalutata: 1.000€ (rendita catastale) x 1.05 = 1.050€.

2. Poi, calcoliamo la base imponibile: 1.050€ (rendita rivalutata) x 160 (coefficiente) = 168.000€.

3. Calcoliamo l'IMU senza considerare lo sconto. Ricorda che l'aliquota deve essere espressa in forma decimale, quindi 0,76% diventa 0,0076. Ecco la formula da applicare:

    IMU = (Base imponibile x Aliquota x % possesso x giorni/365)
    = (168.000€ x 0,0076 x 0,50 x 183/365)
    = 324,07€.

4. Infine, applichiamo lo sconto del 25% sull'importo dell'IMU calcolato sopra:
    IMU scontata = IMU x (100 - sconto)/100
    = 324,07€ x (100 - 25)/100
    = 243,05€.

Dunque, l’IMU da pagare per il tuo immobile è di 243,05€.

Ricorda che la prima rata IMU è dovuta entro il 16 giugno (acconto) e la seconda entro il 16 dicembre (saldo), se devi pagare l'IMU per tutto l'anno solare.

Si noti che questa stima è standard e può variare a seconda di specifiche normative comunali. Per informazioni dettagliate o esenzioni specifiche, ti consiglio di contattare il comune in cui si trova l'immobile o un professionista fiscale.


18/5/2025

Ingestion
    Files in the inbox folder, can add meta data manually. move to staged. should review it and then move to approved
    (.venv) john@CAPRICA:~/AI/CAF-AI-CORE/Code$ python ingestion/run_ingestion_crew.py --file knowledge/staged/imu_torino_sitepages.md
    python run_ingestion_crew.py --file knowledge/staged/imu_torino_sitepages.md --overwrite


    (.venv) john@CAPRICA:~/AI/CAF-AI-CORE/Code$ python ingestion/run_ingestion_crew.py --file knowledge/staged/pension_italy_sono_una_donna_quando_potrò_andare_in_pensione__2025-05-14.md

Test
(.venv) john@CAPRICA:~/AI/CAF-AI-CORE/Code$ python ingestion/query_caf_kb.py --query "Qual è il codice catastale di Torino?"
