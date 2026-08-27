from day09.nodes import (
    MAX_REWRITES,
    MAX_STEPS,
    classify_node,
    direct_generate_node,
    fallback_node,
    generate_node,
    quality_node,
    retrieve_node,
    rewrite_node,
    tool_node,
    validate_node,
)
from day09.state import create_initial_state


TERMINAL_STATUSES = {"completed", "error", "stopped"}


def stop_if_max_steps_reached(state: dict) -> bool:
    """Yeni bir node çalıştırmadan önce deterministik step guard."""
    if state["step_count"] < MAX_STEPS:
        return False

    state.update(
        {
            "status": "stopped",
            "errors": state["errors"] + ["MAX_STEPS sınırına ulaşıldı."],
            "node_trace": state["node_trace"] + ["max_step_guard"],
        }
    )
    return True


def run_native_workflow(query: str) -> dict:
    print(f"YENİ SORU: {query}")
    state = create_initial_state(query)

    print("[SİSTEM] Sınıflandırma yapılıyor...")
    state.update(classify_node(state))

    target_route = state["route"]
    print(f"[ROTA BULUNDU] Soru şu rotaya gidiyor: {target_route}")

    if target_route == "smalltalk":
        state.update(direct_generate_node(state))

    elif target_route == "knowledge":
        while state["status"] not in TERMINAL_STATUSES:
            if stop_if_max_steps_reached(state):
                break

            print("[SİSTEM] Veritabanında arama yapılıyor...")
            state.update(retrieve_node(state))

            # Önceki akıştaki ana eksik buydu: retrieve quality üretmez.
            state.update(quality_node(state))
            quality = state["retrieval_quality"]

            if quality == "usable":
                print("[BAŞARILI] Kullanılabilir veri bulundu.")
                state.update(generate_node(state))
                state.update(validate_node(state))

            elif quality == "weak":
                print(
                    "[UYARI] Veri kalitesi zayıf. "
                    f"Mevcut Rewrite: {state['rewrite_count']} / {MAX_REWRITES}"
                )

                if state["rewrite_count"] < MAX_REWRITES:
                    print("[SİSTEM] Soru bir kez yeniden yazılıyor...")
                    state.update(rewrite_node(state))
                else:
                    print("[FALLBACK] Rewrite sınırına ulaşıldı.")
                    state.update(fallback_node(state))

            else:
                state.update(
                    {
                        "status": "error",
                        "errors": state["errors"]
                        + [f"Bilinmeyen retrieval quality: {quality}"],
                    }
                )

    elif target_route == "tool":
        state.update(tool_node(state))

    else:
        state.update(
            {
                "status": "error",
                "errors": state["errors"] + ["Bilinmeyen rota"],
            }
        )

    return state


if __name__ == "__main__":
    result_1 = run_native_workflow("Selam, nasılsın?")
    print("Test 1 Trace:", result_1["node_trace"])
    print("Test 1 Cevap:", result_1["answer"])
    print("-" * 30)

    result_2 = run_native_workflow("Docker volume nedir?")
    print("Test 2 Trace:", result_2["node_trace"])
    print("Test 2 Cevap:", result_2["answer"])
    print("-" * 30)

    result_3 = run_native_workflow("Zayıf sonuç üretmesi gereken test sorgusu")
    print("Test 3 Trace:", result_3["node_trace"])
    print("Test 3 Cevap:", result_3["answer"])
    print("Test 3 Rewrite Sayısı:", result_3["rewrite_count"])
