# Time Tracking Application

A simple command-line application to track time spent on various tasks organized by projects with daily records.

## Features

- **Projects**: Organize your work into projects
- **Tasks**: Create tasks under each project
- **Daily Records**: Each day has its own record with a start time
- **Notes**: Add multiple notes throughout the day with time tracking
- **Automatic Time Calculation**: Time is calculated based on your start time and cumulative minutes worked
- **Data Persistence**: All data is saved to a JSON file

## Installation

No installation required! Just ensure you have Python 3.6+ installed.

## Usage

### Starting the Application

Run the application with:

```bash
python3 time_tracker.py
```

Or make it executable and run directly:

```bash
chmod +x time_tracker.py
./time_tracker.py
```

### Commands

#### Managing Projects

**Add a new project:**
```
> project add ClientWebsite
```

**List all projects:**
```
> project list
```

#### Managing Tasks

**Add a task to a project:**
```
> task add ClientWebsite Design homepage
```

**List all tasks:**
```
> task list
```

**List tasks for a specific project:**
```
> task list ClientWebsite
```

#### Tracking Time

**Start your workday (required before adding notes):**
```
> start 09:00
```
This sets your start time for today at 9:00 AM.

**Add a note with time spent:**
```
> note "Design homepage" 30 Created mockup for header section
```
This adds a note to the "Design homepage" task indicating you spent 30 minutes on it.

**View today's summary:**
```
> today
```
Shows all notes for today, grouped by task and project, with time calculations.

**View a specific day's summary:**
```
> day 2025-10-24
```

**List all recorded days:**
```
> days
```

#### Other Commands

**Show help:**
```
> help
```

**Exit the application:**
```
> quit
```

## Example Workflow

Here's a typical workflow for using the time tracker:

```bash
# 1. Start the application
python3 time_tracker.py

# 2. Create projects
> project add ClientWebsite
> project add InternalTools

# 3. Add tasks to projects
> task add ClientWebsite "Design homepage"
> task add ClientWebsite "Implement contact form"
> task add InternalTools "Bug fixes"

# 4. Start your workday
> start 09:00

# 5. Add notes throughout the day as you work
> note "Design homepage" 45 Initial mockup in Figma
> note "Design homepage" 30 Refined color scheme
> note "Implement contact form" 60 Created HTML structure
> note "Bug fixes" 20 Fixed login issue

# 6. View your daily summary
> today
```

## Data Structure

### Projects
Projects are top-level containers for organizing related tasks.

### Tasks
Tasks belong to a project and represent specific work items.

### Daily Records
Each day you work, you create a daily record with a start time. The system tracks:
- Date
- Start time
- All notes for that day

### Notes
Notes are time entries that belong to a task. Each note includes:
- Task name
- Content/description
- Minutes spent
- Timestamp when the note was added

The current time is automatically calculated based on:
- Your start time for the day
- Sum of all minutes from previous notes

## Data Storage

All data is stored in `time_tracker_data.json` in the same directory as the application. This file is automatically created on first use and updated whenever you make changes.

The data structure includes:
- All projects
- All tasks with their project associations
- Daily records with notes

## Time Calculation

The application calculates your current time based on:
1. Your start time for the day
2. The cumulative minutes you've logged in notes

For example:
- Start time: 09:00
- First note: 30 minutes → Current time: 09:30
- Second note: 45 minutes → Current time: 10:15
- Third note: 15 minutes → Current time: 10:30

This helps you track where you are in your workday and ensures accurate time logging.

## Tips

1. **Start each day**: Always use the `start` command when you begin working
2. **Frequent notes**: Add notes regularly throughout the day for accurate tracking
3. **Be specific**: Include meaningful descriptions in your notes
4. **Review daily**: Use `today` at the end of your day to review your work
5. **Task names**: Use clear, descriptive task names that you'll remember

## Requirements

- Python 3.6 or higher
- No external dependencies required

## License

This is a personal time tracking tool. Use and modify as needed.
