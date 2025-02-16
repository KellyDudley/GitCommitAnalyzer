#!/usr/bin/env python3
"""
Git Commit Analyzer
A comprehensive tool for analyzing Git repository commit history and generating statistics.

Author: KellyDudley
Version: 1.0.0
License: MIT
"""

import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import calendar

try:
    import git
    import click
    from visualizer import CommitVisualizer
    from report_generator import HTMLReportGenerator
    from csv_exporter import CSVExporter
except ImportError as e:
    print(f"Required packages not installed. Please run: pip install -r requirements.txt")
    print(f"Import error: {e}")
    sys.exit(1)


class GitCommitAnalyzer:
    def __init__(self, repo_path="."):
        """Initialize the analyzer with a repository path."""
        self.repo_path = repo_path
        try:
            self.repo = git.Repo(repo_path)
        except git.exc.InvalidGitRepositoryError:
            raise ValueError(f"'{repo_path}' is not a valid Git repository")
    
    def get_commit_stats(self):
        """Get basic commit statistics."""
        commits = list(self.repo.iter_commits())
        total_commits = len(commits)
        
        if total_commits == 0:
            return {"total_commits": 0, "authors": [], "date_range": None}
        
        authors = Counter()
        dates = []
        
        for commit in commits:
            authors[commit.author.name] += 1
            dates.append(commit.committed_datetime)
        
        dates.sort()
        date_range = {
            "first_commit": dates[0].isoformat(),
            "last_commit": dates[-1].isoformat()
        }
        
        return {
            "total_commits": total_commits,
            "authors": dict(authors),
            "date_range": date_range
        }
    
    def analyze_commit_frequency(self):
        """Analyze commit frequency patterns."""
        commits = list(self.repo.iter_commits())
        if not commits:
            return {}
        
        hourly_counts = defaultdict(int)
        daily_counts = defaultdict(int)
        monthly_counts = defaultdict(int)
        weekday_counts = defaultdict(int)
        
        for commit in commits:
            dt = commit.committed_datetime
            hourly_counts[dt.hour] += 1
            daily_counts[dt.date().isoformat()] += 1
            monthly_counts[f"{dt.year}-{dt.month:02d}"] += 1
            weekday_counts[calendar.day_name[dt.weekday()]] += 1
        
        return {
            "hourly_distribution": dict(hourly_counts),
            "daily_commits": dict(daily_counts),
            "monthly_commits": dict(monthly_counts),
            "weekday_distribution": dict(weekday_counts)
        }


@click.command()
@click.option('--repo', '-r', default='.', help='Path to git repository (default: current directory)')
@click.option('--output', '-o', type=click.Choice(['json', 'text', 'html']), default='text', help='Output format')
@click.option('--frequency', '-f', is_flag=True, help='Include commit frequency analysis')
@click.option('--visualize', '-v', is_flag=True, help='Generate visualization charts')
@click.option('--report', default='report.html', help='HTML report filename (when output=html)')
@click.option('--export-csv', is_flag=True, help='Export data to CSV files')
def main(repo, output, frequency, visualize, report, export_csv):
    """Analyze Git commit history and generate statistics."""
    try:
        analyzer = GitCommitAnalyzer(repo)
        stats = analyzer.get_commit_stats()
        
        if frequency:
            freq_stats = analyzer.analyze_commit_frequency()
            stats['frequency_analysis'] = freq_stats
        
        if output == 'json':
            print(json.dumps(stats, indent=2))
        elif output == 'html':
            chart_files = {}
            if visualize and frequency and 'frequency_analysis' in stats:
                try:
                    visualizer = CommitVisualizer()
                    plots = visualizer.generate_all_plots(stats['frequency_analysis'])
                    
                    # Map plot files to chart types
                    for plot_path in plots:
                        if 'hourly' in plot_path:
                            chart_files['hourly'] = plot_path
                        elif 'weekday' in plot_path:
                            chart_files['weekday'] = plot_path
                        elif 'timeline' in plot_path:
                            chart_files['timeline'] = plot_path
                except Exception as e:
                    click.echo(f"Warning: Could not generate charts: {e}", err=True)
            
            # Generate HTML report
            report_gen = HTMLReportGenerator()
            report_path = report_gen.generate_report(stats, repo, report, chart_files)
            print(f"HTML report generated: {os.path.abspath(report_path)}")
        else:
            print("=== Git Commit Analysis ===")
            print(f"Repository: {os.path.abspath(repo)}")
            print(f"Total commits: {stats['total_commits']}")
            
            if stats['total_commits'] > 0:
                print(f"\nDate range:")
                print(f"  First commit: {stats['date_range']['first_commit']}")
                print(f"  Last commit: {stats['date_range']['last_commit']}")
                
                print(f"\nAuthors:")
                for author, count in stats['authors'].items():
                    print(f"  {author}: {count} commits")
                
                if frequency and 'frequency_analysis' in stats:
                    freq_data = stats['frequency_analysis']
                    
                    print(f"\n=== Frequency Analysis ===")
                    
                    print(f"\nMost active hours (24h format):")
                    hourly = sorted(freq_data['hourly_distribution'].items(), 
                                  key=lambda x: x[1], reverse=True)[:5]
                    for hour, count in hourly:
                        print(f"  {hour:02d}:00 - {count} commits")
                    
                    print(f"\nMost active weekdays:")
                    weekday = sorted(freq_data['weekday_distribution'].items(), 
                                   key=lambda x: x[1], reverse=True)
                    for day, count in weekday:
                        print(f"  {day}: {count} commits")
        
        if visualize and frequency and 'frequency_analysis' in stats:
            try:
                visualizer = CommitVisualizer()
                plots = visualizer.generate_all_plots(stats['frequency_analysis'])
                print(f"\n=== Visualizations Generated ===")
                for plot in plots:
                    print(f"  Created: {plot}")
            except ImportError:
                click.echo("Warning: matplotlib not available. Install it to generate charts.", err=True)
            except Exception as e:
                click.echo(f"Warning: Could not generate visualizations: {e}", err=True)
        
        if export_csv:
            try:
                exporter = CSVExporter()
                csv_files = []
                
                # Export commit details
                commit_file, commit_count = exporter.export_commit_details(analyzer.repo)
                csv_files.append(f"{commit_file} ({commit_count} commits)")
                
                # Export author statistics
                author_file, author_count = exporter.export_author_stats(stats)
                csv_files.append(f"{author_file} ({author_count} authors)")
                
                # Export frequency data if available
                if 'frequency_analysis' in stats:
                    freq_file, freq_count = exporter.export_frequency_data(stats['frequency_analysis'])
                    csv_files.append(f"{freq_file} ({freq_count} records)")
                    
                    timeline_file, timeline_count = exporter.export_daily_timeline(stats['frequency_analysis'])
                    csv_files.append(f"{timeline_file} ({timeline_count} days)")
                
                print(f"\n=== CSV Files Exported ===")
                for csv_info in csv_files:
                    print(f"  {csv_info}")
                    
            except Exception as e:
                click.echo(f"Warning: Could not export CSV files: {e}", err=True)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()