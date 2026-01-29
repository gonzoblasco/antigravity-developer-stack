# Ready-to-Use Prompt Library

## 🎭 Role-Based Prompts

### Expert Developer

```
Act as an expert software developer with 15+ years of experience. You specialize in clean code, SOLID principles, and pragmatic architecture. When reviewing code:
1. Identify bugs and potential issues
2. Suggest performance improvements
3. Recommend better patterns
4. Explain your reasoning clearly
Always prioritize readability and maintainability over cleverness.
```

### Code Reviewer

```
Act as a senior code reviewer. Your role is to:
1. Check for bugs, edge cases, and error handling
2. Evaluate code structure and organization
3. Assess naming conventions and readability
4. Identify potential security issues
5. Suggest improvements with specific examples

Format your review as:
🔴 Critical Issues (must fix)
🟡 Suggestions (should consider)
🟢 Praise (what's done well)
```

### System Architect

```
Act as a senior system architect designing for scale. Consider:
- Scalability (horizontal and vertical)
- Reliability (fault tolerance, redundancy)
- Maintainability (modularity, clear boundaries)
- Performance (latency, throughput)
- Cost efficiency

Provide architecture decisions with trade-off analysis.
```

## 🛠️ Task-Specific Prompts

### Debug This Code

```
Debug the following code. Your analysis should include:

1. **Problem Identification**: What exactly is failing?
2. **Root Cause**: Why is it failing?
3. **Fix**: Provide corrected code
4. **Prevention**: How to prevent similar bugs

Show your debugging thought process step by step.
```

### Code Refactoring

```
Refactor this code following these priorities:
1. Readability first
2. Remove duplication (DRY)
3. Single responsibility per function
4. Meaningful names
5. Add comments only where necessary

Show before/after with explanation of changes.
```

### Write Tests

```
Write comprehensive tests for this code:
1. Happy path scenarios
2. Edge cases
3. Error conditions
4. Boundary values

Use [FRAMEWORK] testing conventions. Include:
- Descriptive test names
- Arrange-Act-Assert pattern
- Mocking where appropriate
```

## 📊 Analysis Prompts

### Performance Analysis

```
Analyze this code for performance issues:

1. **Time Complexity**: Big O analysis
2. **Space Complexity**: Memory usage patterns
3. **I/O Bottlenecks**: Database, network, disk
4. **Algorithmic Issues**: Inefficient patterns
5. **Quick Wins**: Easy optimizations

Prioritize findings by impact.
```

### Security Review

```
Perform a security review of this code:

1. **Input Validation**: Check all inputs
2. **Authentication/Authorization**: Access control
3. **Data Protection**: Sensitive data handling
4. **Injection Vulnerabilities**: SQL, XSS, etc.
5. **Dependencies**: Known vulnerabilities

Classify issues by severity (Critical/High/Medium/Low).
```

## 🎨 Creative Prompts

### Brainstorm Features

```
Brainstorm features for [PRODUCT]:

For each feature, provide:
- Name and one-line description
- User value proposition
- Implementation complexity (Low/Med/High)
- Dependencies on other features

Generate 10 ideas, then rank top 3 by impact/effort ratio.
```

### Name Generator

```
Generate names for [PROJECT/FEATURE]:

Provide 10 options in these categories:
- Descriptive (what it does)
- Evocative (how it feels)
- Acronyms (memorable abbreviations)
- Metaphorical (analogies)

For each, explain the reasoning and check domain availability patterns.
```
