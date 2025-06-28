# Monkey Claude

**Let Claude build its own tools to solve complex problems dynamically.**

Monkey Claude bridges the gap between LLMs' reasoning capabilities and their inability to execute complex deterministic algorithms. Instead of being limited to pre-built tools, Claude can create custom solutions on-the-fly for your specific queries.

## Key Features

- **Dynamic Tool Creation**: Claude generates custom tools based on your specific problem
- **Complex Data Analysis**: Handles sophisticated calculations and data processing tasks
- **Real-time Problem Solving**: Adapts to unique queries that don't fit standard tool templates

## Quick Start

```bash
# Install dependencies
uv install

# Run with a complex query
uv run main.py --debug "Your complex question here"
```

## Example Usage

**Query**: "When was the best time to buy Palantir stock in the last year? What was the price at that time? What is the current price?"

```bash
uv run main.py --debug "When was the best time to buy palantir stock in the last year? What was the price at that time? What is the current price?"
```

**Output**:
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

## Use Cases

- **Financial Analysis**: Stock performance, market trends, portfolio optimization
- **Data Processing**: Complex calculations on large datasets
- **Research Tasks**: Multi-step analysis requiring custom algorithms
- **Problem Solving**: Unique queries that need tailored solutions

## Installation

```bash
# Clone the repository
git clone [your-repo-url]
cd monkey-claude

# Install with uv
uv install

# Or with pip
pip install -r requirements.txt
```

## Configuration

```bash
# Set your API keys
export ANTHROPIC_API_KEY="your_key_here"

# Optional: Configure additional settings
export DEBUG=true
```

## Command Line Options

```bash
uv run main.py [OPTIONS] "Your query"

Options:
  --debug     Enable debug mode for detailed logging
  --help      Show this message and exit
```

## How It Works

1. **Query Analysis**: Claude analyzes your problem to understand what tools are needed
2. **Tool Generation**: Creates custom functions and algorithms specific to your query
3. **Execution**: Runs the generated tools with appropriate data sources
4. **Results**: Provides comprehensive analysis and insights

## Roadmap

- [ ] **Feedback Loop Integration**: Automatic tool refinement based on execution results and exceptions
- [ ] **OpenWebUI Integration**: Web interface for easier interaction and visualization
- [ ] **MCP Support**: Integration with Model Context Protocol for enhanced capabilities
- [ ] **Tool Persistence**: Save and reuse successful tools for similar queries
- [ ] **Performance Optimization**: Caching and optimization for frequently used patterns

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.
