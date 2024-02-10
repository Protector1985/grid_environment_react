import React from 'react';
import css from './style/style.module.css'
import  Character  from '../Character/Character';
import {  useDispatch, useSelector } from 'react-redux';
import { setExpensiveArray, setCheapArray, addLevel, removeIndex, setGoodGoal, resetGoodGoal, resetBadGoal, decreaseLevel, setBadGoal, setActionReward} from '../../redux/slices/canvasSlice';

interface Tile {
    playerPosition: number,
    index: number,
    playerDirection: "LEFT" | "RIGHT" | "UP" | "DOWN";
}
const Tile:React.FC<Tile> = ({playerDirection, playerPosition, index}) => {
    const {expensive, cheap, goal, badGoal, level} = useSelector((state:any) => state.canvasSlice)
     
    const dispatch = useDispatch()
    
    function returnTiles() {
      
        if (expensive.includes(index) && index !== playerPosition) {
            return <img className={css.image} src={require("../assets/expensive/expensive.png")} />
        
        } else if (cheap.includes(index) && index !== playerPosition) {
            return <img className={css.image} src={require("../assets/cheap/1.png")} />
        
        } else if (goal === index && index !== playerPosition){
            return <img className={css.image} src={require("../assets/goal/1.png")} />
        
        } else if (badGoal === index && index !== playerPosition){ 
            return <img className={css.image} src={require("../assets/badGoal/1.png")} />
        
        //Agent hit an expensive item === good
        } else if (expensive.includes(index) && index === playerPosition) {
            const newarr = expensive.filter((item:any) => index !== item);
            dispatch(removeIndex(index))
            dispatch(setExpensiveArray(newarr));
            dispatch(setActionReward(0.5))
            if(newarr.length == 0) {
                dispatch(setGoodGoal(index))
            } 
            return <Character isMoving={true} direction={playerDirection} row={1} />
        
        } else if (badGoal === index && index === playerPosition) {
            dispatch(removeIndex(index))
            dispatch(resetBadGoal());
            dispatch(decreaseLevel())
            dispatch(resetGoodGoal())
            dispatch(setActionReward(-1.0))
        } else if (goal === index && index === playerPosition) {
            dispatch(removeIndex(index))
            dispatch(resetGoodGoal());
            dispatch(resetBadGoal())
            dispatch(addLevel())
            dispatch(setActionReward(1.0))
            return <Character isMoving={true} direction={playerDirection} row={1} />
            
        } else if (cheap.includes(index) && index === playerPosition) {
            const newarr = cheap.filter((item:any) => index !== item); 
            dispatch(removeIndex(index))
            dispatch(setCheapArray(newarr)); 
            dispatch(setActionReward(-0.5))
            if(newarr.length == 0) {
                dispatch(setBadGoal(index))
            } 
            return <Character isMoving={true} direction={playerDirection} row={1} />
        
        } else if (index === playerPosition) {
            return <Character isMoving={true} direction={playerDirection} row={1} />
        } 
    }


    return (
        <div className={css.wrapper}>
          {returnTiles()}
        </div>
    )
}

export default Tile