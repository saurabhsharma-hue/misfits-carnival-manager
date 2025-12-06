#!/usr/bin/env python3

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import xlsxwriter

def create_exact_plan_structure():
    """
    Create the exact plan structure as requested:
    1. Club expansion
    2. Club launches
    3. Summary
    4. Weekly execution
    5. Milestone
    6. City progress
    7. Working sheet (original)
    8. Events (original - keep as is)
    9. Logic (calculations explanation)
    """

    file_path = 'OND-JFM Plan with actionbales V5.xlsx'
    working_sheet = pd.read_excel(file_path, sheet_name='Working sheet')

    # Try to read events sheet
    try:
        events_sheet = pd.read_excel(file_path, sheet_name='Events')
    except:
        events_sheet = None

    print('🎯 CREATING EXACT PLAN STRUCTURE AS REQUESTED')
    print('=' * 60)

    # TOP 3 for maximum scaling
    TOP_3_MAXIMUM_SCALING = ['BOARDGAMING', 'SOCIAL_DEDUCTIONS', 'MUSIC']

    # Create new workbook
    workbook = xlsxwriter.Workbook('OND-JFM EXACT PLAN STRUCTURE V12.xlsx', {'nan_inf_to_errors': True})

    # Define formats
    header_format = workbook.add_format({
        'bold': True, 'bg_color': '#4472C4', 'font_color': 'white',
        'border': 1, 'align': 'center', 'valign': 'vcenter'
    })

    max_scaling_format = workbook.add_format({
        'bold': True, 'bg_color': '#FF0000', 'font_color': 'white',
        'border': 1, 'align': 'center'
    })

    high_priority_format = workbook.add_format({
        'bold': True, 'bg_color': '#FF6B6B', 'font_color': 'white',
        'border': 1, 'align': 'center'
    })

    medium_priority_format = workbook.add_format({
        'bold': True, 'bg_color': '#FFA500', 'font_color': 'white',
        'border': 1, 'align': 'center'
    })

    data_format = workbook.add_format({'border': 1, 'align': 'left', 'text_wrap': True})
    number_format = workbook.add_format({'border': 1, 'align': 'center', 'num_format': '#,##0'})
    currency_format = workbook.add_format({'border': 1, 'align': 'center', 'num_format': '₹#,##0'})
    dropdown_format = workbook.add_format({
        'border': 1, 'align': 'center', 'bg_color': '#F2F2F2', 'locked': False
    })

    # Enhanced target days for TOP 3 maximum scaling
    enhanced_target_days = {
        ('BOARDGAMING', 'GCR Extn.', 'Gurgaon'): 'Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday',
        ('BOARDGAMING', 'Golf Course Road', 'Gurgaon'): 'Monday, Wednesday, Thursday, Friday, Saturday, Sunday',
        ('BOARDGAMING', 'MG Road', 'Gurgaon'): 'Monday, Tuesday, Thursday, Friday, Saturday, Sunday',
        ('SOCIAL_DEDUCTIONS', 'GCR Extn.', 'Gurgaon'): 'Monday, Wednesday, Thursday, Friday, Saturday, Sunday',
        ('SOCIAL_DEDUCTIONS', 'South City', 'Gurgaon'): 'Monday, Tuesday, Thursday, Friday, Saturday, Sunday',
        ('MUSIC', 'GCR Extn.', 'Gurgaon'): 'Monday, Tuesday, Wednesday, Thursday, Saturday, Sunday',
        ('MUSIC', 'Golf Course Road', 'Gurgaon'): 'Monday, Wednesday, Thursday, Friday, Saturday, Sunday',
        ('MUSIC', 'South City', 'Gurgaon'): 'Monday, Tuesday, Thursday, Friday, Saturday, Sunday',
    }

    # Generate all actions first
    club_launch_actions = []
    club_expansion_actions = []
    launch_counter = 1
    expansion_counter = 1
    start_date = datetime(2024, 10, 28)

    # GENERATE CLUB LAUNCH ACTIONS
    working_sheet_sorted = working_sheet.copy()
    working_sheet_sorted['Revenue_Impact'] = working_sheet_sorted['Revenue by March'] - working_sheet_sorted['Current revenue']
    working_sheet_sorted = working_sheet_sorted.sort_values('Revenue_Impact', ascending=False)

    for idx, row in working_sheet_sorted.iterrows():
        activity = row['Activity']
        city = row['City']
        area = row['Area']
        current_clubs = row['Current_Clubs_Count'] if pd.notna(row['Current_Clubs_Count']) else 0
        clubs_needed_feb = row['Clubs_Needed_Feb'] if pd.notna(row['Clubs_Needed_Feb']) else current_clubs

        new_clubs_needed = clubs_needed_feb - current_clubs if clubs_needed_feb > current_clubs else 0

        if new_clubs_needed > 0:
            is_top3 = activity in TOP_3_MAXIMUM_SCALING

            target_attendance = row['Total people in a meetup']
            price = row['Average Price per Person (₹)']
            target_revenue = row['Revenue by March']
            current_revenue = row['Current revenue']
            revenue_increase = target_revenue - current_revenue

            # Get target days
            key = (activity, area, city)
            if key in enhanced_target_days:
                target_days = enhanced_target_days[key]
                target_meetups = len([d.strip() for d in target_days.split(',') if d.strip()])
            else:
                target_days = str(row['Target days by December in a week'])
                try:
                    if pd.notna(target_days) and target_days != 'nan':
                        target_meetups = len([d.strip() for d in target_days.split(',') if d.strip()])
                    else:
                        target_meetups = 3
                        target_days = 'Monday, Wednesday, Friday'
                except:
                    target_meetups = 3
                    target_days = 'Monday, Wednesday, Friday'

            revenue_per_club = revenue_increase / new_clubs_needed if new_clubs_needed > 0 else 0

            # Timeline based on priority
            if is_top3:
                base_week = 2
                priority_label = "HIGH"
            else:
                if revenue_per_club > 50000:
                    base_week = 5
                    priority_label = "MEDIUM"
                else:
                    base_week = 8
                    priority_label = "LOW"

            # Create individual launch actions for each new club
            for club_num in range(1, int(new_clubs_needed) + 1):
                target_week = base_week + ((launch_counter - 1) % 3)
                target_date = (start_date + timedelta(weeks=target_week-1)).strftime('%b %d, %Y')

                if new_clubs_needed == 1:
                    club_name = f"{activity} Club - {area}"
                    club_identifier = f"First club in {area}"
                else:
                    club_name = f"{activity} Club #{club_num} - {area}"
                    club_identifier = f"Club {club_num} of {int(new_clubs_needed)} planned clubs"

                if is_top3:
                    action_prefix = "🔥 MAX SCALING LAUNCH"
                else:
                    action_prefix = "STANDARD LAUNCH"

                specific_action = f"{action_prefix}: Launch {club_name} with {target_meetups} days/week ({target_days})"
                success_criteria = f"Club operational with {int(target_attendance)} people/meetup for {2 if is_top3 else 3}+ weeks"

                dependencies = [
                    f"Secure venue for {target_meetups} days/week in {area}",
                    f"Recruit Community Manager for {area}",
                    f"Marketing campaign for {activity} in {area}",
                    f"Equipment/setup for {int(target_attendance)} people capacity"
                ]
                dependencies_str = " | ".join(dependencies)

                club_strategy = row['Club_Strategy']
                strategy_notes = f"NEW AREA: {club_identifier} | TARGET: {target_days} ({int(target_attendance)} people) | REVENUE TARGET: ₹{revenue_per_club:,.0f} | STRATEGY: {club_strategy}"

                club_launch_actions.append({
                    'ID': f'LAUNCH_{launch_counter:03d}',
                    'Type': f'{activity} Launch',
                    'Priority': priority_label,
                    'City': city,
                    'Area': area,
                    'Activity': activity,
                    'Club_Name': club_name,
                    'Target_Schedule': target_days,
                    'Target_Capacity': int(target_attendance) if pd.notna(target_attendance) else 20,
                    'Specific_Action': specific_action,
                    'Success_Criteria': success_criteria,
                    'Revenue_Target': revenue_per_club,
                    'Target_Week': target_week,
                    'Target_Date': target_date,
                    'Duration': 2 if is_top3 else 3,
                    'Owner': f'{activity.title()} Launch Team',
                    'Dependencies': dependencies_str,
                    'Strategy_Notes': strategy_notes
                })
                launch_counter += 1

    # GENERATE CLUB EXPANSION ACTIONS
    for idx, row in working_sheet.iterrows():
        activity = row['Activity']
        city = row['City']
        area = row['Area']
        current_clubs = row['Current_Clubs_Count'] if pd.notna(row['Current_Clubs_Count']) else 0

        if current_clubs <= 0:
            continue

        current_meetups = row['Number of Meetups per Week currenty']
        current_attendance = row['Average Attendance per Meetup']
        target_attendance = row['Total people in a meetup']
        current_revenue = row['Current revenue']
        target_revenue = row['Revenue by March']
        club_strategy = row['Club_Strategy']

        is_top3 = activity in TOP_3_MAXIMUM_SCALING

        current_days = str(row['Current Days with Meetups'])
        key = (activity, area, city)
        if key in enhanced_target_days:
            target_days = enhanced_target_days[key]
        else:
            target_days = str(row['Target days by December in a week'])

        # Parse days properly
        try:
            if pd.notna(current_days) and current_days != 'nan':
                current_days_list = [d.strip() for d in current_days.split(',') if d.strip()]
                current_days_clean = ', '.join(current_days_list)
                current_meetups_calc = len(current_days_list)
            else:
                current_days_clean = f"{int(current_meetups)} days/week"
                current_meetups_calc = current_meetups
        except:
            current_days_clean = f"{int(current_meetups)} days/week"
            current_meetups_calc = current_meetups

        try:
            if pd.notna(target_days) and target_days != 'nan':
                target_days_list = [d.strip() for d in target_days.split(',') if d.strip()]
                target_days_clean = ', '.join(target_days_list)
                target_meetups_calc = len(target_days_list)
            else:
                target_days_clean = target_days
                target_meetups_calc = current_meetups_calc
        except:
            target_days_clean = target_days
            target_meetups_calc = current_meetups_calc

        meetup_increase = target_meetups_calc - current_meetups_calc if target_meetups_calc > current_meetups_calc else 0
        people_increase = target_attendance - current_attendance if pd.notna(target_attendance) and pd.notna(current_attendance) else 0
        revenue_increase = target_revenue - current_revenue

        if meetup_increase > 0 or people_increase > 0 or revenue_increase > 1000:
            if current_clubs == 1:
                club_to_expand = f"{activity} Club - {area}"
                club_identifier = f"Only club in {area}"
            else:
                club_to_expand = f"{activity} Main Club - {area}"
                club_identifier = f"Primary club (1 of {int(current_clubs)} clubs)"

            changes = []
            if meetup_increase > 0:
                changes.append(f"Expand from {current_meetups_calc} to {target_meetups_calc} days/week")
                changes.append(f"Current: {current_days_clean}")
                changes.append(f"Target: {target_days_clean}")

            if people_increase > 0:
                changes.append(f"Increase capacity from {int(current_attendance)} to {int(target_attendance)} people/meetup")

            if is_top3:
                base_week = 1
                priority_label = "HIGH"
            else:
                activity_revenue = working_sheet[working_sheet['Activity'] == activity]['Revenue by March'].sum() - working_sheet[working_sheet['Activity'] == activity]['Current revenue'].sum()
                if activity_revenue > 300000:
                    base_week = 6
                    priority_label = "MEDIUM"
                else:
                    base_week = 10
                    priority_label = "LOW"

            target_week = base_week + (expansion_counter % 2)
            target_date = (start_date + timedelta(weeks=target_week-1)).strftime('%b %d, %Y')

            if is_top3:
                action_prefix = "🔥 MAX SCALING"
            else:
                action_prefix = "STANDARD SCALING"

            specific_action = f"{action_prefix}: Expand {club_to_expand} - {' | '.join(changes)}"
            success_criteria = f"Club operational with target schedule and capacity for {2 if is_top3 else 3}+ consecutive weeks"

            dependencies = []
            if meetup_increase > 0:
                dependencies.append(f"Secure venue access for {target_meetups_calc} days/week")
                dependencies.append(f"Confirm {target_days_clean} availability")
            if people_increase > 0:
                dependencies.append(f"Venue capacity for {int(target_attendance)} people")
            dependencies.append("Community Manager capacity planning")

            dependencies_str = " | ".join(dependencies)
            strategy_notes = f"CLUB: {club_identifier} | CURRENT: {current_days_clean} ({int(current_attendance)} people) | TARGET: {target_days_clean} ({int(target_attendance)} people) | STRATEGY: {club_strategy}"

            club_expansion_actions.append({
                'ID': f'EXP_{expansion_counter:03d}',
                'Type': f'{activity} Expansion',
                'Priority': priority_label,
                'City': city,
                'Area': area,
                'Activity': activity,
                'Club_To_Expand': club_to_expand,
                'Current_Schedule': current_days_clean,
                'Target_Schedule': target_days_clean,
                'Current_Capacity': int(current_attendance) if pd.notna(current_attendance) else 0,
                'Target_Capacity': int(target_attendance) if pd.notna(target_attendance) else 0,
                'Specific_Action': specific_action,
                'Success_Criteria': success_criteria,
                'Revenue_Impact': revenue_increase,
                'Target_Week': target_week,
                'Target_Date': target_date,
                'Duration': 2 if is_top3 else 3,
                'Owner': f'{activity.title()} Expansion Team',
                'Dependencies': dependencies_str,
                'Strategy_Notes': strategy_notes
            })
            expansion_counter += 1

    # 1. CLUB EXPANSION SHEET
    print("📊 1. Creating Club Expansion sheet...")
    ws_expansions = workbook.add_worksheet('Club_Expansion')

    expansion_headers = [
        'Action ID', 'Week Group', 'Type', 'Priority', 'City', 'Area', 'Activity',
        'Club To Expand', 'Current Schedule', 'Target Schedule', 'Current Capacity', 'Target Capacity',
        'Specific Action', 'Success Criteria', 'Revenue Impact (₹)',
        'Status', 'Target Date', 'Duration (weeks)', 'Owner', 'Dependencies', 'Strategy Notes'
    ]

    for col, header in enumerate(expansion_headers):
        ws_expansions.write(0, col, header, header_format)
        if col in [7, 12, 19, 20]:
            ws_expansions.set_column(col, col, 30)
        elif col in [8, 9]:
            ws_expansions.set_column(col, col, 20)
        else:
            ws_expansions.set_column(col, col, 12)

    club_expansion_actions.sort(key=lambda x: (0 if x['Activity'] in TOP_3_MAXIMUM_SCALING else 1, x['Target_Week']))

    for row_idx, action in enumerate(club_expansion_actions, start=1):
        week = action['Target_Week']
        week_group = f"Nov 2024 (W{week})" if week <= 4 else f"Dec 2024 (W{week})" if week <= 8 else f"Jan 2025 (W{week})" if week <= 13 else f"Feb 2025 (W{week})"

        is_top3_action = action['Activity'] in TOP_3_MAXIMUM_SCALING
        format_to_use = max_scaling_format if is_top3_action else data_format

        ws_expansions.write(row_idx, 0, action['ID'], format_to_use)
        ws_expansions.write(row_idx, 1, week_group, format_to_use)
        ws_expansions.write(row_idx, 2, action['Type'], format_to_use)
        ws_expansions.write(row_idx, 3, action['Priority'], format_to_use)
        ws_expansions.write(row_idx, 4, action['City'], data_format)
        ws_expansions.write(row_idx, 5, action['Area'], data_format)
        ws_expansions.write(row_idx, 6, action['Activity'], format_to_use)
        ws_expansions.write(row_idx, 7, action['Club_To_Expand'], data_format)
        ws_expansions.write(row_idx, 8, action['Current_Schedule'], data_format)
        ws_expansions.write(row_idx, 9, action['Target_Schedule'], format_to_use if is_top3_action else data_format)
        ws_expansions.write(row_idx, 10, action['Current_Capacity'], number_format)
        ws_expansions.write(row_idx, 11, action['Target_Capacity'], number_format)
        ws_expansions.write(row_idx, 12, action['Specific_Action'], data_format)
        ws_expansions.write(row_idx, 13, action['Success_Criteria'], data_format)
        ws_expansions.write(row_idx, 14, action['Revenue_Impact'], currency_format)

        ws_expansions.data_validation(row_idx, 15, row_idx, 15, {
            'validate': 'list',
            'source': ['NOT_STARTED', 'IN_PROGRESS', 'BLOCKED', 'DONE']
        })
        ws_expansions.write(row_idx, 15, 'NOT_STARTED', dropdown_format)

        ws_expansions.write(row_idx, 16, action['Target_Date'], data_format)
        ws_expansions.write(row_idx, 17, action['Duration'], number_format)
        ws_expansions.write(row_idx, 18, action['Owner'], data_format)
        ws_expansions.write(row_idx, 19, action['Dependencies'], data_format)
        ws_expansions.write(row_idx, 20, action['Strategy_Notes'], data_format)

    # 2. CLUB LAUNCHES SHEET
    print("📊 2. Creating Club Launches sheet...")
    ws_launches = workbook.add_worksheet('Club_Launches')

    launch_headers = [
        'Action ID', 'Week Group', 'Type', 'Priority', 'City', 'Area', 'Activity',
        'Club Name', 'Target Schedule', 'Target Capacity', 'Specific Action',
        'Success Criteria', 'Revenue Target (₹)', 'Status', 'Target Date',
        'Duration (weeks)', 'Owner', 'Dependencies', 'Strategy Notes'
    ]

    for col, header in enumerate(launch_headers):
        ws_launches.write(0, col, header, header_format)
        if col in [7, 10, 17, 18]:
            ws_launches.set_column(col, col, 30)
        elif col in [8]:
            ws_launches.set_column(col, col, 20)
        else:
            ws_launches.set_column(col, col, 12)

    club_launch_actions.sort(key=lambda x: (0 if x['Activity'] in TOP_3_MAXIMUM_SCALING else 1, x['Target_Week']))

    for row_idx, action in enumerate(club_launch_actions, start=1):
        week = action['Target_Week']
        week_group = f"Nov 2024 (W{week})" if week <= 4 else f"Dec 2024 (W{week})" if week <= 8 else f"Jan 2025 (W{week})" if week <= 13 else f"Feb 2025 (W{week})"

        is_top3_action = action['Activity'] in TOP_3_MAXIMUM_SCALING
        format_to_use = max_scaling_format if is_top3_action else data_format

        ws_launches.write(row_idx, 0, action['ID'], format_to_use)
        ws_launches.write(row_idx, 1, week_group, format_to_use)
        ws_launches.write(row_idx, 2, action['Type'], format_to_use)
        ws_launches.write(row_idx, 3, action['Priority'], format_to_use)
        ws_launches.write(row_idx, 4, action['City'], data_format)
        ws_launches.write(row_idx, 5, action['Area'], data_format)
        ws_launches.write(row_idx, 6, action['Activity'], format_to_use)
        ws_launches.write(row_idx, 7, action['Club_Name'], data_format)
        ws_launches.write(row_idx, 8, action['Target_Schedule'], format_to_use if is_top3_action else data_format)
        ws_launches.write(row_idx, 9, action['Target_Capacity'], number_format)
        ws_launches.write(row_idx, 10, action['Specific_Action'], data_format)
        ws_launches.write(row_idx, 11, action['Success_Criteria'], data_format)
        ws_launches.write(row_idx, 12, action['Revenue_Target'], currency_format)

        ws_launches.data_validation(row_idx, 13, row_idx, 13, {
            'validate': 'list',
            'source': ['NOT_STARTED', 'IN_PROGRESS', 'BLOCKED', 'DONE']
        })
        ws_launches.write(row_idx, 13, 'NOT_STARTED', dropdown_format)

        ws_launches.write(row_idx, 14, action['Target_Date'], data_format)
        ws_launches.write(row_idx, 15, action['Duration'], number_format)
        ws_launches.write(row_idx, 16, action['Owner'], data_format)
        ws_launches.write(row_idx, 17, action['Dependencies'], data_format)
        ws_launches.write(row_idx, 18, action['Strategy_Notes'], data_format)

    # 3. SUMMARY SHEET
    print("📊 3. Creating Summary sheet...")
    ws_summary = workbook.add_worksheet('Summary')

    summary_headers = [
        'Metric', 'Current State', 'Target State', 'Gap', 'Actions Required', 'Timeline', 'Priority'
    ]

    for col, header in enumerate(summary_headers):
        ws_summary.write(0, col, header, header_format)
        ws_summary.set_column(col, col, 18)

    total_current_clubs = working_sheet['Current_Clubs_Count'].sum()
    total_target_clubs = working_sheet['Clubs_Needed_Feb'].sum()
    total_current_revenue = working_sheet['Current revenue'].sum()
    total_target_revenue = working_sheet['Revenue by March'].sum()
    total_launch_actions = len(club_launch_actions)
    total_expansion_actions = len(club_expansion_actions)
    top3_launch_actions = len([a for a in club_launch_actions if a['Activity'] in TOP_3_MAXIMUM_SCALING])
    top3_expansion_actions = len([a for a in club_expansion_actions if a['Activity'] in TOP_3_MAXIMUM_SCALING])

    summary_data = [
        {
            'Metric': 'Total Clubs',
            'Current': f"{int(total_current_clubs)} clubs",
            'Target': f"{int(total_target_clubs)} clubs",
            'Gap': f"{int(total_target_clubs - total_current_clubs)} new clubs",
            'Actions': f"{total_launch_actions} launch actions",
            'Timeline': "Nov 2024 - Feb 2025",
            'Priority': "HIGH"
        },
        {
            'Metric': 'Total Revenue',
            'Current': f"₹{total_current_revenue:,.0f}",
            'Target': f"₹{total_target_revenue:,.0f}",
            'Gap': f"₹{total_target_revenue - total_current_revenue:,.0f}",
            'Actions': f"{total_expansion_actions} expansion actions",
            'Timeline': "Nov 2024 - Feb 2025",
            'Priority': "HIGH"
        },
        {
            'Metric': 'TOP 3 Activities',
            'Current': "Standard scaling",
            'Target': "Maximum scaling (7 days/week)",
            'Gap': "Enhanced day coverage",
            'Actions': f"{top3_launch_actions + top3_expansion_actions} priority actions",
            'Timeline': "Nov 2024 - Jan 2025",
            'Priority': "CRITICAL"
        },
        {
            'Metric': 'Secondary Activities',
            'Current': "Moderate scaling",
            'Target': "Steady growth support",
            'Gap': "Balanced expansion",
            'Actions': f"{total_launch_actions + total_expansion_actions - top3_launch_actions - top3_expansion_actions} support actions",
            'Timeline': "Dec 2024 - Feb 2025",
            'Priority': "MEDIUM"
        }
    ]

    for row_idx, data in enumerate(summary_data, start=1):
        priority_format_to_use = max_scaling_format if data['Priority'] == 'CRITICAL' else high_priority_format if data['Priority'] == 'HIGH' else medium_priority_format

        ws_summary.write(row_idx, 0, data['Metric'], priority_format_to_use)
        ws_summary.write(row_idx, 1, data['Current'], data_format)
        ws_summary.write(row_idx, 2, data['Target'], data_format)
        ws_summary.write(row_idx, 3, data['Gap'], data_format)
        ws_summary.write(row_idx, 4, data['Actions'], data_format)
        ws_summary.write(row_idx, 5, data['Timeline'], data_format)
        ws_summary.write(row_idx, 6, data['Priority'], priority_format_to_use)

    # 4. WEEKLY EXECUTION SHEET
    print("📊 4. Creating Weekly Execution sheet...")
    ws_weekly = workbook.add_worksheet('Weekly_Execution')

    weekly_headers = [
        'Week', 'Period', 'Focus Area', 'Launch Actions', 'Expansion Actions',
        'Revenue Target (₹)', 'Key Activities', 'Success Metrics', 'Risks & Mitigation'
    ]

    for col, header in enumerate(weekly_headers):
        ws_weekly.write(0, col, header, header_format)
        ws_weekly.set_column(col, col, 20)

    weekly_plan = []
    for week in range(1, 17):
        if week <= 4:
            period = f"Nov 2024 (W{week})"
            focus = "TOP 3 Expansion Priority"
        elif week <= 8:
            period = f"Dec 2024 (W{week})"
            focus = "TOP 3 Launch + Scale"
        elif week <= 12:
            period = f"Jan 2025 (W{week})"
            focus = "Secondary Activities"
        else:
            period = f"Feb 2025 (W{week})"
            focus = "Optimization & Final Push"

        week_launches = len([a for a in club_launch_actions if a['Target_Week'] == week])
        week_expansions = len([a for a in club_expansion_actions if a['Target_Week'] == week])

        week_revenue = sum([a['Revenue_Target'] for a in club_launch_actions if a['Target_Week'] == week]) + \
                      sum([a['Revenue_Impact'] for a in club_expansion_actions if a['Target_Week'] == week])

        if week <= 4:
            activities = "Expand existing TOP 3 clubs to maximum days"
            metrics = "90% expanded clubs operational"
            risks = "Venue availability, CM capacity"
        elif week <= 8:
            activities = "Launch TOP 3 new clubs + continue expansion"
            metrics = "80% new TOP 3 clubs operational"
            risks = "Marketing effectiveness, attendance"
        elif week <= 12:
            activities = "Launch secondary activity clubs"
            metrics = "70% secondary clubs operational"
            risks = "Market saturation, resource allocation"
        else:
            activities = "Final optimization + target achievement"
            metrics = "95% revenue targets achieved"
            risks = "Seasonal variations, retention"

        weekly_plan.append({
            'Week': f"W{week}",
            'Period': period,
            'Focus': focus,
            'Launch_Actions': week_launches,
            'Expansion_Actions': week_expansions,
            'Revenue_Target': week_revenue,
            'Activities': activities,
            'Metrics': metrics,
            'Risks': risks
        })

    for row_idx, plan in enumerate(weekly_plan, start=1):
        week_num = row_idx
        is_priority_week = week_num <= 8
        format_to_use = high_priority_format if is_priority_week else medium_priority_format

        ws_weekly.write(row_idx, 0, plan['Week'], format_to_use)
        ws_weekly.write(row_idx, 1, plan['Period'], format_to_use)
        ws_weekly.write(row_idx, 2, plan['Focus'], format_to_use)
        ws_weekly.write(row_idx, 3, plan['Launch_Actions'], number_format)
        ws_weekly.write(row_idx, 4, plan['Expansion_Actions'], number_format)
        ws_weekly.write(row_idx, 5, plan['Revenue_Target'], currency_format)
        ws_weekly.write(row_idx, 6, plan['Activities'], data_format)
        ws_weekly.write(row_idx, 7, plan['Metrics'], data_format)
        ws_weekly.write(row_idx, 8, plan['Risks'], data_format)

    # 5. MILESTONE SHEET
    print("📊 5. Creating Milestone sheet...")
    ws_milestone = workbook.add_worksheet('Milestone')

    milestone_headers = [
        'Milestone ID', 'Description', 'Target Date', 'Priority', 'Dependencies',
        'Success Criteria', 'Owner', 'Status', 'Progress %', 'Notes'
    ]

    for col, header in enumerate(milestone_headers):
        ws_milestone.write(0, col, header, header_format)
        ws_milestone.set_column(col, col, 18)

    milestones = [
        {
            'ID': 'M001',
            'Description': 'TOP 3 Club Expansions Complete',
            'Date': 'Dec 31, 2024',
            'Priority': 'CRITICAL',
            'Dependencies': 'Venue agreements, CM training',
            'Success': 'All TOP 3 clubs operational at target days',
            'Owner': 'Operations Team',
            'Status': 'NOT_STARTED',
            'Progress': 0,
            'Notes': 'Foundation for revenue scaling'
        },
        {
            'ID': 'M002',
            'Description': 'TOP 3 New Club Launches (Phase 1)',
            'Date': 'Jan 15, 2025',
            'Priority': 'CRITICAL',
            'Dependencies': 'Market research, venue setup',
            'Success': '50% of TOP 3 new clubs launched',
            'Owner': 'Launch Team',
            'Status': 'NOT_STARTED',
            'Progress': 0,
            'Notes': 'Critical for revenue targets'
        },
        {
            'ID': 'M003',
            'Description': 'Secondary Activities Scaling',
            'Date': 'Feb 15, 2025',
            'Priority': 'HIGH',
            'Dependencies': 'TOP 3 success, resource allocation',
            'Success': '70% of secondary clubs operational',
            'Owner': 'Growth Team',
            'Status': 'NOT_STARTED',
            'Progress': 0,
            'Notes': 'Balanced portfolio growth'
        },
        {
            'ID': 'M004',
            'Description': 'Revenue Target Achievement',
            'Date': 'Mar 31, 2025',
            'Priority': 'CRITICAL',
            'Dependencies': 'All previous milestones',
            'Success': '₹57.6L revenue achieved',
            'Owner': 'Executive Team',
            'Status': 'NOT_STARTED',
            'Progress': 0,
            'Notes': 'Ultimate success metric'
        }
    ]

    for row_idx, milestone in enumerate(milestones, start=1):
        priority_format_to_use = max_scaling_format if milestone['Priority'] == 'CRITICAL' else high_priority_format

        ws_milestone.write(row_idx, 0, milestone['ID'], priority_format_to_use)
        ws_milestone.write(row_idx, 1, milestone['Description'], data_format)
        ws_milestone.write(row_idx, 2, milestone['Date'], data_format)
        ws_milestone.write(row_idx, 3, milestone['Priority'], priority_format_to_use)
        ws_milestone.write(row_idx, 4, milestone['Dependencies'], data_format)
        ws_milestone.write(row_idx, 5, milestone['Success'], data_format)
        ws_milestone.write(row_idx, 6, milestone['Owner'], data_format)

        ws_milestone.data_validation(row_idx, 7, row_idx, 7, {
            'validate': 'list',
            'source': ['NOT_STARTED', 'IN_PROGRESS', 'BLOCKED', 'DONE']
        })
        ws_milestone.write(row_idx, 7, milestone['Status'], dropdown_format)

        ws_milestone.write(row_idx, 8, milestone['Progress'], number_format)
        ws_milestone.write(row_idx, 9, milestone['Notes'], data_format)

    # 6. CITY PROGRESS SHEET
    print("📊 6. Creating City Progress sheet...")
    ws_city = workbook.add_worksheet('City_Progress')

    city_headers = [
        'City', 'Activity', 'Current Clubs', 'Target Clubs', 'New Clubs Needed',
        'Current Revenue', 'Target Revenue', 'Revenue Gap', 'Progress %',
        'Launch Actions', 'Expansion Actions', 'Total Actions', 'Priority Level'
    ]

    for col, header in enumerate(city_headers):
        ws_city.write(0, col, header, header_format)
        ws_city.set_column(col, col, 15)

    city_progress = []
    for idx, row in working_sheet.iterrows():
        activity = row['Activity']
        city = row['City']
        current_clubs = row['Current_Clubs_Count'] if pd.notna(row['Current_Clubs_Count']) else 0
        target_clubs = row['Clubs_Needed_Feb'] if pd.notna(row['Clubs_Needed_Feb']) else current_clubs
        current_revenue = row['Current revenue']
        target_revenue = row['Revenue by March']

        new_clubs_needed = target_clubs - current_clubs if target_clubs > current_clubs else 0
        revenue_gap = target_revenue - current_revenue
        progress_pct = (current_revenue / target_revenue * 100) if target_revenue > 0 else 100

        launch_actions_count = len([a for a in club_launch_actions if a['Activity'] == activity and a['City'] == city])
        expansion_actions_count = len([a for a in club_expansion_actions if a['Activity'] == activity and a['City'] == city])
        total_actions = launch_actions_count + expansion_actions_count

        is_top3 = activity in TOP_3_MAXIMUM_SCALING
        priority_level = "HIGH" if is_top3 else "MEDIUM" if revenue_gap > 50000 else "LOW"

        city_progress.append({
            'City': city,
            'Activity': activity,
            'Current_Clubs': current_clubs,
            'Target_Clubs': target_clubs,
            'New_Clubs_Needed': new_clubs_needed,
            'Current_Revenue': current_revenue,
            'Target_Revenue': target_revenue,
            'Revenue_Gap': revenue_gap,
            'Progress_Pct': progress_pct,
            'Launch_Actions': launch_actions_count,
            'Expansion_Actions': expansion_actions_count,
            'Total_Actions': total_actions,
            'Priority_Level': priority_level
        })

    city_progress.sort(key=lambda x: (0 if x['Activity'] in TOP_3_MAXIMUM_SCALING else 1, -x['Revenue_Gap']))

    for row_idx, progress in enumerate(city_progress, start=1):
        is_top3_activity = progress['Activity'] in TOP_3_MAXIMUM_SCALING
        format_to_use = max_scaling_format if is_top3_activity else data_format

        ws_city.write(row_idx, 0, progress['City'], data_format)
        ws_city.write(row_idx, 1, progress['Activity'], format_to_use)
        ws_city.write(row_idx, 2, progress['Current_Clubs'], number_format)
        ws_city.write(row_idx, 3, progress['Target_Clubs'], number_format)
        ws_city.write(row_idx, 4, progress['New_Clubs_Needed'], number_format)
        ws_city.write(row_idx, 5, progress['Current_Revenue'], currency_format)
        ws_city.write(row_idx, 6, progress['Target_Revenue'], currency_format)
        ws_city.write(row_idx, 7, progress['Revenue_Gap'], currency_format)
        ws_city.write(row_idx, 8, progress['Progress_Pct'], number_format)
        ws_city.write(row_idx, 9, progress['Launch_Actions'], number_format)
        ws_city.write(row_idx, 10, progress['Expansion_Actions'], number_format)
        ws_city.write(row_idx, 11, progress['Total_Actions'], number_format)
        ws_city.write(row_idx, 12, progress['Priority_Level'], format_to_use)

    # 7. WORKING SHEET (Original)
    print("📊 7. Creating Working Sheet (original)...")
    ws_working = workbook.add_worksheet('Working_Sheet')

    for col_idx, col_name in enumerate(working_sheet.columns):
        ws_working.write(0, col_idx, col_name, header_format)
        ws_working.set_column(col_idx, col_idx, 15 if col_idx < 9 else 12)

    for row_idx, (idx, row) in enumerate(working_sheet.iterrows(), start=1):
        for col_idx, value in enumerate(row):
            if pd.isna(value):
                value = ""
            ws_working.write(row_idx, col_idx, value, data_format)

    # 8. EVENTS SHEET (Original - keep as is)
    print("📊 8. Creating Events sheet (original)...")
    ws_events = workbook.add_worksheet('Events')

    if events_sheet is not None:
        for col_idx, col_name in enumerate(events_sheet.columns):
            ws_events.write(0, col_idx, col_name, header_format)
            ws_events.set_column(col_idx, col_idx, 15)

        for row_idx, (idx, row) in enumerate(events_sheet.iterrows(), start=1):
            for col_idx, value in enumerate(row):
                if pd.isna(value):
                    value = ""
                ws_events.write(row_idx, col_idx, value, data_format)
    else:
        ws_events.write(0, 0, "Events sheet not found in original file", header_format)

    # 9. LOGIC SHEET
    print("📊 9. Creating Logic sheet...")
    ws_logic = workbook.add_worksheet('Logic')

    logic_headers = ['Component', 'Logic', 'Formula/Calculation', 'Purpose']

    for col, header in enumerate(logic_headers):
        ws_logic.write(0, col, header, header_format)
        ws_logic.set_column(col, col, 25)

    logic_explanations = [
        {
            'Component': 'Club Launches',
            'Logic': 'New clubs needed = Clubs_Needed_Feb - Current_Clubs_Count',
            'Formula': 'IF(Clubs_Needed_Feb > Current_Clubs_Count, Clubs_Needed_Feb - Current_Clubs_Count, 0)',
            'Purpose': 'Identify gaps requiring new club launches'
        },
        {
            'Component': 'Club Expansions',
            'Logic': 'Expansion needed if target days > current days OR target capacity > current capacity',
            'Formula': 'IF(OR(target_days > current_days, target_attendance > current_attendance), TRUE, FALSE)',
            'Purpose': 'Identify existing clubs needing scaling'
        },
        {
            'Component': 'TOP 3 Prioritization',
            'Logic': 'BOARDGAMING, SOCIAL_DEDUCTIONS, MUSIC get maximum scaling (7 days/week)',
            'Formula': 'IF(Activity IN [BOARDGAMING, SOCIAL_DEDUCTIONS, MUSIC], "HIGH", revenue_based_priority)',
            'Purpose': 'Focus maximum resources on highest impact activities'
        },
        {
            'Component': 'Revenue Calculation',
            'Logic': 'Revenue = Days/week × Attendance × Price × 4 weeks',
            'Formula': 'target_days × target_attendance × price × 4',
            'Purpose': 'Calculate monthly revenue potential'
        },
        {
            'Component': 'Timeline Distribution',
            'Logic': 'TOP 3 in weeks 1-8, Secondary in weeks 5-16',
            'Formula': 'IF(TOP3, WEEK(1-8), WEEK(5-16))',
            'Purpose': 'Phased execution prioritizing high-impact activities'
        },
        {
            'Component': 'Priority Assignment',
            'Logic': 'HIGH for TOP 3, MEDIUM for revenue >50k, LOW for others',
            'Formula': 'IF(TOP3, "HIGH", IF(revenue_gap > 50000, "MEDIUM", "LOW"))',
            'Purpose': 'Resource allocation based on impact'
        }
    ]

    for row_idx, logic in enumerate(logic_explanations, start=1):
        ws_logic.write(row_idx, 0, logic['Component'], high_priority_format)
        ws_logic.write(row_idx, 1, logic['Logic'], data_format)
        ws_logic.write(row_idx, 2, logic['Formula'], data_format)
        ws_logic.write(row_idx, 3, logic['Purpose'], data_format)

    workbook.close()

    print("✅ Exact plan structure created!")
    print(f"📁 File: OND-JFM EXACT PLAN STRUCTURE V12.xlsx")

    print(f"\n🎯 PLAN STRUCTURE SUMMARY:")
    print(f"📋 Total Actions: {len(club_launch_actions) + len(club_expansion_actions)}")
    print(f"🚀 Club Launches: {len(club_launch_actions)}")
    print(f"📈 Club Expansions: {len(club_expansion_actions)}")

    print(f"\n📊 SHEETS IN ORDER:")
    print("1. Club_Expansion - All expansion actions with specific club details")
    print("2. Club_Launches - All launch actions with specific details")
    print("3. Summary - High-level metrics and targets")
    print("4. Weekly_Execution - 16-week execution plan")
    print("5. Milestone - Key milestone tracking")
    print("6. City_Progress - Progress by city and activity")
    print("7. Working_Sheet - Original master data")
    print("8. Events - Original events data (kept as is)")
    print("9. Logic - Calculation explanations and formulas")

if __name__ == "__main__":
    create_exact_plan_structure()