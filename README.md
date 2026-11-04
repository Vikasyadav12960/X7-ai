\# X7 AI



\*\*A local-first AI-assisted URL security scanner.\*\*



X7 AI analyzes submitted URLs using rule-based security checks and provides additional explanations through a locally running AI model.



\## Features



\- Rule-based URL risk detection

\- Risk scoring from 0 to 100

\- Safe, suspicious and dangerous classifications

\- Detection reasons for flagged URLs

\- Local AI explanations powered by Ollama and Hermes 3

\- SQLite scan history

\- Dark-themed web interface

\- AI fallback when the local model is unavailable



\## Technology Stack



| Component | Technology |

|---|---|

| Backend | Python, Flask |

| Frontend | HTML, CSS |

| Database | SQLite |

| AI runtime | Ollama |

| AI model | Hermes 3 |



\## Project Structure



```text

X7-ai/

├── app.py

├── ai.py

├── checker.py

├── db.py

├── requirements.txt

├── README.md

├── .gitignore

└── templates/

&#x20;   └── index.html

```



\## Requirements



\- Python 3.10 or newer

\- Ollama

\- Hermes 3 model



\## Installation



Clone the repository:



```bash

git clone https://github.com/Vikasyadav12960/X7-ai.git

cd X7-ai

```



Create and activate a virtual environment.



\*\*Windows PowerShell:\*\*



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

pip install -r requirements.txt

```



\## Configure Local AI



Install Ollama from:



https://ollama.com/



Download the model:



```bash

ollama pull hermes3

```



Start Ollama and make sure its local API is available at:



```text

http://127.0.0.1:11434

```



X7 AI uses the local `hermes3:latest` model for scan explanations.



\## Run the Application



Start the Flask application:



```powershell

python app.py

```



Open:



```text

http://127.0.0.1:5000

```



Paste a URL into the scanner and submit it to view the result.



\## Risk Classification



| Risk Score | Classification |

|---|---|

| 0–29 | Safe |

| 30–59 | Suspicious |

| 60–100 | Dangerous |



The scanner uses heuristic indicators such as IP-based URLs, brand impersonation, suspicious TLDs, URL shorteners, and suspicious keywords.



Scores are capped at 100.



\## AI Analysis



The rule-based detection engine determines the risk score and verdict.



Hermes 3 provides an explanation of the detected indicators. It does not determine or override the scanner's verdict.



If local AI analysis is unavailable, the rule-based result remains available.



\## Database



Scan history is stored locally in SQLite.



The local database file is excluded from Git to prevent personal scan history from being published.



\## Security Disclaimer



X7 AI is an experimental security-analysis project.



Its heuristic checks can produce false positives and false negatives. A safe classification does not guarantee that a URL is legitimate or free from threats.



Always verify important links through trusted sources. Do not enter sensitive information into suspicious websites.



\## License



No license has been specified yet.
