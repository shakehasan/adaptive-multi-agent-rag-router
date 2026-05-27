"""Supervisor agent orchestrating the worker graph."""

from __future__ import annotations

from amarr.core.errors import AmarrError
from amarr.routing.router import Router

from .base import BaseAgent
from .coder import CodingAgent
from .critic import CriticAgent
from .fallback import FallbackAgent
from .planner import PlannerAgent
from .researcher import ResearchAgent
from .retriever import RetrievalAgent
from .state import TaskState
from .synthesizer import SynthesisAgent
from .verifier import VerificationAgent


class SupervisorAgent(BaseAgent):
    """Coordinate planning, retrieval, critique, verification, and synthesis."""

    def __init__(self, router: Router, retrieval_agent: RetrievalAgent) -> None:
        super().__init__("supervisor")
        self.router = router
        self.planner = PlannerAgent()
        self.retrieval = retrieval_agent
        self.researcher = ResearchAgent()
        self.coder = CodingAgent()
        self.critic = CriticAgent()
        self.verifier = VerificationAgent()
        self.synthesizer = SynthesisAgent()
        self.fallback = FallbackAgent()

    def run(self, state: TaskState) -> TaskState:
        """Run the full workflow with failure recovery."""
        try:
            state.route = self.router.route(state.query)
            state.add_message(self.name, "router", "route", state.route.reason)
            for agent in [self.planner, self.retrieval, self.researcher, self.coder, self.critic, self.verifier, self.synthesizer]:
                state = agent.run(state)
            self.router.record_success(state.route.selected_alias)
            return state
        except AmarrError as exc:
            if state.route is not None:
                self.router.record_failure(state.route.selected_alias)
            state.warnings.append(str(exc))
            return self.fallback.run(state)
