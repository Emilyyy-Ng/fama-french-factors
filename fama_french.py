from typing import Optional
import pandas as pd
import pandas_datareader.famafrench as ff
import os

# URL mapping
FF_URLS: dict[str, dict[str, str]] = {
    "ff3": {
        "D": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip",
        "W": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_weekly_CSV.zip",
        "M": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip",
        "Y": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip"
    },
    "ff5": {
        "D": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip",
        "M": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip",
        "Y": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip"
    }
}

def _parse_date(date_str: str) -> pd.Timestamp:
    """Parse date string flexibly based on frequency."""
    if date_str is None:
        return None
    
    date_str = str(date_str).strip()
    
    # Try YYYY-MM-DD first
    try:
        return pd.to_datetime(date_str, format="%Y-%m-%d")
    except ValueError:
        # Try YYYY-MM
        try:
            return pd.to_datetime(date_str, format="%Y-%m")
        except ValueError:
            # Try YYYY
            try:
                return pd.to_datetime(date_str, format="%Y")
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD (e.g., '2026-01-01').")
                    
def _fetch_ff_factors(url: str, freq, start_date: Optional[str] = None, 
                      end_date: Optional[str] = None,
                      return_type: str = "period") -> pd.DataFrame:
    """
    Fetch Fama-French factors.
    
    Args:
        url: URL to download from
        freq: 'D', 'W', 'M', or 'Y'
        start_date: Start date (e.g., '2024-01-01' or '2024-01')
        end_date: End date (e.g., '2024-12-31' or '2024-12')
        return_type: 'period' (PeriodIndex) or 'datetime' (DatetimeIndex)
    
    Returns:
        DataFrame with factors
    """
    # Define parameters
    f = freq.upper()
    if f == "D":
        date_len = 8
        period_freq = "D"
    elif f == "W":
        date_len = 8
        period_freq = "W-FRI"
    elif f == "M":
        date_len = 6
        period_freq = "M"
    else:  # Y
        date_len = 4
        period_freq = "Y"

    # Parse dates
    start_dt = _parse_date(start_date) if start_date else None
    end_dt = _parse_date(end_date) if end_date else None

    # Validate date range
    if start_dt and end_dt and start_dt > end_dt:
        raise ValueError("Start date must be earlier than or equal to end date.")
    
    if start_dt and start_dt > pd.Timestamp.now():
        raise ValueError("Start date cannot be a future date.")

    try:
        # Primary: Direct download
        df = pd.read_csv(url, skiprows=3)
        df.rename(columns={str(df.columns[0]): "Date"}, inplace=True)
        df["Date"] = df["Date"].astype(str).str.strip()
        df = df[df["Date"].str.len() == date_len]
        
        # Convert to decimal
        for col in df.columns:
            if col != "Date":
                df[col] = pd.to_numeric(df[col], errors="coerce") / 100
        
        df = df.dropna()
        
        # Create PeriodIndex
        df.index = pd.PeriodIndex(df["Date"], freq=period_freq)
        df.drop("Date", axis=1, inplace=True)
        
        # Filter
        if start_dt:
            start = pd.Period(start_dt, freq=period_freq)
            df = df[df.index >= start]
        if end_dt:
            end = pd.Period(end_dt, freq=period_freq)
            df = df[df.index <= end]
        
        # Convert based on return_type
        if return_type == "datetime":
            if f == "W":
                df.index = df.index.to_timestamp(how='end').normalize()
            elif f == "M":
                df.index = df.index.to_timestamp(how='end').normalize()
            elif f == "Y":
                df.index = df.index.to_timestamp(how='end').normalize()
            else:
                df.index = df.index.to_timestamp().normalize()
        
        return df

    except Exception as e1:
        # Fallback: pandas_datareader
        try:
            print("Using fallback with pandas_datareader...")
            _, name = os.path.split(url)
            name = name.replace("_CSV.zip", "")

            start_str = start_dt.strftime("%Y-%m-%d") if start_dt else None
            end_str = end_dt.strftime("%Y-%m-%d") if end_dt else None
            raw = ff.FamaFrenchReader(name, start=start_str, end=end_str).read()
            df = raw[0]
            df = df / 100
            
            # Convert to DatetimeIndex if requested
            if return_type == "datetime":
                if f == "W":
                    df.index = df.index.to_timestamp(how='end').normalize()
                elif f == "M":
                    df.index = df.index.to_timestamp(how='end').normalize()
                elif f == "Y":
                    df.index = df.index.to_timestamp(how='end').normalize()
                else:
                    df.index = df.index.to_timestamp().normalize()
            
            return df
            
        except Exception as e2:
            raise ValueError(
                "Failed to fetch data from both primary and fallback sources. "
                "Please check your internet connection."
            ) from e2


def get_ff3(frequency: str = "D", start_date: Optional[str] = None, 
            end_date: Optional[str] = None,
            return_type: str = "period") -> pd.DataFrame:
    """Download Fama-French 3 factors (Market, Size, Value, and Risk-Free)."""
    freq = frequency.upper()
    if freq not in FF_URLS['ff3']:
        raise ValueError(f"Invalid frequency. Choose from: {list(FF_URLS['ff3'].keys())}")
    return _fetch_ff_factors(FF_URLS['ff3'][freq], freq, start_date, end_date, return_type)


def get_ff5(frequency: str = "D", start_date: Optional[str] = None, 
            end_date: Optional[str] = None,
            return_type: str = "period") -> pd.DataFrame:
    """Download Fama-French 5 factors (Market, Size, Value, Profitability, Investment, and Risk-Free)."""
    freq = frequency.upper()
    if freq not in FF_URLS['ff5']:
        raise ValueError(f"Invalid frequency. Choose from: {list(FF_URLS['ff5'].keys())}")
    return _fetch_ff_factors(FF_URLS['ff5'][freq], freq, start_date, end_date, return_type)


# ============ HELPER FUNCTIONS ============

def to_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert PeriodIndex to DatetimeIndex.
    
    Args:
        df: DataFrame with PeriodIndex
    """
    df = df.copy()
    df.index = df.index.to_timestamp(how='end').normalize() 
    return df


def to_period_index(df: pd.DataFrame) -> pd.DataFrame:
    """Convert DatetimeIndex to PeriodIndex (infers frequency automatically)."""
    df = df.copy()
    freq = pd.infer_freq(df.index)
    if freq:
        if freq == 'ME':
            freq = 'M'
        elif freq == 'YE':
            freq = 'Y'
        df.index = df.index.to_period(freq)
    return df