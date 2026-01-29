#!/usr/bin/env python3
"""
Project Architect
Automated architectural linter that checks for project health hygiene.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

def check_hygiene(root_path: Path) -> List[Dict[str, str]]:
    findings = []
    
    # Check 1: README
    if not (root_path / "README.md").exists():
        findings.append({
            "severity": "HIGH",
            "check": "Missing Documentation",
            "message": "No README.md found. Every project requires a README."
        })
        
    # Check 2: Gitignore
    if not (root_path / ".gitignore").exists():
        findings.append({
            "severity": "HIGH",
            "check": "Source Control Hygiene",
            "message": "No .gitignore found. Risk of committing temporary files."
        })
        
    # Check 3: Docker/Containerization (Soft check)
    if not (root_path / "Dockerfile").exists() and not (root_path / "docker-compose.yml").exists():
        findings.append({
            "severity": "MEDIUM",
            "check": "Containerization",
            "message": "No Dockerfile or docker-compose.yml found. Consider containerizing for consistent environments."
        })
        
    # Check 4: Structure (src folder) - highly opinionated, maybe too much?
    # Keeping it simple: separate source code if not a tiny script repo
    # If root has many files, suggest src/
    
    file_count = sum(1 for _ in root_path.iterdir() if _.is_file())
    if file_count > 10 and not (root_path / "src").exists():
         findings.append({
            "severity": "LOW",
            "check": "Project Structure",
            "message": "Root directory seems cluttered. Consider moving source code to a 'src/' directory."
        })

    # Check 5: License
    if not (root_path / "LICENSE").exists():
         findings.append({
            "severity": "MEDIUM",
            "check": "Legal",
            "message": "No LICENSE file found."
        })

    return findings

def main():
    parser = argparse.ArgumentParser(description="Project Architect Linter")
    parser.add_argument('target', help='Target directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    target_path = Path(args.target).resolve()
    
    if not target_path.exists():
        print(f"Error: Target path {target_path} does not exist.")
        sys.exit(1)
        
    print(f"🏗️  Architectural Review for: {target_path.name}")
    print("=" * 50)
    
    findings = check_hygiene(target_path)
    
    if not findings:
        print("✅  Clean health check! No obvious issues found.")
    else:
        for f in findings:
            icon = "🔴" if f['severity'] == "HIGH" else "jq" if f['severity'] == "MEDIUM" else "🔵"
            if f['severity'] == "MEDIUM": icon = "🟠" 
            
            print(f"{icon}  [{f['severity']}] {f['check']}")
            print(f"    {f['message']}")
            print()
            
    print("=" * 50)
    print(f"Total Findings: {len(findings)}")

if __name__ == '__main__':
    main()
