import React, { useCallback, useEffect, useRef, useState } from 'react';
import GameCanvas from './components/GameCanvas/GameCanvas';
import css from './styles/styles.module.css'
import { makeMove, sanitizeDirectionString } from './utils';
import html2canvas from 'html2canvas';
import axios from 'axios'
import { useSelector, useDispatch } from 'react-redux';
import { movePlayer, setDirection } from './redux/slices/playerSlice';
import {setActionReward, deductMovementPoints, setBoard, } from "./redux/slices/canvasSlice"
function App() {

  
  const gameCanvasRef = useRef(null);
  const [currentImage, setCurrentImage] = useState<string | null>(null)
  const {position, direction} = useSelector((state:any) => state.playerSlice)
  const {movementPoints, level, actionReward, playerDirection} = useSelector((state:any) => state.canvasSlice)
  const [stageLocked, setStageLocked] = useState(false)
  const [hitWall, setHitWall] = useState<string | null>(null)
  const [trainingStarted, setTrainingStarted] = useState(false)
  const dispatch = useDispatch()
    
  useEffect(() => {
      setStageLocked(false) 
   }, [level])
 
  const convertToImage = useCallback(async () => {
    if (gameCanvasRef.current) {
      const canvas = await html2canvas(gameCanvasRef.current);
      const image = canvas.toDataURL('image/png');
      setCurrentImage(image);
  
      try {
        const response = await axios.post("http://localhost:5000/v1/ai/startTraining", {dataURL: image, data:{reward:actionReward, direction:sanitizeDirectionString(direction)}});
        
        //action reward has to be zeroed out after each step.
        dispatch(setActionReward(0))
        
        const move = response.data.data.makeMove;
        const moveDone = makeMove(move, position, dispatch);
        
        if(typeof moveDone === "string") {
          dispatch(movePlayer(position))
          setHitWall(moveDone)
        } else {
          dispatch(movePlayer(moveDone))
        }
        dispatch(deductMovementPoints())

      } catch (error) {
        console.error('Error in making move:', error);
      }
    }
  },[position, trainingStarted, direction, actionReward]);

    
    useEffect(() => {
      if(trainingStarted) {
        const timeout = setTimeout(() => {
          convertToImage()
        }, 15)
      return () => clearTimeout(timeout)
    }
    },[position, trainingStarted, direction, actionReward])

    //generates a unique index for each item on the field
    useEffect(() => {
      if(position && !stageLocked) {
        dispatch(setBoard(position))
        setStageLocked(true)
      }
    }, [position, stageLocked, dispatch, level, direction]);
    
   
  
  
  return (
    <div className={css.wrapper}>
      <div ref={gameCanvasRef}>
        <GameCanvas playerDirection={direction} gridSize={45} playerPosition={position} />
      </div>
      <button onClick={() => setTrainingStarted(!trainingStarted)}>{trainingStarted? "Stop Training" : "Start Training"}</button>
    </div>
  );
}

export default App;
