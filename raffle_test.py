import random

import raffle


def test_trivial_case():
    prizes = ['foo']
    entries = ['alice']
    preferences = {'alice': ['foo']}

    results = raffle.raffle(prizes, entries, preferences)
    assert results == {'alice': 'foo'}


def test_selection_order_is_drawn_at_random():
    entries = ['alice', 'bob', 'carol']

    draw = raffle.draw_selection_order
    assert draw(entries, random.Random(4)) == ['alice', 'carol', 'bob']
    assert draw(entries, random.Random(999)) == ['carol', 'alice', 'bob']
    assert draw(entries, random.Random(-8675309)) == ['bob', 'alice', 'carol']


def test_selection_order_only_includes_each_participant_once():
    entries = [
        'alice',
        'bob',
        'alice',
        'carol',
        'bob',
        'carol',
        'alice',
        'alice',
    ]

    results = list(raffle.draw_selection_order(entries, random.Random(42)))
    assert len(results) == 3
    assert set(results) == {'alice', 'carol', 'bob'}