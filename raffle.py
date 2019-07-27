#!/usr/bin/env python3

import random
from typing import NewType, Mapping, Collection, Iterable, Sequence

Participant = NewType('Participant', str)
Prize = NewType('Prize', str)


def raffle(prizes: Sequence[Prize],
           entries: Collection[Participant],
           preferences: Mapping[Participant, Sequence[Prize]],
           random_source: random.Random = random.SystemRandom()
           ) -> Mapping[Participant, Prize]:

    hat = list(entries)
    results = {}

    for prize in prizes:
        winner = hat.pop()
        results[winner] = prize

    return results


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
) -> Mapping[Participant, Prize]:

    remaining_prizes = list(prizes)
    results = {}

    for participant in selection_order:
        for preference in preferences[participant]:
            if preference in remaining_prizes:
                remaining_prizes.remove(preference)
                results[participant] = preference
                break

    return results
