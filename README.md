## Monkey Claude
Let claude built its own tools to solve the problems you throw at it.
Useful to bridge the gap between the strengths of LLMs and their lack of ability to run complex determnistic algorithms.
### Examples:
```bash
uv run main.py --debug "When was the best time to buy palantir stock in the last year? What was the price at that time? What is the current price?"
```
```
Based on the data, here's what I found about Palantir (PLTR) stock over the last year:

**Best time to buy in the last year:**
- **Date:** August 5, 2024
- **Price:** $24.09
- This was the lowest price point for PLTR stock in the past year

**Current price:**
- **$130.74** (as of the most recent trading day in the data)

**Key insights:**
- Palantir stock has experienced tremendous growth, increasing by approximately **443%** from its lowest point to the current price
- The stock hit its low of $24.09 in early August 2024, during what appears to have been a broader market pullback
- Since then, PLTR has seen significant appreciation, particularly accelerating from November 2024 onwards
- The stock reached peaks above $140 in mid-June 2025 before pulling back slightly to the current level

This represents one of the most impressive stock performances over the past year, with those who bought at the August 2024 low seeing more than a 5x return on their investment.
```

### TODO
1. Integrate a feedback loop for broken tools and exceptions
2. Integrate with openwebui
3. Integrate with MCPs?
