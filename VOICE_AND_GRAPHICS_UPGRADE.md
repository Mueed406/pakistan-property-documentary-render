# Evidence-based Hybrid Urdu Documentary Renderer

This project uses source-attributed real footage and code-driven motion graphics. Claims about the May 2026 Islamabad Cooperative Housing Society investigation are allegations attributed to contemporaneous reports, not convictions.

## Better voice setup (preferred: official Azure F0)
Microsoft Azure Speech F0 includes a 500,000-character/month free neural TTS allowance (subject to Microsoft terms). Use the Pakistani Urdu voice `ur-PK-AsadNeural`.

Create an Azure Speech **F0** resource through your own authorized Azure account and set two **GitHub Actions repository secrets**:
- `AZURE_SPEECH_KEY`: resource key
- `AZURE_SPEECH_REGION`: e.g. `eastus`, matching your resource

Never paste secrets into code, commits, chat, or issues. The GitHub workflow will detect the credentials and choose official neural Urdu speech. Without them it uses a *tuned* Piper offline voice for an **unapproved review copy**, not proof of natural narration.

## Current design
- Research and verification: Geo News May 8 2026; CDA Housing Schemes; SECP real estate warning.
- Audio chunk generation with native Urdu UTF-8 script and subtitle cues.
- Code-rendered ASS animations timed using recorded cue boundaries.
- FFmpeg cut assembly and original low-volume music mix.
- Human voice and factual review mandatory before publication.

Sources:
https://www.geo.tv/latest/663415-major-housing-fraud-exposed-in-islamabad-society
https://www.cda.gov.pk/housing-schemes
https://www.secp.gov.pk/wp-content/uploads/2025/02/Press-Release-Feb-7-Fraudulent-Real-Estate-Investment-Schemes.pdf

## Quality notes
Improving EQ, amplitude or noise variation does NOT reliably transform robotic Piper TTS into a human-like narrator. For that, a better trained voice model/service is required.
