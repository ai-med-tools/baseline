from __future__ import annotations

from typing import Union

from baseline.epicrisis.epicrisis import Epicrisis
from baseline.solution.implementation.solution_abstract import SolutionAbstract
from baseline.solution.solution_factory import SolutionFactory
from baseline.tools.singleton import MetaSingleton


class Marker:
    _solution: SolutionAbstract

    def __init__(self, epicrisis: Epicrisis):
        self._solution = SolutionFactory(epicrisis).get()

    async def markup_async(self, timeoutFile: int) -> list[dict[str, Union[int, str]]]:
        return await self._solution.execute_async(timeoutFile)

    def markup(self, timeoutFile: int) -> list[dict[str, Union[int, str]]]:
        return self._solution.execute(timeoutFile)
