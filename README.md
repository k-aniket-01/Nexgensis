# FastBox Delivery System

A Python-based delivery simulation system that assigns packages to the nearest delivery agent, calculates delivery distances, generates agent-level statistics, and produces structured JSON reports.

The project is implemented with a focus on **clean architecture, reusable functions, dynamic processing, input validation, type safety, and automated testing**.

---

## Author

**Aniket Khomane**

* khomaneaniket9420@gmail.com
* Python & Backend Developer

---

## Table of Contents

* [Project Overview](#project-overview)
* [Problem Statement](#problem-statement)
* [Features](#features)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Application Flow](#application-flow)
* [Architecture](#architecture)
* [Delivery Algorithm](#delivery-algorithm)
* [Distance Calculation](#distance-calculation)
* [Efficiency Calculation](#efficiency-calculation)
* [Input Format](#input-format)
* [Output Format](#output-format)
* [Design Approach](#design-approach)
* [Validation](#validation)
* [Installation](#installation)
* [Running the Application](#running-the-application)
* [Running Tests](#running-tests)
* [Error Handling](#error-handling)
* [Complexity](#complexity)
* [Assumptions](#assumptions)
* [Design Decisions](#design-decisions)
* [Future Improvements](#future-improvements)
* [Author](#author)

---

# Project Overview

FastBox Delivery System is a Python application that simulates package deliveries.

The system receives information about:

* Warehouses
* Delivery agents
* Packages

For every package, the system determines the closest delivery agent to the package's warehouse.

The selected agent then performs the following delivery route:

```text
Agent → Warehouse → Destination
```

The application calculates the total distance traveled by each agent and generates statistics based on their deliveries.

---

# Problem Statement

The system needs to process a set of warehouses, agents, and packages.

For each package:

1. Identify the warehouse associated with the package.
2. Calculate the distance from every available agent to that warehouse.
3. Select the nearest agent.
4. Calculate the delivery distance.
5. Assign the package to the selected agent.
6. Update the agent's delivery statistics.
7. Calculate the agent's delivery efficiency.
8. Generate a final JSON report.

The solution should be dynamic and should not depend on hardcoded agent IDs, warehouse IDs, package counts, or test-case counts.

---

# Features

* Dynamic JSON input processing
* Support for a single JSON file
* Support for processing multiple JSON files
* Pydantic-based data validation
* Input normalization
* Euclidean distance calculation
* Dynamic nearest-agent selection
* Package assignment
* Agent statistics aggregation
* Efficiency calculation
* Automatic report generation
* Error handling for invalid input
* Automated unit tests
* Clean separation of responsibilities
* No hardcoded agent, warehouse, or package IDs

---

# Technology Stack

| Technology   | Purpose                       |
| ------------ | ----------------------------- |
| Python 3.10+ | Application development       |
| Pydantic     | Data modelling and validation |
| Pytest       | Automated testing             |
| JSON         | Input and output format       |
| pathlib      | File and directory handling   |
| argparse     | Command-line interface        |
| math         | Distance calculation          |

The project primarily uses Python's standard library along with Pydantic and Pytest.

---

# Project Structure

```text
delivery_system/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── services.py
│   └── utils.py
│
├── data/
│   ├── base_case.json
│   │
│   └── test_cases/
│       ├── test_case_1.json
│       ├── test_case_2.json
│       ├── test_case_3.json
│       ├── test_case_4.json
│       ├── test_case_5.json
│       ├── test_case_6.json
│       ├── test_case_7.json
│       ├── test_case_8.json
│       ├── test_case_9.json
│       └── test_case_10.json
│
├── reports/
│   └── Generated JSON reports
│
├── tests/
│   ├── __init__.py
│   ├── test_distance.py
│   ├── test_delivery.py
│   └── test_report.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Application Flow

The complete application flow is:

```text
                    Input JSON
                        │
                        ▼
                   load_json()
                        │
                        ▼
                Normalize Input
                        │
                        ▼
                Pydantic Validation
                        │
                        ▼
                Delivery Simulation
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
      Find Nearest Agent      Calculate Distance
             │                     │
             └──────────┬──────────┘
                        ▼
                Update Statistics
                        │
                        ▼
                Calculate Efficiency
                        │
                        ▼
                  Build Report
                        │
                        ▼
                   save_json()
                        │
                        ▼
                  JSON Report
```

---

# Architecture

The application follows a simple layered architecture.

```text
┌─────────────────────────────┐
│           main.py           │
│     Application Flow        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         services.py         │
│      Business Logic         │
└──────┬────────────────┬─────┘
       │                │
       ▼                ▼
┌─────────────┐   ┌─────────────┐
│  schemas.py │   │   utils.py  │
│ Data Models │   │  Utilities  │
└─────────────┘   └─────────────┘
       │                │
       └───────┬────────┘
               ▼
            JSON Data
```

### `main.py`

Responsible for application orchestration.

It handles:

* Command-line arguments
* Input file/directory selection
* Calling the required service functions
* Top-level error handling

It does not contain the core delivery algorithm.

---

### `schemas.py`

Contains Pydantic models used to represent the application's internal data.

Main schemas:

```text
PackageSchema
AgentSchema
WarehouseSchema
DeliveryInputSchema
AgentStatsSchema
DeliveryReportSchema
```

The schemas provide:

* Type validation
* Required-field validation
* Structured data
* Consistent internal representation

---

### `services.py`

Contains the application's business logic.

Important functions include:

```text
normalize_input()
normalize_locations()
normalize_packages()
find_nearest_agent()
calculate_delivery_distance()
simulate_delivery()
calculate_efficiencies()
build_report()
```

---

### `utils.py`

Contains generic reusable functionality.

```text
load_json()
save_json()
calculate_distance()
```

The distance calculation is kept in a reusable function so that the formula is not duplicated throughout the application.

---

# Delivery Algorithm

For every package, the system performs the following operations:

```text
1. Find package warehouse
        ↓
2. Get warehouse location
        ↓
3. Calculate distance from every agent
        ↓
4. Select nearest agent
        ↓
5. Calculate Agent → Warehouse
        ↓
6. Calculate Warehouse → Destination
        ↓
7. Add both distances
        ↓
8. Assign package to agent
        ↓
9. Update agent statistics
```

The application repeats this process for every package in the input.

---

# Distance Calculation

The system uses Euclidean distance.

Given two points:

```text
Point A = (x1, y1)
Point B = (x2, y2)
```

the distance is:

```text
distance = √((x2 - x1)² + (y2 - y1)²)
```

The implementation uses Python's `math.hypot()`:

```python
math.hypot(
    x2 - x1,
    y2 - y1,
)
```

This calculation is centralized in:

```text
app/utils.py
```

through:

```python
calculate_distance()
```

---

# Delivery Distance

The total delivery distance for a package is:

```text
Agent → Warehouse
+
Warehouse → Destination
```

For example:

```text
Agent A1      = (5, 5)
Warehouse W1  = (0, 0)
Destination   = (30, 40)
```

Agent to warehouse:

```text
√((5 - 0)² + (5 - 0)²)
= 7.07
```

Warehouse to destination:

```text
√((30 - 0)² + (40 - 0)²)
= 50.00
```

Total:

```text
7.07 + 50.00
= 57.07
```

---

# Nearest Agent Selection

The nearest agent is selected dynamically.

The implementation does not contain hardcoded agent IDs such as:

```text
A1
A2
A3
```

Instead, all agents are evaluated.

Conceptually:

```text
Agent A1 → Warehouse = 10.5
Agent A2 → Warehouse = 25.3
Agent A3 → Warehouse = 7.8

Nearest Agent = A3
```

The implementation uses Python's `min()` with a key function.

This allows the application to work with any number of agents.

---

# Efficiency Calculation

After all packages have been processed:

```text
efficiency =
    total_distance / packages_delivered
```

For example:

```text
Total distance     = 100
Packages delivered = 4

Efficiency = 100 / 4
           = 25
```

The agent with the lowest distance-per-package value is selected as the `best_agent` in the generated report.

Agents with zero deliveries receive:

```json
"efficiency": null
```

to avoid division by zero.

---

# Input Normalization

The application separates the external JSON structure from its internal data model.

For example, warehouse information may be represented as:

```json
{
    "warehouses": {
        "W1": [0, 0],
        "W2": [50, 75]
    }
}
```

The application normalizes this into structured objects such as:

```text
WarehouseSchema
    ├── id
    └── location
```

This means the business logic does not need to know exactly how the original JSON represents the warehouse data.

The flow becomes:

```text
External JSON
     ↓
Normalization
     ↓
Pydantic Models
     ↓
Business Logic
```

This keeps the service layer cleaner and easier to maintain.

---

# Validation

Validation is performed at multiple levels.

## Schema Validation

Pydantic validates:

* Required fields
* Data types
* Coordinate structure
* Non-empty identifiers
* Basic field constraints

## Business Validation

The service layer validates:

* Duplicate warehouse IDs
* Duplicate agent IDs
* Duplicate package IDs
* Missing required sections
* Packages referencing unknown warehouses
* Invalid input structures

This separates:

```text
Data validation
```

from:

```text
Business-rule validation
```

---

# Dynamic Processing

The application avoids hardcoding:

* Agent IDs
* Warehouse IDs
* Package IDs
* Number of agents
* Number of warehouses
* Number of packages
* Number of test cases

For example, the code does not depend on:

```python
"A1"
"A2"
"A3"
```

or:

```python
range(1, 11)
```

Instead, the application discovers the data dynamically.

This means new agents, warehouses, packages, or test cases can be added without modifying the core business logic.

---

# Processing Multiple Test Cases

The application can process a complete directory of JSON files.

For example:

```text
data/test_cases/
├── test_case_1.json
├── test_case_2.json
├── test_case_3.json
└── ...
```

Running:

```bash
python -m app.main data/test_cases
```

automatically discovers all `.json` files.

Reports are generated as:

```text
reports/
├── test_case_1_report.json
├── test_case_2_report.json
├── test_case_3_report.json
└── ...
```

Adding a new JSON file to the directory does not require modifying the Python code.

---

# Output Format

The generated report contains agent-level statistics.

Example:

```json
{
    "agents": {
        "A1": {
            "packages_delivered": 2,
            "total_distance": 78.28,
            "efficiency": 39.14
        },
        "A2": {
            "packages_delivered": 2,
            "total_distance": 72.24,
            "efficiency": 36.12
        },
        "A3": {
            "packages_delivered": 1,
            "total_distance": 14.14,
            "efficiency": 14.14
        }
    },
    "best_agent": "A3"
}
```

The values depend on the input dataset.

---

# Installation

## Prerequisites

Python 3.10 or higher is recommended.

Check your Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

---

# Clone the Repository

Clone the repository:

```bash
git clone https://github.com/k-aniket-01/Nexgensis.git
```

Navigate into the project:

```bash
cd delivery_system
```

---

# Create Virtual Environment

## Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

## Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

# Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

# Running the Application

## Process One Test Case

```bash
python -m app.main data/test_cases/test_case_1.json
```

A report will be generated inside:

```text
reports/
```

---

## Process All Test Cases

```bash
python -m app.main data/test_cases
```

The application automatically processes all JSON files in the directory.

---

## Process Base Case

```bash
python -m app.main data/base_case.json
```

---

# Custom Output Location

A custom output directory can be provided:

```bash
python -m app.main data/test_cases --output results
```

Reports will then be generated inside:

```text
results/
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Run with detailed output:

```bash
pytest -v
```

The test suite covers the core functionality of the application.

---

# Testing Strategy

The project uses unit tests to verify individual pieces of business logic.

## Distance Tests

`tests/test_distance.py`

Tests:

* Distance between two different points
* Distance between identical points

## Delivery Tests

`tests/test_delivery.py`

Tests:

* Nearest-agent selection
* Delivery distance calculation

## Report Tests

`tests/test_report.py`

Tests:

* Efficiency-based agent selection
* Report generation

Testing individual functions makes it easier to identify which part of the application is failing.

---

# Error Handling

The application handles common input errors such as:

```text
Input file does not exist
Invalid JSON
Missing warehouses
Missing agents
Missing packages
Invalid coordinates
Duplicate IDs
Unknown warehouse references
Invalid package structure
```

Errors are reported with meaningful messages instead of allowing unexpected exceptions to propagate through the application.

---

# Complexity

Let:

```text
P = number of packages
A = number of agents
```

For every package, the system calculates the distance from every agent to the package's warehouse.

Therefore, the primary simulation complexity is:

```text
O(P × A)
```

For example, with:

```text
100 packages
10 agents
```

the nearest-agent calculation requires approximately:

```text
100 × 10 = 1,000
```

distance comparisons.

For the assignment's expected data sizes, this approach is simple and appropriate.

For very large datasets, spatial indexing techniques such as KD-trees could be considered.

---

# Design Principles

The project follows several software engineering principles.

## Separation of Concerns

Each module has a specific responsibility.

```text
main.py
    Application flow

schemas.py
    Data models and validation

services.py
    Business logic

utils.py
    Generic reusable functionality
```

---

## DRY — Don't Repeat Yourself

Repeated logic is extracted into reusable functions.

For example, the Euclidean distance calculation exists only in:

```text
calculate_distance()
```

rather than being duplicated in multiple places.

---

## Single Responsibility

Functions are kept focused on one primary task.

For example:

```text
find_nearest_agent()
```

is responsible for finding the nearest agent.

It does not also write files or generate reports.

---

## Dynamic Design

The system does not depend on fixed:

```text
Agent IDs
Warehouse IDs
Package IDs
Package counts
Test-case counts
```

This allows the application to process different datasets without changing the business logic.

---

# Why Pydantic?

Pydantic is used to define structured internal data models.

For example:

```python
class PackageSchema(BaseModel):
    id: str
    warehouse: str
    destination: tuple[float, float]
```

This provides:

* Type validation
* Structured data
* Clear contracts between application layers
* Easier testing
* Easier serialization

Although this project does not use FastAPI, Pydantic is useful independently for data modelling and validation.

---

# Why Not Use a Database?

The assignment provides JSON input files and requires JSON output.

A database would add unnecessary complexity because the current problem does not require:

* Persistent application state
* Concurrent writes
* Querying large datasets
* Transactions
* User management

Therefore, JSON is sufficient for the scope of this assignment.

---

# Why Not Build a REST API?

The assignment is focused on Python programming and data processing rather than API development.

Adding FastAPI would introduce additional components without solving a requirement of the assignment.

The business logic is nevertheless separated into services so that it could later be exposed through an API if required.

---

# Assumptions

The implementation follows these assumptions:

1. Coordinates are two-dimensional `(x, y)` points.
2. Euclidean distance is used.
3. A package is assigned to the agent closest to its warehouse.
4. Delivery distance is calculated as:

```text
Agent → Warehouse → Destination
```

5. Each package is processed independently.
6. An agent can deliver multiple packages.
7. There is no vehicle capacity restriction.
8. There is no delivery time-window restriction.
9. There is no package priority.
10. There is no route optimization between multiple packages.
11. Efficiency is calculated as:

```text
total distance / packages delivered
```

12. Agents with zero deliveries have `null` efficiency.

---

# Assignment Sample Data Note

The implementation follows the mathematical rules defined by the assignment:

```text
Agent → Warehouse → Destination
```

using Euclidean distance for each segment.

If any sample output in the assignment document differs from the result calculated from the provided input and formula, the implementation follows the defined algorithm and actual input data rather than hardcoding the sample output.

This keeps the implementation deterministic and data-driven.


# Complete Execution Flow

The complete workflow can be summarized as:

```text
                 User
                  │
                  ▼
        python -m app.main
                  │
                  ▼
            Read JSON
                  │
                  ▼
         Normalize Input
                  │
                  ▼
        Pydantic Validation
                  │
                  ▼
        For each package
                  │
                  ▼
        Find package warehouse
                  │
                  ▼
        Find nearest agent
                  │
                  ▼
      Agent → Warehouse
                  │
                  ▼
      Warehouse → Destination
                  │
                  ▼
        Update agent stats
                  │
                  ▼
       Calculate efficiency
                  │
                  ▼
          Build report
                  │
                  ▼
          Save JSON file
```

---

# Conclusion

The FastBox Delivery System demonstrates a clean Python implementation for a data-processing and simulation problem.

The solution focuses on:

* Clean project structure
* Reusable functions
* Pydantic data validation
* Separation of concerns
* Dynamic processing
* Avoidance of unnecessary hardcoding
* Unit testing
* Clear input/output handling

The implementation is intentionally kept simple enough for the assignment while following practices that can be extended into a larger backend application.
