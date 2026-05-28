"""Kivy mobile UI for cali-workout."""

from __future__ import annotations

import datetime as dt

from dataclasses import dataclass
from typing import TYPE_CHECKING

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from cali.workouts import COOLDOWN, WARMUP, WORKOUTS

if TYPE_CHECKING:
    from cali.models import Exercise


@dataclass(frozen=True)
class TimerStep:
    """A single timed step in the mobile workout flow."""

    label: str
    exercise: Exercise


class CaliWorkoutApp(App):
    """Simple Android-friendly workout timer UI."""

    def build(self) -> BoxLayout:
        self.today = dt.datetime.now().strftime('%A')
        self.workout = WORKOUTS[self.today]
        self.steps = self._build_steps()
        self.step_index = 0
        self.remaining_seconds = self.steps[0].exercise.duration_seconds
        self.running = False
        self.clock_event = None

        self.root_layout = BoxLayout(
            orientation='vertical',
            padding=24,
            spacing=16,
        )

        self.title_label = Label(
            text=f'{self.today}: {self.workout.name}',
            font_size='24sp',
            size_hint_y=0.18,
        )
        self.exercise_label = Label(
            text='Press Start',
            font_size='28sp',
            size_hint_y=0.24,
        )
        self.notes_label = Label(
            text='',
            font_size='18sp',
            size_hint_y=0.16,
        )
        self.timer_label = Label(
            text=self._format_time(self.remaining_seconds),
            font_size='48sp',
            size_hint_y=0.24,
        )

        controls = BoxLayout(
            orientation='horizontal',
            spacing=12,
            size_hint_y=0.18,
        )

        self.start_pause_button = Button(text='Start')
        self.start_pause_button.bind(on_press=self.toggle_timer)

        self.skip_button = Button(text='Skip')
        self.skip_button.bind(on_press=self.skip_step)

        self.reset_button = Button(text='Reset')
        self.reset_button.bind(on_press=self.reset_workout)

        controls.add_widget(self.start_pause_button)
        controls.add_widget(self.skip_button)
        controls.add_widget(self.reset_button)

        self.root_layout.add_widget(self.title_label)
        self.root_layout.add_widget(self.exercise_label)
        self.root_layout.add_widget(self.notes_label)
        self.root_layout.add_widget(self.timer_label)
        self.root_layout.add_widget(controls)

        self._render_current_step()
        return self.root_layout

    def _build_steps(self) -> list[TimerStep]:
        steps: list[TimerStep] = []

        for exercise in WARMUP.exercises:
            steps.append(TimerStep('Warm-up', exercise))

        for round_number in range(1, self.workout.rounds + 1):
            for exercise in self.workout.exercises:
                steps.append(
                    TimerStep(
                        f'{self.workout.name} — Round {round_number}/{self.workout.rounds}',
                        exercise,
                    )
                )

        for exercise in COOLDOWN.exercises:
            steps.append(TimerStep('Cooldown', exercise))

        return steps

    def toggle_timer(self, _button: Button) -> None:
        if self.running:
            self.running = False
            self.start_pause_button.text = 'Resume'
            return

        self.running = True
        self.start_pause_button.text = 'Pause'

        if self.clock_event is None:
            self.clock_event = Clock.schedule_interval(self._tick, 1.0)

    def skip_step(self, _button: Button) -> None:
        self._advance_step()

    def reset_workout(self, _button: Button) -> None:
        self.running = False
        self.step_index = 0
        self.remaining_seconds = self.steps[0].exercise.duration_seconds
        self.start_pause_button.text = 'Start'
        self._render_current_step()

    def _tick(self, _dt: float) -> None:
        if not self.running:
            return

        self.remaining_seconds -= 1

        if self.remaining_seconds <= 0:
            self._advance_step()
            return

        self.timer_label.text = self._format_time(self.remaining_seconds)

    def _advance_step(self) -> None:
        self.step_index += 1

        if self.step_index >= len(self.steps):
            self.running = False
            self.exercise_label.text = 'Workout complete. Nice work.'
            self.notes_label.text = ''
            self.timer_label.text = '00:00'
            self.start_pause_button.text = 'Start'
            return

        self.remaining_seconds = self.steps[self.step_index].exercise.duration_seconds
        self._render_current_step()

    def _render_current_step(self) -> None:
        step = self.steps[self.step_index]
        self.exercise_label.text = f'{step.label}\n{step.exercise.name}'
        self.notes_label.text = step.exercise.notes
        self.timer_label.text = self._format_time(self.remaining_seconds)

    @staticmethod
    def _format_time(seconds: int) -> str:
        minutes, remainder = divmod(seconds, 60)
        return f'{minutes:02d}:{remainder:02d}'
