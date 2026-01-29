#!/usr/bin/env python3
import re
import sys
import argparse
from pathlib import Path

"""
Postgres Schema Auditor
=======================
Analyzes SQL schema definitions for common anti-patterns according to Supabase best practices.

Checks:
1. Primary Keys: Checks for `serial` (should be `identity`) and `uuid` (should be `v7` or `v4` with caution).
2. Data Types: Warns about `varchar(n)` (use `text`), `char(n)`, `timestamp` (use `timestamptz`).
3. Foreign Keys: Checks if FK columns have a corresponding index.
4. Naming: Checks for mixed-case identifiers.

Usage:
  python audit_schema.py schema.sql
  cat schema.sql | python audit_schema.py -
"""

COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "RESET": "\033[0m",
}

def print_color(color, text):
    if sys.stdout.isatty():
        print(f"{COLORS.get(color, '')}{text}{COLORS['RESET']}")
    else:
        print(text)

class SchemaAuditor:
    def __init__(self, content):
        self.content = content
        self.lines = content.splitlines()
        self.issues = []
        self.tables = []
        self.indexes = []
        self.foreign_keys = []
        
        self._parse()

    def _parse(self):
        # Naive SQL parsing - sufficient for standard DDL
        # Find tables
        table_pattern = re.compile(r'create\s+table\s+(?:if\s+not\s+exists\s+)?([a-zA-Z0-9_"\.]+)', re.IGNORECASE)
        for i, line in enumerate(self.lines):
            match = table_pattern.search(line)
            if match:
                self.tables.append({"name": match.group(1), "line": i + 1})

        # Find indexes
        index_pattern = re.compile(r'create\s+(?:unique\s+)?index\s+(?:if\s+not\s+exists\s+)?([a-zA-Z0-9_"]+)\s+on\s+([a-zA-Z0-9_"\.]+)\s*(?:using\s+\w+\s*)?\(([^)]+)\)', re.IGNORECASE)
        # Handle multi-line index definitions simply by joining (limitation: simple parsing)
        full_content_normalized = re.sub(r'\s+', ' ', self.content)
        for match in index_pattern.finditer(full_content_normalized):
            idx_name = match.group(1)
            table_name = match.group(2)
            columns = [c.strip().split()[0] for c in match.group(3).split(',')] # Extract col name, ignore asc/desc
            self.indexes.append({"name": idx_name, "table": table_name, "columns": columns})

        # Find inline Foreign Keys & Column Defs
        # This is complex with regex. We'll do line-by-line checks for standard patterns.
        fk_pattern = re.compile(r'\b([a-zA-Z0-9_"]+)\s+.*\breferences\s+([a-zA-Z0-9_"\.]+)', re.IGNORECASE)
        
        table_context = None
        for i, line in enumerate(self.lines):
            clean_line = line.strip()
            if clean_line.lower().startswith("create table"):
                match = table_pattern.search(line)
                if match:
                    table_context = match.group(1)
            elif clean_line.startswith(");"):
                table_context = None
            
            # Check for inline FKs
            if table_context:
                fk_match = fk_pattern.search(clean_line)
                if fk_match and not clean_line.startswith("--"):
                    col_name = fk_match.group(1)
                    ref_table = fk_match.group(2)
                    self.foreign_keys.append({
                        "table": table_context,
                        "column": col_name,
                        "ref_table": ref_table,
                        "line": i + 1
                    })

    def check_best_practices(self):
        self._check_result("Primary Keys", self._check_primary_keys())
        self._check_result("Data Types", self._check_data_types())
        self._check_result("Indexes on Foreign Keys", self._check_fk_indexes())
        self._check_result("Naming Conventions", self._check_naming())

    def _check_result(self, category, issues):
        print(f"\n--- {category} ---")
        if not issues:
            print_color("GREEN", "✓ No issues found")
        else:
            for issue in issues:
                print_color("YELLOW", f"⚠ {issue}")

    def _check_primary_keys(self):
        issues = []
        serial_pattern = re.compile(r'\bserial\b', re.IGNORECASE)
        uuid_pattern = re.compile(r'\buuid\b', re.IGNORECASE)
        default_gen_uuid = re.compile(r'default\s+gen_random_uuid\(\)', re.IGNORECASE)

        for i, line in enumerate(self.lines):
            if serial_pattern.search(line):
                issues.append(f"Line {i+1}: Usage of 'serial' detected. Prefer 'generated always as identity' (SQL Standard).")
            
            if uuid_pattern.search(line) and "primary key" in line.lower():
                 if not default_gen_uuid.search(line) and "uuid_generate_v7" not in line.lower():
                     issues.append(f"Line {i+1}: UUID Primary Key detected without v7 function. Ensure you are using v7 or aware of fragmentation with v4.")

        return issues

    def _check_data_types(self):
        issues = []
        varchar_n = re.compile(r'varchar\s*\(', re.IGNORECASE)
        char_n = re.compile(r'\bchar\s*\(', re.IGNORECASE)
        timestamp = re.compile(r'\btimestamp\b', re.IGNORECASE)
        timestamptz = re.compile(r'\btimestamptz\b', re.IGNORECASE)

        for i, line in enumerate(self.lines):
             if varchar_n.search(line):
                 issues.append(f"Line {i+1}: 'varchar(n)' detected. Prefer 'text' in Postgres (no performance diff, no arbitrary limits).")
             if char_n.search(line):
                 issues.append(f"Line {i+1}: 'char(n)' detected. This pads with spaces. Prefer 'text'.")
             if timestamp.search(line) and not timestamptz.search(line):
                  # simple check, might identify 'timestamp with time zone' which is fine
                  if "with time zone" not in line.lower():
                      issues.append(f"Line {i+1}: 'timestamp' (no tz) detected. Almost always prefer 'timestamptz' to store UTC point-in-time.")
        return issues

    def _check_fk_indexes(self):
        issues = []
        # Naive check: does an index exist where 'table' matches and 'columns' contains the FK column?
        # Note: This is hard to do perfectly with regex on raw SQL text without a full parser state,
        # but we can do a "best effort" check.
        
        # We need to map table names from FK definitions to table names in Index definitions.
        # This naive parser might fail on schemas or quoted names differences.
        
        for fk in self.foreign_keys:
            is_indexed = False
            for idx in self.indexes:
                # Normalize names (remove quotes)
                idx_table = idx['table'].replace('"', '')
                fk_table = fk['table'].replace('"', '')
                
                if idx_table == fk_table:
                    # Check if FK column is the FIRST column in the index
                    if idx['columns'] and idx['columns'][0].replace('"', '') == fk['column'].replace('"', ''):
                        is_indexed = True
                        break
            
            if not is_indexed:
                issues.append(f"Table '{fk['table']}', Column '{fk['column']}': Foreign Key appears unindexed. This will cause slow JOINs and cascading deletes.")
        
        return issues

    def _check_naming(self):
        issues = []
        mixed_case = re.compile(r'"[a-z]+[A-Z]+[^"]*"')
        for i, line in enumerate(self.lines):
            if mixed_case.search(line) and "create" in line.lower():
                issues.append(f"Line {i+1}: Mixed-case quoted identifier detected. Prefer lowercase snake_case to avoid double-quoting hell.")
        return issues

def main():
    parser = argparse.ArgumentParser(description="Audit SQL for Supabase/Postgres Best Practices")
    parser.add_argument("file", nargs="?", help="SQL file path or - for stdin")
    args = parser.parse_args()

    content = ""
    if args.file == "-" or not args.file:
        if sys.stdin.isatty():
             parser.print_help()
             sys.exit(1)
        content = sys.stdin.read()
    else:
        try:
            with open(args.file, 'r') as f:
                content = f.read()
        except Exception as e:
            print_color("RED", f"Error reading file: {e}")
            sys.exit(1)

    print_color("BLUE", "Starting Postgres Schema Audit...")
    auditor = SchemaAuditor(content)
    auditor.check_best_practices()

if __name__ == "__main__":
    main()
