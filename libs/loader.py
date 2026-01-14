import yaml
import importlib
from typing import List, Tuple, Any

def load_tasks(config_path: str) -> List[Tuple[str, Any, int]]:
    """返回 [(任务名, 任务实例, 单独间隔秒), ...]"""
    with open(config_path, encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    tasks = []
    for item in cfg['tasks']:
        name = item['name']
        module_path, class_name = item['class'].rsplit('.', 1)
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        interval = int(item.get('interval', 10))
        tasks.append((name, cls(), interval))
    return tasks