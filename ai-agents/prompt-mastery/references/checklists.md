# Prompt Improvement Guidelines

## Best Practices

1. **Be Specific**: Vague prompts produce inconsistent results
2. **Show, Don't Tell**: Examples are more effective than descriptions
3. **Test Extensively**: Evaluate on diverse, representative inputs
4. **Iterate Rapidly**: Small changes can have large impacts
5. **Monitor Performance**: Track metrics in production
6. **Version Control**: Treat prompts as code with proper versioning
7. **Document Intent**: Explain why prompts are structured as they are

## Anti-Patterns

### ❌ Vague Instructions

Don't: "Make this better"
Do: "Refactor for readability: extract functions, remove duplication, use meaningful names"

### ❌ Kitchen Sink Prompt

Don't: Include every possible instruction "just in case"
Do: Curate context to only what's relevant for the specific task

### ❌ No Negative Instructions

Don't: Only say what to do
Do: Include explicit constraints: "Do NOT change functionality, only improve structure"

### ❌ Over-engineering

Don't: Start with complex multi-shot prompts
Do: Progressive disclosure - start simple, add complexity when needed

## ⚠️ Sharp Edges

| Issue                                           | Severity | Solution                                |
| :---------------------------------------------- | :------- | :-------------------------------------- |
| Using imprecise language in prompts             | High     | Be explicit with terminology            |
| Expecting specific format without specifying it | High     | Specify format explicitly with examples |
| Only saying what to do, not what to avoid       | Medium   | Include explicit don'ts                 |
| Changing prompts without measuring impact       | Medium   | A/B test and track metrics              |
| Including irrelevant context 'just in case'     | Medium   | Curate context carefully                |
| Biased or unrepresentative examples             | Medium   | Use diverse examples                    |
| Using default temperature for all tasks         | Medium   | Task-appropriate temperature            |
| Not considering prompt injection in user input  | High     | Sanitize and validate inputs            |

## Prompt Improvement Checklist

When crafting prompts, ensure:

- [ ] **Clear objective**: What exactly do you want?
- [ ] **Context provided**: Background information included?
- [ ] **Format specified**: How should output be structured?
- [ ] **Examples given**: Are there reference examples?
- [ ] **Constraints defined**: Any limitations or requirements?
- [ ] **Success criteria**: How do you measure good output?

## Optimization Workflow

```
1. Start Simple → Test
2. Add Constraints → Test
3. Add Examples → Test
4. Add Reasoning → Test
5. Refine → Test
```

**Key metrics:**

- Accuracy (correctness of output)
- Consistency (reproducibility)
- Token usage (cost)
- Latency (response time)
