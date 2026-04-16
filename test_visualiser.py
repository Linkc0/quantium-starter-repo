import pandas as pd

import visualiser


def _sample_data():
    return pd.DataFrame(
        {
            "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
            "sales": [10.0, 20.5, 5.0, 17.25],
            "region": ["north", "south", "north", "east"],
        }
    )


def test_chart_generation_sets_expected_titles_and_colors():
    figure = visualiser.chartGeneration(_sample_data())

    assert figure.layout.title.text == "Pink Morsel Sales"
    assert figure.layout.xaxis.title.text == "Date"
    assert figure.layout.yaxis.title.text == "Sales"
    assert figure.layout.title.font.color == visualiser.COLORS["secondary"]
    assert figure.layout.font.color == visualiser.COLORS["font"]


def test_chart_generation_uses_date_for_x_and_sales_for_y():
    figure = visualiser.chartGeneration(_sample_data())
    assert list(figure.data[0].x) == ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"]
    assert list(figure.data[0].y) == [10.0, 20.5, 5.0, 17.25]


def test_update_graph_returns_all_rows_for_all_region(monkeypatch):
    test_df = _sample_data()
    monkeypatch.setattr(visualiser, "data", test_df)

    figure = visualiser.update_graph("all")
    assert list(figure.data[0].x) == list(test_df["date"])
    assert list(figure.data[0].y) == list(test_df["sales"])


def test_update_graph_filters_by_region(monkeypatch):
    test_df = _sample_data()
    monkeypatch.setattr(visualiser, "data", test_df)

    figure = visualiser.update_graph("north")

    expected = test_df[test_df["region"] == "north"]
    assert list(figure.data[0].x) == list(expected["date"])
    assert list(figure.data[0].y) == list(expected["sales"])


def test_update_graph_returns_empty_series_for_missing_region(monkeypatch):
    test_df = _sample_data()
    monkeypatch.setattr(visualiser, "data", test_df)

    figure = visualiser.update_graph("west")
    assert list(figure.data[0].x) == []
    assert list(figure.data[0].y) == []
