# rcp-detectors

# Intelligent ILI Data Alignment & Corrosion Growth Analysis

This project presents an automated system for aligning In-Line Inspection (ILI) datasets collected at different times and analyzing corrosion growth in oil & gas pipelines.

The solution replaces a traditionally manual, time-consuming engineering process with a scalable, explainable, and auditable workflow.

---

## Problem Statement
ILI tools detect thousands of pipeline anomalies per inspection run.  
Comparing defects across multiple inspections is challenging due to:
- Odometer drift
- Tool speed variation
- Reference point inconsistencies
- Defect evolution over time

Manual alignment can take weeks and is error-prone.

---

## Solution Overview
The system performs:

1. **Reference-based alignment**
   - Uses fixed pipeline landmarks (girth welds, valves) as anchors
   - Applies piecewise distance correction

2. **Anomaly matching**
   - Matches defects across runs using distance, clock position, and geometry
   - Assigns confidence scores to each match

3. **Growth rate estimation**
   - Computes depth, length, and width growth for carried-over defects
   - Flags new and missing anomalies

4. **Explainable visualization**
   - Interactive diagrams showing alignment and match confidence

---

## Key Features
- Physics- and rules-based alignment
- Confidence-aware matching (no forced matches)
- Multi-run defect trajectory support
- Interactive Plotly visualizations
- Designed for regulatory explainability

---

## Repository Structure
