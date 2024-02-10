// features/playerSlice.js
import { createSlice } from '@reduxjs/toolkit';
import { FLOAT } from 'html2canvas/dist/types/css/property-descriptors/float';


const directions = ["UP", "DOWN", "LEFT", "RIGHT"];

export const canvasSlice = createSlice({
  name: 'canvas',
  initialState: {
    expensive: [] as number[], // Explicitly declare the type of the array
    cheap: [] as number[],
    goal:null as number | null,
    badGoal: null as number | null,
    totalRewards:0 as FLOAT,
    actionReward: 0 as FLOAT,
    level: 1,
    movementPoints: 1.00,
    bordSize: 45,
    
    filledTiles: [] as number[],
  },
  reducers: {
    resetGoodGoal: (state) => {
        state.goal = null
    },
    resetBadGoal: (state) => {
        state.badGoal = null
    },
    setBadGoal: (state, action) => {
        state.filledTiles.push(action.payload); 
        const generateUniqueIndex = () => {
            let index;
            do {
                index = Math.floor(Math.random() * state.bordSize);
            } while (state.filledTiles.includes(index));
            state.filledTiles.push(index);
            return index;
        };
         state.badGoal = generateUniqueIndex()
    },
    setGoodGoal: (state, action) => {
        state.filledTiles.push(action.payload); 
        const generateUniqueIndex = () => {
            let index;
            do {
                index = Math.floor(Math.random() * state.bordSize);
            } while (state.filledTiles.includes(index));
            state.filledTiles.push(index);
            return index;
        };
         state.goal = generateUniqueIndex()
    },
    setBoard: (state, action) => {
        state.filledTiles.push(action.payload); 
        const generateUniqueIndex = () => {
            let index;
            do {
                index = Math.floor(Math.random() * state.bordSize);
            } while (state.filledTiles.includes(index));
            state.filledTiles.push(index);
            return index;
        };

        const cheapItems = Array.from({length: state.level >= 0 ? state.level : 0}, () => generateUniqueIndex());
        cheapItems.forEach(item => {
          state.cheap.push(item)
        });

        const expensiveItems = Array.from({length: state.level >= 0 ? state.level : 0}, () => generateUniqueIndex());
        expensiveItems.forEach(item => {
          state.expensive.push(item)
        });
       
        
    },
   
    removeIndex: (state, action) => {
        state.filledTiles = state.filledTiles.filter(item => item !== action.payload);
      },
  
    setExpensiveArray: (state, action) => {
        state.expensive = action.payload
    },
    setCheapArray: (state, action) => {
        state.cheap = action.payload
    },
    setGoalIndex: (state, action) => {
        state.goal= action.payload;
    },
    setBadGoalIndex: (state, action) => {
        state.badGoal = action.payload;
    },
    setTotalRewards: (state, action) => {
        state.totalRewards= action.payload;
    },
 
    deductMovementPoints: (state) => {
        state.movementPoints = state.movementPoints - (1 / state.bordSize)
    },
    resetMovementPoints: (state) => {
        state.movementPoints = 1.00
    },
    decreaseLevel: (state) => {
        state.level--
    },
    addLevel: (state) => {
        state.level++
    },
    setActionReward: (state, action) => {
        console.log(action.payload)
        state.actionReward = action.payload
    }

  }
});

// Export the actions
export const {setActionReward, decreaseLevel, resetBadGoal, resetGoodGoal, setGoodGoal, setBadGoal, removeIndex, setBoard, addLevel, setExpensiveArray, setCheapArray, setTotalRewards, setGoalIndex, setBadGoalIndex, deductMovementPoints, resetMovementPoints } = canvasSlice.actions;

// Export the reducer
export default canvasSlice.reducer;