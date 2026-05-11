---
tags:
  - resource
  - terminology
  - systems_thinking
  - system_dynamics
keywords:
  - stocks and flows
  - stock and flow
  - accumulation
  - rate of change
  - system dynamics
  - Jay Forrester
  - Donella Meadows
  - levels and rates
  - inertia
  - buffering
  - delays
topics:
  - systems thinking
  - system dynamics
  - modeling and simulation
language: markdown
date of note: 2026-03-13
status: active
building_block: concept
---

# Term: Stocks and Flows

## Definition

**Stocks and flows** are the fundamental building blocks of system dynamics models. A **stock** is an accumulation -- a quantity that can be measured at a single point in time (e.g., water in a bathtub, money in a bank account, cases in a backlog, carbon dioxide in the atmosphere). A **flow** is the rate of change of a stock over time -- the movement that adds to (inflow) or subtracts from (outflow) the accumulated quantity (e.g., water entering through the faucet, revenue per month, cases resolved per week).

The mathematical relationship is precise: a stock at any time equals its initial value plus the integral of all inflows minus all outflows up to that moment. Conversely, a flow is the derivative of its associated stock. Jay Forrester, who founded system dynamics at MIT in the 1950s, originally called stocks **"levels"** and flows **"rates"** in his landmark *Industrial Dynamics* (1961). Donella Meadows later popularized the "stocks and flows" terminology in *Thinking in Systems: A Primer* (2008), offering a practical heuristic: **stocks are what you would still see if the system stopped**; flows are what would vanish.

## Key Properties

- **Accumulation creates memory**: Stocks remember the history of all past flows. Today's population reflects decades of births and deaths; today's backlog reflects the cumulative imbalance between case arrivals and resolutions.
- **Inertia and resistance to change**: Because stocks change only through their flows, they cannot be altered instantaneously. A workforce cannot double overnight; trust cannot be rebuilt in a day. This inertia is why systems resist rapid intervention.
- **Buffering and shock absorption**: Stocks decouple the timing of inflows from outflows, absorbing fluctuations. Inventory buffers production variability from demand variability; savings buffer income shocks from spending needs.
- **Delays**: The process of accumulation introduces time lags between a change in flow and its full effect on the stock, creating the oscillation, overshoot, and undershoot characteristic of dynamic systems.
- **Flows are the only drivers of change**: No stock changes without a flow. If you want to change a stock, you must identify and alter the flows -- a simple but frequently violated principle in policy design.
- **Stock-flow distinction maps to units**: Stocks have units of quantity (people, dollars, cases). Flows have units of quantity per time (people/year, dollars/month, cases/week). If the units do not include "per time," it is a stock.

## Related Terms

- **[Systems Thinking](term_systems_thinking.md)**: The broader analytical framework within which stocks and flows operate; stocks and flows are the quantitative backbone of systems thinking
- **[Habit Loop](term_habit_loop.md)**: Habits can be modeled as stocks (accumulated behavior patterns) maintained by reinforcing flows (cue-routine-reward cycles)
- **[Compound Effect](term_compound_effect.md)**: Compounding is a reinforcing flow into a stock; the compound effect is stock accumulation made visible over time
- **[Open Loops](term_open_loops.md)**: Open loops accumulate as a cognitive stock; the capture-clarify-organize process is an outflow that drains the stock

## References

### Vault Sources
- [Digest: Thinking in Systems](../digest/digest_thinking_in_systems_meadows.md) -- Meadows' primer; the primary source for stocks-and-flows thinking applied to real systems

### External Sources
- [Forrester, J.W. (1961). *Industrial Dynamics*. MIT Press](https://mitpress.mit.edu/9780262560115/industrial-dynamics/) -- the foundational text that introduced levels (stocks) and rates (flows)
- [Meadows, D.H. (2008). *Thinking in Systems: A Primer*. Chelsea Green Publishing](https://www.chelseagreen.com/product/thinking-in-systems/) -- the most accessible treatment of stocks and flows
- [The Systems Thinker: Step-By-Step Stocks and Flows](https://thesystemsthinker.com/step-by-step-stocks-and-flows-improving-the-rigor-of-your-thinking/) -- practical guide to identifying stocks and flows in real systems
- [MIT OCW: Introduction to System Dynamics (15.871)](https://ocw.mit.edu/courses/15-871-introduction-to-system-dynamics-fall-2013/) -- Forrester's home department course materials
- [Integration and Implementation Insights: Four Core System Dynamics Concepts](https://i2insights.org/2025/09/16/four-core-system-dynamics-concepts/) -- stocks, flows, feedback, and delays as the four pillars

---

**Last Updated**: March 13, 2026
**Status**: Active -- systems thinking and system dynamics terminology
