VENV		:= .venv
MYPY_FLAGS	:= --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

run: $(VENV)
	@$(ARGS) uv run python src || true

debug: $(VENV)
	@$(ARGS) uv run python -m pdb src || true

install $(VENV):
	@uv sync

lint: $(VENV)
	-@uv run flake8 src
	-@uv run mypy src $(MYPY_FLAGS)

lint-strict: $(VENV)
	-@uv run flake8 src
	-@uv run mypy src --strict

clean:
	-@find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) -exec rm -rf {} +

fclean: clean
	@rm -rf $(VENV)

.PHONY: run debug install lint lint-strict clean fclean
