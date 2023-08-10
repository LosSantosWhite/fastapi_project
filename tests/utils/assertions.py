from typing import Any, List


def assert_dict_response(got: Any, want: Any):
    if isinstance(got, dict) and isinstance(want, dict):
        for k, v in want.items():
            got_attr = got.get(k)
            if isinstance(got_attr, dict):
                assert_dict_response(got_attr, v)
            elif isinstance(got_attr, list):
                for i, item in enumerate(got_attr):
                    assert_dict_response(item, v[i])
            else:
                message = (
                    f"got: {got_attr} ({type(got_attr)}), " f"want: {v} ({type(v)})"
                )
                assert got_attr == v, message
    else:
        message = f"got: {got} ({type(got)}), " f"want:{want} ({type(want)})"
        assert got == want, message


def assert_list_response(got: List, want: List):
    if isinstance(got, list) and isinstance(want, list) and len(got) == len(want):
        for g, w in zip(got, want):
            assert_dict_response(got=g, want=w)
    else:
        message = f"got: {got} ({type(got)}), " f"want:{want} ({type(want)})"
        assert got == want, message
