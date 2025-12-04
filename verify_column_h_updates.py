#!/usr/bin/env python3

import pandas as pd

def verify_column_h_updates():
    """
    Verify that column H in Club_Expansions has been updated with club names
    """

    replica_file = 'OND-JFM Plan REPLICA with Club Maintenance.xlsx'

    try:
        # Read the updated Club_Expansions sheet
        club_expansions = pd.read_excel(replica_file, sheet_name='Club_Expansions')

        print('🔍 VERIFYING COLUMN H UPDATES IN CLUB_EXPANSIONS')
        print('=' * 60)
        print(f'Total rows: {len(club_expansions)}')

        # Check column H (Specific Action) - index 7
        specific_actions = club_expansions['Specific Action']

        print('\n📋 SAMPLE UPDATED SPECIFIC ACTIONS (Column H):')
        print('=' * 50)

        for i, action in enumerate(specific_actions.head(10), 1):
            print(f'{i:2d}. {action}')

        # Check if club names are present
        actions_with_clubs = []
        for i, action in enumerate(specific_actions):
            if any(club_keyword in str(action) for club_keyword in ['Ballers', 'Mehfil', 'Dice', 'Fork', 'Current']):
                actions_with_clubs.append((i+2, action))  # +2 because of header and 0-indexing

        print(f'\n🎯 ACTIONS WITH CLUB NAMES: {len(actions_with_clubs)}')
        print('=' * 40)

        for row_num, action in actions_with_clubs[:10]:
            print(f'Row {row_num}: {action}')

        # Check new Club Name column (should be column 18)
        if 'Club Name' in club_expansions.columns:
            club_names = club_expansions['Club Name']
            print(f'\n📊 CLUB NAME COLUMN ADDED:')
            print('=' * 30)

            unique_clubs = club_names.dropna().unique()
            print(f'Unique club names: {len(unique_clubs)}')
            for club in unique_clubs[:10]:
                print(f'• {club}')

        return True

    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == "__main__":
    verify_column_h_updates()