#!/usr/bin/env python3
"""Build the repository-wide Hi Tax Index from scenario packages.

The script intentionally uses only the Python standard library. It reads the
small scalar subset of YAML needed for the index and takes attempt metrics from
each package's RESULTS.csv. Vendor-native fields remain in the scenario package;
the index only displays explicitly defined aggregate footprint fields.
"""

from __future__ import annotations

import argparse
import ast
import csv
import difflib
import html
import os
import re
import statistics
import sys
from pathlib import Path
from urllib.parse import quote


MISSING_VALUES = {
    "",
    "not_applicable",
    "not_exposed",
    "not_measured",
    "not_provided",
    "self_reported",
    "unknown",
}

ROUTE_LABELS = {
    "first-party-subscription": "官方订阅",
    "official-api": "官方 API",
    "third-party-gateway": "第三方中转",
    "self-hosted": "自部署",
}

VISUAL_LABELS = {
    "public": "公开视觉",
    "private_evidence": "私有视觉",
    "not_provided": "无视觉证据",
}

COMPARISON_LABELS = {
    "mode-confounded": "对比受 mode 混杂",
}

TICK = chr(96)


def parse_scalar(raw_value: str):
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value[1:-1]
    if value == "true":
        return True
    if value == "false":
        return False
    if value in {"null", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", value):
        return float(value)
    return value


def read_yaml_scalars(path: Path) -> dict[str, object]:
    """Read scalar YAML paths without adding a PyYAML dependency.

    Scenario manifests use mappings for every field consumed by the index.
    Lists and block scalars are deliberately ignored.
    """

    values: dict[str, object] = {}
    stack: list[tuple[int, str]] = []

    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        stripped = raw_line.lstrip()
        if not stripped or stripped.startswith("#") or stripped.startswith("- "):
            continue

        indent = len(raw_line) - len(stripped)
        if "\t" in raw_line[:indent]:
            raise ValueError(f"{path}:{line_number}: YAML indentation contains a tab")
        if ":" not in stripped:
            continue

        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]+", key):
            continue

        while stack and stack[-1][0] >= indent:
            stack.pop()

        path_parts = [item[1] for item in stack] + [key]
        scalar_path = ".".join(path_parts)
        raw_value = raw_value.strip()

        if not raw_value:
            stack.append((indent, key))
            continue

        values[scalar_path] = parse_scalar(raw_value)

    return values


def is_missing(value: object) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    return text in MISSING_VALUES or (text.startswith("<") and text.endswith(">"))


def value_at(values: dict[str, object], key: str, default: object = "—"):
    value = values.get(key)
    return default if is_missing(value) else value


def status_at(values: dict[str, object], key: str, default: object):
    value = values.get(key)
    if value is None or str(value).strip() == "":
        return default
    return value


def read_valid_attempts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "status" not in reader.fieldnames:
            raise ValueError(f"{path}: missing status column")
        rows = [row for row in reader if row.get("status") == "valid"]
    if not rows:
        raise ValueError(f"{path}: no valid attempts")
    return rows


def number_from(row: dict[str, str], *field_names: str) -> float | None:
    for field_name in field_names:
        raw_value = row.get(field_name, "").strip()
        if raw_value in MISSING_VALUES:
            continue
        try:
            return float(raw_value)
        except ValueError:
            continue
    return None


def collect_numbers(
    rows: list[dict[str, str]], *field_names: str
) -> list[float]:
    numbers: list[float] = []
    for row in rows:
        number = number_from(row, *field_names)
        if number is not None:
            numbers.append(number)
    return numbers


def format_number(value: float, decimals: int = 3) -> str:
    if float(value).is_integer():
        return f"{int(value):,}"
    rendered = f"{value:,.{decimals}f}"
    return rendered.rstrip("0").rstrip(".")


def metric_summary(values: list[float], decimals: int = 3) -> str:
    if not values:
        return "—"
    median = statistics.median(values)
    minimum = min(values)
    maximum = max(values)
    median_text = format_number(median, decimals)
    if minimum == maximum:
        return median_text
    return (
        f"{median_text} "
        f"({format_number(minimum, decimals)}–{format_number(maximum, decimals)})"
    )


def markdown_cell(value: object) -> str:
    text = html.escape(str(value), quote=False)
    return text.replace("|", "&#124;").replace("\n", " ").strip()


def markdown_path(path: Path) -> str:
    return quote(path.as_posix(), safe="/._-")


def scenario_summary(repo_root: Path, manifest_path: Path) -> dict[str, object]:
    package_dir = manifest_path.parent
    manifest = read_yaml_scalars(manifest_path)
    results_path = package_dir / "RESULTS.csv"
    if not results_path.is_file():
        raise ValueError(f"{package_dir}: missing RESULTS.csv")

    rows = read_valid_attempts(results_path)
    declared_valid = value_at(manifest, "scenario.valid_repetitions", len(rows))
    if isinstance(declared_valid, int) and declared_valid != len(rows):
        raise ValueError(
            f"{manifest_path}: valid_repetitions={declared_valid}, "
            f"but RESULTS.csv has {len(rows)} valid rows"
        )

    total_inputs = collect_numbers(
        rows, "total_input_tokens", "input_tokens_including_cached"
    )
    context_totals = collect_numbers(rows, "context_total_tokens")
    output_tokens = collect_numbers(rows, "output_tokens")

    latency_ms = collect_numbers(rows, "response_latency_ms")
    latency_ui_seconds = collect_numbers(rows, "ui_latency_seconds")
    if len(latency_ms) == len(rows):
        latency_seconds = [value / 1000 for value in latency_ms]
        latency_method = "事件时间戳"
        latency_decimals = 3
    elif len(latency_ui_seconds) == len(rows):
        latency_seconds = latency_ui_seconds
        latency_method = "UI 整秒"
        latency_decimals = 3
    else:
        latency_seconds = []
        latency_method = "未统一"
        latency_decimals = 3

    plan = str(value_at(manifest, "account.subscription_plan"))
    multiplier = value_at(manifest, "account.usage_multiplier", "")
    if multiplier != "—" and str(multiplier) not in plan:
        plan = f"{plan} {multiplier}".strip()

    visual_access = status_at(
        manifest, "evidence.visual_evidence_access", "public"
    )
    package_level = status_at(manifest, "evidence.package_level", "—")
    quota_attribution = status_at(
        manifest, "quota.attribution", "not_provided"
    )
    comparison_status = status_at(manifest, "comparison.status", "")

    captured_from = str(value_at(manifest, "scenario.captured_from_utc", ""))
    captured_date = (
        captured_from[:10]
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", captured_from)
        else package_dir.parent.name
    )

    return {
        "case_id": str(value_at(manifest, "prompt.case_id")),
        "agent": str(value_at(manifest, "agent.product")),
        "version": str(value_at(manifest, "agent.version")),
        "model": str(
            value_at(
                manifest,
                "model.observed",
                value_at(manifest, "model.requested"),
            )
        ),
        "effort": str(
            value_at(
                manifest,
                "reasoning.effort_observed",
                value_at(manifest, "reasoning.effort_requested"),
            )
        ),
        "plan": plan,
        "route": str(value_at(manifest, "route.category")),
        "profile": str(value_at(manifest, "harness.context_profile")),
        "session": str(value_at(manifest, "harness.session_state")),
        "os": str(value_at(manifest, "environment.os")),
        "architecture": str(value_at(manifest, "environment.architecture")),
        "valid_attempts": len(rows),
        "total_input": metric_summary(total_inputs),
        "context_total": metric_summary(context_totals),
        "output_tokens": metric_summary(output_tokens),
        "latency": metric_summary(latency_seconds, latency_decimals),
        "latency_method": latency_method,
        "package_level": str(package_level),
        "visual_access": str(visual_access),
        "quota_attribution": str(quota_attribution),
        "comparison_status": str(comparison_status),
        "captured_date": captured_date,
        "package_path": package_dir.relative_to(repo_root),
    }


def render_index(repo_root: Path) -> str:
    manifest_paths = sorted((repo_root / "runs").glob("*/*/manifest.yaml"))
    if not manifest_paths:
        raise ValueError("no scenario manifests found under runs/YYYY-MM-DD/")

    scenarios = [
        scenario_summary(repo_root, manifest_path)
        for manifest_path in manifest_paths
    ]
    scenarios.sort(
        key=lambda item: (
            str(item["case_id"]).casefold(),
            str(item["agent"]).casefold(),
            str(item["version"]).casefold(),
            str(item["model"]).casefold(),
        )
    )

    unique_agents = {str(item["agent"]) for item in scenarios}
    valid_attempts = sum(int(item["valid_attempts"]) for item in scenarios)

    lines = [
        "<!-- Generated by scripts/build-results-index.py. Do not edit manually. -->",
        "",
        "# Hi Tax Index",
        "",
        "> 不做简单排行榜；汇总相同 prompt 在不同 Agent harness 中的可观察 token footprint、延迟与证据强度。",
        "",
        "[返回项目首页](README.md) | [查看场景目录](runs/README.md) | [阅读贡献与口径规则](CONTRIBUTING.md)",
        "",
        f"- 场景数：{len(scenarios)}",
        f"- Agent 产品数：{len(unique_agents)}",
        f"- 有效 attempts：{valid_attempts}",
        "",
        "## 阅读规则",
        "",
        "1. 只在 prompt、会话状态、harness profile 等条件相近时比较；每一行都链接到完整场景。",
        "2. “总输入”是统一展示名，不是统一厂商字段：Codex 使用包含 cached input 的原生 input，Claude 使用普通 input、cache creation 与 cache read 之和。",
        "3. “Context total”是该场景明确定义的总输入加 output，只描述 token footprint，不等于 API 费用、订阅额度或积分。",
        "4. 延迟后的标签表示测量精度；事件时间戳与 UI 整秒显示不能假装具有相同精度。",
        "5. 表内数字显示中位数；括号内为最小值–最大值。原生缓存字段和每次 attempt 明细请进入场景页查看。",
        "",
    ]

    case_ids = sorted({str(item["case_id"]) for item in scenarios})
    for case_id in case_ids:
        case_scenarios = [
            item for item in scenarios if str(item["case_id"]) == case_id
        ]
        prompt_path = Path("prompts") / f"{case_id}.txt"
        safe_case_id = re.fullmatch(r"[A-Za-z0-9._-]+", case_id)
        if safe_case_id and (repo_root / prompt_path).is_file():
            case_heading = (
                f"## {TICK}{markdown_cell(case_id)}{TICK} "
                f"([精确输入]({markdown_path(prompt_path)}))"
            )
        else:
            case_heading = f"## {TICK}{markdown_cell(case_id)}{TICK}"
        lines.extend(
            [
                case_heading,
                "",
                "| Agent / 版本 | 模型 · Effort | 订阅 / 路由 | Harness | N | 总输入 | Context total | Output | 延迟 | 证据 / 额度归因 |",
                "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
            ]
        )

        for item in case_scenarios:
            package_path = Path(str(item["package_path"]))
            scenario_readme = markdown_path(package_path / "README.md")
            agent_label = (
                f"[{markdown_cell(item['agent'])} "
                f"{markdown_cell(item['version'])}]({scenario_readme})"
                f"<br><sub>{markdown_cell(item['captured_date'])}</sub>"
            )
            model_label = (
                f"{markdown_cell(item['model'])}"
                f"<br><sub>{markdown_cell(item['effort'])}</sub>"
            )
            route_label = ROUTE_LABELS.get(
                str(item["route"]), str(item["route"])
            )
            plan_label = (
                f"{markdown_cell(item['plan'])}"
                f"<br><sub>{markdown_cell(route_label)}</sub>"
            )
            harness_label = (
                f"{markdown_cell(item['profile'])} · "
                f"{markdown_cell(item['session'])}"
                f"<br><sub>{markdown_cell(item['os'])} "
                f"{markdown_cell(item['architecture'])}</sub>"
            )
            if item["comparison_status"]:
                comparison_label = COMPARISON_LABELS.get(
                    str(item["comparison_status"]),
                    str(item["comparison_status"]),
                )
                harness_label += (
                    f"<br><sub>{markdown_cell(comparison_label)}</sub>"
                )
            latency_label = (
                f"{markdown_cell(item['latency'])} s"
                f"<br><sub>{markdown_cell(item['latency_method'])}</sub>"
                if item["latency"] != "—"
                else "—"
            )
            visual_label = VISUAL_LABELS.get(
                str(item["visual_access"]), str(item["visual_access"])
            )
            evidence_label = (
                f"{markdown_cell(item['package_level'])} · "
                f"{markdown_cell(visual_label)}"
                f"<br><sub>quota: "
                f"{markdown_cell(item['quota_attribution'])}</sub>"
            )

            lines.append(
                "| "
                + " | ".join(
                    [
                        agent_label,
                        model_label,
                        plan_label,
                        harness_label,
                        markdown_cell(item["valid_attempts"]),
                        markdown_cell(item["total_input"]),
                        markdown_cell(item["context_total"]),
                        markdown_cell(item["output_tokens"]),
                        latency_label,
                        evidence_label,
                    ]
                )
                + " |"
            )
        lines.append("")

    fence = TICK * 3
    lines.extend(
        [
            "## 更新这个页面",
            "",
            "本页由场景包自动生成。新增或修改场景后运行：",
            "",
            f"{fence}sh",
            "python3 scripts/build-results-index.py",
            "./scripts/verify-all.sh",
            fence,
            "",
            "Pull Request 会检查本页是否与全部场景包保持一致。",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=script_path.parent.parent,
        help="repository root; defaults to the script's parent repository",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("RESULTS.md"),
        help="output path relative to the repository root",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the existing output differs; do not write",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    output_path = (
        args.output
        if args.output.is_absolute()
        else repo_root / args.output
    )

    try:
        rendered = render_index(repo_root)
    except (OSError, ValueError) as error:
        print(f"build-results-index: {error}", file=sys.stderr)
        return 1

    existing = (
        output_path.read_text(encoding="utf-8")
        if output_path.is_file()
        else ""
    )

    if args.check:
        if existing == rendered:
            print(f"results index is current: {output_path.relative_to(repo_root)}")
            return 0
        print(
            f"results index is stale: run {Path(__file__).name}",
            file=sys.stderr,
        )
        diff = difflib.unified_diff(
            existing.splitlines(),
            rendered.splitlines(),
            fromfile=str(output_path),
            tofile="generated",
            lineterm="",
        )
        for line in diff:
            print(line, file=sys.stderr)
        return 1

    if existing == rendered:
        print(f"results index unchanged: {output_path.relative_to(repo_root)}")
        return 0

    output_path.write_text(rendered, encoding="utf-8")
    try:
        os.chmod(output_path, 0o664)
    except OSError:
        pass
    print(f"results index written: {output_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
