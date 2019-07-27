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


def test_prize_assignments_with_uniform_preferences():
    prizes = ['foo', 'bar', 'baz']
    preferences = {
        'alice': ['foo', 'bar', 'baz'],
        'bob': ['foo', 'bar', 'baz'],
        'carol': ['foo', 'bar', 'baz']
    }

    assign = raffle.assign_prizes
    assert assign(prizes, preferences, ['alice', 'bob', 'carol']) == {
        'alice': 'foo',
        'bob': 'bar',
        'carol': 'baz'
    }
    assert assign(prizes, preferences, ['bob', 'carol', 'alice']) == {
        'alice': 'baz',
        'bob': 'foo',
        'carol': 'bar'
    }


def test_prize_assignments_based_on_preferences():
    prizes = ['foo', 'bar', 'baz']
    selection_order = ['alice', 'bob', 'carol']

    assign = raffle.assign_prizes
    assert assign(
        prizes, {
            'alice': ['baz', 'foo', 'bar'],
            'bob': ['bar', 'foo', 'baz'],
            'carol': ['foo', 'bar', 'baz']
        }, selection_order) == {
            'alice': 'baz',
            'bob': 'bar',
            'carol': 'foo'
        }
    assert assign(
        prizes, {
            'alice': ['baz', 'foo', 'bar'],
            'bob': ['baz', 'foo', 'baz'],
            'carol': ['foo', 'bar', 'baz']
        }, selection_order) == {
            'alice': 'baz',
            'bob': 'foo',
            'carol': 'bar'
        }


def test_can_have_multiple_copies_of_prizes():
    prizes = ['foo', 'foo', 'bar']
    preferences = {
        'alice': ['foo', 'bar'],
        'bob': ['foo', 'bar'],
        'carol': ['foo', 'bar']
    }

    assign = raffle.assign_prizes
    assert assign(prizes, preferences, ['alice', 'bob', 'carol']) == {
        'alice': 'foo',
        'bob': 'foo',
        'carol': 'bar'
    }
    assert assign(prizes, preferences, ['carol', 'bob', 'alice']) == {
        'alice': 'bar',
        'bob': 'foo',
        'carol': 'foo'
    }


## TODO: all the validation: not enough prizes, mismatched preferences, mismatched entries
