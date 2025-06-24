"""
This module contains the mappings dictionary used for constructing variables in the Call Reports dataset.
The mappings define how to create various financial variables by combining or transforming existing columns.
"""

mappings = [
    # Loans: Total Loans = RCON2122.combine_first(RCFD2122), then mask zeros.
    {
        "first_col": "RCON2122",
        "second_col": "RCON2122",
        "new_var": "Total Loans",
        "method": "secondary",   # Gives RCON2122 if available, else RCFD2122.
        "mask_zeros": True
    },
    # Assets: Create Total Assets from RCON2170 and mask zeros.
    {
        "first_col": "RCFD2170",
        "second_col": "RCON2170",
        "new_var": "Total Assets",
        "method": "secondary",   # Since both are the same, this simply copies RCON2170.
        "mask_zeros": True
    },
    # Create 'QA Total Assets' from RCON3368 and RCFD3368:
    {
        "first_col": "RCFD3368",
        "second_col": "RCON3368",
        "new_var": "QA Total Assets",
        "method": "secondary",   # Since both are the same, this simply copies RCON3368.
    },
    # Equity Capital: Create Total Equity Capital from RCON3210 and RCFD3210 and mask zeros.
    {
        "first_col": "RCON3210",
        "second_col": "RCFD3210",
        "new_var": "Total Equity Capital",
        "method": "secondary",   # Since both are the same, this simply copies RCON3210.
    },
    # AOCI: Create AOCI from RCONB530 and RCFDB530 and mask zeros.
    {
        "first_col": "RCONB530",
        "second_col": "RCFDB530",
        "new_var": "AOCI",
        "method": "secondary",   # Since both are the same, this simply copies RCONB530.
    },
    # ********************************************************************************************************
    # ****************************************** Security Variables ******************************************
    # ********************************************************************************************************
    # ------------------------------------------ INTERMEDIATE STEPS ------------------------------------------
    # Create RCON1754_right = RCON1754_x.combine_first(RCON1754)
    {
        "new_var":              "RCON1754_right",
        "first_col":            "RCON1754",      # fallback column
        "second_col":           "RCON1754_x",   # primary column
        "method":               "secondary"
    },
    # Create RCFD1754_right = RCFD1754_x.combine_first(RCFD1754)
    {
        "new_var":              "RCFD1754_right",
        "first_col":            "RCFD1754",      # fallback column
        "second_col":           "RCFD1754_x",   # primary column
        "method":               "secondary"
    },
    # Create 1754_right from RCFD1754_right and RCON1754_right
    # This takes the row-wise minimum:
    {
        "new_var":              "1754_right",
        "first_col":            "RCFD1754_right",
        "second_col":           "RCON1754_right",
        "method":               "secondary"
    },
    # Create '1771_right' from RCON1771 and RCFD1771:
    {
        "new_var":              "1771_right",
        "first_col":            "RCFD1771",
        "second_col":           "RCON1771",
        "method":               "secondary"
    },
    # Create 1772_right from RCFD1772 and RCON1772:
    {
        "new_var":              "1772_right",
        "first_col":            "RCFD1772",
        "second_col":           "RCON1772",
        "method":               "secondary"
    },
    # Create B989_right from RCFDB989 and RCONB989:
    {
        "new_var":              "B989_right",
        "first_col":            "RCFDB989",
        "second_col":           "RCONB989",
        "method":               "secondary",
    },
    # ------------------------------------------ VARIABLES ------------------------------------------
    {
        "new_var":          "HTM Securities",
        "first_col":        "1754_right",       
        "second_col":       "1754_right",
        "switch_date":      "2019-03-31",           # First date with the new MDRM code.
        "first_col_post":   "RCFDJJ34",
        "second_col_post":  "RCONJJ34",
        "method":           "secondary",
    },
    # Create AFS Securities from RCON1773 and RCFD1773_x:
    {
        "new_var":          "AFS Securities",
        "first_col":        "RCFD1773_x",
        "second_col":       "RCON1773",
        "method":           "secondary",
    },
    # Create 'Securities AC' from 1754_right and 1772_right:
    {
        "new_var":          "Securities AC",
        "first_col":        "1754_right",
        "second_col":       "1772_right",
        "method":           "sum",
    },
    # Create 'Securities Fair Value' from 1771_right and AFS Securities:
    {
        "new_var":          "Securities FV",
        "first_col":        "1771_right",
        "second_col":       "AFS Securities",
        "method":           "sum",
    },
    # Create 'Equity Securities' from 'RCFDJA22' and 'RCONJA22':
    {
        "new_var":          "Equity Securities",
        "first_col":        "RCFDJA22",
        "second_col":       "RCONJA22",
        "method":           "secondary",
    },
    # Create FFS from B989_right and RCONB987:
    {
        "new_var":          "FFS",
        "first_col":        "B989_right",
        "second_col":       "RCONB987",
        "method":           "sum",
    },
    # ********************************************************************************************************
    # ************************************************* Cash *************************************************
    # ********************************************************************************************************
    # Create 0081_right from RCFD0081 and RCON0081:
    {
        "new_var":          "0081_right",
        "first_col":        "RCFD0081",
        "second_col":       "RCON0081",
        "method":           "secondary",   
    },
    # Create 0071_right from RCFD0071 and RCON0071:
    {
        "new_var":          "0071_right",
        "first_col":        "RCFD0071",
        "second_col":       "RCON0071",
        "method":           "secondary",   
    },
    # Create 'Cash' from 0081_right and 0071_right:
    {
        "new_var":          "Cash 2",
        "first_col":        "0081_right",
        "second_col":       "0071_right",
        "method":           "sum",
        "mask_zeros":       True
    },
    # Create 'Cash 1' from RCON0010 and RCFD0010:
    {
        "new_var":          "Cash 1",
        "first_col":        "RCON0010",
        "second_col":       "RCFD0010",
        "method":           "first",
    },
    # Create 'Cash' from Cash 1 and Cash 2:
    {
        "new_var":          "Cash",
        "first_col":        "Cash 1",
        "second_col":       "Cash 2",
        "method":           "first",
    },
    
    # ********************************************************************************************************
    # *********************************************** Deposits ***********************************************
    # ********************************************************************************************************
    # Create Total Deposits from RCON2200 (a simple copy) and mask zeros.
    {
        "new_var":          "Total Deposits",
        "first_col":        "RCON2200",
        "second_col":       "RCON2200",
        "method":           "secondary",   # Since both are the same, this simply copies RCON2200.
        "mask_zeros":       True
    },
    # Create 'Insured Deposit Accounts' from RCONF049 and RCONF045:
    {
        "new_var":          "Insured Deposit Accounts",
        "first_col":        "RCONF049",
        "second_col":       "RCONF045",
        "method":           "sum",
        "mask_zeros":       True
    },
    # Create 'Number of Insured Deposit Accounts' from RCONF050 and RCONF046:
    {
        "new_var":          "Number of Insured Deposit Accounts",
        "first_col":        "RCONF050",
        "second_col":       "RCONF046",
        "method":           "sum",
    },
    # Create 'Uninsured Deposit Accounts' from RCONF051 and RCONF047:
    {
        "new_var":          "Uninsured Deposit Accounts",
        "first_col":        "RCONF051",
        "second_col":       "RCONF047",
        "method":           "sum",
    },
    # Create 'Number of Uninsured Deposit Accounts' from RCONF052 and RCONF048:
    {
        "new_var":          "Number of Uninsured Deposit Accounts",
        "first_col":        "RCONF052",
        "second_col":       "RCONF048",
        "method":           "sum",
    },
    # Create 'Transaction Deposits' from RCON2215 (a simple copy) and mask zeros.
    {
        "new_var":          "Transaction Deposits",
        "first_col":        "RCON2215",
        "second_col":       "RCON2215",
        "method":           "secondary",   # Since both are the same, this simply copies RCON2215.
        "mask_zeros":       True
    },
    # total time deposits (small + large)
    {
        "new_var":          "Time Deposits",
        "first_col":        "RCON6648",       # < $100 k
        "second_col":       "RCON2604",       # ≥ $100 k (pre-2010)
        "method":           "sum",
        "mask_zeros":       True
    },
    # ********************************************************************************************************
    # ****************************************** Interest Expenses *******************************************
    # ********************************************************************************************************
    # Create 'Transaction Deposit Expenses' from RIAD4508:
    {
        "new_var":          "Transaction Deposit Expenses",
        "first_col":        "RIAD4508",
        "second_col":       "RIAD4508",  # Since both are the same, this simply copies RCON2215.
        "method":           "secondary"
    },
    # Create 'Savings Expenses' fro RIAD0093:
    {
        "new_var":          "Savings Expenses",
        "first_col":        "RIAD0093",
        "second_col":       "RIAD0093",  # Since both are the same, this simply copies RCON2215.
        "method":           "secondary"
    },
    # Create 'Small TD Expense' from RIADA518:
    # Note: This is a special case where the column is used both before and after the
    {
        "new_var":        "Small TD Expense",
        "first_col":      "RIADA518",          # < $100 k (old code)
        "second_col":     "RIADA518",          # same column, makes 'secondary' a copy
        "switch_date":    "2017-03-31",        # first quarter with HK-codes
        "first_col_post": "RIADHK03",          # ≤ $250 k
        "second_col_post":"RIADHK03",
        "method":         "secondary",
    },
    # Create 'Large TD Expense' from RIADA517:
    # Note: This is a special case where the column is used both before and after the
    {
        "new_var":        "Large TD Expense",
        "first_col":      "RIADA517",          # ≥ $100 k (old code)
        "second_col":     "RIADA517",
        "switch_date":    "2017-03-31",
        "first_col_post": "RIADHK04",          # > $250 k
        "second_col_post":"RIADHK04",
        "method":         "secondary",
    },
    # Create 'Time Deposit Expenses' from 'Small TD Expense' and 'Large TD Expense':
    {
        "new_var":          "Time Deposit Expenses",
        "first_col":        "Small TD Expense",
        "second_col":       "Large TD Expense",
        "method":           "sum",
    },
    # Create 'Total Interest Expenses' from RIAD4073:
    {
        "new_var":          "Total Interest Expenses",
        "first_col":        "RIAD4073",
        "second_col":       "RIAD4073",  # Since both are the same, this simply copies RCON2215.
        "method":           "secondary",
    },
    # Create 'Interest Expenses on Subordinated Debt' from RIAD4200:
    {
        "new_var":          "Interest Expenses on Subordinated Debt",
        "first_col":        "RIAD4200",
        "second_col":       "RIAD4200",  # Since both are the same, this simply copies RCON2215.
        "method":           "secondary",
    },
    # Create 'Other Interest Expenses' from RIAD4185:
    {
        "new_var":          "Other Interest Expenses",
        "first_col":        "RIAD4185",
        "second_col":       "RIAD4185",  # Since both are the same, this simply copies RCON2215.
        "method":           "secondary",
    },
    # Create 'Interest Expenses on FFS' from RIAD4180:
    {
        "new_var":          "Interest Expenses on FFS",
        "first_col":        "RIAD4180",
        "second_col":       "RIAD4180",  # Since both are the same, this simply copies RCON2215.
        "method":           "secondary",
    },
    # Create 'Interest Expenses on Foreign Deposits' from RIAD4172:
    {
        "new_var":          "Interest Expenses on Foreign Deposits",
        "first_col":        "RIAD4172",
        "second_col":       "RIAD4172",  # Since both are the same, this simply copies RCON2215.
        "method":           "secondary",
    },
    # Create 'Total Interest Income' from RIAD4107:
    {
        "new_var":          "Total Interest Income",
        "first_col":        "RIAD4107",
        "second_col":       "RIAD4107",  # Since both are the same, this simply copies RCON2215.
        "method":           "secondary",
    }, 
    # Create 'Net Interest Income' from RIAD4340:
    {
        "new_var":          "Net Interest Income",
        "first_col":        "RIAD4340",
        "second_col":       "RIAD4340",  # Since both are the same, this simply copies RCON2215.
        "method":           "secondary",
    },
] 