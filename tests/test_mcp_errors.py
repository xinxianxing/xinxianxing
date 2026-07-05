from src.mcp.errors import XinxianxingMcpError


def test_xinxianxing_mcp_error_string_representation() -> None:
    err = XinxianxingMcpError(code="E_TEST", message="boom", details={"k": "v"})

    assert str(err) == "E_TEST: boom"
    assert err.details == {"k": "v"}
