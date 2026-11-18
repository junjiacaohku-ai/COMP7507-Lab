<div align="center">

# COMP7507 Data Visualization — Labs

**Tableau exploration. Interactive dashboards. Visual storytelling. Network analysis.**

A collection of five completed lab assignments for **HKU COMP7507**, covering Tableau, Plotly Dash, dashboard design, implementation planning, and Gephi network visualization.

[![HKU COMP7507](https://img.shields.io/badge/HKU-COMP7507-6E56CF)](https://github.com/junjiacaohku-ai/COMP7507-Lab)
[![Labs](https://img.shields.io/badge/Labs-5-0072B2)](#2-labs)
[![Tableau](https://img.shields.io/badge/Tableau-Workbooks-E97627?logo=tableau&logoColor=white)](https://www.tableau.com/)
[![Plotly Dash](https://img.shields.io/badge/Plotly-Dash-3F4F75?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![Gephi](https://img.shields.io/badge/Gephi-Network_Analysis-2C2C2C)](https://gephi.org/)
[![GitHub stars](https://img.shields.io/github/stars/junjiacaohku-ai/COMP7507-Lab?style=social)](https://github.com/junjiacaohku-ai/COMP7507-Lab/stargazers)

[Overview](#1-overview) · [Labs](#2-labs) · [Repository Structure](#3-repository-structure) · [Quick Start](#4-quick-start) · [Notes](#5-notes)

</div>

---

<a id="1-overview"></a>
## 1. Overview

This repository archives my completed work, original lab handouts, supporting datasets, dashboards, screenshots, and planning documents for **HKU COMP7507 Data Visualization**.

The labs progress from basic visual exploration in Tableau to an interactive Plotly Dash narrative, a more advanced Tableau dashboard, a user-centred wine analytics application plan, and network visualization with Gephi. Original filenames and directory organization are preserved so each lab can be revisited as submitted.

**Course:** COMP7507, 2026–27 Semester 1  
**Author:** Cao Junjia

<a id="2-labs"></a>
## 2. Labs

| Lab | Topic | Main work | Files |
|---|---|---|---|
| **Lab 1** | Tableau basics and dataset exploration | Wine review exploration, foundational Tableau charts, and a packaged workbook containing the workbook data | [Workbook](<Lab1 - Getting Familiar with Tableau/Wine Overview Exploration.twbx>) · [Directory](<Lab1 - Getting Familiar with Tableau/>) |
| **Lab 2** | Plotly, Dash, and narrative structure | An interactive wine-origin dashboard with a country choropleth, dual-mode bar chart, price–rating density heatmap, linked filters, and dynamic summary statistics | [Dashboard code](<Lab2 - Ploty and Dash/web_visualization/>) · [Screenshot](<Lab2 - Ploty and Dash/lab2_dashboard_screenshot.png>) |
| **Lab 3** | Interactive Tableau dashboards | A more advanced Tableau workbook using the wine review dataset and a Tableau Hyper extract | [Workbook](<Lab3 – Building an Interactive Dashboard in Tableau/工作簿 1.twb>) · [Directory](<Lab3 – Building an Interactive Dashboard in Tableau/>) |
| **Lab 4** | Vibe coding and application design | A four-page implementation plan for **Wine Selection Assistant**, a three-stage Dash concept covering market exploration, candidate shortlisting, and review-based comparison | [Plan PDF](<Lab4_Vibe Coding (Wine Analytics Application)/Lab4_Final_Implementation_Plan.pdf>) · [Plan HTML](<Lab4_Vibe Coding (Wine Analytics Application)/Lab4_Final_Implementation_Plan.html>) |
| **Lab 5** | Network visualization with Gephi | Twitter network analysis with the original and filtered graph views, editable Gephi project, and node/edge data | [Gephi project](<Lab5 – Network Visualization with Gephi/Lab5.gephi>) · [Original view](<Lab5 – Network Visualization with Gephi/original.png>) · [Filtered view](<Lab5 – Network Visualization with Gephi/filtered.png>) |

### Lab 2 dashboard preview

![Interactive wine origin dashboard built with Plotly Dash](<Lab2 - Ploty and Dash/lab2_dashboard_screenshot.png>)

The completed dashboard asks how origin shapes wine style, price, and critic reputation. It preserves the global map while country selections drive the lower charts, handles missing prices per view, and applies a minimum sample-size threshold to the value ranking.

The course-provided example dashboard is also preserved in `example_dashboard/` for reference; the completed Lab 2 work is in `web_visualization/`.

<a id="3-repository-structure"></a>
## 3. Repository Structure

```text
COMP7507-Lab/
├── Lab1 - Getting Familiar with Tableau/
│   ├── Wine Overview Exploration.twbx      # Packaged Tableau workbook
│   ├── Wine Overview Exploration.twb       # Tableau workbook source
│   ├── data/                               # Wine reviews and category mapping
│   └── Lab1 handouts (PDF)
├── Lab2 - Ploty and Dash/
│   ├── web_visualization/                  # Completed interactive dashboard
│   │   ├── app.py                          # Dash layout, figures, and callbacks
│   │   ├── src/data_loader.py              # Data loading and cleaning
│   │   ├── assets/styles.css               # Dashboard styling
│   │   ├── data/                           # Included CSV datasets
│   │   └── requirements.txt
│   ├── example_dashboard/                  # Course-provided reference app
│   ├── lab2_dashboard_screenshot.png
│   └── Lab2 handouts and reference archive
├── Lab3 – Building an Interactive Dashboard in Tableau/
│   ├── 工作簿 1.twb                         # Completed Tableau workbook
│   ├── winemag-data-with-year+.hyper       # Tableau data extract
│   ├── data/
│   └── Lab3 handout (PDF)
├── Lab4_Vibe Coding (Wine Analytics Application)/
│   ├── Lab4_Final_Implementation_Plan.pdf  # Final four-page design plan
│   ├── Lab4_Final_Implementation_Plan.html # Browser-readable plan
│   └── Original Lab4 brief (HTML)
├── Lab5 – Network Visualization with Gephi/
│   ├── Lab5.gephi                          # Editable Gephi project
│   ├── original.png / filtered.png         # Before-and-after graph views
│   ├── data/                               # Twitter nodes and edges CSV files
│   └── Lab5 handout (PDF)
└── README.md
```

<a id="4-quick-start"></a>
## 4. Quick Start

### Clone

```bash
git clone https://github.com/junjiacaohku-ai/COMP7507-Lab.git
cd COMP7507-Lab
```

The repository includes the full CSV datasets and Tableau workbook files, so the initial clone may take a little longer than a code-only repository.

### Run the Lab 2 dashboard

**Requirements:** Python 3.9+ and the packages in `requirements.txt`.

```bash
cd "Lab2 - Ploty and Dash/web_visualization"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:8050** in a browser. All required data is already included under `web_visualization/data/`; no separate download or API credentials are needed.

The dashboard supports:

- Multi-country and wine-category filtering, plus a price-range slider.
- A global country-rating choropleth and dynamic selection summaries.
- Switchable style-mix and underrated-province bar views.
- A log-price versus critic-points density heatmap with an OLS reference trend.

### Open the other labs

- **Lab 1:** Open `Wine Overview Exploration.twbx` in Tableau. The unpacked `.twb` and source CSV files are also included.
- **Lab 3:** Open `工作簿 1.twb` in Tableau. If Tableau asks for the data source, reconnect it to the included `winemag-data-with-year+.hyper` file in the same directory.
- **Lab 4:** Open the implementation plan PDF for the final formatted version, or either HTML file in a browser. This lab contains the original brief and design plan, not a completed application.
- **Lab 5:** Open `Lab5.gephi` in Gephi. The source node and edge tables are in `data/`, and the two PNG files record the original and filtered views.

<a id="5-notes"></a>
## 5. Notes

- These files are individual coursework submissions shared as a learning portfolio; please do not reuse the answers as your own coursework.
- Original course handouts, starter materials, and reference examples retain their respective terms and licences.
- The wine review data originates from the course-provided Wine Reviews dataset; the Lab 5 node and edge files are also course-provided data.
- Lab directories retain their original standalone data copies rather than relying on files elsewhere in the repository.
- Python virtual environments, bytecode caches, and macOS `.DS_Store` files are excluded from Git. All source code, dependency lists, datasets, documents, workbooks, projects, and images are included.
- The Lab 2 dashboard is a local teaching application, not a deployed or production-hardened web service.

---

<div align="center">

**COMP7507 — From visual exploration to interactive and network-based storytelling.**

HKU · Data Visualization · Tableau + Plotly Dash + Gephi

</div>
