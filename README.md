# CDCN_Covid19_BE

Backend for Covid19 NER tasks 

To run:
- First, make sure that: Tessaract with the Vietnamese Dictionary, Java 8 and Python 3.10 with Pip is installed on the system and is added to `PATH`

- Clone the repo
```
git clone --recurse <repo url>
cd <repo>
```
- Activate VirtualEnv (if desired) and install dependencies:
```
virtualenv -py python3.10 .
pip install -r requirements.txt
```
- Change directory to `src/` and start the API server
```
cd src/
uvicorn api:app
```

The model for NER should be installed automatically downloaded if it is not found during the first run
