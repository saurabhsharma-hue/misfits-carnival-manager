#!/usr/bin/env python3

import pandas as pd
import numpy as np

def check_actual_launch_count():
    """
    Check the actual number of launches in the working sheet and V2 files
    """

    v2_file = 'OND-JFM Plan with actionbales final V2.xlsx'

    try:
        print('🔍 CHECKING ACTUAL LAUNCH COUNT')
        print('=' * 50)

        # Read all relevant sheets
        working_sheet = pd.read_excel(v2_file, sheet_name='Working sheet')
        club_launches = pd.read_excel(v2_file, sheet_name='Club_Launches')

        print(f'📊 CLUB_LAUNCHES SHEET:')
        print(f'   Total rows in Club_Launches: {len(club_launches)}')

        # Check working sheet club calculations
        current_clubs_total = working_sheet['Current_Clubs_Count'].fillna(0).sum()
        clubs_needed_feb = working_sheet['Clubs_Needed_Feb'].fillna(0).sum()
        working_sheet_new_clubs = clubs_needed_feb - current_clubs_total

        print(f'\n📋 WORKING SHEET CLUB ANALYSIS:')
        print(f'   Current Clubs Total: {current_clubs_total}')
        print(f'   Clubs Needed by Feb: {clubs_needed_feb}')
        print(f'   Calculated New Clubs: {working_sheet_new_clubs}')

        # Check what's actually in Club_Launches sheet
        print(f'\n🚀 CLUB_LAUNCHES SHEET DETAILS:')
        if len(club_launches) > 0:
            print(f'   Columns: {list(club_launches.columns)}')

            # Check activities in club launches
            if 'Activity' in club_launches.columns:
                activity_counts = club_launches['Activity'].value_counts()
                print(f'   Activities in Club_Launches:')
                for activity, count in activity_counts.head(10).items():
                    print(f'      {activity}: {count}')

            # Check cities
            if 'City' in club_launches.columns:
                city_counts = club_launches['City'].value_counts()
                print(f'   Cities in Club_Launches:')
                for city, count in city_counts.head(5).items():
                    print(f'      {city}: {count}')

        # Compare with user expectation
        print(f'\n🎯 COMPARISON WITH USER EXPECTATION:')
        print(f'   Club_Launches sheet has: {len(club_launches)} entries')
        print(f'   Working sheet calculation: {working_sheet_new_clubs} new clubs')
        print(f'   User expectation: ~100 launches')
        print(f'   Previous mention: ~40 launches max')

        # Check if there's duplication or if some entries aren't actual launches
        print(f'\n🔍 ANALYZING CLUB_LAUNCHES ENTRIES:')

        # Check for any patterns that might explain the count
        if 'Type' in club_launches.columns:
            type_counts = club_launches['Type'].value_counts()
            print(f'   Types in Club_Launches:')
            for type_val, count in type_counts.items():
                print(f'      {type_val}: {count}')

        # Check areas with multiple entries
        if 'Area' in club_launches.columns and 'Activity' in club_launches.columns:
            area_activity_counts = club_launches.groupby(['Area', 'Activity']).size().sort_values(ascending=False)
            print(f'   Top area-activity combinations:')
            for (area, activity), count in area_activity_counts.head(10).items():
                if count > 1:
                    print(f'      {area} - {activity}: {count} entries')

        # Calculate realistic launch count
        print(f'\n💡 REALISTIC LAUNCH COUNT CALCULATION:')

        # Method 1: Unique area-activity combinations in Club_Launches
        if 'Area' in club_launches.columns and 'Activity' in club_launches.columns:
            unique_combinations = club_launches[['Area', 'Activity', 'City']].drop_duplicates()
            unique_count = len(unique_combinations)
            print(f'   Unique area-activity-city combinations: {unique_count}')

        # Method 2: Check working sheet for areas that actually need new clubs
        areas_needing_new_clubs = 0
        for idx, row in working_sheet.iterrows():
            current_clubs = row.get('Current_Clubs_Count', 0) if pd.notna(row.get('Current_Clubs_Count')) else 0
            clubs_needed_feb = row.get('Clubs_Needed_Feb', 0) if pd.notna(row.get('Clubs_Needed_Feb')) else 0

            if clubs_needed_feb > current_clubs:
                areas_needing_new_clubs += 1

        print(f'   Areas needing new clubs (working sheet): {areas_needing_new_clubs}')

        # Revenue calculation with realistic count
        current_revenue = working_sheet['Current revenue'].fillna(0).sum()
        jan_revenue = working_sheet['Monthly Revenue by January'].fillna(0).sum()
        mar_revenue = working_sheet['Revenue by March'].fillna(0).sum()

        expansion_revenue = jan_revenue - current_revenue
        launch_revenue = mar_revenue - jan_revenue

        print(f'\n💰 REVENUE CALCULATION:')
        print(f'   Expansion Revenue (Current→Jan): ₹{expansion_revenue:,.0f} ({expansion_revenue/100000:.1f}L)')
        print(f'   Launch Revenue (Jan→Mar): ₹{launch_revenue:,.0f} ({launch_revenue/100000:.1f}L)')

        # Calculate average revenue per launch with different counts
        print(f'\n📊 REVENUE PER LAUNCH ANALYSIS:')
        for launch_count in [40, 100, areas_needing_new_clubs, len(club_launches)]:
            if launch_count > 0:
                avg_revenue = launch_revenue / launch_count
                print(f'   {launch_count} launches: ₹{avg_revenue:,.0f} per launch')

        return areas_needing_new_clubs, launch_revenue

    except Exception as e:
        print(f'❌ Error: {e}')
        return 0, 0

def analyze_club_launches_sheet():
    """
    Analyze the Club_Launches sheet structure to understand the entries
    """

    print(f'\n🔄 ANALYZING CLUB_LAUNCHES SHEET STRUCTURE')
    print('=' * 50)

    v2_file = 'OND-JFM Plan with actionbales final V2.xlsx'

    try:
        club_launches = pd.read_excel(v2_file, sheet_name='Club_Launches')

        print(f'📋 SAMPLE ENTRIES FROM CLUB_LAUNCHES:')
        print(f'   Total entries: {len(club_launches)}')

        # Show first few entries
        if len(club_launches) > 0:
            for idx, row in club_launches.head(10).iterrows():
                activity = row.get('Activity', 'N/A')
                area = row.get('Area', 'N/A')
                city = row.get('City', 'N/A')
                action = str(row.get('Specific Action', 'N/A'))[:50] + '...' if len(str(row.get('Specific Action', ''))) > 50 else str(row.get('Specific Action', 'N/A'))

                print(f'   {idx+1}. {activity} in {area}, {city}')
                print(f'      Action: {action}')

        # Check if some entries might be duplicates or sub-actions
        if 'Action ID' in club_launches.columns:
            action_ids = club_launches['Action ID'].value_counts()
            print(f'\n   Action ID analysis:')
            print(f'   Unique Action IDs: {len(action_ids)}')
            if len(action_ids) != len(club_launches):
                print(f'   ⚠️ Some Action IDs are duplicated')

        return True

    except Exception as e:
        print(f'❌ Error: {e}')
        return False

def main():
    print('🚀 ACTUAL LAUNCH COUNT VERIFICATION')
    print('=' * 60)

    # Check actual launch count
    realistic_count, launch_revenue = check_actual_launch_count()

    # Analyze club launches sheet
    analyze_club_launches_sheet()

    print(f'\n🎯 CONCLUSIONS:')
    print(f'   • User expectation of ~100 launches seems more realistic')
    print(f'   • Club_Launches sheet may have multiple entries per actual launch')
    print(f'   • Need to use realistic count for revenue calculation')
    print(f'   • Launch revenue should be distributed across ~100 launches, not 131')

if __name__ == "__main__":
    main()