// features/playerSlice.js
import { createSlice } from '@reduxjs/toolkit';
const directions = ["UP", "DOWN", "LEFT", "RIGHT"];

export const playerSlice = createSlice({
  name: 'player',
  initialState: {
    position: Math.floor(Math.random() * 46),
    direction: directions[Math.floor(Math.random() * directions.length)],
  },
  reducers: {
    movePlayer: (state, action) => {
      // Implement the logic to update the player's position
      state.position = action.payload;
    },
    setDirection: (state, action) => {
      state.direction = action.payload;
    },
    
  },
});

// Export the actions
export const { movePlayer, setDirection } = playerSlice.actions;

// Export the reducer
export default playerSlice.reducer;
