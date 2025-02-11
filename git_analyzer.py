#!/usr/bin/env python3
"""
Git Commit Analyzer
A tool for analyzing Git repository commit history and generating statistics.
"""

import os
import sys
import json
from datetime import datetime
from collections import defaultdict, Counter

try:
    import git
    import click
except ImportError:
    print("Required packages not installed. Please run: pip install -r requirements.txt")
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


@click.command()
@click.option('--repo', '-r', default='.', help='Path to git repository (default: current directory)')
@click.option('--output', '-o', type=click.Choice(['json', 'text']), default='text', help='Output format')
def main(repo, output):
    """Analyze Git commit history and generate statistics."""
    try:
        analyzer = GitCommitAnalyzer(repo)
        stats = analyzer.get_commit_stats()
        
        if output == 'json':
            print(json.dumps(stats, indent=2))
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
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()