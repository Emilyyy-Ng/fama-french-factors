# Fama-French Factors

Download Fama-French factor data directly from [Kenneth R. French's data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/index.html).

## Installation

### Option 1: Install via pip
```bash
pip install git+https://github.com/Emilyyy-Ng/fama-french-factors.git
```

### Option 2: Clone the repository
```bash
git clone https://github.com/Emilyyy-Ng/fama-french-factors.git
cd fama-french-factors
pip install -r requirements.txt
```

### Option 3: Download the single file
```bash
# Download just the Python file
curl -O https://raw.githubusercontent.com/Emilyyy-Ng/fama-french-factors/main/fama_french.py

# Install dependencies
pip install pandas pandas-datareader
```

## Quick Start

```python
from fama_french import get_ff3, get_ff5

# Get daily Fama-French 3 factors
df_ff3 = get_ff3("D", start_date="2024-01-01", end_date="2026-07-31")

# Get monthly 5 factors as DatetimeIndex
df_ff5 = get_ff5("M", return_type="datetime")
```

## API Reference

### `get_ff3(frequency, start_date, end_date, return_type)`
Download Fama-French 3 factors (Mkt-RF, SMB, HML, RF).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frequency` | str | "D" | "D" (daily), "W" (weekly), "M" (monthly), "Y" (yearly) |
| `start_date` | str | None | Start date (e.g., "2024-01-01") |
| `end_date` | str | None | End date (e.g., "2024-12-31") |
| `return_type` | str | "period" | "period" (PeriodIndex) or "datetime" (DatetimeIndex) |

### `get_ff5(frequency, start_date, end_date, return_type)`
Download Fama-French 5 factors (Mkt-RF, SMB, HML, RMW, CMA, RF).

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `frequency` | str | "D" | "D" (daily), "M" (monthly), "Y" (yearly) |

The rest are the same as above.

### Helper Functions

```python
from fama_french import to_datetime_index, to_period_index

# Convert PeriodIndex to DatetimeIndex
df_dt = to_datetime_index(df)

# Convert DatetimeIndex to PeriodIndex
df_period = to_period_index(df_dt)
```

## Example Output

```python
>>> df = get_ff3("M", start_date="2026-01")
>>> print(df)
         Mkt-RF     SMB     HML      RF
Date                                   
2026-01  0.0103  0.0218  0.0380  0.0030
2026-02 -0.0117  0.0016  0.0280  0.0028
2026-03 -0.0518  0.0044  0.0329  0.0029
2026-04  0.0995  0.0019 -0.0137  0.0029
2026-05  0.0491 -0.0159 -0.0231  0.0031
2026-06 -0.0107  0.0339  0.0358  0.0029
2026-07 -0.0060 -0.0196  0.0211  0.0033
```

## Dependencies

- pandas
- pandas-datareader

## License

[MIT License](LICENSE)