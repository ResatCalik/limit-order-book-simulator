
`docs/architecture.md`

```md
# Architecture Notes

## 1. Project intention

This project is a software engineering exercise built around a matching engine domain.

It is not being built to become a real trading platform.
It is being built to practice:

- deterministic business logic
- stateful backend design
- event-oriented thinking
- algorithmic modeling
- gradual refactoring
- test-driven development habits

The financial domain is used as a realistic system-design context.

## 2. High-level design direction

The architecture will evolve from a simple order container into a structured matching engine.

The target design is:

- `Order`
- `Trade`
- `PriceLevel`
- `OrderBookSide`
- `OrderBook`
- `MatchingEngine`

## 3. Planned domain model

### Order

Represents an order submitted to the system.

Planned fields:

- `order_id`
- `side`
- `price`
- `initial_quantity`
- `remaining_quantity`
- `timestamp`
- `status`

Responsibilities:

- hold order data
- validate order values
- track lifecycle state

### Trade

Represents an execution created by matching compatible buy and sell orders.

Planned fields:

- `trade_id`
- `buy_order_id`
- `sell_order_id`
- `price`
- `quantity`
- `timestamp`

Responsibilities:

- record execution details
- provide output for logs, replay, and analytics

### PriceLevel

Represents a single price level.

Responsibilities:

- hold all orders at one price
- preserve FIFO order within that level
- allow add/remove operations on that queue

### OrderBookSide

Represents one side of the book.

There will be:
- one bid side
- one ask side

Responsibilities:

- manage price levels
- provide best price on that side
- add/remove price levels when empty

### OrderBook

Represents the full book.

Responsibilities:

- contain both bid and ask sides
- expose best bid and best ask
- expose current visible state of the book

### MatchingEngine

Represents the application core.

Responsibilities:

- receive new orders
- decide whether they cross the opposite side
- generate trades
- handle partial fills
- insert remaining quantity back into the book
- cancel existing orders
- modify orders using a cancel-plus-add flow

## 4. Processing model

Initial processing model:

- single process
- single-threaded
- deterministic
- test-first where practical

This is intentional.

The project should first prove:
- correctness
- clarity
- maintainability

Only after that should it explore:
- throughput
- concurrency
- queue-based ingestion
- more advanced data structures

## 5. Matching rules for the core version

The first meaningful version of the engine should follow these rules:

### Buy order behavior
A buy order matches when its price is greater than or equal to the current best ask.

### Sell order behavior
A sell order matches when its price is less than or equal to the current best bid.

### Price priority
Better prices must be matched first.

### Time priority
Within the same price level, older orders must be matched first.

### Partial fill
If one side has a smaller remaining quantity, that quantity is traded and the other order remains partially open.

### Cancel
An existing live order can be removed from the book.

### Modify
Modify will be modeled as:

1. cancel the existing active order
2. create a new replacement order

This keeps the logic simpler and easier to test.

## 6. Data structure direction

The project will start with simple and understandable runtime structures.

Initial likely approach:

- order lookup by id using a dictionary
- separate storage for bids and asks
- explicit price levels
- cached or quickly accessible best bid / best ask

The project is intentionally **not** starting with:
- AVL trees
- custom pointer-heavy structures
- advanced lock-free or queue-based concurrency
- compile-time techniques

Those ideas are valuable, but they belong to later phases.

## 7. Testing strategy

Testing is a first-class part of the project.

The system should be covered by:

- unit tests for model validation
- unit tests for book ordering
- unit tests for best bid / best ask
- scenario tests for matching
- scenario tests for partial fill
- scenario tests for cancel and modify
- replay-style tests later on

Important principle:
Every new matching rule should come with tests.

## 8. CI strategy

The repository already uses GitHub Actions.

CI responsibilities:

- install dependencies
- run unit tests
- prevent silent regressions

Later CI may also include:

- linting
- formatting checks
- coverage reporting

## 9. Phase roadmap

### Phase 0 — Bootstrap
Completed or mostly completed:
- repository setup
- virtual environment
- base models
- tests
- CI

### Phase 1 — Core engine correctness
Next target:
- add `Trade`
- add `PriceLevel`
- introduce `MatchingEngine`
- implement first real match flow
- implement partial fill
- implement cancel
- implement modify

### Phase 2 — Internal structure improvements
- add order lookup by id
- introduce order statuses
- add event log
- add replay support

### Phase 3 — Simulator features
- market orders
- multi-symbol support
- market data event generation
- snapshot and incremental output

### Phase 4 — Engineering depth
- benchmark scripts
- synthetic order flow
- concurrency experiments
- latency and throughput measurements

## 10. Guiding principle

This project should grow like a real engineering system:

- start small
- keep it correct
- refactor when needed
- test every rule
- optimize only after correctness