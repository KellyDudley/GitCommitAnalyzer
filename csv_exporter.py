"""
CSV Export module for Git Commit Analyzer
"""

import csv
import pandas as pd
from datetime import datetime


class CSVExporter:
    def __init__(self):
        pass
    
    def export_commit_details(self, repo, output_file="commits.csv"):
        """Export detailed commit information to CSV."""
        commits_data = []
        
        for commit in repo.iter_commits():
            commit_info = {
                'hash': commit.hexsha[:8],
                'author': commit.author.name,
                'author_email': commit.author.email,
                'date': commit.committed_datetime.isoformat(),
                'message': commit.message.strip().replace('\n', ' '),
                'files_changed': len(commit.stats.files),
                'insertions': commit.stats.total['insertions'],
                'deletions': commit.stats.total['deletions'],
                'weekday': commit.committed_datetime.strftime('%A'),
                'hour': commit.committed_datetime.hour
            }
            commits_data.append(commit_info)
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            if commits_data:
                fieldnames = commits_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(commits_data)
        
        return output_file, len(commits_data)
    
    def export_author_stats(self, stats, output_file="authors.csv"):
        """Export author statistics to CSV."""
        authors_data = []
        
        for author, count in stats.get('authors', {}).items():
            authors_data.append({
                'author': author,
                'commit_count': count,
                'percentage': round(count / stats['total_commits'] * 100, 2)
            })
        
        # Sort by commit count descending
        authors_data.sort(key=lambda x: x['commit_count'], reverse=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            if authors_data:
                fieldnames = ['author', 'commit_count', 'percentage']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(authors_data)
        
        return output_file, len(authors_data)
    
    def export_frequency_data(self, frequency_stats, output_file="frequency.csv"):
        """Export frequency analysis data to CSV."""
        freq_data = []
        
        # Hourly distribution
        for hour, count in frequency_stats.get('hourly_distribution', {}).items():
            freq_data.append({
                'type': 'hourly',
                'category': f'{hour:02d}:00',
                'count': count
            })
        
        # Weekday distribution
        for day, count in frequency_stats.get('weekday_distribution', {}).items():
            freq_data.append({
                'type': 'weekday',
                'category': day,
                'count': count
            })
        
        # Monthly distribution
        for month, count in frequency_stats.get('monthly_commits', {}).items():
            freq_data.append({
                'type': 'monthly',
                'category': month,
                'count': count
            })
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            if freq_data:
                fieldnames = ['type', 'category', 'count']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(freq_data)
        
        return output_file, len(freq_data)
    
    def export_daily_timeline(self, frequency_stats, output_file="timeline.csv"):
        """Export daily commit timeline to CSV."""
        daily_data = []
        
        for date_str, count in frequency_stats.get('daily_commits', {}).items():
            daily_data.append({
                'date': date_str,
                'commits': count
            })
        
        # Sort by date
        daily_data.sort(key=lambda x: x['date'])
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            if daily_data:
                fieldnames = ['date', 'commits']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(daily_data)
        
        return output_file, len(daily_data)