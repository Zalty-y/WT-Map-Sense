## Scenario 1
Fresh spawn with no movement; comparison of vehicle indices when switching to a second player on the same team.
Data:
- scenario_1_player_1
- scenario_1_player_2
Result:
- Indices were consistent.
- Sadly, indices do not correlate to player order.

## Scenario 2
A few seconds of movement; one late vehicle spawn; comparison of vehicle indices when switching to a second player on the same team and comparing to data from scenario 1.
Data:
- scenario_1_player_1
- scenario_1_player_2
- scenario_2_player_1
- scenario_2_player_2
Result:
- Indices were consistent within the player switches.
- Indices were consistent with scenario 1 data.
- Late-spawn vehicle appended to the bottom of the list (last index).
- Maybe, the indices are based on spawn order?

## Scenario 3
Swapped to an enemy player and back to the original player; comparison of vehicle indices before and after swapping to enemy player.
Data:
- scenario_2_player_2
- scenario_3_player_2
Result:
- Data was identical.
- Switching teams in replay has no effect on vehicle indices.

## Scenario 4
Teammate death; Late vehicle spawn.
Data:
- scenario_2_player_2
- scenario_4_player_2
Result:
- Destroyed vehicle removed from list.
- Late-spawn vehicle appended to the bottom of the list.

## Scenario 5
Selected player death.
Data:
- scenario_4_player_2
- scenario_5_player_2
Result:
- Indices were consistent.

## Scenario 6
A few seconds after scenario 5; same player; two more team deaths
Data:
- scenario_5_player_2
- scenario_6_player_2
Result:
- Selected player removed from list.
- Two teammates removed from list.

## Scenario 7
Checking if battle events affected indicies between swapping players; swapped to player 1.
Data:
- scenario_6_player_2
- scenario_7_player_1
Result:
- Indices were consistent.

## Scenario 8
Swapping back to player 2; checking indices after vehicle spawn of selected player.
Data:
- scenario_6_player_2
- scenario_8_player_2
Result:
- Indices were consistent.
- Selected player appended to the bottom of the list.

## Conclusion
The order of the vehicles in map_obj.json depends on the vehicle spawn and won't change unless a vehicle is destoryed (shifting up all subsequent vehicles) or a new vehicle spawns, getting appended to the bottom of the list.
