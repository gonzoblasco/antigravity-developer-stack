#!/usr/bin/env python3
"""
Architecture Diagram Generator
Generates a Mermaid JS graph of the project structure.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Set

IGNORED_DIRS = {
    '.git', '__pycache__', 'node_modules', 'venv', '.env', '.idea', '.vscode',
    'dist', 'build', 'coverage', '.next', '.nuxt', 'target', 'bin', 'obj'
}

IGNORED_FILES = {
    '.DS_Store', 'Thumbs.db', '.gitignore', '.dockerignore', 'LICENSE', 
    'README.md', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'
}

def generate_mermaid_graph(root_path: Path, max_depth: int = 2) -> str:
    """Scans directory and returns mermaid graph definition"""
    lines = ["graph TD"]
    
    # Sanitize root name for mermaid (alphanumeric only)
    root_id = "root"
    lines.append(f"    {root_id}[{root_path.name}/]")
    
    def scan(current_path: Path, parent_id: str, current_depth: int):
        if current_depth > max_depth:
            return

        try:
            # Sort for consistent output: directories first, then files
            entries = sorted(list(current_path.iterdir()), key=lambda e: (not e.is_dir(), e.name.lower()))
            
            for entry in entries:
                if entry.name in IGNORED_DIRS or entry.name in IGNORED_FILES:
                    continue
                
                # Simple ID generation: parent_id + index, but using hash to specific path might be safer against collision if we had complex linkage
                # specific unique ID based on path hash to avoid collisions?
                # for simple visualization, just unique incremental or based on name might be risky if dup names in diff folders.
                # using formatted path as ID.
                
                node_id = f"node_{abs(hash(str(entry)))}" 
                
                if entry.is_dir():
                    lines.append(f"    {parent_id} --> {node_id}[{entry.name}/]")
                    scan(entry, node_id, current_depth + 1)
                else:
                    lines.append(f"    {parent_id} --> {node_id}({entry.name})")

        except PermissionError:
            pass

    scan(root_path, root_id, 1)
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate Mermaid Architecture Diagram")
    parser.add_argument('target', help='Target directory')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--depth', type=int, default=2, help='Max recursion depth (default: 2)')
    
    args = parser.parse_args()
    target_path = Path(args.target).resolve()
    
    if not target_path.exists():
        print(f"Error: Target path {target_path} does not exist.")
        sys.exit(1)
        
    diagram = generate_mermaid_graph(target_path, args.depth)
    
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(diagram)
            print(f"Diagram written to {args.output}")
        except Exception as e:
            print(f"Error writing file: {e}")
            sys.exit(1)
    else:
        print(diagram)

if __name__ == '__main__':
    main()
