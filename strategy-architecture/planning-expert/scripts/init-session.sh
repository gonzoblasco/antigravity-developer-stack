#!/bin/bash
# Initialize planning files for a new session
# Usage: ./init-session.sh [project-name]

set -e

PROJECT_NAME="${1:-project}"
DATE=$(date +%Y-%m-%d)

echo "Initializing planning files for: $PROJECT_NAME"

# Create task_plan.md if it doesn't exist
if [ ! -f "task_plan.md" ]; then
    cat > task_plan.md << 'EOF'
# Task Plan: [Brief Description]

**Goal**: [One clear sentence describing the desired end state]

**Current Phase**: Phase 1

---

## Phases

### Phase 1: Requirements & Discovery
- [ ] Understand user intent
- [ ] Identify constraints
- [ ] Document in findings.md
- **Status**: in_progress

### Phase 2: Planning & Architecture
- [ ] Define technical approach
- [ ] Create project structure
- **Status**: pending

### Phase 3: Implementation
- [ ] Execute plan with TDD-like granularity
- [ ] Write to files before executing
- **Status**: pending

### Phase 4: Verification & Delivery
- [ ] Verify all requirements met
- [ ] Deliver outcome to user
- **Status**: pending

---

## Decisions Made
| Decision | Rationale |
|----------|-----------|
|          |           |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
|       | 1       |            |

> [!TIP]
> **Attention Manipulation**: Re-read this file before every major decision to keep the goal in your attention window.
EOF
    echo "Created task_plan.md"
else
    echo "task_plan.md already exists, skipping"
fi

# Create findings.md if it doesn't exist
if [ ! -f "findings.md" ]; then
    cat > findings.md << 'EOF'
# Findings & Discoveries

**Topic**: [Brief description]

## Key Findings
- [Point 1]
- [Point 2]

## Technical Decisions
| Decision | Rationale |
| :--- | :--- |
| | |

## Resources & Links
- [Link/Path]
EOF
    echo "Created findings.md"
else
    echo "findings.md already exists, skipping"
fi

# Create progress.md if it doesn't exist
if [ ! -f "progress.md" ]; then
    cat > progress.md << EOF
# Progress Log

**Session Date**: $DATE

## Current Status
- **Phase**: 1 - Requirements & Discovery
- **Focus**: Initial setup

## Actions Taken
- [ ] Initialization of planning files

## Test Results
| Test | Result | Notes |
| :--- | :--- | :--- |
| | | |
EOF
    echo "Created progress.md"
else
    echo "progress.md already exists, skipping"
fi

echo ""
echo "Planning files initialized!"
echo "Files: task_plan.md, findings.md, progress.md"
