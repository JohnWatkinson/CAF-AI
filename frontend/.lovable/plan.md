

## Assistente IMU - Chat per Consulenza Fiscale

### 🎯 Contesto
Applicazione di consulenza fiscale IMU rivolta a:
- **Professionisti**: Commercialisti, CAF, consulenti fiscali
- **Cittadini**: Proprietari immobiliari che devono calcolare l'IMU

Tono: Istituzionale ma accessibile, come uno sportello comunale digitale.

---

### 🎨 Design Istituzionale

**Palette Colori:**
- **Primario**: Blu istituzionale (#1e3a5f) - come i portali dell'Agenzia delle Entrate
- **Secondario**: Blu chiaro (#3b82f6) - elementi interattivi
- **Sfondo**: Bianco (#ffffff) con grigio chiaro (#f8fafc)
- **Messaggi Utente**: Blu scuro con testo bianco
- **Messaggi Assistente**: Grigio neutro (#f1f5f9)
- **Testo**: Nero/grigio scuro per massima leggibilità

**Stile Visivo:**
- Design pulito e minimalista, niente fronzoli
- Icona professionale nell'header (simbolo IMU/casa stilizzata)
- Nessuna illustrazione cartoon - solo elementi grafici sobri
- Aspetto che ispira fiducia e competenza

---

### 📱 Struttura Pagina

**Header:**
- Icona casa/documento (simbolo IMU)
- Titolo: "Assistente IMU"
- Sottotitolo: "Calcolo Imposta Municipale"
- Pulsante "Nuova conversazione" (con icona refresh)

**Area Chat:**
- Messaggi utente: blu a destra
- Messaggi assistente: grigio a sinistra
- Rendering markdown (grassetto, elenchi)
- Scroll automatico
- Indicatore "Sto pensando..." durante l'attesa

**Input:**
- Campo testo grande: "Scrivi la tua domanda sull'IMU..."
- Pulsante "Invia" ben visibile
- Enter per inviare

**Footer:**
- "Powered by CAF-AI" discreto in basso

---

### ⚙️ Funzionalità

**Flusso Chat:**
1. Caricamento → invio automatico "Ciao" per avviare
2. Risposta di benvenuto dall'assistente
3. Conversazione naturale con session_id persistente
4. "Nuova conversazione" azzera tutto

**Connessione API:**
- URL da `VITE_API_URL`
- POST /chat con message e session_id
- Gestione errori dettagliata in italiano

**Accessibilità:**
- Font 18px minimo
- Bottoni 48px di altezza
- Alto contrasto
- Mobile responsive

---

### 📁 Componenti

- `ChatHeader` - intestazione con titolo e reset
- `ChatMessages` - area messaggi scrollabile
- `MessageBubble` - singolo messaggio con markdown
- `ChatInput` - input e pulsante invio
- `LoadingIndicator` - "Sto pensando..."
- `useChat` - hook per logica chat e API

