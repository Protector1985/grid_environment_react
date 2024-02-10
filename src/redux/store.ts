
import { configureStore } from '@reduxjs/toolkit';
import playerSlice from './slices/playerSlice';
import canvasSlice from './slices/canvasSlice';



export const store = configureStore({
  reducer: {
    playerSlice: playerSlice,
    canvasSlice: canvasSlice
  },
});