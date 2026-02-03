# DSCI 551 Semester Project - Custom DataFrame Implementation

This project implements a custom DataFrame class from scratch with SQL-like operations, designed to parse and analyze CSV data. Built for my DSCI 551 course at USC, it demonstrates core data structure concepts and database operations without relying on pandas' built-in functionality.

## Features

- **Custom CSV Parser**: Reads and processes CSV files into a DataFrame structure
- **SQL-Style Operations**:
  - Projection (column selection)
  - Filtering (row selection with conditions)
  - Group By with aggregation functions (sum, mean, count, etc.)
  - Join operations (inner, left, right joins)
- **Data Analysis**: Applied to 2022-23 Golden State Warriors basketball statistics
- **Interactive Dashboard**: Streamlit app for visualizing results

## Tech Stack

- Python
- Streamlit
- Custom data structures (no pandas for core DataFrame logic)

## Usage

The main DataFrame class is implemented in `project.py`. To run the Streamlit dashboard:
```bash
streamlit run streamlitapp.py
```
Then you upload the 2 CSV files into the app. Now you're able to do SQL like functions on the data!

## Project Structure

- `project.py` - Core DataFrame implementation with all operations
- `streamlitapp.py` - Streamlit dashboard for demonstration
- Data files - 2022-23 Warriors statistics CSV & player CSV

## What I Learned

Building this from scratch gave me a deeper understanding of how dataframes actually work under the hood - memory management, indexing, and efficient data operations. It was challenging but really rewarding to implement joins and group-by logic without relying on existing libraries.
