# Distributed Matching Engine

A distributed matching engine implementation using gRPC for communication between components. The system consists of multiple matching engines that can process orders and synchronize order books across nodes.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── main.py
├── common/
│   ├── __init__.py
│   ├── order.py
│   └── orderbook.py
├── engine/
│   ├── __init__.py
│   ├── match_engine.py
│   ├── exchange.py
│   └── synchronizer.py
├── network/
│   ├── __init__.py
│   └── grpc_server.py
├── client/
│   ├── __init__.py
│   ├── client.py
│   └── custom_formatter.py
├── proto/
│   ├── __init__.py
│   ├── matching_service.proto
│   ├── matching_service_pb2.py
│   ├── matching_service_pb2_grpc.py
│   └── matching_service_pb2.pyi
└── simulation/
    ├── __init__.py
    ├── simulation.py
    ├── exchange_start.py
    ├── client_start.py
    └── test.py
```

## Setup

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate protocol buffer code (if modifying proto files):
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/matching_service.proto
```


## Architecture

The system has the following main components:

- **Exchange**: Central coordinator that manages client registration and matching engine assignment
- **Matching Engines**: Multiple matching engine nodes that process orders and maintain order books
- **Synchronizer**: Component that handles order book synchronization between matching engines
- **Clients**: Trading clients that can submit orders and receive fills

### Key Components

- `engine/match_engine.py`: Core matching engine implementation
- `engine/exchange.py`: Exchange layer for client management
- `engine/synchronizer.py`: Order book synchronization between engines
- `common/orderbook.py`: Order book implementation with price-time priority
- `network/grpc_server.py`: gRPC server implementations
- `client/client.py`: Trading client implementation
- `proto/matching_service.proto`: Protocol buffer definitions

## Features

- Multiple matching engine nodes running simultaneously
- Order book synchronization between engines
- Client registration and authentication
- Order routing based on best prices
- Fill notifications and position tracking
- Price-time priority matching algorithm
- Support for multiple trading symbols

## Running the System

The system needs to be run in two separate terminal windows/processes:

### Terminal 1 - Start Exchange and Matching Engines:
```bash
# Start the exchange and matching engines
python simulation/exchange_start.py
```

### Terminal 2 - Start Clients:
```bash
# Start the clients
python simulation/client_start.py
```

The simulation will run for a default duration of 10 seconds, during which clients will submit random orders and receive fills.

### Expected Output
- Terminal 1 will show logs from the exchange and matching engines, including:
  - Server startup messages
  - Order book updates
  - Routing decisions
  
- Terminal 2 will show client activity, including:
  - Client registration
  - Order submissions
  - Fill notifications
  - Final positions

### Monitoring
- Check the `logs/` directory for detailed logs from each component:
  - `logs/engine_logs/`: Matching engine logs
  - `logs/exchange_logs/`: Exchange logs
  - `logs/client_logs/`: Client logs
  - `logs/synchronizer_logs/`: Synchronization logs

## Configuration

Key configuration parameters:

- `NUM_ENGINES`: Number of matching engine nodes (default: 2)
- `PASSWORD`: Authentication key for clients (default: "password")
- `IP_ADDR`: Network address for services (default: "127.0.0.1")
- Base ports:
  - Exchange: 50050
  - Matching Engines: 50051+

## Protocol

The system uses gRPC for communication with the following main service calls:

- `SubmitOrder`: Submit a new order
- `CancelOrder`: Cancel an existing order
- `GetFills`: Stream of fill notifications
- `RegisterClient`: Client registration
- `BroadcastOrderbook`: Synchronize order book updates
- `SyncOrderBook`: Get current order book state

## Logging

The system includes comprehensive logging with different log files for:

- Exchange
- Matching Engines
- Clients
- Synchronizers

Logs are stored in the `logs/` directory with subdirectories for each component type.

## Testing

Run simulations using:
```bash
python simulation/simulation.py
```

The simulation supports configurable parameters for:
- Number of matching engines
- Number of clients
- Trading symbols
- Order frequency
- Simulation duration


