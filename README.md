<div align="center">
  <h1>Automatic Generation of <br> Study Texts from Lecture Slides</h1>
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain" />
  <img src="https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg?style=for-the-badge" alt="CC BY 4.0 License" />
</div>

<br/>
<div align="center">A pipeline that employs specialized components to convert lecture slide decks into grounded study texts.</div>
<br/>

<div align="center">
  <img src='arch.png'></img>
</div>


## Getting Started

1. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env and set your OPENROUTER_API_KEY
   ```

2. **Run the pipeline:**
   ```bash
   uv sync --group notebook
   uv run jupyter lab main.ipynb
   ```
   Models and run parameters are configured in the notebook. Outputs are written to `results/`.


## Project Structure
- `main.ipynb`: entry point.
- `pipeline/`: agents (`nodes.py`), orchestration (`graph.py`), writer (`compose.py`), prompts, LLM client, disk cache and PDF export.
- `runs.py`: experiment tracing.
- `data/`: lecture material used in the paper.