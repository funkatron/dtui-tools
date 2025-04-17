# Sandbox Directory

This directory is for experimental work, prototyping, and quick testing. It's separate from the main package code to keep experiments isolated from production code.

## Structure

```
sandbox/
├── notebooks/         # Jupyter notebooks for interactive experiments
├── scripts/          # One-off scripts and utilities
├── data/             # Data used in experiments
│   ├── raw/         # Original, unprocessed data
│   └── processed/   # Processed or transformed data
├── experiments/      # Structured experiment code
└── results/         # Outputs and results from experiments
```

## Usage Guidelines

1. **Notebooks**: Use for interactive exploration and visualization
2. **Scripts**: For one-off utilities or quick tests
3. **Experiments**: For more structured experimental code that might be moved to the main package
4. **Data**: Keep raw data in `raw/` and any processed versions in `processed/`
5. **Results**: Store experiment outputs, visualizations, and metrics

## Best Practices

- Keep experiments reproducible
- Document key findings in the experiment directory
- Clean up old experiments periodically
- Don't commit large data files to version control
- Use relative imports from the main package when needed

## Example Workflow

1. Start in `notebooks/` for initial exploration
2. Move promising code to `experiments/` for more structured testing
3. If successful, refactor and move to the main package
4. Store results and visualizations in `results/`