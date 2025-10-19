# dash-website

Sports Analytics Website - Technical Specifications
1. Executive Summary
This document outlines the technical architecture for a collaborative sports analytics website designed to minimize friction for Python-focused developers. The system prioritizes ease of contribution, cost-effective data storage, and rapid metric development.
Key Design Principles:

Python-first development (minimal frontend skills required)
Low-friction page creation (drop a file, get a page)
Cost-effective storage for large tabular datasets
Support for R integration (nflverse package)
Self-service for internal users


2. Technology Stack
2.1 Frontend

Framework: Dash (Plotly)
UI Components: Dash Bootstrap Components
Rationale: Pure Python development, built-in multi-page support, excellent for interactive analytics with complex controls

2.2 Backend

API Framework: FastAPI
Purpose: Handle heavy data queries, R service integration, data preprocessing
Rationale: Python-native, async support, auto-generated API docs

2.3 Data Layer

Primary Database: PostgreSQL (metadata, user info, small reference tables)
Analytics Data Storage: Parquet files in object storage
Query Engine: DuckDB (in-process analytics on Parquet files)
Rationale: Cost-effective for large tabular data, excellent query performance, no expensive SQL cluster needed

2.4 R Integration

Approach: Scheduled jobs + file storage (MVP)
Future Option: Plumber API for real-time queries
Rationale: Minimal complexity to start, can upgrade as needed

2.5 Hosting & Infrastructure

Options (in order of complexity):

Local Development (start here)
Railway/Render (free tier → paid, easiest deployment)
DigitalOcean App Platform (simple, affordable)
AWS/GCP (most flexible, higher learning curve)