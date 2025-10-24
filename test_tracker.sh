#!/bin/bash
# Test script for time tracker

echo "Testing Time Tracker Application..."

# Clean up any existing data
rm -f time_tracker_data.json

# Create a test commands file
cat > /tmp/test_commands.txt << 'EOF'
project add ClientWebsite
project add InternalTools
project list
task add ClientWebsite "Design homepage"
task add ClientWebsite "Implement contact form"
task add InternalTools "Bug fixes"
task list
start 09:00
note "Design homepage" 45 Initial mockup in Figma
note "Design homepage" 30 Refined color scheme
note "Implement contact form" 60 Created HTML structure
note "Bug fixes" 20 Fixed login issue
today
days
quit
EOF

# Run the time tracker with test commands
python3 time_tracker.py < /tmp/test_commands.txt

echo ""
echo "Test completed!"
echo ""
echo "Checking data file..."
if [ -f time_tracker_data.json ]; then
    echo "Data file created successfully!"
    echo ""
    cat time_tracker_data.json
else
    echo "Error: Data file not created"
fi
