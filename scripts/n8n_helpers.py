import json
import uuid


def node(name, ntype, params, position, type_version=1):
    return {
        "parameters": params,
        "id": str(uuid.uuid4()),
        "name": name,
        "type": ntype,
        "typeVersion": type_version,
        "position": position,
    }


def code_node(name, js_code, position):
    return node(name, "n8n-nodes-base.code", {"jsCode": js_code}, position, type_version=2)


def sticky(content, position, width=340, height=260, color=None, name="Sticky Note"):
    params = {"content": content, "height": height, "width": width}
    if color is not None:
        params["color"] = color
    return node(name, "n8n-nodes-base.stickyNote", params, position, type_version=1)


def chain(*names):
    conn = {}
    for a, b in zip(names, names[1:]):
        conn.setdefault(a, {"main": [[]]})
        conn[a]["main"][0].append({"node": b, "type": "main", "index": 0})
    return conn


def branch(source, targets):
    return {source: {"main": [[{"node": t, "type": "main", "index": 0} for t in targets]]}}


def merge_connections(*dicts):
    out = {}
    for d in dicts:
        for k, v in d.items():
            if k not in out:
                out[k] = {"main": [list(v["main"][0])]}
            else:
                out[k]["main"][0].extend(v["main"][0])
    return out


def workflow(name, nodes, connections):
    return {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "pinData": {},
        "settings": {"executionOrder": "v1"},
    }


def save_workflow(wf, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(wf, f, indent=2)
