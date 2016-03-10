def pytest_collection_modifyitems(session, config, items):
    unit = [item for item in items if item.get_marker("unit")]
    integration = [item for item in items if item.get_marker("integration")]
    ui = [item for item in items if item.get_marker("ui")]
    feature = [item for item in items if item.get_marker("feature")]
    unmarked = [item for item in items if
                item not in unit and item not in integration and item not in ui and item not in feature]

    items.clear()
    items.extend(unit + integration + ui + feature + unmarked)
