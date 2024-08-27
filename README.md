# 5x5 Chess Game

## Overview

This repository contains a simple 5x5 chess-like game that can be played between two players. The game is implemented using Python and WebSockets for the server-side, and HTML/JavaScript for the client-side.

## Features

- A 5x5 board with different types of pieces.
- Two types of heroes with special movement capabilities.
- Basic movement and capture mechanics.
- WebSocket communication for real-time game updates.

## Setup

### Prerequisites

- Python 3.7 or later
- `websockets` library for Python

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Simran-Namdev/SimranNamdev21BAI10472
   ```

2. **Install Python Dependencies**

   Make sure you have `websockets` installed. If not, you can install it using pip:

   ```bash
   pip install websockets
   ```

3. **Run the Server**

   Start the WebSocket server by running:

   ```bash
   python server.py
   ```

   This will start the server on `ws://localhost:8765`.

4. **Open the Client**

   Open `index.html` in a web browser to start playing the game. Ensure your browser supports WebSockets.

## How to Play

1. **Start the Game**

   - Open `index.html` in your browser.
   - The game board will be displayed, and the current player's turn will be shown.

2. **Select a Piece**

   - Click on a piece on the board that belongs to you (player 1 or player 2). The valid move options will be highlighted.

3. **Move the Piece**

   - Click on the movement buttons to move the selected piece in the desired direction.
   - The valid moves will be highlighted, and you can only move to a valid position.

4. **Winning the Game**

   - The game will end when one player has no pieces left on the board. An alert will notify the winner.

5. **Disconnect**

   - You can close the browser tab to disconnect from the game.

## WebSocket Communication

- **Message Format**
  - `select x y`: Selects the piece at position `(x, y)`.
  - `move direction`: Moves the selected piece in the specified direction.
  - `disconnect`: Closes the connection.

- **Server Responses**
  - `board_state`: Sends the current state of the board and the current player's turn.
  - `valid_moves`: Sends the valid moves for the selected piece.
  - `win`: Sends a message when a player wins the game.
