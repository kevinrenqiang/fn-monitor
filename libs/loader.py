import importlib
from typing import Dict, Any

def load_tasks(config_path: str) -> Dict[str, Any]:
    """动态加载所有任务类"""
    import yaml
    with open(config_path, encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    interval = cfg.get('interval', 10)
    tasks = {}
    for item in cfg['tasks']:
        name = item['name']
        module_path, class_name = item['class'].rsplit('.', 1)
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
        tasks[name] = cls()
    return interval, tasks