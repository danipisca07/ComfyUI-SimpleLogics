try:
    from .nodes import NODE_CLASS_MAPPINGS as nodes_mappings, NODE_DISPLAY_NAME_MAPPINGS as nodes_display_names
    from .geocalib_to_fspy import NODE_CLASS_MAPPINGS as geocalib_mappings, NODE_DISPLAY_NAME_MAPPINGS as geocalib_display_names
except ImportError:
    from nodes import NODE_CLASS_MAPPINGS as nodes_mappings, NODE_DISPLAY_NAME_MAPPINGS as nodes_display_names
    from geocalib_to_fspy import NODE_CLASS_MAPPINGS as geocalib_mappings, NODE_DISPLAY_NAME_MAPPINGS as geocalib_display_names

# Merge all node mappings
NODE_CLASS_MAPPINGS = {**nodes_mappings, **geocalib_mappings}
NODE_DISPLAY_NAME_MAPPINGS = {**nodes_display_names, **geocalib_display_names}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
