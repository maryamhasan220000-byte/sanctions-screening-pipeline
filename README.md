# Sanctions Screening Pipeline

A Python-based file pipeline that cross-references 
user-provided watchlists against official government 
sanctions data, producing tiered match reports with 
full audit logging.

## What It Does

- Reads a watchlist CSV of names to screen
- Loads official sanctions data (OFAC SDN List, with 
  EU and UN support configurable)
- Runs fuzzy name matching with configurable thresholds
- Produces exact match and partial match CSV reports
- Generates a human-readable summary report
- Logs all pipeline activity to structured JSON logs

## Why I Built This

Built as part of my transition into data engineering. 
The domain knowledge comes from my MSc Financial 
Economics dissertation on Lebanon's 2019 financial 
crisis, which involved research into capital controls 
and financial sanctions in distressed economies.

This project applies that domain knowledge to a real 
compliance problem — sanctions screening — which is 
highly relevant to the Dutch financial sector where 
I am currently based.

## Tech Stack

- Python 3
- Standard library only — csv, json, os, datetime
- difflib for fuzzy name matching
- Config-driven architecture via config.json

## Data Sources

- OFAC SDN List (US Treasury) — publicly available
- EU Consolidated Sanctions List — coming soon
- UN Security Council List — coming soon

## How To Run

1. Clone the repository
2. Add your watchlist to data/input/watchlist.csv
3. Add sanctions files to data/sanctions/
4. Update config.json with correct filepaths
5. Run: python main.py

## Project Structure

sanctions_pipeline/
├── config.json          # pipeline configuration
├── main.py              # entry point
├── loader.py            # data loading
├── matcher.py           # name matching engine
├── reporter.py          # output generation
├── logger.py            # structured JSON logging
├── data/
│   ├── input/           # watchlist goes here
│   ├── sanctions/       # government lists go here
│   └── output/          # reports generated here
└── logs/                # pipeline logs
