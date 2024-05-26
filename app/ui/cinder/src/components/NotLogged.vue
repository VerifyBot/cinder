<template>
  <v-container>
    <v-responsive class="text-center fill-height">

      <!-- title -->

      <v-row class="d-flex align-center justify-center pt-10 mt-10">
        <div class="text-h1 title" style="font-family: 'Lemon', sans-serif !important;">
          cinder ‎
        </div>
      </v-row>
      <v-row class="d-flex align-center justify-center">
        <div class="text-h5 text-primary-darken-1"
          style="font-family: 'Bree Serif', sans-serif !important; user-select: none;">
          <i>where love starts.</i>
        </div>
      </v-row>

      <div class="py-15"></div>

      <!-- <v-row class="d-flex align-center justify-center mb-5 flex-column">
        <div><v-btn color="pink" block variant="outline" @click="sendTest">test</v-btn></div>
        <div><u>Result</u>: <b>{{ testResult }}</b></div>
      </v-row> -->

      <!-- log in -->
      <v-row class="d-flex align-center justify-center">
        <v-btn prepend-icon="mdi-key-chain" style="width: 400px;font-family: 'Bree Serif'" variant="tonal" size="x-large" color="green"
          @click="$router.push('/login')">
          Log In
        </v-btn>
      </v-row>

      <div class="py-10"></div>

      <!-- sign up -->
      <v-row class="d-flex align-center justify-center">
        <v-btn prepend-icon="mdi-account-question" style="width: 400px; font-family: 'Bree Serif'" variant="tonal" size="x-large" color="blue"
          @click="$router.push('/signup')">
          Sign Up
        </v-btn>
      </v-row>

      <div class="py-10" v-if="TICTACTOE"></div>
      <v-row class="d-flex align-center justify-center">
        <canvas ref="boardCanvas" style="border-radius: 10px" @click="handleCanvasClick"></canvas>

      </v-row>
    </v-responsive>


  </v-container>
</template>

<script>
export default {
  data() {
    return {
      testResult: null,
      canvas: null,
      ctx: null,
      currentPlayer: 'O',
      board: [['', '', ''], ['', '', ''], ['', '', '']],
      gameOver: false,
      userInteractionEnabled: true, // Controls whether user interactions are enabled

      TICTACTOE: false
    };
  },
  mounted() {
    if (this.TICTACTOE) {
      this.canvas = this.$refs.boardCanvas;
      this.canvas.width = this.canvas.height = 150; // Set canvas width to 300px for a 3x3 grid
      this.ctx = this.canvas.getContext('2d');
      this.drawBoard();
    }

  },
  methods: {
    async sendTest() {
      const js = await this.api.post('/reverse', { text: window.prompt("what?")});
      this.testResult = js.data.reversed;
    },

    drawBoard() {
      // Draw the game board with rounded lines
      this.ctx.fillStyle = '#1f222e';
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
      this.ctx.strokeStyle = '#0da192';
      this.ctx.lineWidth = this.canvas.width / 30;

      for (let i = 1; i < 3; i++) {
        // Vertical lines
        this.ctx.beginPath();
        this.ctx.moveTo(i * (this.canvas.width / 3), 0);
        this.ctx.lineTo(i * (this.canvas.width / 3), this.canvas.height);
        this.ctx.stroke();

        // Horizontal lines
        this.ctx.beginPath();
        this.ctx.moveTo(0, i * (this.canvas.height / 3));
        this.ctx.lineTo(this.canvas.width, i * (this.canvas.height / 3));
        this.ctx.stroke();
      }

      // Draw X and O symbols
      for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
          const symbol = this.board[row][col];
          if (symbol === 'O' || symbol === 'X') {
            this.drawSymbol(symbol, col, row);
          }
        }
      }
    },
    drawSymbol(symbol, x, y) {
      // Set the font size and color
      this.ctx.font = '50px sans-serif';
      this.ctx.fillStyle = symbol === 'O' ? '#27ae60' : '#b71540';

      // Calculate the center of the square
      const squareCenterX = x * (this.canvas.width / 3) + (this.canvas.width / 6);
      const squareCenterY = y * (this.canvas.height / 3) + (this.canvas.height / 6);

      // Measure the text metrics
      const textMetrics = this.ctx.measureText(symbol);

      // Calculate the position to center the text
      const textX = squareCenterX - (textMetrics.width / 2);
      const textY = squareCenterY + (textMetrics.actualBoundingBoxAscent / 2);

      // Draw the text at the calculated position
      this.ctx.fillText(symbol, textX, textY);
    },

    drawWinner(who) {
      this.ctx.font = '90px Arial';
      this.ctx.fillStyle = 'blue';

      console.log('draw winner called on', who)

      let emoji;
      if (who === 'X') emoji = '😈';
      else if (who === 'O') emoji = '🏅';
      else emoji = '😴';

      const textWidth = this.ctx.measureText(emoji).width;
      const textHeight = parseInt(this.ctx.font);

      const x = (this.canvas.width - textWidth) / 2;
      const y = (this.canvas.height + textHeight) / 2;

      this.ctx.fillText(emoji, x, y);

    },

    handleCanvasClick(event) {
      if (this.gameOver) {
        this.resetGame();
        return;
      }
      if (!this.userInteractionEnabled)
        return;

      const rect = this.canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      const row = Math.floor((y / this.canvas.height) * 3);
      const col = Math.floor((x / this.canvas.width) * 3);

      if (this.board[row][col] === '') {
        this.board[row][col] = 'O';
        this.drawBoard();
        this.disableUserInteraction(); // Disable user interaction during the computer's move

        if (!this.checkWinner('O')) {
          setTimeout(() => {
            this.computerMove();
            this.drawBoard();
            if (this.checkWinner('X')) {
              this.enableUserInteraction();
              this.drawWinner('X');
              this.gameOver = true;
            }
            this.enableUserInteraction(); // Enable user interaction after the computer's move
          }, 500); // Delay the computer's move by 1 second (adjust as needed)
        }
      }
    },
    computerMove() {
      // Implement logic for the computer's move (random placement of 'X')
      const emptyCells = [];
      for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
          if (this.board[row][col] === '') {
            emptyCells.push({ row, col });
          }
        }
      }

      if (emptyCells.length > 0) {
        const randomIndex = Math.floor(Math.random() * emptyCells.length);
        const { row, col } = emptyCells[randomIndex];
        this.board[row][col] = 'X';
      }
    },
    checkWinner(player) {
      // Implement logic to check for a winner using a smart modulo calculation
      const winningCombos = [
        [[0, 0], [0, 1], [0, 2]],
        [[1, 0], [1, 1], [1, 2]],
        [[2, 0], [2, 1], [2, 2]],
        [[0, 0], [1, 0], [2, 0]],
        [[0, 1], [1, 1], [2, 1]],
        [[0, 2], [1, 2], [2, 2]],
        [[0, 0], [1, 1], [2, 2]],
        [[0, 2], [1, 1], [2, 0]],
      ];

      for (const combo of winningCombos) {
        const [a, b, c] = combo;
        if (
          this.board[a[0]][a[1]] === player &&
          this.board[b[0]][b[1]] === player &&
          this.board[c[0]][c[1]] === player
        ) {
          this.enableUserInteraction();

          if (player === 'O')
            this.drawWinner('O')
          else
            this.drawWinner('X')

          this.gameOver = true;
          return true;
        }
      }

      // Check for a tie (no more empty cells)
      if (!this.board.flat().includes('')) {
        this.drawWinner('Tie')
        this.gameOver = true;
      }

      return false;
    },
    resetGame() {
      this.currentPlayer = 'O';
      this.board = [['', '', ''], ['', '', ''], ['', '', '']];
      this.gameOver = false;
      this.drawBoard();
    },
    disableUserInteraction() {
      this.userInteractionEnabled = false;
    },

    enableUserInteraction() {
      this.userInteractionEnabled = true;
    },
  }
};
</script>




<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Permanent+Marker&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Bree+Serif&family=Lemon&display=swap');

.title {
  font-family: "Permanent Marker";
}

.title {
  font-weight: bold;
  background: -webkit-linear-gradient(#ed3c6e, #FFBD33);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  user-select: none;
}

/*  on mobile */
@media (max-width: 600px) {
  .title {
    font-size: 16vw !important;
  }
}

.section-title {
  color: #FF5733;
  font-weight: bold;
  
}

/* bofbody * {
  overflow: hidden !important; */
</style>