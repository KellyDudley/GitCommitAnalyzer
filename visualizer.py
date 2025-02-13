"""
Visualization module for Git Commit Analyzer
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
import os

class CommitVisualizer:
    def __init__(self, output_dir="plots"):
        """Initialize the visualizer with output directory."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def plot_hourly_distribution(self, hourly_data, save=True):
        """Create a bar chart showing commit distribution by hour."""
        hours = list(range(24))
        counts = [hourly_data.get(h, 0) for h in hours]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(hours, counts, color='skyblue', alpha=0.7)
        
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Commits')
        plt.title('Commit Distribution by Hour')
        plt.xticks(range(0, 24, 2))
        plt.grid(True, alpha=0.3)
        
        # Highlight the most active hour
        max_hour = max(hourly_data.items(), key=lambda x: x[1])[0] if hourly_data else 0
        bars[max_hour].set_color('orange')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f"{self.output_dir}/hourly_distribution.png", dpi=300, bbox_inches='tight')
            plt.close()
            return f"{self.output_dir}/hourly_distribution.png"
        else:
            plt.show()
            return None
    
    def plot_weekday_distribution(self, weekday_data, save=True):
        """Create a bar chart showing commit distribution by weekday."""
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        counts = [weekday_data.get(day, 0) for day in weekdays]
        
        plt.figure(figsize=(10, 6))
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6']
        bars = plt.bar(weekdays, counts, color=colors, alpha=0.8)
        
        plt.xlabel('Day of Week')
        plt.ylabel('Number of Commits')
        plt.title('Commit Distribution by Weekday')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f"{self.output_dir}/weekday_distribution.png", dpi=300, bbox_inches='tight')
            plt.close()
            return f"{self.output_dir}/weekday_distribution.png"
        else:
            plt.show()
            return None
    
    def plot_commit_timeline(self, daily_commits, save=True):
        """Create a line chart showing commits over time."""
        if not daily_commits:
            return None
            
        dates = [datetime.fromisoformat(date) for date in daily_commits.keys()]
        counts = list(daily_commits.values())
        
        plt.figure(figsize=(14, 6))
        plt.plot(dates, counts, marker='o', linestyle='-', linewidth=2, markersize=4)
        
        plt.xlabel('Date')
        plt.ylabel('Number of Commits')
        plt.title('Commit Activity Timeline')
        
        # Format x-axis to show dates nicely
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        plt.xticks(rotation=45)
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save:
            plt.savefig(f"{self.output_dir}/commit_timeline.png", dpi=300, bbox_inches='tight')
            plt.close()
            return f"{self.output_dir}/commit_timeline.png"
        else:
            plt.show()
            return None
    
    def generate_all_plots(self, frequency_data):
        """Generate all visualization plots."""
        plots_generated = []
        
        if 'hourly_distribution' in frequency_data:
            plot_path = self.plot_hourly_distribution(frequency_data['hourly_distribution'])
            if plot_path:
                plots_generated.append(plot_path)
        
        if 'weekday_distribution' in frequency_data:
            plot_path = self.plot_weekday_distribution(frequency_data['weekday_distribution'])
            if plot_path:
                plots_generated.append(plot_path)
        
        if 'daily_commits' in frequency_data:
            plot_path = self.plot_commit_timeline(frequency_data['daily_commits'])
            if plot_path:
                plots_generated.append(plot_path)
        
        return plots_generated