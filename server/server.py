import asyncio
import websockets
import json

class Piece:
    def __init__(self, x, y, player, piece_id):
        self.x = x
        self.y = y
        self.player = player
        self.piece_id = piece_id

    def move(self, direction):
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1
        elif direction == 'fl':
            self.x -= 1
            self.y -= 1
        elif direction == 'fr':
            self.x += 1
            self.y -= 1
        elif direction == 'bl':
            self.x -= 1
            self.y += 1
        elif direction == 'br':
            self.x += 1
            self.y += 1

    def __str__(self):
        return 'P' if self.player == 1 else 'p'

class Hero1(Piece):
    def __str__(self):
        return 'H1' if self.player == 1 else 'h1'

    def move(self, direction):
        if direction == 'up':
            self.y -= 2
        elif direction == 'down':
            self.y += 2
        elif direction == 'left':
            self.x -= 2
        elif direction == 'right':
            self.x += 2
        elif direction == 'fl':
            self.x -= 2
            self.y -= 2
        elif direction == 'fr':
            self.x += 2
            self.y -= 2
        elif direction == 'bl':
            self.x -= 2
            self.y += 2
        elif direction == 'br':
            self.x += 2
            self.y += 2

class Hero2(Piece):
    def __str__(self):
        return 'H2' if self.player == 1 else 'h2'

    def move(self, direction):
        if direction == 'fl':
            self.x -= 2
            self.y -= 2
        elif direction == 'fr':
            self.x += 2
            self.y -= 2
        elif direction == 'bl':
            self.x -= 2
            self.y += 2
        elif direction == 'br':
            self.x += 2
            self.y += 2

class Pawn(Piece):
    def __str__(self):
        return 'P' if self.player == 1 else 'p'

class Game:
    def __init__(self):
        self.board = [[None]*5 for _ in range(5)]
        self.pieces = {}
        self.current_player = 1

    def add_piece(self, piece):
        self.pieces[piece.piece_id] = piece
        self.board[piece.y][piece.x] = piece

    def get_valid_moves(self, piece_id):
        piece = self.pieces.get(piece_id)
        if not piece or piece.player != self.current_player:
            return []

        directions = []
        if isinstance(piece, Pawn):
            directions = ['up', 'down', 'left', 'right', 'fl', 'fr', 'bl', 'br']
        elif isinstance(piece, Hero1):
            directions = ['up', 'down', 'left', 'right']
        elif isinstance(piece, Hero2):
            directions = ['fl', 'fr', 'bl', 'br']

        valid_moves = []

        for direction in directions:
            x, y = piece.x, piece.y
            if direction == 'up':
                y -= 1
            elif direction == 'down':
                y += 1
            elif direction == 'left':
                x -= 1
            elif direction == 'right':
                x += 1
            elif direction == 'fl':
                x -= 1
                y -= 1
            elif direction == 'fr':
                x += 1
                y -= 1
            elif direction == 'bl':
                x -= 1
                y += 1
            elif direction == 'br':
                x += 1
                y += 1

            if 0 <= x < 5 and 0 <= y < 5:
                target_piece = self.board[y][x]
                if target_piece is None or target_piece.player != piece.player:
                    valid_moves.append(direction)

                if isinstance(piece, Hero1) or isinstance(piece, Hero2):
                    # Check for multiple steps if Hero1 or Hero2
                    if direction in ['up', 'down', 'left', 'right']:
                        for step in range(1, 2):
                            x_temp, y_temp = piece.x, piece.y
                            if direction == 'up':
                                y_temp -= step
                            elif direction == 'down':
                                y_temp += step
                            elif direction == 'left':
                                x_temp -= step
                            elif direction == 'right':
                                x_temp += step

                            if 0 <= x_temp < 5 and 0 <= y_temp < 5:
                                target_piece_temp = self.board[y_temp][x_temp]
                                if target_piece_temp is not None:
                                    if target_piece_temp.player != piece.player:
                                        valid_moves.append(direction)
                                        break
                                    else:
                                        break
                    elif direction in ['fl', 'fr', 'bl', 'br']:
                        for step in range(1, 2):
                            x_temp, y_temp = piece.x, piece.y
                            if direction == 'fl':
                                x_temp -= step
                                y_temp -= step
                            elif direction == 'fr':
                                x_temp += step
                                y_temp -= step
                            elif direction == 'bl':
                                x_temp -= step
                                y_temp += step
                            elif direction == 'br':
                                x_temp += step
                                y_temp += step

                            if 0 <= x_temp < 5 and 0 <= y_temp < 5:
                                target_piece_temp = self.board[y_temp][x_temp]
                                if target_piece_temp is not None:
                                    if target_piece_temp.player != piece.player:
                                        valid_moves.append(direction)
                                        break
                                    else:
                                        break

        return valid_moves

    def move_piece(self, piece_id, direction):
        piece = self.pieces.get(piece_id)
        if not piece or piece.player != self.current_player:
            return  # Invalid move

        # Save the piece's previous position
        prev_x, prev_y = piece.x, piece.y
        piece.move(direction)

        # Check if the move is within board bounds
        if 0 <= piece.x < 5 and 0 <= piece.y < 5:
            target_piece = self.board[piece.y][piece.x]

            # Capture the opponent's piece if present
            if target_piece and target_piece.player != piece.player:
                del self.pieces[target_piece.piece_id]

            # Update the board
            self.board[prev_y][prev_x] = None
            self.board[piece.y][piece.x] = piece
            self.current_player = 2 if self.current_player == 1 else 1

            # Check for win condition
            if not any(piece.player == self.current_player for piece in self.pieces.values()):
                return f'Player {self.current_player} wins!'
        else:
            # Move was out of bounds, revert the change
            piece.x, piece.y = prev_x, prev_y

    def get_board_state(self):
        return [[str(cell) if cell else '-' for cell in row] for row in self.board]

async def handle_connection(websocket, path):
    game = Game()
    piece_id = 0

    # Add pieces for both players
    for i in range(5):
        game.add_piece(Pawn(i, 0, 1, piece_id))
        piece_id += 1
        game.add_piece(Pawn(i, 4, 2, piece_id))
        piece_id += 1
    game.add_piece(Hero1(2, 0, 1, piece_id))
    piece_id += 1
    game.add_piece(Hero2(1, 0, 1, piece_id))
    piece_id += 1
    game.add_piece(Hero1(2, 4, 2, piece_id))
    piece_id += 1
    game.add_piece(Hero2(1, 4, 2, piece_id))
    
    selected_piece = None

    try:
        while True:
            if selected_piece is not None:
                valid_moves = game.get_valid_moves(selected_piece)
                await websocket.send(json.dumps({
                    'type': 'valid_moves',
                    'valid_moves': valid_moves,
                    'selected_piece': selected_piece
                }))
            
            await websocket.send(json.dumps({'type': 'board_state', 'board': game.get_board_state(), 'current_player': game.current_player}))

            message = await websocket.recv()
            
            if message.startswith('select'):
                _, x, y = message.split()
                x, y = int(x), int(y)
                selected_piece = None
                
                # Find the piece at the specified position
                for piece in game.pieces.values():
                    if piece.x == x and piece.y == y and piece.player == game.current_player:
                        selected_piece = piece.piece_id
                        break
            
            elif message.startswith('move'):
                _, direction = message.split()
                result = game.move_piece(selected_piece, direction)
                if result:
                    await websocket.send(json.dumps({'type': 'win', 'message': result}))
                    break
                selected_piece = None

            elif message == 'disconnect':
                break

    except websockets.ConnectionClosed:
        print("Connection closed")

    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    start_server = websockets.serve(handle_connection, 'localhost', 8765)
    await start_server
    await asyncio.Future()  # run forever

asyncio.run(main())