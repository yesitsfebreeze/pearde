"""Plan-owned Scope presentation of published state and verification evidence."""
import json
import sys


def render(request):
    item = request["item"]
    attrs = item.get("attributes", {})
    return {"version": 1, "title": item.get("name") or item["id"], "sections": [
        {"label": "State", "value": attrs.get("prd.state", "plan")},
        {"label": "Verification", "value": {"completed": attrs.get("prd.checks_done"), "total": attrs.get("prd.checks_total"), "checks": attrs.get("prd.checks", [])}},
        {"label": "Claim", "value": attrs.get("prd.claim")},
        {"label": "Plan", "value": {key.removeprefix("prd."): value for key, value in attrs.items() if key.startswith("prd.")}},
        {"label": "Provenance", "value": item.get("contributors", [])}]}


if __name__ == "__main__":
    for line in sys.stdin:
        frame = json.loads(line)
        try:
            reply = {"result": render(frame["args"])}
        except (KeyError, TypeError, ValueError) as error:
            reply = {"error": str(error)}
        print(json.dumps(dict(reply, id=frame["id"])), flush=True)
