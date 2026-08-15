from src.judge import judge_response
from src.attacker import mutate_prompt

def run_adaptive_attack(target, probe, max_turns: int = 4):
    original_payload = probe.payload
    current_prompt = probe.payload

    for turn in range(max_turns):
        print(f"  Turn {turn + 1}: sending prompt...")
        response = target.send(current_prompt)
        verdict = judge_response(current_prompt, response)

        if verdict["verdict"] == "COMPLY":
            print(f"  Turn {turn + 1}: SUCCESS")
            return {
                "success": True,
                "turns_used": turn + 1,
                "final_prompt": current_prompt,
                "final_response": response,
                "reasoning": verdict["reasoning"],
            }

        print(f"  Turn {turn + 1}: refused, mutating...")
        current_prompt = mutate_prompt(original_payload, current_prompt, response)

    return {
        "success": False,
        "turns_used": max_turns,
        "final_prompt": current_prompt,
        "final_response": response,
        "reasoning": "Target resisted all mutation attempts.",
    }