from app.handlers.jobs import format_info

# TODO: Add tests

def test_dummy():

    info = "Outage on Street"
    street = "Street"
    
    result = "Outage on <b>Street</b>"

    assert format_info(info, street) == result
    assert format_info(info, "Not existing street") != result
    assert format_info(info, "Not existing street") == info
