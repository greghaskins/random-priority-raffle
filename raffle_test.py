import random
import pytest

import raffle


def test_trivial_case():
    prizes = ['foo']
    entries = ['alice']
    preferences = {'alice': ['foo']}

    results = raffle.raffle(prizes, entries, preferences)
    assert results == [('alice', 'foo')]


def test_full_example():
    prizes = ['foo', 'bar', 'baz']
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
    preferences = {
        'alice': ['foo', 'bar', 'baz'],
        'bob': ['foo', 'baz', 'bar'],
        'carol': ['baz', 'bar', 'foo']
    }
    rnd = random.Random("4f917c6e0da")

    assert raffle.raffle(prizes, entries, preferences, rnd) == [
        ('alice', 'foo'),
        ('carol', 'baz'),
        ('bob', 'bar'),
    ]


def test_raffle_throws_exception_when_validation_fails():
    prizes = ['foo', 'baz']
    entries = ['alice', 'bob', 'carol']
    preferences = {
        'alice': ['foo', 'bar'],
        'bob': ['foo', 'foo', 'foo'],
    }

    with pytest.raises(ValueError) as exception_info:
        raffle.raffle(prizes, entries, preferences)

    assert len(exception_info.value.args[0]) == 4


def test_selection_order_is_drawn_at_random():
    entries = ['alice', 'bob', 'carol']

    draw = raffle.draw_selection_order
    assert draw(entries, random.Random(4)) == ['alice', 'carol', 'bob']
    assert draw(entries, random.Random(999)) == ['carol', 'alice', 'bob']
    assert draw(entries, random.Random(-8675309)) == ['bob', 'alice', 'carol']


def test_selection_order_is_independent_of_input_order():
    entries1 = ['alice', 'bob', 'carol']
    entries2 = ['carol', 'alice', 'bob']
    entries3 = ['bob', 'carol', 'alice']

    draw = raffle.draw_selection_order
    assert draw(entries1, random.Random(-8675309)) == ['bob', 'alice', 'carol']
    assert draw(entries2, random.Random(-8675309)) == ['bob', 'alice', 'carol']
    assert draw(entries3, random.Random(-8675309)) == ['bob', 'alice', 'carol']


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
    assert assign(prizes, preferences, ['alice', 'bob', 'carol']) == [
        ('alice', 'foo'),
        ('bob', 'bar'),
        ('carol', 'baz'),
    ]
    assert assign(prizes, preferences, ['bob', 'carol', 'alice']) == [
        ('bob', 'foo'),
        ('carol', 'bar'),
        ('alice', 'baz'),
    ]


def test_prize_assignments_based_on_preferences():
    prizes = ['foo', 'bar', 'baz']
    selection_order = ['alice', 'bob', 'carol']

    assign = raffle.assign_prizes
    assert assign(
        prizes, {
            'alice': ['baz', 'foo', 'bar'],
            'bob': ['bar', 'foo', 'baz'],
            'carol': ['foo', 'bar', 'baz']
        }, selection_order) == [
            ('alice', 'baz'),
            ('bob', 'bar'),
            ('carol', 'foo'),
        ]
    assert assign(
        prizes, {
            'alice': ['baz', 'foo', 'bar'],
            'bob': ['baz', 'foo', 'baz'],
            'carol': ['foo', 'bar', 'baz']
        }, selection_order) == [
            ('alice', 'baz'),
            ('bob', 'foo'),
            ('carol', 'bar'),
        ]


def test_can_have_multiple_copies_of_prizes():
    prizes = ['foo', 'foo', 'bar']
    preferences = {
        'alice': ['foo', 'bar'],
        'bob': ['foo', 'bar'],
        'carol': ['foo', 'bar']
    }

    assign = raffle.assign_prizes
    assert assign(prizes, preferences, ['alice', 'bob', 'carol']) == [
        ('alice', 'foo'),
        ('bob', 'foo'),
        ('carol', 'bar'),
    ]
    assert assign(prizes, preferences, ['carol', 'bob', 'alice']) == [
        ('carol', 'foo'),
        ('bob', 'foo'),
        ('alice', 'bar'),
    ]


def test_validate_returns_error_when_not_enough_prizes_for_participants():
    preferences = {
        'alice': ['foo', 'bar', 'baz'],
        'bob': ['foo', 'bar', 'baz'],
        'carol': ['foo', 'bar', 'baz'],
        'dave': ['foo', 'bar', 'baz']
    }

    assert "not enough prizes for 3 participants" in raffle.validate(
        prizes=['foo', 'bar'],
        entries=['alice', 'bob', 'carol'],
        preferences=preferences)
    assert "not enough prizes for 4 participants" in raffle.validate(
        prizes=['foo', 'bar', 'bar'],
        entries=['alice', 'bob', 'carol', 'dave'],
        preferences=preferences)


def test_validate_only_counts_unique_participants_in_entry_list():
    preferences = {
        'alice': ['foo', 'bar', 'baz'],
        'bob': ['foo', 'bar', 'baz'],
        'carol': ['foo', 'bar', 'baz'],
        'dave': ['foo', 'bar', 'baz']
    }

    assert not raffle.validate(prizes=['foo', 'bar'],
                               entries=['alice', 'bob', 'bob'],
                               preferences=preferences)
    assert not raffle.validate(prizes=['foo', 'bar', 'bar'],
                               entries=['alice', 'bob', 'bob', 'carol'],
                               preferences=preferences)


def test_preferences_must_include_each_distinct_prize():
    prizes = ['foo', 'foo', 'bar', 'baz', 'foo']
    entries = ['alice', 'bob']

    assert "'alice' does not have prize 'baz' in preference list" in raffle.validate(
        prizes, entries, {
            'alice': ['foo', 'bar'],
            'bob': ['foo', 'bar', 'baz']
        })
    assert "'bob' does not have prize 'bar' in preference list" in raffle.validate(
        prizes, entries, {
            'alice': ['foo', 'bar', 'baz'],
            'bob': ['foo', 'boo']
        })
    assert "'bob' does not have prize 'baz' in preference list" in raffle.validate(
        prizes, entries, {
            'alice': ['foo', 'bar', 'baz'],
            'bob': ['foo']
        })


def test_each_entry_must_have_preferences():
    prizes = ['foo', 'bar', 'baz']
    entries = ['alice', 'bob', 'carol']

    assert "missing preferences for entry 'carol'" in raffle.validate(
        prizes, entries, {
            'alice': ['foo', 'bar', 'baz'],
            'bob': ['foo', 'bar', 'baz']
        })
