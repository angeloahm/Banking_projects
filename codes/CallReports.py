import pandas as pd
import numpy as np
import os

class CallReports:
    def __init__(self, folder_path, essential_vars=None):
        """
        Initialize the analysis class with the folder path where 'call_reports.csv' is stored.
        
        Parameters:
          folder_path (str): Path to the folder containing 'call_reports.csv'.
          essential_vars (list, optional): List of columns that must always be included.
                Defaults to ['IDRSSD', 'Financial Institution Name', 'Date'].
        """
        self.folder_path = folder_path
        # Build full path for the call_reports.csv file.
        self.file_path = os.path.join(folder_path, "call_reports.csv")
        
        if essential_vars is None:
            self.essential_vars = ['IDRSSD', 'Financial Institution Name', 'Date']
        else:
            self.essential_vars = essential_vars
        
        # DataFrames will be loaded later, once variables to select are provided.
        self.df_selected = None
        self.df_constructed = None
        self.df_balanced = None

    def select_variables(self, variables=None):
        """
        Select a subset of columns for analysis and load only those columns from the CSV file.
        Essential variables are always included.
        
        Also, check for duplicate columns that come in pairs ending with '_x' and '_y'. For each pair,
        compute the maximum gap (absolute difference) between the entries. The maximum gap is printed,
        and if the gap is zero, the '_y' column is dropped (keeping the '_x' column).
        
        Finally, reorder the columns so that the essential variables (self.essential_vars)
        and the 'Year' column (if it exists) are the first columns in the DataFrame.
        
        Parameters:
        variables (list, optional): Additional variable names to include besides essential ones.
                                        If None, only essential variables will be selected.
        
        Returns:
        DataFrame with the selected (and cleaned) columns, with essential_vars and 'Year' ordered first.
        """
        # Combine the essential variables and any additional requested variables.
        if variables is None:
            vars_to_select = self.essential_vars.copy()
        else:
            vars_to_select = list(set(self.essential_vars + variables))
        
        # Read only the header of the CSV to know which columns exist.
        try:
            df_header = pd.read_csv(self.file_path, nrows=0)
        except Exception as e:
            raise IOError(f"Error reading file header from {self.file_path}: {e}")
        
        available_in_file = df_header.columns.tolist()
        
        # Warn if some requested variables are not in the file.
        missing_vars = [v for v in vars_to_select if v not in available_in_file]
        if missing_vars:
            print("Warning: The following variables are not in the data and will be skipped:", missing_vars)
        
        # Determine the final list of columns to load.
        available_vars = [v for v in vars_to_select if v in available_in_file]
        
        # Load only the selected columns from the CSV.
        self.df_selected = pd.read_csv(self.file_path, usecols=available_vars)
        
        # Ensure the 'Date' column is converted to datetime if present.
        if 'Date' in self.df_selected.columns:
            self.df_selected['Date'] = pd.to_datetime(self.df_selected['Date'], errors='coerce')
        
        # Check for duplicate variables that come with suffixes '_x' and '_y'.
        for col in self.df_selected.columns:
            if col.endswith("_x"):
                base = col[:-2]  # Remove the '_x' suffix
                col_y = base + "_y"
                if col_y in self.df_selected.columns:
                    try:
                        # Compute maximum absolute difference ("gap") between the two columns.
                        gap = (self.df_selected[col] - self.df_selected[col_y]).abs().max()
                    except Exception as e:
                        # If subtraction fails (e.g., non-numeric data), compare equality.
                        diff = self.df_selected[col] != self.df_selected[col_y]
                        gap = 0 if not diff.any() else "Mismatch"
                    
                    print(f"Duplicate variable {base}: max gap between {col} and {col_y} is {gap}")
                    
                    # If the gap is zero, drop the duplicate '_y' column.
                    if gap == 0:
                        print(f"Dropping duplicate column {col_y} as it is identical to {col}.")
                        self.df_selected.drop(columns=[col_y], inplace=True)
        
        # Reorder columns: ensure that the columns in essential_vars and 'Year'
        # are the first columns, followed by the rest in their original order.
        order_cols = []
        for col in self.essential_vars:
            if col in self.df_selected.columns:
                order_cols.append(col)
        if 'Year' in self.df_selected.columns:
            order_cols.append('Year')
        # Append any remaining columns that were not in order_cols.
        other_cols = [col for col in self.df_selected.columns if col not in order_cols]
        self.df_selected = self.df_selected[order_cols + other_cols]
        
        return self.df_selected
        
    def compare_variables(self, var_RCFD, var_RCON):
        """
        Compare two columns (e.g., a RCFD column and a RCON column).
        
        Returns:
          A dictionary with counts for:
            - both_valid: Observations where both are not NaN.
            - RCFD_only: Observations where only var_RCFD is not NaN.
            - RCON_only: Observations where only var_RCON is not NaN.
            - both_NaN: Observations where both are NaN.
          
        Note: This function requires that select_variables() has been run.
        """
        if self.df_selected is None:
            raise ValueError("Data has not been subset. Please run select_variables() first.")
        
        for var in [var_RCFD, var_RCON]:
            if var not in self.df_selected.columns:
                raise ValueError(f"Column {var} is not available in the selected DataFrame.")
        
        df_subset = self.df_selected[[var_RCFD, var_RCON]]
        both_valid = df_subset.dropna().shape[0]
        rcf_only = ((df_subset[var_RCFD].notna()) & (df_subset[var_RCON].isna())).sum()
        rcon_only = ((df_subset[var_RCON].notna()) & (df_subset[var_RCFD].isna())).sum()
        both_nan = ((df_subset[var_RCFD].isna()) & (df_subset[var_RCON].isna())).sum()
        
        return {
            "both_valid": both_valid,
            "RCFD_only": rcf_only,
            "RCON_only": rcon_only,
            "both_NaN": both_nan
        }

    def construct_definitions(self, mappings):
        """
        Construct new variables, handling MDRM code changes at specific switch_dates.
        
        Parameters:
            mappings (list): Each mapping dictionary may contain:
                - 'new_var': Name of the new variable.
                - 'first_col', 'second_col': Column names for initial period.
                - 'method': (optional) Combination method ('secondary', 'first', 'min', 'max', 'mean', 'sum').
                - 'mask_zeros': (optional) if True, mask zeros as NaN.
                - 'switch_date': (optional) date the MDRM codes change.
                - 'first_col_post', 'second_col_post': (optional) Column names after switch_date.
                If these are not provided, the original columns are used throughout.
                
        Returns:
            DataFrame with constructed variables appended.
            
        -------------------------------------- Examples --------------------------------------
        1) For a variable that changes MDRM codes, we use the 'switch_date' to determine when to switch columns.
        Suppose the variable "Held-to-maturity securities" changes MDRM codes on 2019-03-31:        
            mappings = [
                {
                    "new_var": "Held-to-maturity securities",
                    "first_col": "RCFD1754",
                    "second_col": "RCON1754",
                    "switch_date": "2019-03-31",
                    "first_col_post": "RCFDJJ34",
                    "second_col_post": "RCONJJ34",
                    "method": "secondary",
                    "mask_zeros": True
                }
            ]
        
        Then, the resulting series is constructed as:
        
            Date          Columns used
            -------------------------------------
            2018-12-31 → RCFD1754 & RCON1754
            2019-03-30 → RCFD1754 & RCON1754
            ------------------------------------- switch_date = 2019-03-31
            2019-03-31 → RCFDJJ34 & RCONJJ34
            2020-06-30 → RCFDJJ34 & RCONJJ34
        
        For a variable without code changes, such as "Total Loans":
        
            mappings = [
                {
                    "new_var": "Total Loans",
                    "first_col": "RCON2122",
                    "second_col": "RCON2122",
                    "method": "secondary",
                    "mask_zeros": True
                }
            ]
        
        The resulting series uses the same columns across all dates:
        
            Date          Columns used
            -------------------------------------
            2005-12-31 → RCON2122
            2019-03-31 → RCON2122
            2023-12-31 → RCON2122
        """
        if self.df_selected is None:
            raise ValueError("Please run select_variables() first.")
            
        df = self.df_selected.copy()

        for mapping in mappings:
            new_var = mapping['new_var']
            df[new_var] = np.nan

            method = mapping.get('method', 'secondary')
            mask_zeros = mapping.get('mask_zeros', False)
            
            switch_date = pd.Timestamp(mapping.get('switch_date', '2100-01-01'))

            # Before switch_date
            first_col = mapping['first_col']
            second_col = mapping['second_col']
            
            pre_mask = df['Date'] < switch_date
            
            # Function to combine two columns
            def combine_cols(df_slice, col1, col2, method):
                if method == "min":
                    return df_slice[[col1, col2]].min(axis=1)
                elif method == "max":
                    return df_slice[[col1, col2]].max(axis=1)
                elif method == "mean":
                    return df_slice[[col1, col2]].mean(axis=1, skipna=True)
                elif method == "sum":
                    return df_slice[col1].fillna(0) + df_slice[col2].fillna(0)
                elif method == "first":
                    return df_slice[col1].combine_first(df_slice[col2])
                elif method == "secondary":
                    return df_slice[col2].combine_first(df_slice[col1])
                else:
                    raise ValueError(f"Unknown method '{method}'")

            # Apply to pre-switch dates
            result_pre = combine_cols(df.loc[pre_mask], first_col, second_col, method)
            if mask_zeros:
                result_pre = result_pre.mask(result_pre == 0, np.nan)
            df.loc[pre_mask, new_var] = result_pre

            # Apply post-switch if columns provided
            if 'switch_date' in mapping:
                first_col_post = mapping.get('first_col_post', first_col)
                second_col_post = mapping.get('second_col_post', second_col)
                
                post_mask = df['Date'] >= switch_date
                result_post = combine_cols(df.loc[post_mask], first_col_post, second_col_post, method)
                if mask_zeros:
                    result_post = result_post.mask(result_post == 0, np.nan)
                df.loc[post_mask, new_var] = result_post

        self.df_constructed = df
        return df

    def create_balanced_panel(self, df_input=None):
        """
        Transform the given dataset (or the constructed dataset) into a balanced panel by retaining
        only banks (identified by 'IDRSSD') that appear in all dates.
        
        Parameters:
          df_input (DataFrame, optional): The DataFrame to convert. Defaults to using self.df_constructed.
        
        Returns:
          A balanced panel DataFrame.
        """
        if df_input is None:
            if self.df_constructed is None:
                raise ValueError("No constructed DataFrame available. Please run construct_definitions() first.")
            df_input = self.df_constructed
        
        if "IDRSSD" not in df_input.columns or "Date" not in df_input.columns:
            raise ValueError("Both 'IDRSSD' and 'Date' columns must be in the DataFrame for creating a balanced panel.")
        
        n_dates = df_input["Date"].nunique()
        valid_banks = df_input.groupby("IDRSSD")["Date"].nunique()[lambda x: x == n_dates].index
        balanced_df = df_input[df_input["IDRSSD"].isin(valid_banks)].copy()
        self.df_balanced = balanced_df
        return balanced_df 