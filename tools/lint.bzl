"Define linter aspects"

load("@aspect_rules_lint//lint:ruff.bzl", "ruff_aspect")


ruff = ruff_aspect(
    binary = "@@//tools:ruff",
    configs = [
        "@@//:.ruff.toml",
    ],
)

ruff_test = make_lint_test(aspect = ruff)
