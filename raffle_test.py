import raffle

def test_trivial_case():
    prizes = ['foo']
    entries = ['alice']
    preferences = {'alice': ['foo']}

    results = raffle.raffle(prizes, entries, preferences)
    assert results == {'alice': 'foo'}

