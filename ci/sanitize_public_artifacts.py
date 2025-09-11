#!/usr/bin/env python3
"""
Public Artifacts Sanitization Script

This script sanitizes artifacts before publishing to public repositories
to ensure no sensitive information is exposed.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path


class ArtifactSanitizer:
    """Sanitizes artifacts for public consumption."""
    
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.sensitive_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'private_key\s*=\s*["\'][^"\']+["\']',
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',  # Email addresses
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit card numbers
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        ]
        
        self.sensitive_files = [
            '.env',
            '.env.local',
            '.env.production',
            'secrets.json',
            'credentials.json',
            'config.json',
            'private.key',
            'id_rsa',
            'id_dsa',
            '*.pem',
            '*.p12',
            '*.pfx',
            'cloudbuild.yaml',
            '.gitlab-ci.yml',
            'sanitization_report.json'
        ]
    
    def sanitize_file(self, file_path):
        """Sanitize a single file."""
        if not os.path.exists(file_path):
            return True
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            issues_found = []
            
            # Check for sensitive patterns
            for pattern in self.sensitive_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    issues_found.extend(matches)
                    # Replace with placeholder
                    content = re.sub(pattern, '[REDACTED]', content, flags=re.IGNORECASE)
            
            if issues_found:
                print(f"⚠️  Found sensitive data in {file_path}:")
                for issue in set(issues_found):
                    print(f"    - {issue}")
                
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Sanitized {file_path}")
                else:
                    print(f"🔍 [DRY RUN] Would sanitize {file_path}")
            else:
                print(f"✅ {file_path} is clean")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return False
    
    def remove_sensitive_files(self, directory):
        """Remove sensitive files from directory."""
        removed_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                
                # Check if file matches sensitive patterns
                should_remove = False
                for pattern in self.sensitive_files:
                    if self._matches_pattern(relative_path, pattern):
                        should_remove = True
                        break
                
                if should_remove:
                    if not self.dry_run:
                        try:
                            os.remove(file_path)
                            removed_files.append(relative_path)
                            print(f"🗑️  Removed sensitive file: {relative_path}")
                        except Exception as e:
                            print(f"❌ Error removing {relative_path}: {e}")
                    else:
                        print(f"🔍 [DRY RUN] Would remove: {relative_path}")
                        removed_files.append(relative_path)
        
        return removed_files
    
    def _matches_pattern(self, file_path, pattern):
        """Check if file path matches pattern."""
        import fnmatch
        return fnmatch.fnmatch(file_path, pattern)
    
    def sanitize_git_history(self):
        """Sanitize git history for sensitive information."""
        if self.dry_run:
            print("🔍 [DRY RUN] Would sanitize git history")
            return True
        
        try:
            # This is a placeholder - in real implementation, you'd use git filter-branch
            # or BFG Repo-Cleaner to remove sensitive data from git history
            print("⚠️  Git history sanitization requires manual intervention")
            print("   Consider using BFG Repo-Cleaner or git filter-branch")
            return True
        except Exception as e:
            print(f"❌ Error sanitizing git history: {e}")
            return False
    
    def create_sanitization_report(self, directory):
        """Create a report of sanitization actions."""
        report = {
            "timestamp": str(Path().cwd()),
            "dry_run": self.dry_run,
            "directory": directory,
            "actions_taken": []
        }
        
        # Scan for sensitive files
        sensitive_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                
                for pattern in self.sensitive_files:
                    if self._matches_pattern(relative_path, pattern):
                        sensitive_files.append(relative_path)
                        break
        
        report["sensitive_files_found"] = sensitive_files
        
        # Save report
        report_path = os.path.join(directory, "sanitization_report.json")
        if not self.dry_run:
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📄 Sanitization report saved to {report_path}")
        
        return report


def main():
    """Main sanitization function."""
    parser = argparse.ArgumentParser(description="Sanitize artifacts for public publishing")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be done without making changes")
    parser.add_argument("--remove-only", action="store_true",
                       help="Only remove sensitive files, don't sanitize content")
    parser.add_argument("--directory", default=".", 
                       help="Directory to sanitize (default: current directory)")
    
    args = parser.parse_args()
    
    print("🧹 Starting Artifact Sanitization...")
    print("=" * 50)
    
    if args.dry_run:
        print("🔍 Running in DRY RUN mode - no changes will be made")
    
    sanitizer = ArtifactSanitizer(dry_run=args.dry_run)
    
    if args.remove_only:
        # Only remove sensitive files
        print("\n🗑️  Removing sensitive files only...")
        removed_files = sanitizer.remove_sensitive_files(args.directory)
        print(f"✅ Removed {len(removed_files)} sensitive files")
    else:
        # Full sanitization process
        # Sanitize files
        print("\n📁 Sanitizing files...")
        files_to_check = [
            "README.md",
            "requirements.txt",
            "Dockerfile",
            "docker-compose.yml",
            ".gitlab-ci.yml"
        ]
        
        for file_path in files_to_check:
            sanitizer.sanitize_file(file_path)
        
        # Remove sensitive files
        print("\n🗑️  Removing sensitive files...")
        removed_files = sanitizer.remove_sensitive_files(args.directory)
        
        # Sanitize git history
        print("\n📚 Checking git history...")
        sanitizer.sanitize_git_history()
        
        # Create report
        print("\n📄 Creating sanitization report...")
        report = sanitizer.create_sanitization_report(args.directory)
    
    print("\n" + "=" * 50)
    print("✅ Sanitization completed!")
    
    if args.dry_run:
        print("🔍 This was a dry run - no actual changes were made")
        print("   Run without --dry-run to apply changes")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
