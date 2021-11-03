from src.rembg.bg import get_model

available_models = ['u2net', 'u2netp', 'u2net_human_seg']

for m in available_models:
    get_model(m)
