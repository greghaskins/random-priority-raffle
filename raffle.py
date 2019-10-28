#!/usr/bin/env python3

import random
from typing import NewType, Mapping, Collection, Iterable, Sequence, NamedTuple

Participant = NewType('Participant', str)
Prize = NewType('Prize', str)
Error = NewType('Error', str)


class Assignment(NamedTuple):
    participant: Participant
    prize: Prize


def raffle(prizes: Sequence[Prize],
           entries: Collection[Participant],
           preferences: Mapping[Participant, Sequence[Prize]],
           random_source: random.Random = random.SystemRandom()
           ) -> Sequence[Assignment]:

    errors = validate(prizes, entries, preferences)
    if errors:
        raise ValueError(errors)
    selection_order = draw_selection_order(entries, random_source)
    results = assign_prizes(prizes, preferences, selection_order)
    return results


def validate(prizes: Sequence[Prize], entries: Collection[Participant],
             preferences: Mapping[Participant, Sequence[Prize]]
             ) -> Collection[Error]:
    errors = []
    number_of_participants = len(set(entries))

    if len(prizes) < number_of_participants:
        errors.append(
            f"not enough prizes for { number_of_participants } participants")

    distinct_prizes = set(prizes)
    for participant in preferences:
        for prize in distinct_prizes:
            if prize not in preferences[participant]:
                errors.append(
                    f"'{participant}' does not have prize '{prize}' in preference list"
                )

    for entry in entries:
        if entry not in preferences:
            errors.append(f"missing preferences for entry '{ entry}'")

    return errors


def draw_selection_order(
        entries: Collection[Participant],
        random_source: random.Random,
) -> Iterable[Participant]:

    selection_order = []
    hat = list(entries)

    while hat:
        random_index = random_source.randrange(len(hat))
        participant = hat.pop(random_index)
        if participant not in selection_order:
            selection_order.append(participant)

    return selection_order


def assign_prizes(
        prizes: Collection[Prize],
        preferences: Mapping[Participant, Sequence[Prize]],
        selection_order: Iterable[Participant],
) -> Sequence[Assignment]:

    remaining_prizes = list(prizes)
    results = []

    for participant in selection_order:
        for preference in preferences[participant]:
            if preference in remaining_prizes:
                remaining_prizes.remove(preference)
                results.append(Assignment(participant, preference))
                break

    return results
