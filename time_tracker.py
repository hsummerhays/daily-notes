#!/usr/bin/env python3
"""
Time Tracking Application
Track time spent on tasks organized by projects with daily records.
"""

import json
import os
import shlex
from datetime import datetime, date
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


DATA_FILE = "time_tracker_data.json"


@dataclass
class Note:
    """A note entry with time tracking for a specific task."""
    task_name: str
    content: str
    minutes: int
    timestamp: str

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'Note':
        return Note(**data)


@dataclass
class DailyRecord:
    """Represents a day's work with start time and notes."""
    date: str  # YYYY-MM-DD format
    start_time: str  # HH:MM format
    notes: List[Dict]  # List of note dictionaries

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'DailyRecord':
        return DailyRecord(**data)

    def get_total_minutes(self) -> int:
        """Calculate total minutes worked today."""
        return sum(note['minutes'] for note in self.notes)

    def get_current_time(self) -> str:
        """Calculate current time based on start time and total minutes."""
        start_hour, start_min = map(int, self.start_time.split(':'))
        total_minutes = self.get_total_minutes()

        current_hour = start_hour + (start_min + total_minutes) // 60
        current_min = (start_min + total_minutes) % 60

        return f"{current_hour:02d}:{current_min:02d}"


@dataclass
class Task:
    """A task that belongs to a project."""
    name: str
    project_name: str

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'Task':
        return Task(**data)


@dataclass
class Project:
    """A project that contains multiple tasks."""
    name: str

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'Project':
        return Project(**data)


class TimeTracker:
    """Main time tracking application."""

    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.projects: List[Project] = []
        self.tasks: List[Task] = []
        self.daily_records: List[DailyRecord] = []
        self.load_data()

    def load_data(self):
        """Load data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.projects = [Project.from_dict(p) for p in data.get('projects', [])]
                    self.tasks = [Task.from_dict(t) for t in data.get('tasks', [])]
                    self.daily_records = [DailyRecord.from_dict(d) for d in data.get('daily_records', [])]
            except Exception as e:
                print(f"Error loading data: {e}")
                self.projects = []
                self.tasks = []
                self.daily_records = []

    def save_data(self):
        """Save data to JSON file."""
        data = {
            'projects': [p.to_dict() for p in self.projects],
            'tasks': [t.to_dict() for t in self.tasks],
            'daily_records': [d.to_dict() for d in self.daily_records]
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_project(self, name: str) -> bool:
        """Add a new project."""
        if any(p.name == name for p in self.projects):
            print(f"Project '{name}' already exists.")
            return False
        self.projects.append(Project(name=name))
        self.save_data()
        print(f"Project '{name}' created successfully.")
        return True

    def list_projects(self):
        """List all projects."""
        if not self.projects:
            print("No projects found.")
            return
        print("\n=== Projects ===")
        for i, project in enumerate(self.projects, 1):
            task_count = len([t for t in self.tasks if t.project_name == project.name])
            print(f"{i}. {project.name} ({task_count} tasks)")

    def add_task(self, project_name: str, task_name: str) -> bool:
        """Add a new task to a project."""
        if not any(p.name == project_name for p in self.projects):
            print(f"Project '{project_name}' does not exist.")
            return False

        if any(t.name == task_name and t.project_name == project_name for t in self.tasks):
            print(f"Task '{task_name}' already exists in project '{project_name}'.")
            return False

        self.tasks.append(Task(name=task_name, project_name=project_name))
        self.save_data()
        print(f"Task '{task_name}' added to project '{project_name}'.")
        return True

    def list_tasks(self, project_name: Optional[str] = None):
        """List all tasks, optionally filtered by project."""
        tasks = self.tasks
        if project_name:
            tasks = [t for t in tasks if t.project_name == project_name]

        if not tasks:
            print("No tasks found.")
            return

        print("\n=== Tasks ===")
        current_project = None
        for task in sorted(tasks, key=lambda t: (t.project_name, t.name)):
            if task.project_name != current_project:
                current_project = task.project_name
                print(f"\n{current_project}:")
            print(f"  - {task.name}")

    def start_day(self, start_time: str, date_str: Optional[str] = None) -> bool:
        """Start a new day with a start time."""
        if date_str is None:
            date_str = date.today().isoformat()

        # Validate time format
        try:
            datetime.strptime(start_time, "%H:%M")
        except ValueError:
            print("Invalid time format. Please use HH:MM format (e.g., 09:00)")
            return False

        # Check if day already started
        if any(d.date == date_str for d in self.daily_records):
            print(f"Day {date_str} already started.")
            return False

        self.daily_records.append(DailyRecord(date=date_str, start_time=start_time, notes=[]))
        self.save_data()
        print(f"Started day {date_str} at {start_time}")
        return True

    def get_today_record(self) -> Optional[DailyRecord]:
        """Get today's daily record."""
        today = date.today().isoformat()
        for record in self.daily_records:
            if record.date == today:
                return record
        return None

    def add_note(self, task_name: str, content: str, minutes: int) -> bool:
        """Add a note to a task for today."""
        today_record = self.get_today_record()

        if today_record is None:
            print("Please start the day first using 'start' command.")
            return False

        # Find the task
        task = None
        for t in self.tasks:
            if t.name == task_name:
                task = t
                break

        if task is None:
            print(f"Task '{task_name}' not found.")
            return False

        # Create note
        timestamp = datetime.now().strftime("%H:%M:%S")
        note = Note(
            task_name=task_name,
            content=content,
            minutes=minutes,
            timestamp=timestamp
        )

        today_record.notes.append(note.to_dict())
        self.save_data()

        current_time = today_record.get_current_time()
        print(f"Note added to '{task_name}' ({minutes} min). Current time: {current_time}")
        return True

    def show_today(self):
        """Show today's summary."""
        today_record = self.get_today_record()

        if today_record is None:
            print("No record for today. Start the day first.")
            return

        today = date.today().isoformat()
        print(f"\n=== Daily Summary for {today} ===")
        print(f"Start Time: {today_record.start_time}")
        print(f"Total Minutes: {today_record.get_total_minutes()}")
        print(f"Current Time: {today_record.get_current_time()}")

        if not today_record.notes:
            print("\nNo notes yet.")
            return

        print("\n=== Notes ===")
        # Group notes by task
        task_notes = {}
        for note_dict in today_record.notes:
            task_name = note_dict['task_name']
            if task_name not in task_notes:
                task_notes[task_name] = []
            task_notes[task_name].append(note_dict)

        for task_name, notes in task_notes.items():
            # Find project for this task
            project_name = "Unknown"
            for task in self.tasks:
                if task.name == task_name:
                    project_name = task.project_name
                    break

            print(f"\n[{project_name}] {task_name}:")
            task_total = sum(n['minutes'] for n in notes)
            for note_dict in notes:
                print(f"  • {note_dict['content']} ({note_dict['minutes']} min) - {note_dict['timestamp']}")
            print(f"  Total: {task_total} minutes")

    def show_day(self, date_str: str):
        """Show summary for a specific date."""
        record = None
        for r in self.daily_records:
            if r.date == date_str:
                record = r
                break

        if record is None:
            print(f"No record found for {date_str}")
            return

        print(f"\n=== Daily Summary for {date_str} ===")
        print(f"Start Time: {record.start_time}")
        print(f"Total Minutes: {record.get_total_minutes()}")
        print(f"End Time: {record.get_current_time()}")

        if not record.notes:
            print("\nNo notes for this day.")
            return

        print("\n=== Notes ===")
        # Group notes by task
        task_notes = {}
        for note_dict in record.notes:
            task_name = note_dict['task_name']
            if task_name not in task_notes:
                task_notes[task_name] = []
            task_notes[task_name].append(note_dict)

        for task_name, notes in task_notes.items():
            # Find project for this task
            project_name = "Unknown"
            for task in self.tasks:
                if task.name == task_name:
                    project_name = task.project_name
                    break

            print(f"\n[{project_name}] {task_name}:")
            task_total = sum(n['minutes'] for n in notes)
            for note_dict in notes:
                print(f"  • {note_dict['content']} ({note_dict['minutes']} min) - {note_dict['timestamp']}")
            print(f"  Total: {task_total} minutes")

    def list_days(self):
        """List all recorded days."""
        if not self.daily_records:
            print("No daily records found.")
            return

        print("\n=== Daily Records ===")
        for record in sorted(self.daily_records, key=lambda r: r.date, reverse=True):
            total_min = record.get_total_minutes()
            note_count = len(record.notes)
            print(f"{record.date}: {total_min} min, {note_count} notes (Start: {record.start_time})")


def main():
    """Main CLI interface."""
    tracker = TimeTracker()

    print("=" * 50)
    print("Time Tracking Application")
    print("=" * 50)
    print("\nCommands:")
    print("  project add <name>           - Add a new project")
    print("  project list                 - List all projects")
    print("  task add <project> <task>    - Add a task to a project")
    print("  task list [project]          - List all tasks or tasks in a project")
    print("  start <HH:MM>                - Start today with a start time")
    print("  note <task> <minutes> <text> - Add a note to a task")
    print("  today                        - Show today's summary")
    print("  day <YYYY-MM-DD>             - Show summary for a specific day")
    print("  days                         - List all recorded days")
    print("  help                         - Show this help message")
    print("  quit                         - Exit the application")
    print()

    while True:
        try:
            command = input("\n> ").strip()

            if not command:
                continue

            # Use shlex to properly handle quoted strings
            try:
                parts = shlex.split(command)
            except ValueError as e:
                print(f"Error parsing command: {e}")
                continue

            cmd = parts[0].lower()

            if cmd == "quit" or cmd == "exit":
                print("Goodbye!")
                break

            elif cmd == "help":
                print("\nCommands:")
                print("  project add <name>           - Add a new project")
                print("  project list                 - List all projects")
                print("  task add <project> <task>    - Add a task to a project")
                print("  task list [project]          - List all tasks or tasks in a project")
                print("  start <HH:MM>                - Start today with a start time")
                print("  note <task> <minutes> <text> - Add a note to a task")
                print("  today                        - Show today's summary")
                print("  day <YYYY-MM-DD>             - Show summary for a specific day")
                print("  days                         - List all recorded days")
                print("  help                         - Show this help message")
                print("  quit                         - Exit the application")

            elif cmd == "project":
                if len(parts) < 2:
                    print("Usage: project add <name> | project list")
                    continue

                subcmd = parts[1].lower()
                if subcmd == "add":
                    if len(parts) < 3:
                        print("Usage: project add <name>")
                    else:
                        project_name = " ".join(parts[2:])
                        tracker.add_project(project_name)

                elif subcmd == "list":
                    tracker.list_projects()

                else:
                    print(f"Unknown subcommand: {subcmd}")

            elif cmd == "task":
                if len(parts) < 2:
                    print("Usage: task add <project> <task> | task list [project]")
                    continue

                subcmd = parts[1].lower()
                if subcmd == "add":
                    if len(parts) < 4:
                        print("Usage: task add <project> <task>")
                    else:
                        project_name = parts[2]
                        task_name = " ".join(parts[3:])
                        tracker.add_task(project_name, task_name)

                elif subcmd == "list":
                    project_name = parts[2] if len(parts) > 2 else None
                    tracker.list_tasks(project_name)

                else:
                    print(f"Unknown subcommand: {subcmd}")

            elif cmd == "start":
                if len(parts) < 2:
                    print("Usage: start <HH:MM>")
                else:
                    start_time = parts[1]
                    tracker.start_day(start_time)

            elif cmd == "note":
                if len(parts) < 4:
                    print("Usage: note <task> <minutes> <text>")
                else:
                    task_name = parts[1]
                    try:
                        minutes = int(parts[2])
                        content = " ".join(parts[3:])
                        tracker.add_note(task_name, content, minutes)
                    except ValueError:
                        print("Minutes must be a number")

            elif cmd == "today":
                tracker.show_today()

            elif cmd == "day":
                if len(parts) < 2:
                    print("Usage: day <YYYY-MM-DD>")
                else:
                    date_str = parts[1]
                    tracker.show_day(date_str)

            elif cmd == "days":
                tracker.list_days()

            else:
                print(f"Unknown command: {cmd}. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
