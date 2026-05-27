"""Workout definitions."""

from __future__ import annotations

from cali.models import Exercise, Workout

WARMUP = Workout(
    name='Warm-up',
    rounds=1,
    rest_between_exercises=5,
    rest_between_rounds=0,
    exercises=[
        Exercise('March in place', 30),
        Exercise('Arm circles', 30),
        Exercise('Hip circles', 30),
        Exercise('Bodyweight good mornings', 30),
        Exercise('Knee circles / ankle rolls', 30),
        Exercise('Step jacks or jumping jacks', 30),
        Exercise('Shoulder taps from knees or wall', 30),
        Exercise('Easy squats', 30),
        Exercise('Light lunges', 30),
        Exercise('Deep breathing', 30),
    ],
)


COOLDOWN = Workout(
    name='Cooldown',
    rounds=1,
    rest_between_exercises=5,
    rest_between_rounds=0,
    exercises=[
        Exercise('Hamstring stretch', 30),
        Exercise('Quad stretch', 30),
        Exercise('Chest / shoulder stretch', 30),
        Exercise("Child's pose", 30),
        Exercise('Deep breathing', 30),
    ],
)


WORKOUTS: dict[str, Workout] = {
    'Monday': Workout(
        name='Full Body Strength C',
        rounds=3,
        exercises=[
            Exercise('Reverse lunges', 45, '6 reps per leg'),
            Exercise('Incline push-ups', 45, '10 reps'),
            Exercise('Wall sit', 30, '20-30 seconds'),
            Exercise('Glute bridges', 45, '15 reps'),
            Exercise('Plank', 30, '20-30 seconds'),
        ],
    ),
    'Tuesday': Workout(
        name='Mobility + Core',
        rounds=3,
        exercises=[
            Exercise('Cat-cow', 40, '10 reps'),
            Exercise('Bird dogs', 45, '8 per side'),
            Exercise('Side plank from knees - left', 20),
            Exercise('Side plank from knees - right', 20),
            Exercise('Reverse lunges', 45, '6 per leg'),
            Exercise('Slow mountain climbers', 45, '10 per side'),
        ],
        rest_between_exercises=25,
        rest_between_rounds=60,
    ),
    'Wednesday': Workout(
        name='Full Body Strength B',
        rounds=3,
        exercises=[
            Exercise('Sit-to-stand squats', 45, '10 reps'),
            Exercise('Incline push-ups', 45, '8-10 reps'),
            Exercise('Step-ups', 50, '8 per leg'),
            Exercise('Supermans', 40, '10 reps'),
            Exercise('Hollow hold or dead bug hold', 30, '15-20 seconds'),
        ],
    ),
    'Thursday': Workout(
        name='Conditioning Day',
        rounds=5,
        exercises=[
            Exercise('Step jacks or jumping jacks', 30),
            Exercise('Bodyweight squats', 30),
            Exercise('Slow mountain climbers', 30),
        ],
        rest_between_exercises=30,
        rest_between_rounds=30,
    ),
    'Friday': Workout(
        name='Full Body Strength A',
        rounds=3,
        exercises=[
            Exercise('Squats', 45, '10 reps'),
            Exercise('Incline push-ups', 45, '8 reps'),
            Exercise('Glute bridges', 45, '12 reps'),
            Exercise('Dead bugs', 45, '8 per side'),
            Exercise('Plank', 25, '20 seconds'),
        ],
    ),
    'Saturday': Workout(
        name='Longer Easy Session',
        rounds=1,
        exercises=[
            Exercise('Easy walk', 600, '10 minutes minimum; 20-40 preferred'),
            Exercise('Squats', 45, '2 sets of 10 reps'),
            Exercise('Incline push-ups', 45, '2 sets of 8 reps'),
            Exercise('Plank', 25, '2 sets of 20 seconds'),
            Exercise('Stretch', 300, '5 minutes'),
        ],
        rest_between_exercises=30,
        rest_between_rounds=0,
    ),
    'Sunday': Workout(
        name='Recovery / Reset',
        rounds=1,
        exercises=[
            Exercise('Easy walk', 600, '10-20 minutes'),
            Exercise('Light stretching', 300),
        ],
        rest_between_exercises=30,
        rest_between_rounds=0,
    ),
}
