import json
from pathlib import Path

ALLOWED_SUITES = {
    "routing",
    "routing_challenge",
    "workflow",
    "durable",
}
ALLOWED_ROUTES = {
    "smalltalk",
    "knowledge",
    "tool",
}
ALLOWED_TOOL_PROVIDERS = {
    "native",
    "mcp",
}
ALLOWED_TERMINAL_STATUSES = {
    "completed",
    "interrupted",
    "rejected",
    "error",
}

def validate_case(
    case: dict,
    registered_tools: set[str],
) -> None:
    """Tek bir golden case'i doğrular."""

    # TODO 1:
    # id alanının boş olmayan string olduğunu kontrol et.
    if not isinstance(case.get("id"), str) or not case["id"].strip():
        raise ValueError(f"Invalid case id: {case.get('id')}")

    # TODO 2:
    # query alanının boş olmayan string olduğunu kontrol et.
    if not isinstance(case.get("query"), str) or not case["query"].strip():
        raise ValueError(f"Invalid case query: {case.get('query')}")

    # TODO 3:
    # suite değerinin ALLOWED_SUITES içinde olduğunu kontrol et.
    if case.get("suite") not in ALLOWED_SUITES:
        raise ValueError(f"Invalid case suite: {case.get('suite')}")

    # TODO 4:
    # expected_route varsa:
    # - null olabilir.
    # - null değilse ALLOWED_ROUTES içinde olmalı.
    if "expected_route" in case and case["expected_route"] is not None:
        if case["expected_route"] not in ALLOWED_ROUTES:
            raise ValueError(f"Invalid expected_route: {case['expected_route']}")

    # TODO 5:
    # expected_tool varsa:
    # - registered_tools içinde olmalı.
    # - expected_route değeri "tool" olmalı.
    if "expected_tool" in case:
        if case["expected_tool"] not in registered_tools:
            raise ValueError(f"Invalid expected_tool: {case['expected_tool']}")
        if case.get("expected_route") != "tool":
            raise ValueError(
                "expected_route must be 'tool' when expected_tool is specified"
            )

    # expected_source yalnız knowledge route ile anlamlıdır.
    if "expected_source" in case:
        if (
            not isinstance(case["expected_source"], str)
            or not case["expected_source"].strip()
        ):
            raise ValueError(
                f"Invalid expected_source: {case['expected_source']}"
            )
        if case.get("expected_route") != "knowledge":
            raise ValueError(
                "expected_route must be 'knowledge' "
                "when expected_source is specified"
            )

    # expected_action mevcutsa boş olmayan string olmalıdır.
    if "expected_action" in case:
        if (
            not isinstance(case["expected_action"], str)
            or not case["expected_action"].strip()
        ):
            raise ValueError(
                f"Invalid expected_action: {case['expected_action']}"
            )

    # Provider ve terminal değerleri uygulamanın allowlist'iyle uyumlu olmalıdır.
    if (
        "expected_tool_provider" in case
        and case["expected_tool_provider"] not in ALLOWED_TOOL_PROVIDERS
    ):
        raise ValueError(
            "Invalid expected_tool_provider: "
            f"{case['expected_tool_provider']}"
        )

    if (
        "expected_terminal_status" in case
        and case["expected_terminal_status"] not in ALLOWED_TERMINAL_STATUSES
    ):
        raise ValueError(
            "Invalid expected_terminal_status: "
            f"{case['expected_terminal_status']}"
        )

    # Boolean expectation alanlarının yanlışlıkla string/sayı olmasını engelle.
    if "approval_required" in case and not isinstance(
        case["approval_required"], bool
    ):
        raise ValueError(
            f"approval_required must be boolean: {case['approval_required']}"
        )

    # Ambiguous challenge vakalarında null kullanılabildiği için None kabul edilir.
    if (
        "capability_available" in case
        and case["capability_available"] is not None
        and not isinstance(case["capability_available"], bool)
    ):
        raise ValueError(
            "capability_available must be boolean or null: "
            f"{case['capability_available']}"
        )

    # Bir vaka yalnızca tek trajectory karşılaştırma politikası taşımalıdır.
    if "allowed_trajectory" in case and "strict_trajectory" in case:
        raise ValueError(
            "A case cannot contain both allowed_trajectory and strict_trajectory"
        )

    for field_name in ("allowed_trajectory", "strict_trajectory"):
        if field_name not in case:
            continue

        trajectory = case[field_name]
        if not isinstance(trajectory, list) or not trajectory:
            raise ValueError(f"{field_name} must be a non-empty list")
        if not all(
            isinstance(node, str) and node.strip()
            for node in trajectory
        ):
            raise ValueError(
                f"{field_name} must contain non-empty strings"
            )

    # TODO 6:
    # resume_payload varsa:
    # - dictionary olmalı.
    # - decision değeri approve veya reject olmalı.
    if "resume_payload" in case:
        if not isinstance(case["resume_payload"], dict):
            raise ValueError(
                "resume_payload must be a dictionary: "
                f"{case['resume_payload']}"
            )
        if case["resume_payload"].get("decision") not in {"approve", "reject"}:
            raise ValueError(
                "Invalid decision in resume_payload: "
                f"{case['resume_payload'].get('decision')}"
            )
        if case.get("suite") != "durable":
            raise ValueError(
                "resume_payload can only be used in durable suite"
            )


def load_golden_cases(
    path: str | Path,
    registered_tools: set[str],
) -> list[dict]:
    """JSONL dosyasını yükler ve doğrular."""

    # TODO 7:
    # Dosyanın mevcut olduğunu kontrol et.
    dataset_path = Path(path)
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")

    # TODO 8:
    # Dosyayı UTF-8 ile aç.
    # Her dolu satırı json.loads ile parse et.
    cases = []
    with dataset_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                case = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: {exc}"
                ) from exc

            if not isinstance(case, dict):
                raise ValueError(
                    f"Line {line_number} must contain a JSON object"
                )

            # TODO 9:
            # Her vaka için validate_case çağır.
            try:
                validate_case(case, registered_tools)
            except ValueError as exc:
                raise ValueError(
                    f"Invalid case at line {line_number}: {exc}"
                ) from exc

            cases.append(case)

    if not cases:
        raise ValueError("Golden dataset cannot be empty")

    # TODO 10:
    # ID değerlerinin benzersiz olduğunu kontrol et.
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        duplicate_ids = sorted(
            case_id for case_id in set(ids) if ids.count(case_id) > 1
        )
        raise ValueError(f"Duplicate case IDs found: {duplicate_ids}")

    # TODO 11:
    # Doğrulanmış vakaları liste olarak döndür.
    return cases

def select_scored_routing_cases(
    cases: list[dict],
) -> list[dict]:
    """Route metriğine katılacak vakaları seçer."""

    # TODO 12:
    # expected_route değeri null olmayan vakaları döndür.
    return [case for case in cases if case.get("expected_route") is not None]
