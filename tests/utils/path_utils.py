from pathlib import Path

def find_project_root(marker_folder: str = "home_assignment") -> Path:
    """
    Traverses up from the current file location to find the root of the project.
    """
    current = Path(__file__).resolve()
    while current.name != marker_folder:
        if current.parent == current:
            raise RuntimeError(f"Could not find project root named '{marker_folder}'")
        current = current.parent
    return current