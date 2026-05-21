import pandas as pd

# 1. Load the dataset and convert strings to actual datetime objects
df = pd.read_csv('mock_helpdesk_logs.csv')
df['Created_Time'] = pd.to_datetime(df['Created_Time'])
df['Resolved_Time'] = pd.to_datetime(df['Resolved_Time'])

# 2. Calculate actual resolution time in hours
df['Resolution_Hours'] = (df['Resolved_Time'] - df['Created_Time']).dt.total_seconds() / 3600

# 3. Define the SLA rule evaluation function
def check_sla_breach(row):
    if row['Priority'] == 'P1' and row['Resolution_Hours'] > 2.0:
        return 'BREACHED'
    elif row['Priority'] == 'P2' and row['Resolution_Hours'] > 8.0:
        return 'BREACHED'
    elif row['Priority'] == 'P3' and row['Resolution_Hours'] > 24.0:
        return 'BREACHED'
    else:
        return 'COMPLIANT'

# Apply the function across the dataset
df['SLA_Status'] = df.apply(check_sla_breach, axis=1)

# 4. Aggregate Performance Metrics by Vendor
vendor_summary = df.groupby('Vendor_Name').agg(
    Total_Tickets=('Ticket_ID', 'count'),
    Avg_Resolution_Hours=('Resolution_Hours', 'mean'),
    Total_Breaches=('SLA_Status', lambda x: (x == 'BREACHED').sum())
).reset_index()

# Calculate the critical SLA Compliance Rate percentage
vendor_summary['SLA_Compliance_Rate'] = ((vendor_summary['Total_Tickets'] - vendor_summary['Total_Breaches']) / vendor_summary['Total_Tickets']) * 100

print("\n=== VENDOR PERFORMANCE RESULTS ===")
print(vendor_summary.to_string(index=False))

# Export the raw breaches for the executive report
breaches_df = df[df['SLA_Status'] == 'BREACHED']
breaches_df.to_csv('flagged_sla_breaches.csv', index=False)