# Predictive Viability Index (PVI) — Greenhouse Renewable Systems

Complete research package for the manuscript prepared for **AgriEngineering** (MDPI), Special Issue on energy-efficient systems and CO₂ mitigation in agriculture.

## Author
**Hugo Gaspar Hernández Palma**  
Faculty of Engineering, Corporación Universitaria Iberoamericana, Bogotá, Colombia  
Email: hugo.hernandez@docente.ibero.edu.co

## Repository structure
```
manuscript.tex          Full MDPI AgriEngineering manuscript
Definitions/            Official MDPI LaTeX class (unmodified)
figures/                Publication figures (JPG)
data/                   Full experimental dataset
src/                    Reproducible pipeline
README.md, LICENSE, requirements.txt
```

## Dataset (`data/`)
| File | Description |
|------|-------------|
| `greenhouse_load_hourly.csv` | 8,760 h illustrative greenhouse electrical load |
| `price_path_{low,base,high}.csv` | Energy-price paths by volatility regime |
| `configurations.csv` | Six PV / hybrid technology configurations |
| `assumptions.json` | Techno-economic and emission parameters |
| `ml_training_samples.csv` | 1,800 Monte Carlo evaluation samples |
| `pvi_ranking_summary.csv` | Configuration-level PVI ranking |
| `volatility_sensitivity.csv` | Option-value share by volatility regime |
| `ml_performance_metrics.csv` | AUC, Brier, log-loss |
| `co2_illustration.json` | Indicative avoided CO₂ for mid-scale PV |
| `dataset_metadata.json` | Dataset descriptor |

## Pipeline
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/pvi_pipeline.py
```

## Compile manuscript
Use a TeX distribution with the local `Definitions/` folder (or Overleaf):
```bash
pdflatex manuscript.tex
```
Do **not** modify files under `Definitions/`; they are the official MDPI class.

## Licence
- Code (`src/`): MIT
- Data: research use with attribution; recalibrate before operational decisions
- Manuscript: journal open-access licence applies upon acceptance

## Citation
Cite the published AgriEngineering article when available; until then cite this repository and the author.
