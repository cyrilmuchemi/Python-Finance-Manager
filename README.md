# Personal Finance Manager

A command-line personal finance management application built with Python. Track income and expenses, manage category-based budgets, monitor spending, and generate monthly financial summaries — all from a simple interactive interface.

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [Author](#author)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## About the Project

**Personal Finance Manager** is a Python-based command-line application designed to help users organize and monitor their personal finances.

The application allows users to record income and expenses, categorize transactions, establish spending budgets, and review their financial activity through monthly summaries.

The project was developed with an emphasis on practical Python programming concepts, including object-oriented programming, modular design, input validation, exception handling, JSON-based data persistence, and automated testing.

## Features

- **Transaction Management:** Record, view, and search income and expense transactions.
- **Category-Based Budgets:** Set and update spending limits for individual expense categories.
- **Budget Monitoring:** Check category spending against configured budgets and identify overspending.
- **Monthly Financial Reports:** Generate summaries of income, expenses, and net balance for a selected month.
- **Persistent Data Storage:** Save and retrieve financial records using JSON.
- **Input Validation:** Validate transaction details, amounts, dates, and budget values.
- **Data Recovery:** Detect corrupted JSON save files and preserve a backup before initializing fresh data.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core application logic |
| JSON | Local data persistence |
| `datetime` | Date handling and monthly reporting |
| `unittest` | Automated testing |
| `tempfile` | Isolated test environments |

The application uses Python's standard library and does not require a database server or external framework.

## Project Structure

```text
Python-Finance-Manager/
│
├── main.py              # Application entry point and menu navigation
├── models.py            # Transaction and FinanceManager classes
├── transactions.py      # Transaction and budget operations
├── reports.py           # Monthly financial reporting
├── storage.py           # JSON data loading and saving
│
├── test_manager.py      # Finance manager tests
├── test_storage.py      # Data persistence tests
│
├── finance_data.json    # Locally stored financial data
└── README.md
```

## Getting Started

Follow these instructions to run the application locally.

### Prerequisites

You will need:

- Python 3.10 or later.
- Git.
- A terminal or command-line interface.

Check your Python installation:

```bash
python3 --version
```

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/cyrilmuchemi/Python-Finance-Manager.git
```

**2. Navigate into the project directory**

```bash
cd Python-Finance-Manager
```

**3. Create a virtual environment**

```bash
python3 -m venv .venv
```

**4. Activate the virtual environment**

On Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

No additional Python packages are currently required.

## Usage

Start the application with:

```bash
python3 main.py
```

The interactive menu provides the following operations:

| Option | Operation |
|---|---|
| 1 | Add an income or expense transaction |
| 2 | View recorded transactions |
| 3 | Search transactions by category |
| 4 | Set or update a category budget |
| 5 | Check category budget status |
| 6 | Generate a monthly financial summary |
| 7 | Save data and exit |

Financial records are stored locally in `finance_data.json` and loaded when the application starts.

**Note:** The application is intended for local use. Keep your financial data file private and maintain backups of important records.

## Running Tests

The project includes automated tests using Python's built-in `unittest` framework.

Run the complete test suite from the project root:

```bash
python3 -m unittest discover -v
```

The tests cover application functionality and data persistence, including saving, loading, and handling corrupted JSON files.

## Future Improvements

Potential enhancements include:

- [ ] Add transaction editing and deletion.
- [ ] Introduce date-range filtering and more detailed financial analytics.
- [ ] Add CSV and PDF report exports.
- [ ] Implement recurring transactions.
- [ ] Introduce monthly budget tracking and historical comparisons.
- [ ] Build a graphical user interface or web-based version.
- [ ] Add database support for more scalable data management.

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add: describe your changes"
   ```

4. Push your branch and open a pull request.

For significant changes, consider opening an issue first to discuss the proposed implementation.

## Author

**Cyril Muchemi**

- GitHub: [@cyrilmuchemi](https://github.com/cyrilmuchemi)

## Acknowledgements

- The Python community for its documentation and learning resources.
- The open-source community for promoting knowledge sharing and collaborative software development.

## License

No license has currently been specified for this repository. Unless a license is added, the default copyright restrictions apply. See [Choose a License](https://choosealicense.com/) for guidance on selecting an appropriate open-source license.
