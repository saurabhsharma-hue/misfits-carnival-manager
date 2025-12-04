#!/usr/bin/env python3

import pandas as pd

def check_current_sheets_structure():
    """
    Check structure of Weekly_Execution and Milestones sheets
    """

    v2_file = 'OND-JFM Plan with actionbales final V2.xlsx'

    try:
        # Read Weekly_Execution sheet
        weekly_exec = pd.read_excel(v2_file, sheet_name='Weekly_Execution')
        print('📊 WEEKLY_EXECUTION SHEET STRUCTURE:')
        print('=' * 50)
        print(f'Shape: {weekly_exec.shape}')
        print(f'Columns: {list(weekly_exec.columns)}')
        print('\nSample data:')
        print(weekly_exec.head())

        # Read Milestones sheet
        milestones = pd.read_excel(v2_file, sheet_name='Milestones')
        print('\n📊 MILESTONES SHEET STRUCTURE:')
        print('=' * 50)
        print(f'Shape: {milestones.shape}')
        print(f'Columns: {list(milestones.columns)}')
        print('\nSample data:')
        print(milestones.head())

        # Check Club_Launches for status column
        club_launches = pd.read_excel(v2_file, sheet_name='Club_Launches')
        print('\n📊 CLUB_LAUNCHES STATUS COLUMN:')
        print('=' * 50)
        if 'Status' in club_launches.columns:
            status_counts = club_launches['Status'].value_counts()
            print(f'Status distribution: {dict(status_counts)}')
        else:
            print('No Status column found in Club_Launches')

        # Check Club_Expansions for status column
        club_expansions = pd.read_excel(v2_file, sheet_name='Club_Expansions')
        print('\n📊 CLUB_EXPANSIONS STATUS COLUMN:')
        print('=' * 50)
        if 'Status' in club_expansions.columns:
            status_counts = club_expansions['Status'].value_counts()
            print(f'Status distribution: {dict(status_counts)}')
        else:
            print('No Status column found in Club_Expansions')

        return weekly_exec, milestones, club_launches, club_expansions

    except Exception as e:
        print(f'❌ Error: {e}')
        return None, None, None, None

if __name__ == "__main__":
    check_current_sheets_structure()