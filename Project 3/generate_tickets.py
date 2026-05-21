import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for consistent results
np.random.seed(42)
num_tickets = 550

# 1. Define our enterprise parameters
priorities = ['P1', 'P2', 'P3']
priority_probs = [0.15, 0.35, 0.50]  # P3s are more common than critical P1s
vendors = ['NetConnect Solutions', 'Malawi Cloud Partners', 'InnoTech Hardware', 'Internal IT Desk']
issues = {
    'P1': 'ERP System Down, Core Switch Failure, Database Corruption',
    'P2': 'Email Server Delay, Printer Network Offline, VPN Connectivity Issue',
    'P3': 'Password Reset, Software Installation, New Employee Onboarding Set'
}

# 2. Generate timestamps
base_date = datetime(2026, 1, 1)
created_times = [base_date + timedelta(days=np.random.randint(0, 90), 
                                      hours=np.random.randint(0, 24), 
                                      minutes=np.random.randint(0, 60)) for _ in range(num_tickets)]

data = []
for i in range(num_tickets):
    prio = np.random.choice(priorities, p=priority_probs)
    vendor = np.random.choice(vendors)
    created = created_times[i]
    
    # Simulate resolution time based on priority (adding some deliberate SLA breaches)
    if prio == 'P1':
        # Mostly fast, but some bad 3-5 hour resolution times to simulate breaches
        hours_to_resolve = np.random.exponential(scale=1.5) 
    elif prio == 'P2':
        hours_to_resolve = np.random.uniform(2, 12)
    else:
        hours_to_resolve = np.random.uniform(4, 36)
        
    resolved = created + timedelta(hours=hours_to_resolve)
    
    data.append({
        'Ticket_ID': f'TICK-{1000+i}',
        'Priority': prio,
        'Issue_Category': np.random.choice(issues[prio].split(', ')),
        'Created_Time': created,
        'Resolved_Time': resolved,
        'Vendor_Name': vendor
    })

# 3. Save to a raw CSV data file
df = pd.DataFrame(data)
df.to_csv('mock_helpdesk_logs.csv', index=False)
print("Successfully generated mock_helpdesk_logs.csv with 550 entries!")