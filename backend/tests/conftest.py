import pytest

def pytest_collection_modifyitems(config, items):
    for item in items:        
        if "integration" in item.path.parts:
            item.add_marker(pytest.mark.integration)
            
        elif "unit" in item.path.parts:
            item.add_marker(pytest.mark.unit)