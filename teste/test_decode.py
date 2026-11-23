from arsenal.forensics.decode import desfa
def test_base64():
    strat, b=desfa("U2FsdXQ=")
    assert strat=="Base64"
    assert b == b"Salut"
if __name__ == "__main__":
    test_base64()
    print("Testul a trecut cu succes!")