import argparse
import os
import time
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command
from day13.durable_graph import get_durable_graph_builder
from day13.trace import log_trace

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["start", "inspect", "resume"])
    parser.add_argument("--thread-id", required=True)
    parser.add_argument("--decision", choices=["approve", "reject"])
    parser.add_argument("--action", default="publish_report")
    args = parser.parse_args()

    os.makedirs("output/day13", exist_ok=True)
    builder = get_durable_graph_builder()

    with SqliteSaver.from_conn_string("output/day13/checkpoints.sqlite") as checkpointer:
        graph = builder.compile(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": args.thread_id}}

        if args.command == "start":
            print(f"[{args.thread_id}] Workflow çalıştırılıyor... (Action: {args.action})")
            
            start_time = time.time()
            
            graph.invoke({"request": "start_demo", "action_type": args.action}, config)
            duration = int((time.time() - start_time) * 1000)
            
            snapshot = graph.get_state(config)
            state_values = snapshot.values or {}
            is_interrupted = len(snapshot.next) > 0
            
            log_trace(
                thread_id=args.thread_id,
                action_id=state_values.get("action_id"),
                action_type=state_values.get("action_type", args.action),
                resumed=False,
                duration_ms=duration,
                status="interrupted" if is_interrupted else "completed"
            )
            print("Akış tamamlandı veya duraklatıldı.")
            
        elif args.command == "inspect":
            state = graph.get_state(config)
            print(f"[{args.thread_id}] Güncel Durum:")
            if state.values:
                print(state.values)
                print(f"Next Node: {state.next}")
            else:
                print("Bu thread ID için bir kayıt bulunamadı.")
                
        elif args.command == "resume":
            if not args.decision:
                raise ValueError("Resume komutu için --decision argümanı gereklidir.")
            
            start_time = time.time()
            graph.invoke(Command(resume={"decision": args.decision}), config)
            duration = int((time.time() - start_time) * 1000)
            
            snapshot = graph.get_state(config)
            state_values = snapshot.values or {}
            is_interrupted = len(snapshot.next) > 0
            
            log_trace(
                thread_id=args.thread_id,
                action_id=state_values.get("action_id"),
                action_type=state_values.get("action_type"),
                resumed=True,
                approval_decision=args.decision,
                duration_ms=duration,
                status="interrupted" if is_interrupted else "completed"
            )

if __name__ == "__main__":
    main()