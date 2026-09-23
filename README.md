# FastBox Delivery System

## Overview

A Python-based delivery simulation system that:

1. Reads warehouse, agent, and package data.
2. Assigns each package to the nearest agent.
3. Calculates delivery distance.
4. Aggregates agent statistics.
5. Calculates delivery efficiency.
6. Generates a JSON report.

## Architecture

- `schemas.py` - Pydantic data models and schema validation.
- `services.py` - Delivery and reporting business logic.
- `utils.py` - File handling and distance calculation.
- `main.py` - Application entry point.

## Installation

```bash
pip install -r requirements.txt