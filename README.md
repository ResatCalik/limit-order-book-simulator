# Limit Order Book Simulator

An educational, test-driven project for learning stateful backend design through a matching engine simulation.

## Why this project exists

I want to improve myself in backend engineering by building a system that requires:

- clear domain modeling
- deterministic state transitions
- algorithmic thinking
- reliable testing
- real-time system mindset

The financial domain here is mainly used as a problem space.  
The main goal of this project is not quantitative trading.  
The main goal is to learn software engineering by designing a small but realistic order-processing system.

## Project goal

This project aims to simulate the core behavior of a limit order book and a matching engine.

The system will gradually evolve to support:

- buy and sell limit orders
- price-time priority
- partial fills
- order cancel and modify flows
- best bid / best ask tracking
- trade generation
- event logging and replay
- later, benchmarking and concurrency experiments

## Current state

The current version already includes:

- project structure
- Python virtual environment setup
- unit tests
- CI with GitHub Actions
- basic `Order` model
- basic `OrderBook`
- best bid / best ask lookup

This is the bootstrap version of the project.  
The next steps will focus on moving from a simple order container to a real matching engine.

## Planned architecture

The system is being designed around the following core components:

- `Order`
- `Trade`
- `PriceLevel`
- `OrderBookSide`
- `OrderBook`
- `MatchingEngine`

### Component responsibilities

**Order**  
Represents an incoming order with fields such as side, price, quantity, remaining quantity, timestamp, and status.

**Trade**  
Represents an executed match between a buy order and a sell order.

**PriceLevel**  
Groups all orders at the same price and preserves FIFO ordering within that price level.

**OrderBookSide**  
Manages one side of the book, either bids or asks.

**OrderBook**  
Contains both sides of the book and provides book-level queries such as best bid and best ask.

**MatchingEngine**  
Implements matching rules, partial fills, cancel logic, modify flow, and trade creation.

## Development philosophy

This project will be developed in phases.

### Phase 0 — Bootstrap
- repository setup
- tests
- CI
- initial models
- basic order storage

### Phase 1 — Core correctness
- `Trade` model
- `PriceLevel`
- matching logic
- partial fill
- cancel order
- modify order
- stronger unit tests

### Phase 2 — Better internal design
- order lookup by id
- explicit order status
- event log
- replay support
- more scenario-based tests

### Phase 3 — Simulator behavior
- market orders
- multi-symbol support
- market data events
- snapshot and incremental updates
- benchmark scripts

### Phase 4 — Systems engineering extensions
- concurrency experiments
- queue-based ingestion
- throughput and latency measurements
- synthetic order flow generation

## Technical focus areas

This project is mainly about learning and demonstrating:

- backend engineering
- clean architecture
- stateful systems
- algorithmic problem solving
- testing discipline
- CI workflow
- system evolution through refactoring

## Out of scope

At least for now, this project does **not** aim to provide:

- real brokerage integration
- real market connectivity
- investment advice
- production-grade trading infrastructure
- high-frequency trading performance claims

## How to run

After activating the virtual environment:

```bash
python -m pytest
python -m src.main