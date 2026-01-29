#!/usr/bin/env python3
"""
Dependency Analyzer
Analyzes project dependencies from standard files (package.json, requirements.txt).
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any

def analyze_package_json(path: Path) -> Dict[str, Any]:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            
        deps = data.get('dependencies', {})
        dev_deps = data.get('devDependencies', {})
        
        return {
            "type": "npm",
            "file": str(path.name),
            "dependencies_count": len(deps),
            "dev_dependencies_count": len(dev_deps),
            "dependencies_list": list(deps.keys()),
            "dev_dependencies_list": list(dev_deps.keys())
        }
    except Exception as e:
        return {"error": f"Failed to parse package.json: {str(e)}"}

def analyze_requirements_txt(path: Path) -> Dict[str, Any]:
    try:
        deps = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    deps.append(line)
        
        return {
            "type": "pip",
            "file": str(path.name),
            "dependencies_count": len(deps),
            "dependencies_list": deps
        }
    except Exception as e:
        return {"error": f"Failed to parse requirements.txt: {str(e)}"}

def analyze_project(root_path: Path) -> Dict[str, Any]:
    results = {
        "project": str(root_path),
        "analyzed_files": [],
        "summary": {
            "npm_files": 0,
            "pip_files": 0,
            "total_dependencies": 0
        }
    }
    
    # Check for specific files in root (non-recursive for simplicity/speed in this version)
    # Could be expanded to recursive search
    
    pkg_json = root_path / "package.json"
    if pkg_json.exists():
        analysis = analyze_package_json(pkg_json)
        results["analyzed_files"].append(analysis)
        if "dependencies_count" in analysis:
            results["summary"]["npm_files"] += 1
            results["summary"]["total_dependencies"] += analysis["dependencies_count"] + analysis.get("dev_dependencies_count", 0)

    req_txt = root_path / "requirements.txt"
    if req_txt.exists():
        analysis = analyze_requirements_txt(req_txt)
        results["analyzed_files"].append(analysis)
        if "dependencies_count" in analysis:
            results["summary"]["pip_files"] += 1
            results["summary"]["total_dependencies"] += analysis["dependencies_count"]

    return results

def main():
    parser = argparse.ArgumentParser(description="Dependency Analyzer")
    parser.add_argument('target', help='Target directory')
    parser.add_argument('--json', action='store_true', help='Output JSON (implied, this tool always outputs JSON-like structure currently)')
    parser.add_argument('--output', '-o', help='Output file path')
    
    args = parser.parse_args()
    target_path = Path(args.target).resolve()
    
    if not target_path.exists():
        print(f"Error: Target path {target_path} does not exist.")
        sys.exit(1)
        
    report = analyze_project(target_path)
    report_json = json.dumps(report, indent=2)
    
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(report_json)
            print(f"Report written to {args.output}")
        except Exception as e:
            print(f"Error writing file: {e}")
            sys.exit(1)
    else:
        print(report_json)

if __name__ == '__main__':
    main()
