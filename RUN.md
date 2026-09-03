# Run instructions

## Windows / Mac / Linux
1. Install Python 3.10+.
2. Open Terminal / Command Prompt in this folder.
3. Run:
   pip install -r requirements.txt
4. Then:
   streamlit run app.py

The browser will open the app.

The app searches PubMed at runtime for API-specific literature and contains a curated starter evidence base from FDA, ICH/EMA and PubMed reviews.

For a production deployment, add:
- a database of API physicochemical properties
- full-text/licensed literature retrieval
- citation-level RAG
- patent/regulatory retrieval
- excipient database with route/dosage-form constraints
- user accounts and saved projects
- PDF report export
- audit trail/versioning
