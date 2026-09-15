VENV		:= .venv
PY_VERSION	:= 3.10
MYPY_FLAGS	:= --python-version $(PY_VERSION) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
CMDS		:= run debug install lint lint-strict clean fclean
ARGS		:= $(filter-out $(CMDS),$(MAKECMDGOALS))
CMD			:= $(or $(firstword $(filter $(CMDS),$(MAKECMDGOALS))),run)

run: $(VENV)
	@uv run python src $(ARGS)

debug: $(VENV)
	@uv run python -m pdb src $(ARGS)

install $(VENV):
	@uv sync

lint: $(VENV)
	-@uv run flake8 src
	-@uv run mypy src $(MYPY_FLAGS)

lint-strict: $(VENV)
	-@uv run flake8 src
	-@uv run mypy src --strict --python-version $(PY_VERSION)

clean:
	-@find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache -o -name .ruff_cache \) -exec rm -rf {} +

fclean: clean
	@rm -rf $(VENV)

$(ARGS): $(CMD)
	@:

.PHONY: $(CMDS) $(ARGS)
